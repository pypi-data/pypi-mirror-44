!! N=====================================================================
!! Atomistica - Interatomic potential library
!! https://github.com/pastewka/atomistica
!! Lars Pastewka, lars.pastewka@iwm.fraunhofer.de, and others
!! See the AUTHORS file in the top-level Atomistica directory.
!!
!! Copyright (2005-2013) Fraunhofer IWM
!!
!! This part of Atomistica is not for distribution.
!! DO NOT DISTRIBUTE.
!! ======================================================================

!**********************************************************************
! This is the kernel for the bond-order potentials of the REBO2 type.
!**********************************************************************

!#define DEBUG_PRINT

#ifndef SCREENING
#define cutfcnbo  cutfcn
#define cutdrvbo  cutdrv
#define cutfcnnc  cutfcn
#define cutdrvnc  cutdrv

#define cut_out_h  cut_in_h
#define cut_out_h  cut_in_h
#endif

#ifndef LAMMPS

#define DCELL_INDEX(ni)  VEC(dc, ni, 3) + (2*maxdc(3)+1) * ( VEC(dc, ni, 2) + (2*maxdc(2)+1) * VEC(dc, ni, 1) )

#endif

#define TOO_SMALL(what, i, ierror)  nebtot = 1 ; this%neb_last(i) = this%neb_seed(i) ; RAISE_DELAYED_ERROR("Internal neighbor list exhausted, *" // what // "* too small: " // "nebtot = " // nebtot // "/" // neb_max // ", nebmax = " // this%nebmax // ", nebavg = " // this%nebavg // ", neb_last(i)-neb_seed(i)+1 = " // (this%neb_last(i)-this%neb_seed(i)+1), ierror)

#ifdef LAMMPS

  recursive subroutine BOP_KERNEL( &
       this, &
       maxnat, natloc, nat, r, &
       tag, ktyp, &
       aptr, a2ptr, bptr, ptrmax, &
       epot, f_inout, wpot_inout, &
       epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
       ierror)

#else

  recursive subroutine BOP_KERNEL( &
       this, cell, &
       maxnat, natloc, nat, r, &
       ktyp, &
       aptr, a2ptr, bptr, ptrmax, dc, &
#ifndef PYTHON
       shear_dx, &
#endif
       epot, f_inout, wpot_inout, &
       epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
       ierror)

#endif

    ! 
    ! donald brenner's hydrocarbon potential.
    ! copyright: Keith Beardmore 28/11/93.
    ! - algorithm from : phys. rev. b 42, 9458-9471(1990).
    ! - plus corrections : phys. rev. b 46, 1948(1990).
    ! - modified to use linked list and pointers
    ! - to reduce size of neb-list. 25/1/94.
    ! - pre-calculates pairwise terms. 29/1/94.
    ! 
    ! copyright: Lars Pastewka 2006-2009
    ! - made Fortran 90 compliant
    ! - new parametrization
    !     D. W. Brenner et al., J. Phys. Cond. Mat. 14, 783 (2002)
    ! - screening functions
    !     M. I. Baskes et al., Modelling Simul. Mater. Sci. Eng. 2, 505 (1994)
    !     L. Pastewka et al., Phys. Rev. B 78, 161402(R) (2008)
    ! - optimizations. 07/2007
    ! - virial. 09/2008
    ! - OO compliant. 02/2009
    !
    ! 
    ! algorithm assumes atoms are ktyp=1 (c), ktyp=3 (h)
    ! 
    ! for REBO:
    ! 
    !       o o o       p p p
    !        \|/         \|/
    !         m m m   n n n              the energy of bond i-j is
    !          \|/     \|/               dependent on all atoms that are 
    !   o   m   k       l   n   p        first, second (or third neighbours
    !    \   \   \     /   /   /         if screening is enabled) of 
    ! o---m---k---i===j---l---n---p      i and j. the resulting forces   
    !    /   /   /     \   \   \         act upon all these atoms.
    !   o   m   k       l   n   p        
    !          /|\     /|\               in the code, the atoms and
    !         m m m   n n n              bonds are identified as shown
    !        /|\         /|\             on the left.
    !       o o o       p p p
    ! 

    use tls

#ifdef _OPENMP
    use omp_lib
#endif

    implicit none

    integer, parameter       :: typemax = 7

    !
    ! Size estimation for internal neighbor lists
    !

    ! ---

    type(BOP_TYPE),      intent(inout) :: this
#ifndef LAMMPS
    real(DP),            intent(in)    :: cell(3, 3)
#endif

    integer,             intent(in)    :: maxnat, natloc, nat
    real(DP),            intent(in)    :: r(3, maxnat)

    integer,             intent(in)    :: ptrmax

    real(DP),            intent(inout) :: f_inout(3, maxnat)
    real(DP),            intent(inout) :: epot
    real(DP),            intent(inout) :: wpot_inout(3, 3)
    real(DP)                           :: wpot(3, 3)

#ifdef LAMMPS
    integer,             intent(in)    :: tag(maxnat)
#endif
    integer,             intent(in)    :: ktyp(maxnat)
    real(DP),  optional, intent(inout) :: epot_per_at(nat)
    real(DP),  optional, intent(inout) :: epot_per_bond(ptrmax)

#ifdef LAMMPS
    integer(NEIGHPTR_T), intent(in)    :: aptr(maxnat+1)
    integer(NEIGHPTR_T), intent(in)    :: a2ptr(maxnat+1)
#else
    integer(8),   intent(in)    :: aptr(maxnat+1)
    integer(8),   intent(in)    :: a2ptr(maxnat+1)
#endif
    integer,             intent(in)    :: bptr(ptrmax)

#ifndef LAMMPS
    integer,             intent(in)    :: dc(3, ptrmax)
#ifndef PYTHON
    real(DP),            intent(in)    :: shear_dx(3)
#endif
#endif


#ifdef LAMMPS
    real(DP),  optional, intent(inout) :: wpot_per_at(6, maxnat)
    real(DP),  optional, intent(inout) :: f_per_bond(3, ptrmax)
    real(DP),  optional, intent(inout) :: wpot_per_bond(6, ptrmax)
#else
    real(DP),  optional, intent(inout) :: wpot_per_at(3, 3, maxnat)
    real(DP),  optional, intent(inout) :: f_per_bond(3, ptrmax)
    real(DP),  optional, intent(inout) :: wpot_per_bond(3, 3, ptrmax)
#endif
    integer,   optional, intent(inout) :: ierror

    ! ---

    ! "short" neighbor list (all neighbors which are not screened)

#ifdef LAMMPS
    integer(C_INTPTR_T) :: jbeg,jend,jn
#else
    integer   :: jbeg,jend,jn
#endif

    real(DP)  :: rij(3)
    real(DP)  :: rlij, rlijr, rljl, rlik
    real(DP)  :: rnij(3), rnik(3), rnjl(3)
    real(DP)  :: df(3)
    real(DP)  :: fcij,dfcijr,fcik,dfcikr,fcjl,dfcjlr
    real(DP)  :: faij,dfaijr,frij,dfrijr
    real(DP)  :: zij,zji
    real(DP)  :: wij(3, 3), wijb(3, 3), wjib(3, 3)
    real(DP)  :: dbidi(3), dbidj(3), dbidk(3, this%nebmax)
    real(DP)  :: dbjdi(3), dbjdj(3), dbjdl(3, this%nebmax)
    real(DP)  :: disjk,disil,dkc(3),dlc(3)
    real(DP)  :: costh
    real(DP)  :: g_costh,dg_dcosth
    real(DP)  :: h_Dr,dh_dDr,dg_dn
#ifdef SEPARATE_H_ARGUMENTS
    real(DP)  :: dh_dr2
#endif
    real(DP)  :: dzfac,dzdrij,dzdrji,dzdrik,dzdrjl
    real(DP)  :: dgdi(3), dgdj(3), dgdk(3), dgdl(3)
    real(DP)  :: dcsdij,dcsdji,dcsdik,dcsdjk,dcsdil,dcsdjl
    real(DP)  :: dcsdi(3), dcsdj(3), dcsdk(3), dcsdl(3)
    real(DP)  :: bij,bji,baveij,dfbij,dfbji
    real(DP)  :: hlfvij,dffac

    real(DP)  :: rik(3), rjl(3)

    real(DP)  :: fi(3), fj(3)

#ifdef DIHEDRAL
    real(DP)  :: costijkl, rlijsq, dcik, dcjl, abs_dc, dot_ij_jl, dot_ik_jl
    real(DP)  :: bdh, bdhij, dbdhij, tij, tije, dtdni, dtdnj, dtdncn
#ifndef SCREENING
    real(DP)  :: dot_ij_ik
#endif
#endif

#if defined(SCREENING) || defined(NUM_NEIGHBORS)
    real(DP)  :: xik
#endif

#ifdef ALT_DIHEDRAL
    integer   :: ik1, ik2, jl1, jl2, k1, k2, l1, l2
#ifndef LAMMPS
    integer   :: kdc1, kdc2, ldc1, ldc2
#endif
    real(DP)  :: rlik1, rnik1(3), rlik2, rnik2(3), rljl1, rnjl1(3), rljl2, rnjl2(3)
    real(DP)  :: fcik1, dfcik1r, fcik2, dfcik2r, fcjl1, dfcjl1r, fcjl2, dfcjl2r
    real(DP)  :: rk1k2(3), rl1l2(3)
    real(DP)  :: costijkl, rlijsq, dck1k2, dcl1l2, abs_dc, dot_ij_k1k2, dot_ij_l1l2, dot_k1k2_l1l2
    real(DP)  :: bdh, bdhij, dbdhij, tij, tije, dtdni, dtdnj, dtdncn
#endif

#ifdef NUM_NEIGHBORS
    real(DP)  :: ni(typemax), nj(typemax)
    real(DP)  :: dnidik(3, this%nebmax, typemax), dnidfcik(this%nebmax, typemax)
    real(DP)  :: dnidij(3, typemax), dnidfcij(typemax)
    real(DP)  :: dnjdjl(3, this%nebmax, typemax), dnjdfcjl(this%nebmax, typemax)
    real(DP)  :: dnjdji(3, typemax), dnjdfcji(typemax)
    real(DP)  :: nti, ntj
    real(DP)  :: nconj,dfdncn
    real(DP)  :: nconji,nconjj,nconjdx,nconjdr
    real(DP)  :: dnconjidxi(this%nebmax),dnconjjdxj(this%nebmax)
    real(DP)  :: dzdni,dzdnj
    real(DP)  :: dncnidk(3, this%nebmax),dncnjdl(3, this%nebmax)
    real(DP)  :: dncnidm(3, this%nebmax*this%nebmax),dncnjdn(3, this%nebmax*this%nebmax)
    real(DP)  :: xikdk(3),xjl,xjldl(3)
    real(DP)  :: xikdm(3, this%nebmax),xjldn(3, this%nebmax)
    real(DP)  :: fxik(this%nebmax),dfxikx,fxjl(this%nebmax),dfxjlx
    real(DP)  :: fij,dfdni,dfdnj,dfdncni,dfdncnj
    real(DP)  :: pij,pji,dpdn1i,dpdn2i,dpdn1j,dpdn2j,dpdnci,dpdnhi,dpdnoi,dpdncj,dpdnhj,dpdnoj
    real(DP)  :: pij_tmp1,pji_tmp1,dpdn2i_tmp1,dpdn1i_tmp1,dpdn2j_tmp1,dpdn1j_tmp1
    real(DP)  :: pij_tmp2,pji_tmp2,dpdn2i_tmp2,dpdn1i_tmp2,dpdn2j_tmp2,dpdn1j_tmp2
    real(DP)  :: f_pij_sw, df_pij_sw, f_pji_sw, df_pji_sw
#endif

#ifdef SCREENING
    real(DP)  :: rljk, dot_ij_ik, dot_ij_jk
    real(DP)  :: rjk(3)
    real(DP)  :: C, dCdrij, dCdrik, dCdrjk, Cmax_C, C_Cmin, fac
    real(DP)  :: xjk, xik_p_xjk, xik_m_xjk
#ifdef SIN_S
    real(DP)  :: csij
#endif
    real(DP)  :: sij, dsijdrij, dsijdrik, dsijdrjk
    real(DP)  :: fcboij, dfcboijr
#ifdef NUM_NEIGHBORS
    real(DP)  :: fcncij, dfcncijr
#endif
    real(DP)  :: zfaci(this%nebmax), zfacj(this%nebmax)
#endif
    real(DP)  :: fcinij, dfcinijr

    integer  :: i,j,k,l,m,n
#ifndef LAMMPS
    integer  :: jdc,kdc,ldc,mdc,ndc
#endif
    integer  :: ij,ik,jl,ln
#ifdef SCREENING
#ifdef LAMMPS
    integer(C_INTPTR_T) :: kn
#else
    integer :: kn
#endif
#endif

#ifdef NUM_NEIGHBORS
    integer  :: km, kmc
#endif

    integer  :: ikc,jlc,lnc
    integer  :: ktypi,ktypj,ktypk,ktypl
    integer  :: ijpot,ikpot,jlpot
    ! seed for the "short" neighbor list
    integer  :: nebtot, istart, ifinsh
    ! seed for the "screened" neighbor list
    integer  :: nebofi(this%nebmax), nebofj(this%nebmax)
    integer  :: nebofk(this%nebmax*this%nebmax), nebofl(this%nebmax*this%nebmax)
#ifndef LAMMPS
    integer  :: dcofi(this%nebmax), dcofj(this%nebmax)
    integer  :: dcofk(this%nebmax*this%nebmax), dcofl(this%nebmax*this%nebmax)
#endif

    integer  :: numnbi,numnbj,numnbk(this%nebmax),numnbl(this%nebmax)

    integer  :: neb_max

    real(DP) :: dri(3, this%nebmax), drj(3, this%nebmax)
    real(DP) :: drk(3, this%nebmax*this%nebmax), drl(3, this%nebmax*this%nebmax)

#ifdef SCREENING
    integer  :: seedi(this%nebmax), seedj(this%nebmax)
    integer  :: seedk(this%nebmax*this%nebmax), seedl(this%nebmax*this%nebmax)

    integer  :: lasti(this%nebmax), lastj(this%nebmax)
    integer  :: lastk(this%nebmax*this%nebmax), lastl(this%nebmax*this%nebmax)

    integer  :: sneb_max

    integer  :: i1,i2

    integer  :: nijc
    integer  :: snebtot, ineb

    logical  :: screened
    logical  :: need_derivative
#endif

#ifndef LAMMPS
    integer  :: maxdc(3)
#endif

    integer  :: ierror_loc

    ! ---

#ifdef DEBUG_OUTPUT

    if (.not. allocated(debug_S)) then
       allocate(debug_S(ptrmax))
       allocate(debug_fC(ptrmax))
       allocate(debug_rl(ptrmax))
    endif

    debug_S   = 0.0_DP
    debug_fC  = 0.0_DP
    debug_rl  = 0.0_DP

#endif


    this%it = this%it + 1

    neb_max   = maxnat*this%nebavg
#ifdef SCREENING
    sneb_max  = neb_max*this%nebavg
#endif

    if (this%neighbor_list_allocated .and. ( size(this%neb) < neb_max .or. size(this%neb_seed) < maxnat )) then

       this%neighbor_list_allocated = .false.

#ifdef NUM_NEIGHBORS
       deallocate(this%nn)
#endif

       deallocate(this%neb_seed)
       deallocate(this%neb_last)

       deallocate(this%neb)
       deallocate(this%nbb)
#ifndef LAMMPS
       deallocate(this%dcell)
#endif
       deallocate(this%bndtyp)
       deallocate(this%bndlen)
       deallocate(this%bndnm)
       deallocate(this%cutfcn)
       deallocate(this%cutdrv)

#ifdef SCREENING
       deallocate(this%cutfcnbo)
       deallocate(this%cutdrvbo)
       deallocate(this%sneb_seed)
       deallocate(this%sneb_last)
       deallocate(this%sneb)
       deallocate(this%sbnd)
       deallocate(this%sfacbo)
       deallocate(this%cutdrik)
       deallocate(this%cutdrjk)
       deallocate(this%cutdrboik)
       deallocate(this%cutdrbojk)

#ifdef NUM_NEIGHBORS
       deallocate(this%cutfcnnc)
       deallocate(this%cutdrvnc)
       deallocate(this%sfacnc)
       deallocate(this%cutdrncik)
       deallocate(this%cutdrncjk)
#endif

#endif

    endif

    !-------prepare brenner material
    if (.not. this%neighbor_list_allocated) then

#ifndef LAMMPS
       write (ilog, '(A)')      "- " // BOP_NAME_STR // " -"
#ifdef DIHEDRAL
       write (ilog, '(5X,A)')   "The " // BOP_NAME_STR // " potential has been compiled including dihedral terms."
#endif
#ifdef ALT_DIHEDRAL
       write (ilog, '(5X,A)')   "The " // BOP_NAME_STR // " potential has been compiled including (alternative style) dihedral terms."
#endif
#ifdef SCREENING
       write (ilog, '(5X,A)')   "The " // BOP_NAME_STR // " potential has been compiled with screening functions."
#endif
       call log_memory_start(BOP_NAME_STR)
#endif

#ifdef SEPARATE_H_ARGUMENTS
       write (ilog, '(5X,A)')   "The " // BOP_NAME_STR // " potential has been compiled with SEPARATE_H_ARGUMENTS."
#endif
#ifdef SEP_NCONJ
       write (ilog, '(5X,A)')   "The " // BOP_NAME_STR // " potential has been compiled with SEP_NCONJ."
#endif
#ifdef EXP_CUT
       write (ilog, '(5X,A)')   "The " // BOP_NAME_STR // " potential has been compiled with exponential cutoff functions."
#endif


#ifdef NUM_NEIGHBORS
       allocate(this%nn(typemax, maxnat))
#endif

       allocate(this%neb_seed(maxnat))
       allocate(this%neb_last(maxnat))

       allocate(this%neb(neb_max))
       allocate(this%nbb(neb_max))
#ifndef LAMMPS
       allocate(this%dcell(neb_max))
#endif
       allocate(this%bndtyp(neb_max))
       allocate(this%bndlen(neb_max))
       allocate(this%bndnm(3, neb_max))
       allocate(this%cutfcn(neb_max))
       allocate(this%cutdrv(neb_max))

#ifndef LAMMPS
       call log_memory_estimate(this%neb)
       call log_memory_estimate(this%nbb)
       call log_memory_estimate(this%dcell)
       call log_memory_estimate(this%bndtyp)
       call log_memory_estimate(this%bndlen)
       call log_memory_estimate(this%bndnm)
       call log_memory_estimate(this%cutfcn)
       call log_memory_estimate(this%cutdrv)
#endif

#ifdef SCREENING
       allocate(this%cutfcnbo(neb_max))
       allocate(this%cutdrvbo(neb_max))
       allocate(this%sneb_seed(neb_max))
       allocate(this%sneb_last(neb_max))
       allocate(this%sneb(sneb_max))
       allocate(this%sbnd(sneb_max))
       allocate(this%sfacbo(sneb_max))
       allocate(this%cutdrik(sneb_max))
       allocate(this%cutdrjk(sneb_max))
       allocate(this%cutdrboik(sneb_max))
       allocate(this%cutdrbojk(sneb_max))

#ifdef NUM_NEIGHBORS
       allocate(this%cutfcnnc(neb_max))
       allocate(this%cutdrvnc(neb_max))
       allocate(this%sfacnc(sneb_max))
       allocate(this%cutdrncik(sneb_max))
       allocate(this%cutdrncjk(sneb_max))
#endif

#ifndef LAMMPS
       call log_memory_estimate(this%cutfcnbo)
       call log_memory_estimate(this%cutdrvbo)
       call log_memory_estimate(this%sneb_seed)
       call log_memory_estimate(this%sneb_last)
       call log_memory_estimate(this%sneb)
       call log_memory_estimate(this%sbnd)
       call log_memory_estimate(this%sfacbo)
       call log_memory_estimate(this%cutdrik)
       call log_memory_estimate(this%cutdrjk)
       call log_memory_estimate(this%cutdrboik)
       call log_memory_estimate(this%cutdrbojk)

#ifdef NUM_NEIGHBORS
       call log_memory_estimate(this%cutfcnnc)
       call log_memory_estimate(this%cutdrvnc)
       call log_memory_estimate(this%sfacnc)
       call log_memory_estimate(this%cutdrncik)
       call log_memory_estimate(this%cutdrncjk)
#endif
#endif
#endif

#ifndef LAMMPS
       call log_memory_stop(BOP_NAME_STR)

       write (ilog, *)
#endif

       this%neighbor_list_allocated = .true.
       
    endif

    ! 
    ! set all p.e. and forces to zero.
    !

    wpot  = 0.0_DP

#ifndef LAMMPS
    maxdc = 0
    do i = 1, nat
       maxdc(1)  = max(maxdc(1), maxval(VEC(dc, aptr(i):a2ptr(i), 1)))
       maxdc(2)  = max(maxdc(2), maxval(VEC(dc, aptr(i):a2ptr(i), 2)))
       maxdc(3)  = max(maxdc(3), maxval(VEC(dc, aptr(i):a2ptr(i), 3)))
    enddo
#endif

#ifdef SCREENING
    this%sfacbo  = 0.0_DP

#ifdef NUM_NEIGHBORS
    this%sfacnc  = 0.0_DP
#endif
#endif

    ! 
    ! calculate the main pairwise terms and store them.
    !

    ierror_loc  = ERROR_NONE

    !$omp  parallel default(none) &
    !$omp& shared(aptr, a2ptr, bptr, f_inout, ktyp) &
#ifdef LAMMPS
    !$omp& shared(tag) &
#else
    !$omp& firstprivate(maxdc) &
    !$omp& shared(cell, dc) &
#ifndef PYTHON
    !$omp& shared(shear_dx) &
#endif
#endif
    !$omp& shared(nat, natloc) &
    !$omp& shared(neb_max, epot_per_at, epot_per_bond) &
    !$omp& shared(r, this, f_per_bond, wpot_per_at, wpot_per_bond) &
#ifdef SCREENING
    !$omp& shared(sneb_max) &
#endif
    !$omp& private(jbeg,jend,jn) &
    !$omp& private(rij) &
    !$omp& private(rlij, rlijr, rljl, rlik) &
    !$omp& private(rnij, rnik, rnjl) &
    !$omp& private(df) &
    !$omp& private(fcij,dfcijr,fcik,dfcikr,fcjl,dfcjlr) &
    !$omp& private(faij,dfaijr,frij,dfrijr) &
    !$omp& private(zij,zji) &
    !$omp& private(wij, wijb, wjib) &
    !$omp& private(dbidi, dbidj, dbidk) &
    !$omp& private(dbjdi, dbjdj, dbjdl) &
    !$omp& private(disjk,disil,dkc,dlc) &
    !$omp& private(costh) &
    !$omp& private(g_costh,dg_dcosth) &
    !$omp& private(h_Dr,dh_dDr,dg_dn) &
#ifdef SEPARATE_H_ARGUMENTS
    !$omp& private(dh_dr2) &
#endif
    !$omp& private(dzfac,dzdrij,dzdrji,dzdrik,dzdrjl) &
    !$omp& private(dgdi, dgdj, dgdk, dgdl) &
    !$omp& private(dcsdij,dcsdji,dcsdik,dcsdjk,dcsdil,dcsdjl) &
    !$omp& private(dcsdi, dcsdj, dcsdk, dcsdl) &
    !$omp& private(bij,bji,baveij,dfbij,dfbji) &
    !$omp& private(hlfvij,dffac) &
    !$omp& private(rik, rjl) &
    !$omp& private(fi, fj) &
#ifdef DIHEDRAL
    !$omp& private(costijkl, rlijsq, dcik, dcjl, abs_dc, dot_ij_jl, dot_ik_jl) &
    !$omp& private(bdh, bdhij, dbdhij, tij, tije, dtdni, dtdnj, dtdncn) &
#ifndef SCREENING
    !$omp& private(dot_ij_ik) &
#endif
#endif
#ifdef ALT_DIHEDRAL
    !$omp& private(ik1, ik2, jl1, jl2, k1, k2, l1, l2, kdc1, kdc2, ldc1, ldc2) &
    !$omp& private(rlik1, rnik1, rlik2, rnik2, rljl1, rnjl1, rljl2, rnjl2) &
    !$omp& private(fcik1, dfcik1r, fcik2, dfcik2r, fcjl1, dfcjl1r, fcjl2, dfcjl2r) &
    !$omp& private(rk1k2, rl1l2) &
    !$omp& private(costijkl, rlijsq, dck1k2, dcl1l2, abs_dc, dot_ij_k1k2, dot_ij_l1l2, dot_k1k2_l1l2) &
    !$omp& private(bdh, bdhij, dbdhij, tij, tije, dtdni, dtdnj, dtdncn) &
#endif
#ifdef NUM_NEIGHBORS
    !$omp& private(ni, nj) &
    !$omp& private(dnidik, dnidfcik, dnidij, dnidfcij) &
    !$omp& private(dnjdjl, dnjdfcjl, dnjdji, dnjdfcji) &
    !$omp& private(nti, ntj) &
#ifndef SEP_NCONJ
    !$omp& private(nconj,dfdncn) &
#endif
    !$omp& private(nconji,nconjj,nconjdx,nconjdr) &
    !$omp& private(dnconjidxi,dnconjjdxj) &
    !$omp& private(dzdni,dzdnj) &
    !$omp& private(dncnidk,dncnjdl) &
    !$omp& private(dncnidm,dncnjdn) &
    !$omp& private(xikdk,xjl,xjldl) &
    !$omp& private(xikdm,xjldn) &
    !$omp& private(fxik,dfxikx,fxjl,dfxjlx) &
    !$omp& private(fij,dfdni,dfdnj,dfdncni,dfdncnj) &
    !$omp& private(pij,pji,dpdnci,dpdnhi,dpdncj,dpdnhj,dpdnoi,dpdnoj) &
    !$omp& private(dpdn1i,dpdn2i,dpdn1j,dpdn2j) &
    !$omp& private(pij_tmp1,pji_tmp1,dpdn2i_tmp1,dpdn1i_tmp1,dpdn2j_tmp1,dpdn1j_tmp1) &
    !$omp& private(pij_tmp2,pji_tmp2,dpdn2i_tmp2,dpdn1i_tmp2,dpdn2j_tmp2,dpdn1j_tmp2) &
    !$omp& private(f_pij_sw, df_pij_sw, f_pji_sw, df_pji_sw) &
#endif
#if defined(SCREENING) || defined(NUM_NEIGHBORS)
    !$omp& private(xik) &
#endif
#ifdef SCREENING
    !$omp& private(rljk, dot_ij_ik, dot_ij_jk) &
    !$omp& private(rjk) &
    !$omp& private(fcboij, dfcboijr) &
#ifdef NUM_NEIGHBORS
    !$omp& private(fcncij, dfcncijr) &
#endif
    !$omp& private(zfaci, zfacj) &
#endif
    !$omp& private(fcinij, dfcinijr) &
    !$omp& private(i,j,k,l,m,n) &
#ifndef LAMMPS
    !$omp& private(jdc,kdc,ldc,mdc,ndc) &
#endif
    !$omp& private(ij,ik,jl,ln) &
#ifdef SCREENING
    !$omp& private(kn) &
#endif
    !$omp& private(ikc,jlc,lnc) &
#ifdef NUM_NEIGHBORS
    !$omp& private(km,kmc) &
#endif
    !$omp& private(ktypi,ktypj,ktypk,ktypl) &
    !$omp& private(ijpot,ikpot,jlpot) &
    !$omp& private(istart, ifinsh) &
    !$omp& private(nebofi, nebofj) &
    !$omp& private(nebofk, nebofl) &
#ifndef LAMMPS
    !$omp& private(dcofi, dcofj) &
    !$omp& private(dcofk, dcofl) &
#endif
    !$omp& private(numnbi, numnbj)&
    !$omp& private(numnbk, numnbl) &
    !$omp& private(nebtot) &
    !$omp& private(dri, drj) &
    !$omp& private(drk, drl) &
#ifdef SCREENING
    !$omp& private(i1,i2) &
    !$omp& private(seedi, seedj) &
    !$omp& private(seedk, seedl) &
    !$omp& private(lasti, lastj) &
    !$omp& private(lastk, lastl) &
    !$omp& private(nijc,ineb) &
    !$omp& private(snebtot) &
    !$omp& private(sij, dsijdrij, dsijdrik, dsijdrjk) &
    !$omp& private(C, dCdrij, dCdrik, dCdrjk, Cmax_C, C_Cmin, fac) &
    !$omp& private(xjk, xik_p_xjk, xik_m_xjk) &
#ifdef SIN_S
    !$omp& private(csij) &
#endif
    !$omp& private(screened, need_derivative) &
#endif
    !$omp& reduction(+:ierror_loc) &
    !$omp& reduction(+:wpot) reduction(+:epot)

    call tls_init(nat, sca=1, vec=1)
#define pe tls_sca1
#define f  tls_vec1

#define nebmax_sq nti
    nebmax_sq = this%nebmax*this%nebmax

#ifdef _OPENMP
    nebtot   = 1 + neb_max*omp_get_thread_num()/omp_get_num_threads()
#ifdef SCREENING
    snebtot  = 1 + sneb_max*omp_get_thread_num()/omp_get_num_threads()
#endif

#else

    nebtot   = 1
#ifdef SCREENING
    snebtot  = 1
#endif

#endif

    !$omp do
    i_loop1: do i = 1, nat
       ktypi = ktyp(i)

       this%neb_seed(i)  = nebtot
       this%neb_last(i)  = nebtot-1

       i_known_el1: if (ktypi > 0) then

          jbeg = aptr(i)
          jend = a2ptr(i)

          jn_loop1: do jn = jbeg, jend

             !
             ! Loop over all pairs
             !

#ifdef LAMMPS
             ! Note that if you use LAMMPS and compile with a check bounds
             ! option the code will bail here. This is because LAMMPS allocates
             ! multiple chunks of memory (pages) for its neighbor list that can
             ! be located anywhere in memory. jn can therefore be negative,
             ! and this is picked by the bounds checker although correct.
             j      = bptr(jn)+1
#else
             j      = bptr(jn)
             jdc    = DCELL_INDEX(jn)
#endif
             ktypj  = ktyp(j)

             j_known_el1: if (ktypj > 0) then

#ifdef LAMMPS
                rij = VEC3(r, j) - VEC3(r, i)
#else
                rij = VEC3(r, j) - VEC3(r, i) - matmul(cell, VEC3(dc, jn))
#ifndef PYTHON
                rij = rij - shear_dx*VEC(dc, jn, 3)
#endif
#endif

                rlij = dot_product(rij, rij)

                ! 
                ! store pair terms for brenner here ( only store c & h atoms ).
                !

                ijpot = Z2pair(this, ktypi, ktypj)

                !
                !  There are different regions that need to be handled differently
                !  -------------- r1 ------ r2 ---------------------- r3 ------ r4
                !   no screening     trans.          screening           cutoff
                !       (a)           (b)               (c)                (d)
                !

#ifdef DEBUG_OUTPUT

                debug_rl(jn) = sqrt(rlij)

#endif

                if (rlij < this%cut_in_l(ijpot)**2) then
                
                   !
                   ! In region (a) -> atoms are allowed to interact
                   !

                   this%cutfcn(nebtot)  = 1.0_DP
                   this%cutdrv(nebtot)  = 0.0_DP

#ifdef SCREENING
                   this%cutfcnbo(nebtot)  = 1.0_DP
                   this%cutdrvbo(nebtot)  = 0.0_DP
#ifdef NUM_NEIGHBORS
                   this%cutfcnnc(nebtot)  = 1.0_DP
                   this%cutdrvnc(nebtot)  = 0.0_DP
#endif
#endif

#ifdef DEBUG_OUTPUT
                   debug_S(jn)            = 1.0_DP
                   debug_fC(jn)           = 1.0_DP
#endif

                   this%neb(nebtot)       = j
                   this%nbb(nebtot)       = jn
#ifndef LAMMPS
                   this%dcell(nebtot)     = jdc
#endif

#ifdef SCREENING
                   this%sneb_seed(nebtot) = snebtot
                   this%sneb_last(nebtot) = snebtot-1
#endif

                   ! 
                   ! bond-length and direction cosines.
                   !

                   rlij                    = sqrt( rlij )
                   this%bndlen(nebtot)     = rlij
                   this%bndnm(1:3, nebtot) = rij / rlij
                   this%bndtyp(nebtot)     = ijpot

                   this%neb_last(i)        = nebtot
                   nebtot                  = nebtot + 1

                   if (this%neb_last(i)-this%neb_seed(i)+1 > this%nebmax) then
                      TOO_SMALL("nebmax", i, ierror_loc)
                   endif

                   if (nebtot > neb_max) then
                      TOO_SMALL("nebavg", i, ierror_loc)
                   endif
      
#ifdef SCREENING
                else if (rlij < this%max_cut_sq(ijpot)) then

                   !
                   ! Compute screening function
                   !

                   screened                = .false.
                   need_derivative         = .false.
#ifdef SIN_S
                   sij                     = 1.0_DP
#else
                   sij                     = 0.0_DP
#endif
                   
                   this%sneb_seed(nebtot)  = snebtot
                   this%sneb_last(nebtot)  = snebtot-1

                   exclude_interactions: if (ijpot /= H_H .and. &
                                             ijpot /= C_H) then

                      !
                      ! within cutoff: compute the screening function for the bond
                      ! i-j
                      !

                      ineb      = snebtot

                      dsijdrij  = 0.0_DP

                      kn = jbeg
                      do while (.not. (screened .or. &
                           sij < this%screening_threshold) .and. kn <= jend)

#ifdef LAMMPS
                         k = bptr(kn)+1
                         rik = VEC3(r, k) - VEC3(r, i)
#else
                         k = bptr(kn)
                         rik = VEC3(r, k) - VEC3(r, i) - &
                              matmul(cell, VEC3(dc, kn))
#ifndef PYTHON
                         rik = rik - shear_dx*VEC(dc, kn, 3)
#endif
#endif
                         ktypk = ktyp(k)

                         if (dot_product(rik, rik) < &
                              this%C_dr_cut(ktypk)*rlij) then

#ifdef LAMMPS
                            k_neq_j: if (k /= j) then
#else
                            k_neq_j: if (k /= j .or. &
                                 any(VEC3(dc, kn) /= VEC3(dc, jn))) then
#endif

                               dot_ij_ik = dot_product(rij, rik)

                               rlik = dot_product(rik, rik)

                               rjk  = -rij + rik

                               dot_ij_jk = dot_product(rij, rjk)

                               rljk = dot_product(rjk, rjk)

                               if (dot_ij_ik > this%dot_threshold .and. &
                                    dot_ij_jk < -this%dot_threshold) then

                                  xik  = rlik/rlij
                                  xjk  = rljk/rlij

                                  xik_m_xjk  = xik-xjk
                                  xik_p_xjk  = xik+xjk

                                  fac        = 1.0_DP/(1-xik_m_xjk**2)

                                  C  = (2*(xik_p_xjk)-(xik_m_xjk)**2-1)*fac

                                  if (C <= this%Cmin(ktypk)) then
                                     screened = .true.
                                  else if (C < this%Cmax(ktypk)) then
                                     need_derivative = .true.

                                     Cmax_C    = this%Cmax(ktypk)-C
                                     C_Cmin    = C-this%Cmin(ktypk)

#ifdef SIN_S
                                     csij      = (1 - cos(PI*(C-Cmin)/ &
                                          this%dC(ktypk)))/2
                                     sij       = sij * csij
#else
                                     sij       = sij - (Cmax_C/C_Cmin)**2
#endif

                                     dCdrik    = 4*xik*fac*(1+(C-1)*xik_m_xjk)
                                     dCdrjk    = 4*xjk*fac*(1-(C-1)*xik_m_xjk)

                                     dCdrij    = -(dCdrik+dCdrjk)

#ifdef SIN_S
                                     fac       = PI/(2*this%dC(ktypk)) * &
                                          sin(PI*(C-Cmin)/this%dC(ktypk)) / csij
#else
                                     fac       = 2*Cmax_C*this%dC(ktypk)/ &
                                          (C_Cmin**3)
#endif
                                  
                                     !
                                     !  the following estimates lack a factor 
                                     !  of sij
                                     !

                                     dsijdrij = dsijdrij + fac*dCdrij
                                     dsijdrik = fac*dCdrik
                                     dsijdrjk = fac*dCdrjk
                                        
                                     this%sneb(snebtot) = k
                                     this%sbnd(snebtot) = kn

                                     this%cutdrik(snebtot) = dsijdrik/rlik
                                     this%cutdrjk(snebtot) = dsijdrjk/rljk

                                     this%sneb_last(nebtot) = snebtot
                                     snebtot                = snebtot + 1

                                  endif

                               endif

                            endif k_neq_j

                         endif

                         kn = kn+1
                      
                      enddo

                   endif exclude_interactions

                   if ((screened .or. sij < this%screening_threshold) .and. &
                        rlij > this%cut_in_h2(ijpot)) then

                      !
                      ! reset our screening neighbor because the bond is 
                      ! screened anyway
                      !

                      snebtot                 = ineb
                      this%sneb_last(nebtot)  = ineb - 1

                   else

                      !
                      ! not screened by another atom: add to local neighbor list
                      !

                      this%neb(nebtot)   = j
                      this%nbb(nebtot)   = jn
#ifndef LAMMPS
                      this%dcell(nebtot) = DCELL_INDEX(jn)
#endif

                      ! 
                      ! bond-length and direction cosines.
                      !

                      rlij                    = sqrt( rlij )
                      this%bndlen(nebtot)     = rlij
                      this%bndnm(1:3, nebtot) = rij / rlij
                      this%bndtyp(nebtot)     = ijpot

                      if ( screened ) then

                         call fCin(this, ijpot, rlij, fcinij, dfcinijr)

                         this%cutfcn(nebtot) = fcinij
                         this%cutdrv(nebtot) = dfcinijr

                         this%cutfcnbo(nebtot) = fcinij
                         this%cutdrvbo(nebtot) = dfcinijr

#ifdef NUM_NEIGHBORS
                         this%cutfcnnc(nebtot) = fcinij
                         this%cutdrvnc(nebtot) = dfcinijr
#endif

#ifdef DEBUG_OUTPUT
                         debug_S(jn)   = 0.0_DP
                         debug_fC(jn)  = this%cutfcn(nebtot)
#endif

                         snebtot                 = ineb
                         this%sneb_last(nebtot)  = ineb - 1

                      else if ( need_derivative ) then

#ifndef SIN_S
                         sij = exp( sij )
#endif

                         call fCin(this, ijpot, rlij, fcinij, dfcinijr)
                         call fCout(this, ijpot, rlij, fcij, dfcijr)
                         call fCbo(this, ijpot, rlij, fcboij, dfcboijr)
#ifdef NUM_NEIGHBORS
                         call fCnc(this, ijpot, rlij, fcncij, dfcncijr)
#endif

                         !
                         ! do also compute the derivatives with respect to the
                         ! neighbors
                         !

                         this%cutfcn(nebtot)  = (1.0_DP-fcinij)*sij*fcij + &
                              fcinij
                         this%cutdrv(nebtot)  = (1.0_DP-fcinij)*sij* &
                              (dfcijr + fcij*dsijdrij/rlij) - &
                              dfcinijr*sij*fcij + dfcinijr
                         this%cutfcnbo(nebtot) = (1.0_DP-fcinij)*sij*fcboij + fcinij
                         this%cutdrvbo(nebtot) = (1.0_DP-fcinij)*sij*(dfcboijr + fcboij*dsijdrij/rlij) - dfcinijr*sij*fcboij + dfcinijr

#ifdef NUM_NEIGHBORS
                         this%cutfcnnc(nebtot) = (1.0_DP-fcinij)*sij*fcncij + &
                              fcinij
                         this%cutdrvnc(nebtot) = (1.0_DP-fcinij)*sij* &
                              (dfcncijr + fcncij*dsijdrij/rlij) - &
                              dfcinijr*sij*fcncij + dfcinijr
#endif

#ifdef DEBUG_OUTPUT
                         debug_S(jn)   = sij
                         debug_fC(jn)  = this%cutfcn(nebtot)
#endif

                         !
                         ! multiply the sij and fcij into the derivatives
                         !

                         this%cutdrboik(ineb:snebtot-1) = this%cutdrik(ineb:snebtot-1)*sij*fcboij * (1.0_DP-fcinij)
                         this%cutdrbojk(ineb:snebtot-1) = this%cutdrjk(ineb:snebtot-1)*sij*fcboij * (1.0_DP-fcinij)

#ifdef NUM_NEIGHBORS
                         this%cutdrncik(ineb:snebtot-1) = &
                              this%cutdrik(ineb:snebtot-1)*sij*fcncij * &
                              (1.0_DP-fcinij)
                         this%cutdrncjk(ineb:snebtot-1) = &
                              this%cutdrjk(ineb:snebtot-1)*sij*fcncij * &
                              (1.0_DP-fcinij)
#endif

                         this%cutdrik(ineb:snebtot-1) = &
                              this%cutdrik(ineb:snebtot-1)*sij*fcij * &
                              (1.0_DP-fcinij)
                         this%cutdrjk(ineb:snebtot-1) = &
                              this%cutdrjk(ineb:snebtot-1)*sij*fcij * &
                              (1.0_DP-fcinij)

                      else

                         !
                         ! we don't need the derivative of the screening
                         ! function with respect to the neighbors because the
                         ! screening function is a constant (=1, locally).
                         !

                         call fCout(this, ijpot, rlij, fcij, dfcijr)
                         call fCbo(this, ijpot, rlij, fcboij, dfcboijr)
#ifdef NUM_NEIGHBORS
                         call fCnc(this, ijpot, rlij, fcncij, dfcncijr)
#endif

                         if (rlij < this%cut_in_h(ijpot)) then

                            call fCin(this, ijpot, rlij, fcinij, dfcinijr)

                            this%cutfcn(nebtot)  = (1.0_DP-fcinij)*fcij + &
                                 fcinij
                            this%cutdrv(nebtot)  = (1.0_DP-fcinij)*dfcijr - &
                                 dfcinijr*fcij + dfcinijr
                            this%cutfcnbo(nebtot) = (1.0_DP-fcinij)*fcboij + fcinij
                            this%cutdrvbo(nebtot) = (1.0_DP-fcinij)*dfcboijr - dfcinijr*fcboij + dfcinijr

#ifdef NUM_NEIGHBORS
                            this%cutfcnnc(nebtot) = (1.0_DP-fcinij)*fcncij + &
                                 fcinij
                            this%cutdrvnc(nebtot) = (1.0_DP-fcinij)*dfcncijr - &
                                 dfcinijr*fcncij + dfcinijr
#endif

                         else

                            this%cutfcn(nebtot) = fcij
                            this%cutdrv(nebtot) = dfcijr

                            this%cutfcnbo(nebtot) = fcboij
                            this%cutdrvbo(nebtot) = dfcboijr

#ifdef NUM_NEIGHBORS
                            this%cutfcnnc(nebtot) = fcncij
                            this%cutdrvnc(nebtot) = dfcncijr
#endif

                         endif

#ifdef DEBUG_OUTPUT
                         debug_S(jn)   = 1.0_DP
                         debug_fC(jn)  = this%cutfcn(nebtot)
#endif

#else ! NO SCREENING

                      else if (rlij < this%cut_in_h2(ijpot)) then

                         ! 
                         ! bond-length and direction cosines.
                         !

                         rlij                    = sqrt( rlij )
                         this%bndlen(nebtot)     = rlij
                         this%bndnm(1:3, nebtot) = rij / rlij
                         this%bndtyp(nebtot)     = ijpot

                         !
                         ! Cut-off function
                         !

                         call fCin(this, ijpot, rlij, fcinij, dfcinijr)

                         this%cutfcn(nebtot)    = fcinij
                         this%cutdrv(nebtot)    = dfcinijr

                         this%neb(nebtot)       = j
                         this%nbb(nebtot)       = jn
#ifndef LAMMPS
                         this%dcell(nebtot)     = DCELL_INDEX(jn)
#endif

                         this%neb_last(i)       = nebtot
                         nebtot                 = nebtot + 1

                         if (this%neb_last(i)-this%neb_seed(i)+1 > &
                              this%nebmax) then
                            TOO_SMALL("nebmax", i, ierror_loc)
                         endif

                         if (nebtot > neb_max) then
                            TOO_SMALL("nebavg", i, ierror_loc)
                         endif

#endif

#ifdef SCREENING

                      endif


                      if (this%sneb_last(nebtot)-this%sneb_seed(nebtot)+1 > &
                           nebmax_sq) then
                         TOO_SMALL("nebmax", i, ierror_loc)
                      endif
                      if (snebtot > sneb_max) then
                         TOO_SMALL("nebavg", i, ierror_loc)
                      endif

                      this%neb_last(i)  = nebtot
                      nebtot            = nebtot + 1

                      if (this%neb_last(i)-this%neb_seed(i)+1 > &
                           this%nebmax) then
                         TOO_SMALL("nebmax", i, ierror_loc)
                      endif

                      if (nebtot > neb_max) then
                         TOO_SMALL("nebavg", i, ierror_loc)
                      endif

                   endif

#endif

                endif

             endif j_known_el1

          enddo jn_loop1

       endif i_known_el1

    enddo i_loop1


    !
    ! Pre-compute neighbors
    !

#ifdef NUM_NEIGHBORS

    !$omp do
    do i = 1, nat
       this%nn(:, i)         = 0.0_DP

       do jn = this%neb_seed(i), this%neb_last(i)
          j  = this%neb(jn)
          if (ktyp(j) > 0) then
             this%nn(ktyp(j), i)  = &
                  this%nn(ktyp(j), i) + this%cutfcnnc(jn)
          endif
       enddo

    enddo

#endif

    ! 
    ! begin potential calculation.
    !

    !$omp do
    i_loop2: do i = 1, natloc

       ktypi  = ktyp(i)
       i_known_el2: if (ktypi > 0) then

          fi = 0.0_DP

          istart = this%neb_seed(i)
          ifinsh = this%neb_last(i)

          !
          ! have a list of all non-negligible bonds on atom i.
          ! calculate the morse terms and derivatives.
          ! i==j loop. consider all pairs of atoms i < j.
          !

          ij_loop: do ij = istart, ifinsh
             j    = this%neb(ij)
#ifdef LAMMPS
             j_gt_i: if (tag(j) >= tag(i)) then
#else
             jdc  = this%dcell(ij)
             j_gt_i: if ((jdc == 0 .and. j > i) .or. jdc > 0) then
#endif

                ijpot    = this%bndtyp(ij)
                rlij     = this%bndlen(ij)

                ar_within_cutoff: if (rlij < this%cut_out_h(ijpot)) then

                   fj     = 0.0_DP

                   ktypj  = ktyp(j)
                   rlijr  = 1.0_DP / rlij
                   rnij   = this%bndnm(1:3, ij)

                   rij    = rlij*rnij

                   ! 
                   ! cutoff function and derivative.
                   !

                   fcij   = this%cutfcn(ij)
                   dfcijr = this%cutdrv(ij)

                   ! 
                   ! begin to sum the number of atoms on i and j
                   !

#ifdef NUM_NEIGHBORS
                   ni        = this%nn(:, i) !- cutfcnnc(ij)
                   nj        = this%nn(:, j) !- cutfcnnc(ij)
                   ni(ktypj) = ni(ktypj) - this%cutfcnnc(ij)
                   nj(ktypi) = nj(ktypi) - this%cutfcnnc(ij)

                   if (ni(rebo2_C_) > 4.0_DP)  ni(rebo2_C_) = 4.0_DP
                   if (ni(rebo2_H_) > 4.0_DP)  ni(rebo2_H_) = 4.0_DP
                   if (ni(rebo2_O_) > 4.0_DP)  ni(rebo2_O_) = 4.0_DP

                   nti = ni(rebo2_C_) + ni(rebo2_H_) + ni(rebo2_O_)

                   if (nj(rebo2_C_) > 4.0_DP)  nj(rebo2_C_) = 4.0_DP
                   if (nj(rebo2_H_) > 4.0_DP)  nj(rebo2_H_) = 4.0_DP
                   if (nj(rebo2_O_) > 4.0_DP)  nj(rebo2_O_) = 4.0_DP

                   ntj = nj(rebo2_C_) + nj(rebo2_H_) + nj(rebo2_O_)

                   dnidik   = 0.0_DP
                   dnidfcik = 0.0_DP
                   dnidij   = 0.0_DP
                   dnidfcij = 0.0_DP
                   dnjdjl   = 0.0_DP
                   dnjdfcjl = 0.0_DP
                   dnjdji   = 0.0_DP
                   dnjdfcji = 0.0_DP
                   nconji   = 0.0_DP
                   nconjj   = 0.0_DP
#endif

                   ! 
                   ! repulsive/attractive potentials
                   !

                   call VA(this, ijpot, rlij, faij, dfaijr)
                   call VR(this, ijpot, rlij, frij, dfrijr)

                   wij   = 0.0_DP
                   wijb  = 0.0_DP
                   wjib  = 0.0_DP

                   ! 
                   ! calculate components of bond order term and derivatives
                   ! with respect to bond i-j for atom i.
                   !

                   zij    = 0.0_DP
                   dbidi  = 0.0_DP
                   dbidj  = 0.0_DP

                   ! 
                   ! restart i-k loop; now nci, nhi and nconj have been calculated
                   !

#ifdef NUM_NEIGHBORS
                   dzdni = 0.0_DP
#endif

                   !
                   ! i--k loop.
                   ikc        = 0
                   kmc        = 0
                   numnbk(1)  = 1
                   ik_loop: do ik = istart, ifinsh

                      ik_neq_ij: if (ik /= ij) then

                         ikc           = ikc + 1
                         k             = this%neb(ik)
#ifndef LAMMPS
                         kdc           = this%dcell(ik)
#endif

                         nebofi(ikc)   = k
#ifndef LAMMPS
                         dcofi(ikc)    = kdc
#endif
#ifdef SCREENING
                         seedi(ikc)    = this%sneb_seed(ik)
                         lasti(ikc)    = this%sneb_last(ik)
#endif

                         ktypk         = ktyp(k)
                         ikpot         = this%bndtyp(ik)
                         rlik          = this%bndlen(ik)
                         rnik          = this%bndnm(1:3, ik)

                         dri(1:3, ikc) = rlik*rnik

                         ! 
                         ! calculate length dependent terms
                         ! (constant for ijk=ccc,cch,chc).
                         !

#ifdef NUM_NEIGHBORS
                         fcik         = this%cutfcnnc(ik)
                         dfcikr       = this%cutdrvnc(ik)

                         !ni(ktypk)               = ni(ktypk) + fcik
                         dnidik(1:3, ikc, ktypk) = rnik * dfcikr

                         ! 
                         ! sum nconj if k is carbon.
                         ! 

                         ! FIXME!!! Generalize
                         ktypk_eq_C: if (ktypk == rebo2_C_) then

                            forall(km = this%neb_seed(k):this%neb_last(k))

                               nebofk(kmc + km-this%neb_seed(k)+1)  = this%neb(km)
#ifndef LAMMPS
                               dcofk(kmc + km-this%neb_seed(k)+1)   = kdc + &
                                    this%dcell(km)
#endif

#ifdef SCREENING
                               seedk(kmc + km-this%neb_seed(k)+1)   = &
                                    this%sneb_seed(km)
                               lastk(kmc + km-this%neb_seed(k)+1)   = &
                                    this%sneb_last(km)
#endif

                               drk(1:3, kmc + km-this%neb_seed(k)+1)  = &
                                    this%bndlen(km)*this%bndnm(1:3, km)

                               xikdm(1:3, km-this%neb_seed(k)+1)      = &
                                    this%cutdrvnc(km)*this%bndnm(1:3, km)

                            endforall

                            xik   = this%nn(rebo2_H_, k) + this%nn(rebo2_C_, k) - fcik
                            xikdk = &
                                 -sum(xikdm(1:3,1:this%neb_seed(k)-this%neb_last(k)+1),2)&
                                 + dnidik(1:3, ikc, ktypk)

                            kmc            = kmc + this%neb_last(k)-this%neb_seed(k)+1
                            numnbk(ikc+1)  = kmc + 1

                            !
                            ! sum f(xik) and derivatives
                            !

                            call fconj(this, xik, fxik(ikc), dfxikx)

                            nconjdr = fxik(ikc) * dfcikr
                            nconjdx = fcik * dfxikx

                            dnconjidxi(ikc) = nconjdx

                            nconji            = nconji + fcik * fxik(ikc)
                            dncnidk(1:3, ikc) = nconjdr * rnik

                            dncnidm(1:3, numnbk(ikc):numnbk(ikc+1)-1) = &
                                 nconjdx*xikdm(1:3,1:numnbk(ikc+1)-numnbk(ikc))
                            
                         else
                            numnbk(ikc+1)     = kmc + 1
                            fxik(ikc)         = 0.0_DP
                            dncnidk(1:3, ikc) = 0.0_DP
                         endif ktypk_eq_C
#endif

                         !
                         ! Compute g(theta) contribution
                         !

                         bo_within_cutoff1: if (rlik < this%cut_out_h(ikpot)) then
                            k        = this%neb(ik)
                            ktypk    = ktyp(k)
                            rnik     = this%bndnm(1:3, ik)
                            rik      = rlik*rnik

                            fcik     = this%cutfcnbo(ik)
                            dfcikr   = this%cutdrvbo(ik)

                            ! 
                            ! calculate length dependent terms
                            ! (constant for ijk=ccc,cch,chc).
                            !

#ifdef SEPARATE_H_ARGUMENTS
                         call h(this, ktypj, ktypi, ktypk, ijpot, ikpot, &
                              rlij, rlik, h_Dr, dh_dDr, dh_dr2)
#else
                         call h(this, ktypj, ktypi, ktypk, ijpot, ikpot, &
                              rlij - rlik, h_Dr, dh_dDr)
#endif

                            ! 
                            ! calculate angle dependent terms
                            ! ( constant for j(.)-i(c)-k(.) ).
                            !

                            !
                            ! cos( thetaijk ), g( thetaijk ) & 
                            ! dg( thetaijk ) / dcos( thetaijk )
                            ! g_costh = g( thetaijk )
                            ! dg_dcosth = dg( thetaijk ) / dcos( thetaijk )
                            !

                            costh  = dot_product(rnik, rnij)
#ifdef NUM_NEIGHBORS
                            call g(this, ktypi, ktypj, costh, nti, g_costh, dg_dcosth, dg_dn)
#else
                            call g(this, ktypj, ktypi, ktypk, ijpot, ikpot, &
                                 costh, g_costh, dg_dcosth)
#endif

                            ! 
                            ! direction cosines of rjk = ( rik - rij ) / disjk
                            !

                            dkc     = rnik * rlik - rnij * rlij
                            disjk   = sqrt( dot_product( dkc, dkc ) )
                            dkc     = dkc / disjk

                            ! 
                            ! dcos( thetaijk ) / drwh
                            ! [where w=x,y,z and h =i,j,k]
                            !

                            dcsdij  =   1.0_DP / rlik - costh * rlijr
                            dcsdik  =   rlijr - costh / rlik
                            dcsdjk  = - disjk * rlijr / rlik

                            dcsdi   = - dcsdij*rnij - dcsdik*rnik
                            dcsdj   =   dcsdij*rnij - dcsdjk*dkc
                            dcsdk   =   dcsdik*rnik + dcsdjk*dkc

                            !
                            ! dg_dn = dg( thetaijk ) / dnti
                            ! dzdni = fcik * exp * dg( thetaijk ) / dnti
                            !

#ifdef NUM_NEIGHBORS
                            dzdni = dzdni + fcik * dg_dn * h_Dr
#endif

                            ! 
                            ! fcik * exp * dg( thetaijk ) / drwh
                            ! [where w=x,y,z and h =i,j,k]
                            !

                            dzfac        = fcik * dg_dcosth * h_Dr

                            dgdi         = dzfac * dcsdi
                            dgdj         = dzfac * dcsdj
                            dgdk         = dzfac * dcsdk

#ifdef SCREENING

                            !
                            ! save for screening function derivative
                            !

                            zfaci(ikc)  = g_costh * h_Dr

#endif

                            ! 
                            ! sum etaij
                            !

                            zij    = zij + fcik * g_costh * h_Dr

                            !
                            ! fcik * g( thetaijk ) * dexp / drij
                            !

                            dzdrij = g_costh * fcik * dh_dDr

                            !
                            ! g( thetaijk ) * ( dfcik / drik * exp + fcik * 
                            ! dexp / drik )
                            !

#ifdef SEPARATE_H_ARGUMENTS
                            dzdrik = g_costh * ( dfcikr * h_Dr + fcik * dh_dr2)
#else
                            dzdrik = g_costh * ( dfcikr * h_Dr - fcik * dh_dDr)
#endif

                            ! 
                            ! sum detaij / drwh [where w=x,y,z and h =i,j,k]
                            ! g * ( fcik * dexp/drwi + dfcik/drwi * exp ) + 
                            ! fcik * exp * dg/drwi
                            !

                            dbidi  = dbidi - dzdrij*rnij - dzdrik*rnik + dgdi

                            !
                            ! g * fcik * dexp/drwj + fcik * exp * dg/drwj
                            !

                            df     = dzdrij*rnij + dgdj
                            dbidj  = dbidj + df

                            !
                            ! g * ( fcik * dexp/drwk + dfcik/drwk * exp ) + 
                            ! fcik * exp * dg/drwk
                            !

                            dbidk(1:3, ikc)  = dzdrik*rnik + dgdk

                            !
                            ! Virial
                            !

                            wijb  = wijb &
                                 - outer_product(rij, df) &
                                 - outer_product(rik, dbidk(1:3, ikc))

                         else

#ifdef SCREENING

                            zfaci(ikc)     = 0.0_DP

#endif

                            dbidk(1:3, ikc)  = 0.0_DP

                         endif bo_within_cutoff1

                      endif ik_neq_ij

                   enddo ik_loop
                   numnbi = ikc

#ifdef NUM_NEIGHBORS

                   !
                   ! Force contributions due to the g(theta) switching function
                   ! and Pcc, Pch
                   !

                   pij    = 0.0_DP
                   dpdnci = 0.0_DP
                   dpdnhi = 0.0_DP
                   dpdnoi = 0.0_DP

                   if (ktypi == rebo2_C_) then
                      if (ktypj == rebo2_C_) then
                         if (ni(rebo2_O_) .le. this%n_o_min) then
                            call eval(this%Pcc, ni(rebo2_H_), ni(rebo2_C_)+ni(rebo2_O_), &
                                      pij, dpdn1i, dpdn2i)
                            dpdnhi = dpdn1i
                            dpdnci = dpdn2i
                            dpdnoi = dpdn2i
                         else if (ni(rebo2_O_) .ge. this%n_o_max) then
                            call eval(this%Pcc_o, ni(rebo2_H_)+ni(rebo2_C_), ni(rebo2_O_), &
                                      pij, dpdn1i, dpdn2i)
                            dpdnhi = dpdn1i
                            dpdnci = dpdn1i
                            dpdnoi = dpdn2i
                         else
                            pij_tmp1    = 0.0_DP
                            dpdn1i_tmp1 = 0.0_DP
                            dpdn2i_tmp1 = 0.0_DP
                            pij_tmp2    = 0.0_DP
                            dpdn1i_tmp2 = 0.0_DP
                            dpdn2i_tmp2 = 0.0_DP

                            call eval(this%Pcc, ni(rebo2_H_), ni(rebo2_C_)+ni(rebo2_O_), &
                                      pij_tmp1, dpdn1i_tmp1, dpdn2i_tmp1)
                            call eval(this%Pcc_o, ni(rebo2_H_)+ni(rebo2_C_), ni(rebo2_O_), &
                                      pij_tmp2, dpdn1i_tmp2, dpdn2i_tmp2)

                            f_pij_sw = 0.5_DP * (1.0_DP + cos(PI * (ni(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min)))
                            df_pij_sw = -PI/(this%n_o_max-this%n_o_min) * 0.5_DP * sin(PI * (ni(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min))

                            pij    = pij_tmp1*f_pij_sw + pij_tmp2*(1.0_DP-f_pij_sw)
                            dpdnhi = dpdn1i_tmp1*f_pij_sw + dpdn1i_tmp2*(1.0_DP-f_pij_sw)
                            dpdnci = dpdn2i_tmp1*f_pij_sw + dpdn1i_tmp2*(1.0_DP-f_pij_sw)
                            dpdnoi = dpdn2i_tmp1*f_pij_sw + dpdn2i_tmp2*(1.0_DP-f_pij_sw) + (pij_tmp1-pij_tmp2)*df_pij_sw
                         end if
                      endif
                   endif

                   if (ktypi == rebo2_C_) then
                      if (ktypj == rebo2_H_) then
                         if (ni(rebo2_O_) .le. this%n_o_min) then
                            call eval(this%Pch, ni(rebo2_H_), ni(rebo2_C_)+ni(rebo2_O_), &
                                      pij, dpdn1i, dpdn2i)
                            dpdnhi = dpdn1i
                            dpdnci = dpdn2i
                            dpdnoi = dpdn2i
                         else if (ni(rebo2_O_) .ge. this%n_o_max) then
                            call eval(this%Pch_o, ni(rebo2_H_)+ni(rebo2_C_), ni(rebo2_O_), &
                                      pij, dpdn1i, dpdn2i)
                            dpdnhi = dpdn1i
                            dpdnci = dpdn1i
                            dpdnoi = dpdn2i
                         else
                            pij_tmp1    = 0.0_DP
                            dpdn1i_tmp1 = 0.0_DP
                            dpdn2i_tmp1 = 0.0_DP
                            pij_tmp2    = 0.0_DP
                            dpdn1i_tmp2 = 0.0_DP
                            dpdn2i_tmp2 = 0.0_DP

                            call eval(this%Pch, ni(rebo2_H_), ni(rebo2_C_)+ni(rebo2_O_), &
                                      pij_tmp1, dpdn1i_tmp1, dpdn2i_tmp1)
                            call eval(this%Pch_o, ni(rebo2_H_)+ni(rebo2_C_), ni(rebo2_O_), &
                                      pij_tmp2, dpdn1i_tmp2, dpdn2i_tmp2)

                            f_pij_sw = 0.5_DP * (1.0_DP + cos(PI * (ni(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min)))
                            df_pij_sw = -PI/(this%n_o_max-this%n_o_min) * 0.5_DP * sin(PI * (ni(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min))

                            pij    = pij_tmp1*f_pij_sw + pij_tmp2*(1.0_DP-f_pij_sw)
                            dpdnhi = dpdn1i_tmp1*f_pij_sw + dpdn1i_tmp2*(1.0_DP-f_pij_sw)
                            dpdnci = dpdn2i_tmp1*f_pij_sw + dpdn1i_tmp2*(1.0_DP-f_pij_sw)
                            dpdnoi = dpdn2i_tmp1*f_pij_sw + dpdn2i_tmp2*(1.0_DP-f_pij_sw) + (pij_tmp1-pij_tmp2)*df_pij_sw
                         end if
                      endif
                   endif

                   if (ktypi == rebo2_C_) then
                      if (ktypj == rebo2_O_) then
                         call eval(this%Pco, ni(rebo2_H_)+ni(rebo2_C_), &
                              ni(rebo2_O_), pij, dpdn1i, dpdn2i)
                         dpdnhi = dpdn1i
                         dpdnci = dpdn1i
                         dpdnoi = dpdn2i
                      endif
                   endif

                   if (ktypi == rebo2_O_) then
                      if (ktypj == rebo2_C_) then
                         call eval(this%Poc, ni(rebo2_H_)+ni(rebo2_C_), &
                              ni(rebo2_O_), pij, dpdn1i, dpdn2i)
                         dpdnhi = dpdn1i
                         dpdnci = dpdn1i
                         dpdnoi = dpdn2i
                      endif
                   endif

                   if (ktypi == rebo2_O_) then
                      if (ktypj == rebo2_H_) then
                         call eval(this%Poh, ni(rebo2_H_)+ni(rebo2_C_), &
                              ni(rebo2_O_), pij, dpdn1i, dpdn2i)
                         dpdnhi = dpdn1i
                         dpdnci = dpdn1i
                         dpdnoi = dpdn2i
                      endif
                   endif

                   if (ktypi == rebo2_O_) then
                      if (ktypj == rebo2_O_) then
                         call eval(this%Poo, ni(rebo2_H_)+ni(rebo2_C_), &
                              ni(rebo2_O_), pij, dpdn1i, dpdn2i)
                         dpdnhi = dpdn1i
                         dpdnci = dpdn1i
                         dpdnoi = dpdn2i
                      endif
                   endif

                   if (ktypi == rebo2_H_) then
                      if (ktypj == rebo2_O_) then
                         call eval(this%Pho, ni(rebo2_H_)+ni(rebo2_C_), &
                              ni(rebo2_O_), pij, dpdn1i, dpdn2i)
                         dpdnhi = dpdn1i
                         dpdnci = dpdn1i
                         dpdnoi = dpdn2i
                      endif
                   endif

                   if (ktypi == rebo2_H_) then
                      if (ktypj == rebo2_H_) then
                         call eval(this%Phh, ni(rebo2_H_), ni(rebo2_C_)+ni(rebo2_O_), &
                                   pij, dpdn1i, dpdn2i)
                         dpdnhi = dpdn1i
                         dpdnci = dpdn2i
                         dpdnoi = dpdn2i
                      endif
                   endif



#ifdef DEBUG_PRINT
!                   write (*, '(A,2I3,4F15.7)')  "(ij) P "//rebo2_el_strs(ktypi)//" "//rebo2_el_strs(ktypj)//":", i, j, ni(rebo2_H_), ni(rebo2_C_), ni(rebo2_O_), pij
                   write (*, '(A,2I3,2X,3I3,F15.7)')  "(ij) P "//rebo2_el_strs(ktypi)//" "//rebo2_el_strs(ktypj)//":", i, j, nint(ni(rebo2_H_))+1, nint(ni(rebo2_C_))+1, nint(ni(rebo2_O_))+1, pij
#endif

                   zij = zij + pij
                   
                   dpdnci = dpdnci + dzdni
                   dpdnhi = dpdnhi + dzdni
                   dpdnoi = dpdnoi + dzdni 
                   
#endif

                   ! 
                   ! bij & 0.5 * fcij * faij * dbij / detaij 
                   ! 

                   call bo(this, ktypi, ijpot, zij, fcij, faij, bij, dfbij)

                   ! 
                   ! do the same for to atom j.
                   ! 
                   ! calculate components of bond order term and derivatives
                   ! with respect to bond i-j for atom j.
                   !

                   zji    = 0.0_DP
                   dbjdi  = 0.0_DP
                   dbjdj  = 0.0_DP

#ifdef NUM_NEIGHBORS
                   dzdnj     = 0.0_DP
#endif

                   ! 
                   ! j--l loop.
                   jlc        = 0
                   lnc        = 0
                   numnbl(1)  = 1
                   jl_loop: do jl = this%neb_seed(j), this%neb_last(j)
                      l    = this%neb(jl)

                      ! consider all neighbours of j, except i.
#ifdef LAMMPS
                      l_neq_i: if (l /= i) then
#else
                      ldc  = jdc + this%dcell(jl)
                      l_neq_i: if (l /= i .or. ldc /= 0) then
#endif
                         jlc           = jlc + 1

                         nebofj(jlc)   = l
#ifndef LAMMPS
                         dcofj(jlc)    = ldc
#endif

#ifdef SCREENING
                         seedj(jlc)    = this%sneb_seed(jl)
                         lastj(jlc)    = this%sneb_last(jl)
#endif

                         ktypl         = ktyp(l)
                         jlpot         = this%bndtyp(jl)
                         rljl          = this%bndlen(jl)
                         rnjl          = this%bndnm(1:3, jl)

                         drj(1:3, jlc) = rljl*rnjl

                         ! 
                         ! calculate length dependent terms
                         ! (constant for jil=ccc,cch,chc).
                         !

#ifdef NUM_NEIGHBORS
                         fcjl         = this%cutfcnnc(jl)
                         dfcjlr       = this%cutdrvnc(jl)

                         !nj(ktypl)    = nj(ktypl) + fcjl
                         dnjdjl(1:3, jlc, ktypl) = rnjl * dfcjlr

                         ! 
                         ! sum nijconj if c-c bond and l  is carbon.
                         !

                         ! FIXME!!! Generalize
                         ktypl_eq_C: if (ktypl == rebo2_C_) then

                            forall (ln = this%neb_seed(l):this%neb_last(l))

                               nebofl(lnc + ln-this%neb_seed(l)+1)  = this%neb(ln)
#ifndef LAMMPS
                               dcofl(lnc + ln-this%neb_seed(l)+1)   = ldc + &
                                    this%dcell(ln)
#endif

#ifdef SCREENING
                               seedl(lnc + ln-this%neb_seed(l)+1)   = &
                                    this%sneb_seed(ln)
                               lastl(lnc + ln-this%neb_seed(l)+1)   = &
                                    this%sneb_last(ln)
#endif

                               drl(1:3, lnc + ln-this%neb_seed(l)+1)  = &
                                    this%bndlen(ln)*this%bndnm(1:3, ln)

                               xjldn(1:3, ln-this%neb_seed(l)+1)      = &
                                    this%cutdrvnc(ln)*this%bndnm(1:3, ln)

                            endforall

                            xjl   = this%nn(rebo2_H_, l) + this%nn(rebo2_C_, l) - fcjl
                            xjldl = &
                                 -sum(xjldn(1:3,1:this%neb_last(l)-this%neb_seed(l)+1),2)&
                                 +dnjdjl(1:3, jlc, ktypl)

                            lnc            = lnc + this%neb_last(l)-this%neb_seed(l)+1
                            numnbl(jlc+1)  = lnc + 1

                            ! 
                            ! sum f(xik) and derivatives.
                            !

                            call fconj(this, xjl, fxjl(jlc), dfxjlx)

                            nconjdr = fxjl(jlc) * dfcjlr
                            nconjdx = fcjl * dfxjlx

                            dnconjjdxj(jlc) = nconjdx

                            nconjj            = nconjj + fcjl * fxjl(jlc)
                            dncnjdl(1:3, jlc) = nconjdr * rnjl ! + nconjdx * xjldl(:)

                            dncnjdn(1:3, numnbl(jlc):numnbl(jlc+1)-1) = &
                                 nconjdx * xjldn(1:3, 1:numnbl(jlc+1)-numnbl(jlc))

                         else
                            numnbl(jlc+1)     = lnc + 1
                            fxjl(jlc)         = 0.0_DP
                            dncnjdl(1:3, jlc) = 0.0_DP
                         endif ktypl_eq_C
#endif

                         !
                         ! Compute g(theta) contribution
                         !

                         bo_within_cutoff2: if (rljl < this%cut_out_h(jlpot)) then

                            ktypl    = ktyp(l)
                            rnjl     = this%bndnm(1:3, jl)
                            rjl      = rljl*rnjl

                            fcjl     = this%cutfcnbo(jl)
                            dfcjlr   = this%cutdrvbo(jl)

                            ! 
                            ! calculate length dependent terms
                            ! (constant for jil=ccc,cch,chc).
                            !

#ifdef SEPARATE_H_ARGUMENTS
                            call h(this, ktypi, ktypj, ktypl, ijpot, jlpot, &
                                 rlij, rljl, h_Dr, dh_dDr, dh_dr2)
#else
                            call h(this, ktypi, ktypj, ktypl, ijpot, jlpot, &
                                 rlij - rljl, h_Dr, dh_dDr)
#endif


                            ! 
                            ! calculate angle dependent terms
                            ! ( constant for i(.)-j(c)-l(.) ).
                            !

                            ! 
                            ! cos( thetajil ), g( thetajil ) & dg( thetajil ) / dcos( thetajil )
                            ! g_costh = g( thetaijk )
                            ! dg_dcosth = dg( thetaijk ) / dcos( thetaijk )
                            !

                            costh = -dot_product(rnjl, rnij)
#ifdef NUM_NEIGHBORS
                            call g(this, ktypj, ktypi, costh, ntj, g_costh, dg_dcosth, dg_dn)
#else
                            call g(this, ktypi, ktypj, ktypl, ijpot, jlpot, &
                                 costh, g_costh, dg_dcosth)
#endif

                            ! 
                            ! direction cosines of ril = ( rjl - rji ) / disjl
                            !

                            dlc     = rnjl * rljl + rnij * rlij
                            disil   = sqrt( dot_product( dlc, dlc ) )
                            dlc     = dlc / disil

                            ! 
                            ! dcos( thetajil ) / drwh
                            ! [where w=x,y,z and h =j,i,l]
                            !

                            dcsdji =  1.0_DP / rljl - costh * rlijr
                            dcsdjl =  rlijr - costh / rljl
                            dcsdil = -disil * rlijr / rljl

                            dcsdj  =   dcsdji*rnij - dcsdjl*rnjl
                            dcsdi  = - dcsdji*rnij                  - dcsdil*dlc
                            dcsdl  =                    dcsdjl*rnjl + dcsdil*dlc

                            !
                            ! dg_dn = dg( thetajil ) / dntj
                            ! dzdnj = fcjl * exp * dg( thetajil ) / dnj
                            !

#ifdef NUM_NEIGHBORS
                            dzdnj = dzdnj + fcjl * dg_dn * h_Dr
#endif

                            ! 
                            ! fcjl * exp * dg( thetajil ) / drwh
                            ! [where w=x,y,z and h =j,i,l]
                            !

                            dzfac = fcjl * dg_dcosth * h_Dr

                            dgdj  = dzfac * dcsdj 
                            dgdi  = dzfac * dcsdi
                            dgdl  = dzfac * dcsdl

#ifdef SCREENING

                            !
                            ! save for screening function derivative
                            !

                            zfacj(jlc)  = g_costh * h_Dr

#endif

                            ! 
                            ! sum etaji
                            !

                            zji    = zji + fcjl * g_costh * h_Dr

                            ! 
                            ! fcjl * g( thetajil ) * dexp / drji
                            !

                            dzdrji = g_costh * fcjl * dh_dDr

                            ! 
                            ! g( thetajil ) * ( dfcjl / drjl * exp + fcjl * 
                            ! dexp / drjl )
                            !

#ifdef SEPARATE_H_ARGUMENTS
                            dzdrjl = g_costh * ( dfcjlr * h_Dr + fcjl * dh_dr2 )
#else
                            dzdrjl = g_costh * ( dfcjlr * h_Dr - fcjl * dh_dDr )
#endif

                            ! 
                            ! sum detaji / drwh [where w=x,y,z and h =j,i,l]
                            ! g * ( fcjl * dexp/drwj + dfcjl/drwj * exp ) + 
                            ! fcjl * exp * dg/drwj
                            !

                            dbjdj = dbjdj + dzdrji*rnij - dzdrjl*rnjl + dgdj

                            !
                            ! g * fcjl * dexp/drwi * fcjl * exp * dg/drwi
                            !

                            df          = - dzdrji*rnij + dgdi
                            dbjdi       = dbjdi + df

                            !
                            ! g * ( fcjl * dexp/drwl + dfcjl/drwl * exp ) + 
                            ! fcjl * exp * dg/drwl
                            !

                            dbjdl(1:3, jlc)  = dzdrjl*rnjl + dgdl

                            !
                            ! Virial
                            !

                            wjib  = wjib &
                                 + outer_product(rij, df) &
                                 - outer_product(rjl, dbjdl(1:3, jlc))

                         else

#ifdef SCREENING

                            zfacj(jlc)     = 0.0_DP

#endif

                            dbjdl(1:3, jlc)  = 0.0_DP

                         endif bo_within_cutoff2

                      endif l_neq_i

                   enddo jl_loop
                   numnbj = jlc

#ifdef NUM_NEIGHBORS

                   !
                   ! Force contributions due to the g(theta) switching function
                   ! and Pcc, Pch
                   !

                   pji    = 0.0_DP
                   dpdncj = 0.0_DP
                   dpdnhj = 0.0_DP
                   dpdnoj = 0.0_DP

                   if (ktypj == rebo2_C_) then
                      if (ktypi == rebo2_C_) then
                         if (nj(rebo2_O_) .le. this%n_o_min) then
                            call eval(this%Pcc, nj(rebo2_H_), nj(rebo2_C_)+nj(rebo2_O_), &
                                      pji, dpdn1j, dpdn2j)
                            dpdnhj = dpdn1j
                            dpdncj = dpdn2j
                            dpdnoj = dpdn2j
                         else if (nj(rebo2_O_) .ge. this%n_o_max) then
                            call eval(this%Pcc_o, nj(rebo2_H_)+nj(rebo2_C_), nj(rebo2_O_), &
                                      pji, dpdn1j, dpdn2j)
                            dpdnhj = dpdn1j
                            dpdncj = dpdn1j
                            dpdnoj = dpdn2j
                         else
                            pji_tmp1    = 0.0_DP
                            dpdn1j_tmp1 = 0.0_DP
                            dpdn2j_tmp1 = 0.0_DP
                            pji_tmp2    = 0.0_DP
                            dpdn1j_tmp2 = 0.0_DP
                            dpdn2j_tmp2 = 0.0_DP

                            call eval(this%Pcc, nj(rebo2_H_), nj(rebo2_C_)+nj(rebo2_O_), &
                                      pji_tmp1, dpdn1j_tmp1, dpdn2j_tmp1)
                            call eval(this%Pcc_o, nj(rebo2_H_)+nj(rebo2_C_), nj(rebo2_O_), &
                                      pji_tmp2, dpdn1j_tmp2, dpdn2j_tmp2)

                            f_pji_sw = 0.5_DP * (1.0_DP + cos(PI * (nj(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min)))
                            df_pji_sw = -PI/(this%n_o_max-this%n_o_min) * 0.5_DP * sin(PI * (nj(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min))

                            pji    = pji_tmp1*f_pji_sw + pji_tmp2*(1.0_DP-f_pji_sw)
                            dpdnhj = dpdn1j_tmp1*f_pji_sw + dpdn1j_tmp2*(1.0_DP-f_pji_sw)
                            dpdncj = dpdn2j_tmp1*f_pji_sw + dpdn1j_tmp2*(1.0_DP-f_pji_sw)
                            dpdnoj = dpdn2j_tmp1*f_pji_sw + dpdn2j_tmp2*(1.0_DP-f_pji_sw) + (pji_tmp1-pji_tmp2)*df_pji_sw
                         end if
                      endif
                   endif

                   if (ktypj == rebo2_C_) then
                      if (ktypi == rebo2_H_) then
                         if (nj(rebo2_O_) .le. this%n_o_min) then
                            call eval(this%Pch, nj(rebo2_H_), nj(rebo2_C_)+nj(rebo2_O_), &
                                      pji, dpdn1j, dpdn2j)
                            dpdnhj = dpdn1j
                            dpdncj = dpdn2j
                            dpdnoj = dpdn2j
                         else if (nj(rebo2_O_) .ge. this%n_o_max) then
                            call eval(this%Pch_o, nj(rebo2_H_)+nj(rebo2_C_), nj(rebo2_O_), &
                                      pji, dpdn1j, dpdn2j)
                            dpdnhj = dpdn1j
                            dpdncj = dpdn1j
                            dpdnoj = dpdn2j
                         else
                            pji_tmp1    = 0.0_DP
                            dpdn1j_tmp1 = 0.0_DP
                            dpdn2j_tmp1 = 0.0_DP
                            pji_tmp2    = 0.0_DP
                            dpdn1j_tmp2 = 0.0_DP
                            dpdn2j_tmp2 = 0.0_DP

                            call eval(this%Pch, nj(rebo2_H_), nj(rebo2_C_)+nj(rebo2_O_), &
                                      pji_tmp1, dpdn1j_tmp1, dpdn2j_tmp1)
                            call eval(this%Pch_o, nj(rebo2_H_)+nj(rebo2_C_), nj(rebo2_O_), &
                                      pji_tmp2, dpdn1j_tmp2, dpdn2j_tmp2)

                            f_pji_sw = 0.5_DP * (1.0_DP + cos(PI * (nj(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min)))
                            df_pji_sw = -PI/(this%n_o_max-this%n_o_min) * 0.5_DP * sin(PI * (nj(rebo2_O_)-this%n_o_min) / (this%n_o_max-this%n_o_min))

                            pji    = pji_tmp1*f_pji_sw + pji_tmp2*(1.0_DP-f_pji_sw)
                            dpdnhj = dpdn1j_tmp1*f_pji_sw + dpdn1j_tmp2*(1.0_DP-f_pji_sw)
                            dpdncj = dpdn2j_tmp1*f_pji_sw + dpdn1j_tmp2*(1.0_DP-f_pji_sw)
                            dpdnoj = dpdn2j_tmp1*f_pji_sw + dpdn2j_tmp2*(1.0_DP-f_pji_sw) + (pji_tmp1-pji_tmp2)*df_pji_sw
                         end if
                      endif
                   endif

                   if (ktypj == rebo2_C_) then
                      if (ktypi == rebo2_O_) then
                         call eval(this%Pco, nj(rebo2_H_)+nj(rebo2_C_), &
                              nj(rebo2_O_), pji, dpdn1j, dpdn2j)
                         dpdnhj = dpdn1j
                         dpdncj = dpdn1j
                         dpdnoj = dpdn2j
                      endif
                   endif

                   if (ktypj == rebo2_O_) then
                      if (ktypi == rebo2_C_) then
                         call eval(this%Poc, nj(rebo2_H_)+nj(rebo2_C_), &
                              nj(rebo2_O_), pji, dpdn1j, dpdn2j)
                         dpdnhj = dpdn1j
                         dpdncj = dpdn1j
                         dpdnoj = dpdn2j
                      endif
                   endif

                   if (ktypj == rebo2_O_) then
                      if (ktypi == rebo2_H_) then
                         call eval(this%Poh, nj(rebo2_H_)+nj(rebo2_C_), &
                              nj(rebo2_O_), pji, dpdn1j, dpdn2j)
                         dpdnhj = dpdn1j
                         dpdncj = dpdn1j
                         dpdnoj = dpdn2j
                      endif
                   endif

                   if (ktypj == rebo2_O_) then
                      if (ktypi == rebo2_O_) then
                         call eval(this%Poo, nj(rebo2_H_)+nj(rebo2_C_), &
                              nj(rebo2_O_), pji, dpdn1j, dpdn2j)
                         dpdnhj = dpdn1j
                         dpdncj = dpdn1j
                         dpdnoj = dpdn2j
                      endif
                   endif

                   if (ktypj == rebo2_H_) then
                      if (ktypi == rebo2_O_) then
                         call eval(this%Pho, nj(rebo2_H_)+nj(rebo2_C_), &
                              nj(rebo2_O_), pji, dpdn1j, dpdn2j)
                         dpdnhj = dpdn1j
                         dpdncj = dpdn1j
                         dpdnoj = dpdn2j
                      endif
                   endif

                   if (ktypj == rebo2_H_) then
                      if (ktypi == rebo2_H_) then
                         call eval(this%Phh, nj(rebo2_H_), nj(rebo2_C_)+nj(rebo2_O_), &
                                   pji, dpdn1j, dpdn2j)
                         dpdnhj = dpdn1j
                         dpdncj = dpdn2j
                         dpdnoj = dpdn2j
                      endif
                   endif



#ifdef DEBUG_PRINT
!                   write (*, '(A,2I3,4F15.7)')  "(ji) P "//rebo2_el_strs(ktypj)//" "//rebo2_el_strs(ktypi)//":", j, i, nj(rebo2_H_), nj(rebo2_C_), nj(rebo2_O_), pji
                   write (*, '(A,2I3,2X,3I3,F15.7)')  "(ji) P "//rebo2_el_strs(ktypj)//" "//rebo2_el_strs(ktypi)//":", j, i, nint(nj(rebo2_H_))+1, nint(nj(rebo2_C_))+1, nint(nj(rebo2_O_))+1, pji
#endif

                   zji = zji + pji

                   dpdncj = dpdncj + dzdnj
                   dpdnhj = dpdnhj + dzdnj
                   dpdnoj = dpdnoj + dzdnj
#endif

                   ! 
                   ! bji & 0.5 * fcij * faij * dbji / detaji 
                   ! 

                   call bo(this, ktypj, ijpot, zji, fcij, faij, bji, dfbji)

                   !
                   ! conjugation variables
                   !

#ifdef NUM_NEIGHBORS
                   if (this%const_nconj) then
                      nconji = 0.0_DP
                      nconjj = 0.0_DP
                   endif
#ifdef SEP_NCONJ
                   if (nconji > 3.0_DP)  nconji = 3.0_DP
                   if (nconjj > 3.0_DP)  nconjj = 3.0_DP
#else
                   nconj = nconji**2 + nconjj**2
                   if (nconj > 9.0_DP)  nconj = 9.0_DP
#endif

                   if (nti > 3.0_DP)     nti = 3.0_DP
                   if (ntj > 3.0_DP)     ntj = 3.0_DP
#endif

#ifdef DIHEDRAL

                   !
                   ! dihedral potential
                   !

                   bdh     = 0.0_DP
                   tij     = 0.0_DP
                   dtdni   = 0.0_DP
                   dtdnj   = 0.0_DP
                   dtdncn  = 0.0_DP

                   if (this%with_dihedral) then

                      ijpot_is_C_C: if (ijpot == C_C) then

                         call eval(this%Tcc, nti, ntj, nconj, tij, dtdni, dtdnj, dtdncn)
                         tije = tij*faij*fcij

                         if (tij /= 0) then

                            rlijsq = rlij**2

                            ik_loop3: do ik = istart, ifinsh
                               ! consider all atoms bound to i, except atom j.
                               if (ik /= ij) then
                                  k        = this%neb(ik)
#ifndef LAMMPS
                                  kdc      = this%dcell(ik)
#endif
                                  rlik     = this%bndlen(ik)
                                  rnik     = this%bndnm(1:3, ik)

                                  fcik     = this%cutfcnbo(ik)
                                  dfcikr   = this%cutdrvbo(ik)

                                  dot_ij_ik  = dot_product(rnij, rnik)
                                  dcik       = 1.0_DP - dot_ij_ik**2

                                  do jl = this%neb_seed(j), this%neb_last(j)
                                     l    = this%neb(jl)
#ifndef LAMMPS
                                     ldc  = jdc + this%dcell(jl)
#endif

                                     !
                                     ! consider all neighbours of j, except i
                                     ! and k
                                     !

#ifdef LAMMPS
                                     if (l /= i .and. l /= k) then
#else
                                     if ((l /= i .or. ldc /= 0) .and. &
                                         (l /= k .or. ldc /= kdc)) then
#endif
                                        rljl     = this%bndlen(jl)
                                        rnjl     = this%bndnm(1:3, jl)

                                        fcjl     = this%cutfcnbo(jl)
                                        dfcjlr   = this%cutdrvbo(jl)

                                        dot_ij_jl  = dot_product(rnij, rnjl)
                                        dot_ik_jl  = dot_product(rnik, rnjl)
                                        dcjl       = 1.0_DP - dot_ij_jl**2
                                        abs_dc     = sqrt( dcik*dcjl )

                                        costijkl = ( dot_ij_ik*dot_ij_jl - dot_ik_jl ) / abs_dc

                                        bdhij    = 1-costijkl**2
                                        bdh      = bdh + bdhij*fcik*fcjl
                                        bdhij    = bdhij*tij*faij*fcij/2

                                        dbdhij   = -2*costijkl*tije*fcik*fcjl/2

                                        df = &
                                             dbdhij * &
                                             ( ( dot_ij_jl/abs_dc + costijkl*dot_ij_ik/dcik ) * rnik &
                                             + ( dot_ij_ik/abs_dc + costijkl*dot_ij_jl/dcjl ) * rnjl &
                                             - ( 2*dot_ik_jl/abs_dc + costijkl*(1.0_DP/dcik + 1.0_DP/dcjl) ) * rnij ) / rlij

                                        !                               VEC3(f, i) = VEC3(f, i) + df(:)
                                        !                               VEC3(f, j) = VEC3(f, j) + (- df(:))
                                        fi     = fi + df
                                        fj     = fj - df

                                        wij    = wij + outer_product(rlij*rnij, df)

                                        df = &
                                             dbdhij * &
                                             ( - 1.0_DP/dcik * costijkl * rnik &
                                             - 1.0_DP/abs_dc * rnjl &
                                             + ( dot_ij_jl/abs_dc + costijkl*dot_ij_ik/dcik ) * rnij ) / rlik &
                                             + bdhij*dfcikr*fcjl * rnik

                                        !                               VEC3(f, i) = VEC3(f, i) + df(:)
                                        fi          = fi         + df
                                        VEC3(f, k)  = VEC3(f, k) + (- df)

                                        wij   = wij + outer_product(rlik*rnik, df)

                                        df = &
                                             dbdhij * &
                                             ( - 1.0_DP/dcjl * costijkl * rnjl &
                                             - 1.0_DP/abs_dc * rnik &
                                             + ( dot_ij_ik/abs_dc + costijkl*dot_ij_jl/dcjl ) * rnij ) / rljl &
                                             + bdhij*fcik*dfcjlr * rnjl

                                        !                               VEC3(f, j) = VEC3(f, j) + df(:)
                                        fj          = fj         + df
                                        VEC3(f, l)  = VEC3(f, l) + (- df)

                                        wij  = wij + outer_product(rljl*rnjl, df)

#ifdef SCREENING

                                        dffac = bdhij*fcjl

                                        i1 = this%sneb_seed(ik)
                                        i2 = this%sneb_last(ik)
                                        if (i1 <= i2) then
                                           this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + dffac
                                        endif

                                        dffac = bdhij*fcik

                                        i1 = this%sneb_seed(jl)
                                        i2 = this%sneb_last(jl)
                                        if (i1 <= i2) then
                                           this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + dffac
                                        endif

#endif SCREENING

                                     endif

                                  enddo

                               endif

                            enddo ik_loop3

                         endif

                      endif ijpot_is_C_C

                   endif

#endif


#ifdef ALT_DIHEDRAL

                   !
                   ! dihedral potential (alternative formulation)
                   !

                   bdh     = 0.0_DP
                   tij     = 0.0_DP
                   dtdni   = 0.0_DP
                   dtdnj   = 0.0_DP
                   dtdncn  = 0.0_DP

                   if (this%with_dihedral) then

                      ijpot_is_C_C: if (ijpot == C_C) then

                         call eval(this%Tcc, nti, ntj, nconj, tij, dtdni, dtdnj, dtdncn)

                         tij     = 2*tij
                         dtdni   = 2*dtdni
                         dtdnj   = 2*dtdnj
                         dtdncn  = 2*dtdncn

                         !                tij  = 0.01
                         tije = tij*faij*fcij

                         tij_neq_0: if (tij /= 0) then

                            rlijsq = rlij**2

                            ik1_loop: do ik1 = istart, ifinsh-1
                               !  consider all atoms bound to i, except atom j.
                               ik1_neq_ij: if (ik1 /= ij) then
                                  k1        = this%neb(ik1)
#ifndef LAMMPS
                                  kdc1      = this%dcell(ik1)
#endif
                                  rlik1     = this%bndlen(ik1)
                                  ikpot     = this%bndtyp(ik1)

                                  ik1_within_cutoff: if (rlik1 < this%cut_out_h(ikpot)) then

                                     rnik1     = this%bndnm(1:3, ik1)

                                     fcik1     = this%cutfcnbo(ik1)
                                     dfcik1r   = this%cutdrvbo(ik1)

                                     ik2_loop: do ik2 = ik1+1, ifinsh
                                        ik2_neq_ij: if (ik2 /= ij) then
                                           k2           = this%neb(ik2)
#ifndef LAMMPS
                                           kdc2         = this%dcell(ik2)
#endif
                                           rlik2        = this%bndlen(ik2)
                                           ikpot        = this%bndtyp(ik2)

                                           ik2_within_cutoff: if (rlik2 < this%cut_out_h(ikpot)) then

                                              rnik2        = this%bndnm(1:3, ik2)

                                              rk1k2        = rlik2*rnik2 - rlik1*rnik1

                                              dot_ij_k1k2  = dot_product(rij, rk1k2)
                                              dck1k2       = rlijsq*dot_product(rk1k2, rk1k2) - dot_product(rij, rk1k2)**2

                                              fcik2        = this%cutfcnbo(ik2)
                                              dfcik2r      = this%cutdrvbo(ik2)

                                              jl1_loop: do jl1 = this%neb_seed(j), this%neb_last(j)-1
                                                 l1    = this%neb(jl1)
#ifndef LAMMPS
                                                 ldc1  = jdc + this%dcell(jl1)
#endif

                                                 !
                                                 ! consider all neighbours of j,
                                                 ! except i and k
                                                 !

#ifdef LAMMPS
                                                 jl1_neq_i_k: if (l1 /= i .and. l1 /= k1 .and. l1 /= k2) then
#else
                                                 jl1_neq_i_k: if ( &
                                                      (l1 /= i .or. ldc1 /= 0) .and. &
                                                      (l1 /= k1 .or. ldc1 /= kdc1) .and. &
                                                      (l1 /= k2 .or. ldc1 /= kdc2) &
                                                      ) then
#endif
                                                    rljl1     = this%bndlen(jl1)
                                                    jlpot     = this%bndtyp(jl1)

                                                    jl1_within_cutoff: if (rljl1 < this%cut_out_h(jlpot)) then

                                                       rnjl1     = this%bndnm(1:3, jl1)

                                                       fcjl1     = this%cutfcnbo(jl1)
                                                       dfcjl1r   = this%cutdrvbo(jl1)

                                                       jl2_loop: do jl2 = jl1+1, this%neb_last(j)
                                                          l2    = this%neb(jl2)
#ifndef LAMMPS
                                                          ldc2  = jdc + this%dcell(jl2)
#endif

                                                          !
                                                          ! consider all neighbours of j, except i and k
                                                          !

#ifdef LAMMPS
                                                          jl2_neq_i_k: if (l2 /= i .and. l2 /= k1 .and. l2 /= k2) then
#else
                                                          jl2_neq_i_k: if ( &
                                                               (l2 /= i .or. ldc2 /= 0) .and. & 
                                                               (l2 /= k1 .or. ldc2 /= kdc1) .and. &
                                                               (l2 /= k2 .or. ldc2 /= kdc2) &
                                                               ) then
#endif
                                                             rljl2          = this%bndlen(jl2)
                                                             jlpot          = this%bndtyp(jl2)

                                                             jl2_within_cutoff: if (rljl2 < this%cut_out_h(jlpot)) then

                                                                rnjl2          = this%bndnm(1:3, jl2)

                                                                fcjl2          = this%cutfcnbo(jl2)
                                                                dfcjl2r        = this%cutdrvbo(jl2)

                                                                rl1l2          = rljl2*rnjl2 - rljl1*rnjl1

                                                                dot_ij_l1l2    = dot_product(rij, rl1l2)
                                                                dot_k1k2_l1l2  = dot_product(rk1k2, rl1l2)
                                                                dcl1l2         = rlijsq*dot_product(rl1l2, rl1l2) - dot_product(rij, rl1l2)**2

                                                                abs_dc         = sqrt( dck1k2*dcl1l2 )

                                                                costijkl       = ( dot_ij_k1k2*dot_ij_l1l2 - rlijsq*dot_k1k2_l1l2 ) / abs_dc

                                                                bdhij          = 1-costijkl**2
                                                                bdh            = bdh + bdhij*fcik1*fcik2*fcjl1*fcjl2
                                                                bdhij          = bdhij*tij*faij*fcij/2

                                                                dbdhij         = -2*costijkl*tije*fcik1*fcik2*fcjl1*fcjl2/2

                                                                df = &
                                                                     dbdhij * &
                                                                     ( ( dot_ij_l1l2/abs_dc + costijkl*dot_ij_k1k2/dck1k2 ) * rk1k2 &
                                                                     + ( dot_ij_k1k2/abs_dc + costijkl*dot_ij_l1l2/dcl1l2 ) * rl1l2 &
                                                                     - ( 2*dot_k1k2_l1l2/abs_dc &
                                                                     + costijkl*( dot_product(rk1k2, rk1k2)/dck1k2 &
                                                                     + dot_product(rl1l2, rl1l2)/dcl1l2 ) ) * rij )

                                                                !                                                       VEC3(f, i) = VEC3(f, i) + df(:)
                                                                !                                                       VEC3(f, j) = VEC3(f, j) + (- df(:))
                                                                fi        = fi + df
                                                                fj        = fj - df

                                                                wij  = wij + outer_product(rij, df)

                                                                df = &
                                                                     dbdhij * &
                                                                     ( - ( 1.0_DP/dck1k2 * costijkl * rk1k2 &
                                                                     + 1.0_DP/abs_dc * rl1l2 ) * rlijsq &
                                                                     + ( dot_ij_l1l2/abs_dc + costijkl*dot_ij_k1k2/dck1k2 ) * rij )

                                                                VEC3(f, k1) = VEC3(f, k1) + df
                                                                VEC3(f, k2) = VEC3(f, k2) + (- df)

                                                                wij   = wij + outer_product(rk1k2, df)

                                                                df = &
                                                                     dbdhij * &
                                                                     ( - ( 1.0_DP/dcl1l2 * costijkl * rl1l2 &
                                                                     + 1.0_DP/abs_dc * rk1k2 ) * rlijsq &
                                                                     + ( dot_ij_k1k2/abs_dc + costijkl*dot_ij_l1l2/dcl1l2 ) * rij )

                                                                VEC3(f, l1) = VEC3(f, l1) + df
                                                                VEC3(f, l2) = VEC3(f, l2) + (- df)

                                                                wij  = wij + outer_product(rl1l2, df)

                                                                df = &
                                                                     bdhij*dfcik1r*fcik2*fcjl1*fcjl2 * rnik1

                                                                !                                                       VEC3(f, i)  = VEC3(f, i) + df(:)
                                                                fi           = fi          + df
                                                                VEC3(f, k1)  = VEC3(f, k1) + (- df)

                                                                wij  = wij + outer_product(rlik1*rnik1, df)

                                                                df = &
                                                                     bdhij*dfcik2r*fcik1*fcjl1*fcjl2 * rnik2

                                                                !                                                       VEC3(f, i)  = VEC3(f, i) + df(:)
                                                                fi           = fi          + df
                                                                VEC3(f, k2)  = VEC3(f, k2) + (- df) 

                                                                wij  = wij + outer_product(rlik2*rnik2, df)

                                                                df = &
                                                                     bdhij*dfcjl1r*fcjl2*fcik1*fcik2 * rnjl1

                                                                !                                                       VEC3(f, j)  = VEC3(f, j) + df(:)
                                                                fj           = fj          + df
                                                                VEC3(f, l1)  = VEC3(f, l1) + (- df)

                                                                wij  = wij + outer_product(rljl1*rnjl1, df)

                                                                df = &
                                                                     bdhij*dfcjl2r*fcjl1*fcik1*fcik2 * rnjl2

                                                                !                                                       VEC3(f, j)  = VEC3(f, j) + df(:)
                                                                fj           = fj          + df
                                                                VEC3(f, l2)  = VEC3(f, l2) + (- df)

                                                                wij  = wij + outer_product(rljl2*rnjl2, df)

#ifdef SCREENING

                                                                dffac = bdhij*fcik2*fcjl1*fcjl2

                                                                i1 = this%sneb_seed(ik1)
                                                                i2 = this%sneb_last(ik1)
                                                                if (i1 <= i2) then
                                                                   this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + dffac
                                                                endif

                                                                dffac = bdhij*fcik1*fcjl1*fcjl2

                                                                i1 = this%sneb_seed(ik2)
                                                                i2 = this%sneb_last(ik2)
                                                                if (i1 <= i2) then
                                                                   this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + dffac
                                                                endif

                                                                dffac = bdhij*fcjl2*fcik1*fcik2

                                                                i1 = this%sneb_seed(jl1)
                                                                i2 = this%sneb_last(jl1)
                                                                if (i1 <= i2) then
                                                                   this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + dffac
                                                                endif

                                                                dffac = bdhij*fcjl1*fcik1*fcik2

                                                                i1 = this%sneb_seed(jl2)
                                                                i2 = this%sneb_last(jl2)
                                                                if (i1 <= i2) then
                                                                   this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + dffac
                                                                endif

#endif SCREENING

                                                             endif jl2_within_cutoff

                                                          endif jl2_neq_i_k

                                                       enddo jl2_loop

                                                    endif jl1_within_cutoff

                                                 endif jl1_neq_i_k

                                              enddo jl1_loop

                                           endif ik2_within_cutoff

                                        endif ik2_neq_ij

                                     enddo ik2_loop

                                  endif ik1_within_cutoff

                               endif ik1_neq_ij

                            enddo ik1_loop

                         endif tij_neq_0

                      endif ijpot_is_C_C

                   endif

#endif

#ifdef NUM_NEIGHBORS

                   !
                   ! compute F-value and derivatives
                   !

                   fij    = 0.0_DP
                   dfdni  = 0.0_DP
                   dfdnj  = 0.0_DP

#ifdef SEP_NCONJ

                   dfdncni = 0.0_DP
                   dfdncnj = 0.0_DP

                   if (ijpot == C_C) then

                      call eval(this%Fcc, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj)

                   else if (ijpot == H_H) then

                      call eval(this%Fhh, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj)

                   else if (ijpot == C_H) then

                      call eval(this%Fch, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj)

                   else if (ijpot == O_O) then

                      call eval(this%Foo, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj)
                      
                   else if (ijpot == O_C) then
                         
                      call eval(this%Foc, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj)
                      
                   else if (ijpot == O_H) then
                      
                      call eval(this%Foh, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj)
                         
                   else if (ijpot == C_O) then
                         
                      call eval(this%Foc, nti, ntj, nconji, nconjj, &
                           fij, dfdni, dfdnj, dfdncni, dfdncnj) 
                         
                   endif

#else

                   dfdncn = 0.0_DP

                   if (ijpot == C_C) then

                      call eval(this%Fcc, nti, ntj, nconj, &
                           fij, dfdni, dfdnj, dfdncn)

                   else if (ijpot == H_H) then

                      call eval(this%Fhh, nti, ntj, nconj, &
                           fij, dfdni, dfdnj, dfdncn)

                   else if (ijpot == C_H) then

                      call eval(this%Fch, nti, ntj, nconj, &
                           fij, dfdni, dfdnj, dfdncn)

                   else if (ijpot == O_O) then

                      call eval(this%Foo, nti, ntj, nconj, &
                           fij, dfdni, dfdnj, dfdncn)
                      
                   else if (ijpot == O_C) then
                         
                      call eval(this%Foc, nti, ntj, nconj, fij, &
                           dfdni, dfdnj, dfdncn)
                      
                   else if (ijpot == O_H) then
                      
                      call eval(this%Foh, nti, ntj, nconj, fij, &
                           dfdni, dfdnj, dfdncn)
                         
                   else if (ijpot == C_O) then
                         
                      call eval(this%Foc, nti, ntj, nconj, fij, &
                           dfdni, dfdnj, dfdncn) 
                         
                   endif

#endif

#ifdef DEBUG_PRINT
!                   write (*, '(A,2I3,4F15.7)')  "     F "//rebo2_el_strs(ktypi)//" "//rebo2_el_strs(ktypj)//":", i, j, nti, ntj, nconj, fij
                   write (*, '(A,2I3,2X,4I3,F15.7)')  "     F "//rebo2_el_strs(ktypi)//" "//rebo2_el_strs(ktypj)//":", i, j, nint(nti), nint(ntj), nint(nconji)+1, nint(nconjj)+1, fij
#endif

                   !
                   ! this still needs to be multiplied by fcij
                   !

#if defined(DIHEDRAL) || defined(ALT_DIHEDRAL)

                   dfdni   = dfdni + dtdni * bdh
                   dfdnj   = dfdnj + dtdnj * bdh
                   dfdncn  = dfdncn + dtdncn * bdh

#endif

                   ! 
                   ! add forces due to fcc.
                   ! - ( 0.5 * fcij * faij * dfcc/drwi ).
                   !

                   dfdni   = 0.5_DP * fcij * faij * dfdni
                   dfdnj   = 0.5_DP * fcij * faij * dfdnj
#ifdef SEP_NCONJ
                   dfdncni = 0.5_DP * fcij * faij * dfdncni
                   dfdncnj = 0.5_DP * fcij * faij * dfdncnj
#else
                   dfdncn  = 0.5_DP * fcij * faij * dfdncn

                   !
                   !          f = nconji**2 + nconjj**2
                   !    =>   df = 2*nconji*dncndi
                   ! 

                   dfdncni = 2*dfdncn*nconji
                   dfdncnj = 2*dfdncn*nconjj
#endif

                   !
                   ! Forces on bond ij due to coordination numbers
                   !

                   df = &
                        - &
                        dfdni * &
                        ( &
                        dnidij(1:3, rebo2_C_) + &
                        dnidij(1:3, rebo2_O_) + &
                        dnidij(1:3, rebo2_H_) &
                        ) &
                        - &
                        dfbij * &
                        ( &
                        dpdnci * dnidij(1:3, rebo2_C_) + &
                        dpdnoi * dnidij(1:3, rebo2_O_) + &
                        dpdnhi * dnidij(1:3, rebo2_H_) &
                        )
                   fi = fi + df
                   fj = fj - df

                   df = &
                        - &
                        dfdnj * &
                        ( &
                        dnjdji(1:3, rebo2_C_) + &
                        dnjdji(1:3, rebo2_O_) + &
                        dnjdji(1:3, rebo2_H_) &
                        ) &
                        - &
                        dfbji * &
                        ( &
                        dpdnci * dnjdji(1:3, rebo2_C_) + &
                        dpdnoi * dnjdji(1:3, rebo2_O_) + &
                        dpdnhi * dnjdji(1:3, rebo2_H_) &
                        )
                   fi = fi - df
                   fj = fj + df
                
                   ! 
                   ! calculate forces on neighbours of i.
                   !

                   do ikc = 1, numnbi
                      k    = nebofi(ikc)
#ifdef LAMMPS
!                      if (k /= j) then
#else
!                      kdc  = dcofi(ikc)
!                      if (k /= j .or. kdc /= jdc) then
#endif

                         !
                         ! - ( 0.5 * fcij * faij * dfcc/drwk ).
                         !

                         df         = &
                              -( dfdni * &
                              ( &
                              dnidik(1:3, ikc, rebo2_C_) + &
                              dnidik(1:3, ikc, rebo2_O_) + &
                              dnidik(1:3, ikc, rebo2_H_) &
                              ) + &
                              dfdncni*dncnidk(1:3, ikc) &
                              ) &
                              - &
                              dfbij * &
                              ( &
                              dpdnci * dnidik(1:3, ikc, rebo2_C_) + &
                              dpdnoi * dnidik(1:3, ikc, rebo2_O_) + &
                              dpdnhi * dnidik(1:3, ikc, rebo2_H_) &
                              )
                         VEC3(f, k) = VEC3(f, k) + df
                         fi         = fi     - df

                         wij        = wij - outer_product(dri(1:3, ikc), df)

                         ! 
                         ! forces on second neighbours due to conjugation.
                         ! 

                         do kmc = numnbk(ikc), numnbk(ikc+1)-1
                            m    = nebofk(kmc)
#ifdef LAMMPS
                            if (m /= i) then
#else
                            mdc  = dcofk(kmc)
                            if (m /= i .or. mdc /= 0) then
#endif
                               df         = -dfdncni*dncnidm(1:3, kmc)
                               VEC3(f, m) = VEC3(f, m) + df
                               VEC3(f, k) = VEC3(f, k) + (- df)

                               wij        = wij - outer_product(drk(1:3, kmc), df)
                            endif
                         enddo

!                      endif
                   enddo

                   ! 
                   ! calculate forces on neighbours of j.
                   ! 

                   do jlc = 1, numnbj
                      l    = nebofj(jlc)
#ifndef LAMMPS
                      ldc  = dcofj(jlc)
#endif

                      ! 
                      ! - ( 0.5 * fcij * faij * dfcc/drwl ).
                      ! 

                      df         = &
                           -( &
                           dfdnj * &
                           ( &
                           dnjdjl(1:3, jlc, rebo2_H_) + &
                           dnjdjl(1:3, jlc, rebo2_C_) + &
                           dnjdjl(1:3, jlc, rebo2_O_) &
                           ) &
                           + &
                           dfdncnj*dncnjdl(1:3, jlc) &
                           ) &
                           - &
                           dfbji * &
                           ( &
                           dpdnhj * dnjdjl(1:3, jlc, rebo2_H_) + &
                           dpdncj * dnjdjl(1:3, jlc, rebo2_C_) + &
                           dpdnoj * dnjdjl(1:3, jlc, rebo2_O_) &
                           )
                      VEC3(f, l) = VEC3(f, l) + df
                      fj         = fj         - df

                      wij        = wij - outer_product(drj(1:3, jlc), df)

                      ! 
                      ! forces on second neighbours due to conjugation.
                      !

                      do lnc = numnbl(jlc), numnbl(jlc+1)-1
                         n    = nebofl(lnc)
#ifdef LAMMPS
                         if (n /= j) then
#else
                         ndc  = dcofl(lnc)
                         if (n /= j .or. ndc /= jdc) then
#endif
                            df         = -dfdncnj*dncnjdn(1:3, lnc)
                            VEC3(f, n) = VEC3(f, n) + df
                            VEC3(f, l) = VEC3(f, l) + (- df)

                            wij        = wij - outer_product(drl(1:3, lnc), df)
                         endif
                      enddo

                   enddo
#endif

                   ! 
                   ! average the bond order terms for atoms i and j.
                   !

#if defined(DIHEDRAL) || defined(ALT_DIHEDRAL)
                   baveij  = 0.5_DP * ( bij + bji + fij + tij*bdh )
#else
#ifdef NUM_NEIGHBORS
                   baveij  = 0.5_DP * ( bij + bji + fij )
#else
                   baveij  = 0.5_DP * ( bij + bji )
#endif
#endif

                   ! 
                   ! now calculate the potential energies and forces for i and j.
                   ! vfac   = frij + baveij * faij
                   ! hlfvij = fcij * vfac / 2.0
                   ! 

                   hlfvij  = 0.5_DP * fcij * ( frij + baveij * faij )
                   pe(i)   = pe(i) + hlfvij
                   pe(j)   = pe(j) + hlfvij

                   if (present(epot_per_bond)) then
                      epot_per_bond(this%nbb(ij))  = epot_per_bond(this%nbb(ij)) + 2*hlfvij
                   endif

!                   epot    = epot + 2*hlfvij

                   !
                   ! dvij / drij
                   ! dffac = ( dfrijr + baveij * dfaijr ) * fcij + dfcijr * vfac
                   !

                   dffac = &
                        dfrijr * fcij + &
                        baveij * dfaijr * fcij + &
                        frij * dfcijr + &
                        baveij * faij * dfcijr

                   !
                   ! compute force without bond order term
                   !

                   df = dffac * rnij
                   fi = fi + df
                   fj = fj - df

                   wij = wij + outer_product(rij, df) - &
                        dfbij*wijb - dfbji*wjib

                   if (present(f_per_bond)) then
                      f_per_bond(1:3, this%nbb(ij))  = &
                           f_per_bond(1:3, this%nbb(ij)) + df
                   endif

                   !
                   !compute force due to bond order term
                   ! - ( dvij / drwi + 0.5 * fcij * faij * 
                   !   ( dbij / drwi + dbji / drwi )
                   !

                   df = - ( dfbij*dbidi + dfbji*dbjdi )
                   fi = fi + df

                   !
                   ! - ( dvij / drwj + 0.5 * fcij * faij * 
                   !   ( dbij / drwj + dbji / drwj )
                   !

                   df = - ( dfbij*dbidj + dfbji*dbjdj )
                   fj = fj + df

                   !
                   ! calculate forces on neighbours of i.
                   !

                   do ikc = 1, numnbi
                      k = nebofi(ikc)

                      !
                      ! - ( 0.5 * fcij * faij * dbij / drwk ).
                      !

                      df         = - dfbij * dbidk(1:3, ikc)
                      VEC3(f, k) = VEC3(f, k) + df

#ifdef SCREENING

                      i1 = seedi(ikc)
                      i2 = lasti(ikc)
                      if (i1 <= i2) then

                         !
                         ! forces due to screening
                         !

                         this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + &
                              zfaci(ikc) * dfbij

#ifdef NUM_NEIGHBORS
                         if (ktyp(k) == rebo2_C_) then
                            dffac = dpdnci * dfbij + dfdni + &
                                 dfdncni*fxik(ikc)
                         else if (ktyp(k) == rebo2_O_) then
                            dffac = dpdnoi * dfbij + dfdni + &
                                 dfdncni*fxik(ikc)
                         else
                            dffac = dpdnhi * dfbij + dfdni + &
                                 dfdncni*fxik(ikc)
                         endif

                         this%sfacnc(i1:i2) = this%sfacnc(i1:i2) + dffac
#endif
                      endif

#ifdef NUM_NEIGHBORS
                      dffac = dfdncni*dnconjidxi(ikc)

#ifdef LAMMPS
                      forall (kmc = numnbk(ikc):numnbk(ikc+1)-1, nebofk(kmc) /= i)
#else
                      forall (kmc = numnbk(ikc):numnbk(ikc+1)-1, nebofk(kmc) /= i .or. dcofk(kmc) /= 0)
#endif
                         this%sfacnc(seedk(kmc):lastk(kmc))  = &
                              this%sfacnc(seedk(kmc):lastk(kmc)) + dffac
                      endforall
#endif

#endif

                   enddo ! ikc

                   !
                   ! calculate forces on neighbours of j.
                   !

                   do jlc = 1, numnbj
                      l = nebofj(jlc)

                      !
                      ! - ( 0.5 * fcij * faij * dbji / drwl ).
                      !

                      df         = - dfbji * dbjdl(1:3, jlc)
                      VEC3(f, l) = VEC3(f, l) + df

#ifdef SCREENING
                         
                      i1 = seedj(jlc)
                      i2 = lastj(jlc)
                      if (i1 <= i2) then

                         !
                         ! forces due to screening
                         !

                         this%sfacbo(i1:i2) = this%sfacbo(i1:i2) + &
                              zfacj(jlc) * dfbji

#ifdef NUM_NEIGHBORS
                         if (ktyp(l) == rebo2_C_) then
                            dffac = dpdncj * dfbji + dfdnj + &
                                 dfdncnj*fxjl(jlc)
                         else if (ktyp(l) == rebo2_O_) then
                            dffac = dpdnoj * dfbji + dfdnj + &
                                 dfdncnj*fxjl(jlc)
                         else
                            dffac = dpdnhj * dfbji + dfdnj + &
                                 dfdncnj*fxjl(jlc)
                         endif

                         this%sfacnc(i1:i2) = this%sfacnc(i1:i2) + dffac
#endif
                      endif

#ifdef NUM_NEIGHBORS
                      dffac = dfdncnj*dnconjjdxj(jlc)

#ifdef LAMMPS
                      forall (lnc = numnbl(jlc):numnbl(jlc+1)-1, nebofl(lnc) /= j)
#else
                      forall (lnc = numnbl(jlc):numnbl(jlc+1)-1, nebofl(lnc) /= j .or. dcofl(lnc) /= jdc)
#endif
                         this%sfacnc(seedl(lnc):lastl(lnc))  = &
                              this%sfacnc(seedl(lnc):lastl(lnc)) + dffac
                      endforall
#endif

#endif

                   enddo ! jlc

#ifdef SCREENING

                   !
                   ! calculate forces on neighbors of i and j due to screening.
                   !

                   dffac = frij + baveij * faij

                   do nijc = this%sneb_seed(ij), this%sneb_last(ij)

                      k = this%sneb(nijc)

#ifdef LAMMPS
                      rik = VEC3(r, k) - VEC3(r, i)
#else
                      rik = VEC3(r, k) - VEC3(r, i) - &
                           matmul(cell, VEC3(dc, this%sbnd(nijc)))
#ifndef PYTHON
                      rik = rik - shear_dx*VEC(dc, this%sbnd(nijc), 3)
#endif
#endif
                      rjk  = -rij + rik

                      df   = dffac * this%cutdrik(nijc) * rik

                      fi          = fi         + df
                      VEC3(f, k)  = VEC3(f, k) + (- df)

                      wij         = wij + outer_product(rik, df)

                      df  = dffac * this%cutdrjk(nijc) * rjk

                      fj          = fj         + df
                      VEC3(f, k)  = VEC3(f, k) + (- df)

                      wij         = wij + outer_product(rjk, df)

                   enddo ! nijc

#endif

                   wpot  = wpot + wij
                   if (present(wpot_per_bond)) then
                      SUM_VIRIAL(wpot_per_bond, this%nbb(ij), wij)
                   endif
                   if (present(wpot_per_at)) then
                      wij  = wij/2
                      SUM_VIRIAL(wpot_per_at, i, wij)
                      SUM_VIRIAL(wpot_per_at, j, wij)
                   endif

                   VEC3(f, j)  = VEC3(f, j) + fj

                endif ar_within_cutoff
             endif  j_gt_i
          enddo ij_loop

          VEC3(f, i)  = VEC3(f, i) + fi

       endif  i_known_el2

    enddo i_loop2

#ifdef SCREENING

    !
    ! Restart loop, now compute forces due to screening
    !

    !$omp do
    i_loop_scr: do i = 1, nat
       i_known_el_scr: if (ktyp(i) > 0) then

          fi = 0.0_DP

          ij_loop_scr: do ij = this%neb_seed(i), this%neb_last(i)
             j    = this%neb(ij)

             fj   = 0.0_DP

             wij  = 0.0_DP

             rij  = this%bndlen(ij) * this%bndnm(1:3, ij)

             istart  = this%sneb_seed(ij)
             ifinsh  = this%sneb_last(ij)

#ifdef NUM_NEIGHBORS
             this%cutdrboik(istart:ifinsh)  = &
                  this%sfacbo(istart:ifinsh) * this%cutdrboik(istart:ifinsh) &
                  + this%sfacnc(istart:ifinsh) * this%cutdrncik(istart:ifinsh)

             this%cutdrbojk(istart:ifinsh)  = &
                  this%sfacbo(istart:ifinsh) * this%cutdrbojk(istart:ifinsh) &
                  + this%sfacnc(istart:ifinsh) * this%cutdrncjk(istart:ifinsh)
#else
             this%cutdrboik(istart:ifinsh)  = &
                  this%sfacbo(istart:ifinsh) * this%cutdrboik(istart:ifinsh)

             this%cutdrbojk(istart:ifinsh)  = &
                  this%sfacbo(istart:ifinsh) * this%cutdrbojk(istart:ifinsh)
#endif

             nijc_loop_scr: do nijc = istart, ifinsh

                k = this%sneb(nijc)

#ifdef LAMMPS
                rik = VEC3(r, k) - VEC3(r, i)
#else
                rik = VEC3(r, k) - VEC3(r, i) - &
                     matmul(cell, VEC3(dc, this%sbnd(nijc)))
#ifndef PYTHON
                rik = rik - shear_dx*VEC(dc, this%sbnd(nijc), 3)
#endif
#endif
                rjk  = -rij + rik

                df          = this%cutdrboik(nijc) * rik

                fi          = fi         + df
                VEC3(f, k)  = VEC3(f, k) + (- df)

                wij         = wij + outer_product(rik, df)

                df          = this%cutdrbojk(nijc) * rjk

                fj          = fj         + df
                VEC3(f, k)  = VEC3(f, k) + (- df)

                wij         = wij + outer_product(rjk, df)

             enddo nijc_loop_scr

             wpot  = wpot + wij
             if (present(wpot_per_bond)) then
                SUM_VIRIAL(wpot_per_bond, this%nbb(ij), wij)
             endif
             if (present(wpot_per_at)) then
                wij  = wij/2
                SUM_VIRIAL(wpot_per_at, i, wij)
                SUM_VIRIAL(wpot_per_at, j, wij)
             endif

             VEC3(f, j)  = VEC3(f, j) + fj

          enddo ij_loop_scr

          VEC3(f, i)  = VEC3(f, i) + fi

       endif i_known_el_scr
    enddo i_loop_scr

#endif

    epot  = epot + sum(pe(1:nat))


    if (present(epot_per_at)) then
       call tls_reduce(nat, sca1=epot_per_at, vec1=f_inout)
    else
       call tls_reduce(nat, vec1=f_inout)
    endif

    !$omp end parallel

    INVOKE_DELAYED_ERROR(ierror_loc, ierror)

    wpot_inout  = wpot_inout + wpot

#ifdef DEBUG_PRINT
    write (*, *)  "-----"
#endif

  endsubroutine BOP_KERNEL

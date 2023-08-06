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

#ifdef SEP_NCONJ

  !>
  !! Initialize F table. Unwrap from single conjugation parameter to
  !! two conjugation parameters if necessary.
  !< 
  subroutine init_f(t, nx, ny, nz, values, dvdx, dvdy, dvdz, error)
    type(table4d_t),    intent(inout) :: t
    integer,            intent(in)    :: nx
    integer,            intent(in)    :: ny
    integer,            intent(in)    :: nz
    real(DP),           intent(in)    :: values(0:nx, 0:ny, 0:nz)
    real(DP), optional, intent(in)    :: dvdx(0:nx, 0:ny, 0:nz)
    real(DP), optional, intent(in)    :: dvdy(0:nx, 0:ny, 0:nz)
    real(DP), optional, intent(in)    :: dvdz(0:nx, 0:ny, 0:nz)
    integer,  optional, intent(inout) :: error

    ! ---

    real(DP) :: nvalues(0:nx, 0:ny, 0:3, 0:3)
    integer  :: i, j, k, l

    ! ---

    nvalues = 0.0_DP
    do i = 0, nx
       do j = 0, ny
          do k = 0, 2
             do l = 0, 2
                nvalues(i,j,k,l) = values(i,j,k*k+l*l)
             enddo
          enddo
       enddo
    enddo

    call init(t, nx, ny, 3, 3, nvalues, error=error)
    PASS_ERROR(error)

  endsubroutine init_f

#else

#define init_f init
#define table4d_prlog table3d_prlog

#endif


  !>
  !! Initialize the REBO with a set of chosen parameters.
  !! Note: General parameters are taken from this and need to be set
  !! before call to this init routine.
  !<
  subroutine rebo2x_db_init_with_parameters( &
       this, &
       in_Fcc, in_dFccdi, in_dFccdj, in_dFccdk, &
       in_Fch, in_dFchdi, in_dFchdj, in_dFchdk, &
       in_Fhh, in_dFhhdi, in_dFhhdj, in_dFhhdk, &
       in_Fsic, in_dFsicdi, in_dFsicdj, in_dFsicdk, &
       in_Fsih, in_dFsihdi, in_dFsihdj, in_dFsihdk, &
       in_Fsisi, in_dFsisidi, in_dFsisidj, in_dFsisidk, & 
       in_Pcc, in_dPccdi, in_dPccdj, in_dPccdk, &
       in_Pch, in_dPchdi, in_dPchdj, in_dPchdk, &
       in_Psic, in_dPsicdi, in_dPsicdj, in_dPsicdk, &
       in_Pcsi, in_dPcsidi, in_dPcsidj, in_dPcsidk, &
       in_Psih, in_dPsihdi, in_dPsihdj, in_dPsihdk, &
       in_Psisi, in_dPsisidi, in_dPsisidj, in_dPsisidk, &
       in_Tcc, error)
    implicit none

    type(BOP_TYPE), intent(inout)  :: this

    real(DP), intent(in)          :: in_Fcc(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFccdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFccdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFccdk(0:, 0:, 0:)

    real(DP), intent(in)          :: in_Fch(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFchdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFchdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFchdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Fhh(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFhhdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFhhdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFhhdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Fsic(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsicdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsicdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsicdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Fsih(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsihdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsihdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsihdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Fsisi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsisidi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsisidj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFsisidk(0:, 0:, 0:)

    real(DP), intent(in)          :: in_Pcc(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPccdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPccdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPccdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Pch(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPchdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPchdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPchdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Psic(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsicdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsicdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsicdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Pcsi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPcsidi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPcsidj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPcsidk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Psih(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsihdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsihdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsihdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Psisi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsisidi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsisidj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPsisidk(0:, 0:, 0:)

    real(DP), intent(in)          :: in_Tcc(0:, 0:, 0:)

    integer, optional, intent(out) :: error

    ! ---

    integer  :: i, j, k

    ! ---

    INIT_ERROR(error)

    if (ilog /= -1) then
       write (ilog, '(A)')   "- "//BOP_NAME_STR//"_db_init -"

       call prlog("     Pair parameters:")
       write (ilog, '(5X,A,F20.10)')  "hh_A        = ", this%hh_A
       write (ilog, '(5X,A,F20.10)')  "hh_Q        = ", this%hh_Q
       write (ilog, '(5X,A,F20.10)')  "hh_alpha    = ", this%hh_alpha
       write (ilog, '(5X,A,F20.10)')  "hh_B1       = ", this%hh_B1
       write (ilog, '(5X,A,F20.10)')  "hh_beta1    = ", this%hh_beta1
       write (ilog, '(5X,A,F20.10)')  "ch_A        = ", this%ch_A
       write (ilog, '(5X,A,F20.10)')  "ch_Q        = ", this%ch_Q
       write (ilog, '(5X,A,F20.10)')  "ch_alpha    = ", this%ch_alpha
       write (ilog, '(5X,A,F20.10)')  "ch_B1       = ", this%ch_B1
       write (ilog, '(5X,A,F20.10)')  "ch_beta1    = ", this%ch_beta1
       write (ilog, '(5X,A,F20.10)')  "cc_A        = ", this%cc_A
       write (ilog, '(5X,A,F20.10)')  "cc_Q        = ", this%cc_Q
       write (ilog, '(5X,A,F20.10)')  "cc_alpha    = ", this%cc_alpha
       write (ilog, '(5X,A,F20.10)')  "cc_B1       = ", this%cc_B1
       write (ilog, '(5X,A,F20.10)')  "cc_B2       = ", this%cc_B2
       write (ilog, '(5X,A,F20.10)')  "cc_B3       = ", this%cc_B3
       write (ilog, '(5X,A,F20.10)')  "cc_beta1    = ", this%cc_beta1
       write (ilog, '(5X,A,F20.10)')  "cc_beta2    = ", this%cc_beta2
       write (ilog, '(5X,A,F20.10)')  "cc_beta3    = ", this%cc_beta3

       call prlog("     Cutoff parameters:")
       write (ilog, '(5X,A,F20.10)')  "cc_in_r1    = ", this%cc_in_r1
       write (ilog, '(5X,A,F20.10)')  "cc_in_r2    = ", this%cc_in_r2
       write (ilog, '(5X,A,F20.10)')  "ch_in_r1    = ", this%ch_in_r1
       write (ilog, '(5X,A,F20.10)')  "ch_in_r2    = ", this%ch_in_r2
       write (ilog, '(5X,A,F20.10)')  "hh_in_r1    = ", this%hh_in_r1
       write (ilog, '(5X,A,F20.10)')  "hh_in_r2    = ", this%hh_in_r2
       write (ilog, '(5X,A,F20.10)')  "sisi_in_r1  = ", this%sisi_in_r1
       write (ilog, '(5X,A,F20.10)')  "sisi_in_r2  = ", this%sisi_in_r2
       write (ilog, '(5X,A,F20.10)')  "sih_in_r1   = ", this%sih_in_r1
       write (ilog, '(5X,A,F20.10)')  "sih_in_r2   = ", this%sih_in_r2
       write (ilog, '(5X,A,F20.10)')  "sic_in_r1   = ", this%sic_in_r1
       write (ilog, '(5X,A,F20.10)')  "sic_in_r2   = ", this%sic_in_r2

#ifdef SCREENING
       call prlog("     Outer cutoff parameters:")
       write (ilog, '(5X,A,F20.10)')  "cc_out_r1   = ", this%cc_out_r1
       write (ilog, '(5X,A,F20.10)')  "cc_out_r2   = ", this%cc_out_r2
       write (ilog, '(5X,A,F20.10)')  "ch_out_r1   = ", this%ch_out_r1
       write (ilog, '(5X,A,F20.10)')  "ch_out_r2   = ", this%ch_out_r2
       write (ilog, '(5X,A,F20.10)')  "hh_out_r1   = ", this%hh_out_r1
       write (ilog, '(5X,A,F20.10)')  "hh_out_r2   = ", this%hh_out_r2
       write (ilog, '(5X,A,F20.10)')  "sisi_out_r1 = ", this%sisi_out_r1
       write (ilog, '(5X,A,F20.10)')  "sisi_out_r2 = ", this%sisi_out_r2
       write (ilog, '(5X,A,F20.10)')  "sih_out_r1  = ", this%sih_out_r1
       write (ilog, '(5X,A,F20.10)')  "sih_out_r2  = ", this%sih_out_r2
       write (ilog, '(5X,A,F20.10)')  "sic_out_r1  = ", this%sic_out_r1
       write (ilog, '(5X,A,F20.10)')  "sic_out_r2  = ", this%sic_out_r2

       call prlog("     Neighbor/conjugation parameters:")
       write (ilog, '(5X,A,F20.10)')  "cc_nc_r1    = ", this%cc_nc_r1
       write (ilog, '(5X,A,F20.10)')  "cc_nc_r2    = ", this%cc_nc_r2
       write (ilog, '(5X,A,F20.10)')  "ch_nc_r1    = ", this%ch_nc_r1
       write (ilog, '(5X,A,F20.10)')  "ch_nc_r2    = ", this%ch_nc_r2
       write (ilog, '(5X,A,F20.10)')  "hh_nc_r1    = ", this%hh_nc_r1
       write (ilog, '(5X,A,F20.10)')  "hh_nc_r2    = ", this%hh_nc_r2
       write (ilog, '(5X,A,F20.10)')  "sisi_nc_r1  = ", this%sisi_nc_r1
       write (ilog, '(5X,A,F20.10)')  "sisi_nc_r2  = ", this%sisi_nc_r2
       write (ilog, '(5X,A,F20.10)')  "sih_nc_r1   = ", this%sih_nc_r1
       write (ilog, '(5X,A,F20.10)')  "sih_nc_r2   = ", this%sih_nc_r2
       write (ilog, '(5X,A,F20.10)')  "sic_nc_r1   = ", this%sic_nc_r1
       write (ilog, '(5X,A,F20.10)')  "sic_nc_r2   = ", this%sic_nc_r2

       call prlog("     Additional screening parameters:")
       write (ilog, '(5X,A,F20.10)')  "hh_C_min     = ", this%hh_Cmin
       write (ilog, '(5X,A,F20.10)')  "hh_C_max     = ", this%hh_Cmax
       write (ilog, '(5X,A,F20.10)')  "ch_C_min     = ", this%ch_Cmin
       write (ilog, '(5X,A,F20.10)')  "ch_C_max     = ", this%ch_Cmax
       write (ilog, '(5X,A,F20.10)')  "sih_C_min    = ", this%sih_Cmin
       write (ilog, '(5X,A,F20.10)')  "sih_C_max    = ", this%sih_Cmax

       call prlog("     Bond-order cutoff:")
       write (ilog, '(5X,A,F20.10)')  "z1          = ", this%z1
       write (ilog, '(5X,A,F20.10)')  "z2          = ", this%z2
#endif
       
       if (this%with_dihedral) then
          call prlog("     Computing dihedral terms.")
       endif
       if (this%const_bo) then
          call prlog("     Fixing bond-order to unity.")
       endif
       if (this%const_nconj) then
          call prlog("     Fixing conjugation variable(s) to zero.")
       endif
       if (this%no_outer_cutoff) then
          call prlog("     Outer cutoff function is disabled.")
       endif

#ifdef EXP_CUT
       call prlog("     Using exponential cut-off functions.")
#else
       call prlog("     Using trigonometric cut-off funtions.")
#endif

       write (ilog, *)
    endif

#ifdef SCREENING
    this%Cmin(H_H)  = this%hh_Cmin
    this%Cmax(H_H)  = this%hh_Cmax
    this%Cmin(C_H)  = this%ch_Cmin
    this%Cmax(C_H)  = this%ch_Cmax
    this%Cmin(Si_H) = this%sih_Cmin
    this%Cmax(Si_H) = this%sih_Cmax

    this%dC = 0.0_DP
    this%C_dr_cut = 0.0_DP
    do i = 1, rebo2_MAX_PAIRS
      if (this%Cmax(i) > this%Cmin(i)) then
        this%dC(i)       = this%Cmax(i)-this%Cmin(i)
        this%C_dr_cut(i) = this%Cmax(i)**2/(4*(this%Cmax(i)-1))
      endif
    enddo
#endif

    !
    ! bond order constants.
    !

    this%conpe(rebo2_C_)  = - 0.5_DP
    this%conpe(rebo2_H_)  = - 0.5_DP
    this%conpe(rebo2_Si_) = - 0.5_DP
    this%conan(rebo2_C_)  = 0.5_DP * this%conpe(rebo2_C_)
    this%conan(rebo2_H_)  = 0.5_DP * this%conpe(rebo2_H_)
    this%conan(rebo2_Si_) = 0.5_DP * this%conpe(rebo2_Si_)
    this%conpf(rebo2_C_)  = this%conpe(rebo2_C_) - 1.0_DP
    this%conpf(rebo2_H_)  = this%conpe(rebo2_H_) - 1.0_DP
    this%conpf(rebo2_Si_) = this%conpe(rebo2_Si_) - 1.0_DP

    !
    ! bond order penalty function constants
    !

#define H_ rebo2_H_
#define C_ rebo2_C_
#define Si_ rebo2_Si_

    this%re        = 1.0_DP
    this%re(H_H)   = this%HH_re
    this%re(C_H)   = this%CH_re
    this%re(Si_H)  = this%SiH_re
    this%re(C_C)   = this%CC_re
    this%re(Si_Si) = this%SiSi_re
    this%re(Si_C)  = this%SiC_re
    this%re(C_Si)  = this%SiC_re

    do j = 1, 5, 2
       do k = 1, 5, 2
          call prlog("     re(" // rebo2_el_strs(j) // ", " // &
               rebo2_el_strs(k) // ") = " // this%re(Z2pair(this, j, k)))
       enddo
    enddo

#undef H_
#undef C_
#undef Si_

    this%bo_override = -1.0_DP
    this%bo_override(H_H) = this%HH_bo
    this%bo_override(C_C) = this%CC_bo
    this%bo_override(C_H) = this%CH_bo

!   
!   Need to add in the Silicon penalty functions - MTK

    !
    ! cutoff constants.
    !

    this%cut_in_l(:)       = 0.0_DP
    this%cut_in_l(C_C)     = this%cc_in_r1
    this%cut_in_l(C_H)     = this%ch_in_r1
    this%cut_in_l(H_H)     = this%hh_in_r1
    this%cut_in_l(Si_Si)   = this%sisi_in_r1
    this%cut_in_l(Si_H)    = this%sih_in_r1
    this%cut_in_l(C_Si)    = this%sic_in_r1
    this%cut_in_l(Si_C)    = this%sic_in_r1

    this%cut_in_h(:)       = 0.0_DP
    this%cut_in_h(C_C)     = this%cc_in_r2
    this%cut_in_h(C_H)     = this%ch_in_r2
    this%cut_in_h(H_H)     = this%hh_in_r2
    this%cut_in_h(Si_Si)   = this%sisi_in_r2
    this%cut_in_h(Si_H)    = this%sih_in_r2
    this%cut_in_h(C_Si)    = this%sic_in_r2
    this%cut_in_h(Si_C)    = this%sic_in_r2

    this%cut_in_h2(:)      = 0.0_DP
    this%cut_in_h2(C_C)    = this%cc_in_r2 ** 2
    this%cut_in_h2(C_H)    = this%ch_in_r2 ** 2
    this%cut_in_h2(H_H)    = this%hh_in_r2 ** 2
    this%cut_in_h2(Si_Si)  = this%sisi_in_r2 ** 2
    this%cut_in_h2(Si_H)   = this%sih_in_r2 **  2
    this%cut_in_h2(C_Si)   = this%sic_in_r2 ** 2
    this%cut_in_h2(Si_C)   = this%sic_in_r2 ** 2

    this%cut_in_m(:)       = 0.0_DP
    this%cut_in_m(C_C)     = (this%cc_in_r1+this%cc_in_r2)/2
    this%cut_in_m(C_H)     = (this%ch_in_r1+this%ch_in_r2)/2
    this%cut_in_m(H_H)     = (this%hh_in_r1+this%hh_in_r2)/2
    this%cut_in_m(Si_Si)   = (this%sisi_in_r1 + this%sisi_in_r2)/2
    this%cut_in_m(Si_H)    = (this%sih_in_r1 + this%sih_in_r2) / 2
    this%cut_in_m(C_Si)    = (this%sic_in_r1 + this%sic_in_r2) / 2
    this%cut_in_m(Si_C)    = (this%sic_in_r1 + this%sic_in_r2) / 2

#ifdef SCREENING
    this%cut_out_l(:)      = 0.0_DP
    this%cut_out_l(C_C)    = this%cc_out_r1
    this%cut_out_l(C_H)    = this%ch_out_r1
    this%cut_out_l(H_H)    = this%hh_out_r1
    this%cut_out_l(Si_Si)  = this%sisi_out_r1
    this%cut_out_l(Si_H)   = this%sih_out_r1
    this%cut_out_l(C_Si)   = this%sic_out_r1
    this%cut_out_l(Si_C)   = this%sic_out_r1

    this%cut_out_h(:)      = 0.0_DP
    this%cut_out_h(C_C)    = this%cc_out_r2
    this%cut_out_h(C_H)    = this%ch_out_r2
    this%cut_out_h(H_H)    = this%hh_out_r2
    this%cut_out_h(Si_Si)  = this%sisi_out_r2
    this%cut_out_h(Si_H)   = this%sih_out_r2
    this%cut_out_h(C_Si)   = this%sic_out_r2
    this%cut_out_h(Si_C)   = this%sic_out_r2

    this%cut_out_h2(:)     = 0.0_DP
    this%cut_out_h2(C_C)   = this%cc_out_r2 ** 2
    this%cut_out_h2(C_H)   = this%ch_out_r2 ** 2
    this%cut_out_h2(H_H)   = this%hh_out_r2 ** 2
    this%cut_out_h2(Si_Si) = this%sisi_out_r2 ** 2
    this%cut_out_h2(Si_H)  = this%sih_out_r2 ** 2
    this%cut_out_h2(C_Si)  = this%sic_out_r2 ** 2
    this%cut_out_h2(Si_C)  = this%sic_out_r2 ** 2

    this%cut_out_m(:)      = 0.0_DP
    this%cut_out_m(C_C)    = (this%cc_out_r1+this%cc_out_r2)/2
    this%cut_out_m(C_H)    = (this%ch_out_r1+this%ch_out_r2)/2
    this%cut_out_m(H_H)    = (this%hh_out_r1+this%hh_out_r2)/2
    this%cut_out_m(Si_Si)  = (this%sisi_out_r1+this%sisi_out_r2)/2
    this%cut_out_m(Si_H)   = (this%sih_out_r1+this%sih_out_r2)/2
    this%cut_out_m(C_Si)   = (this%sic_out_r1+this%sic_out_r2)/2
    this%cut_out_m(Si_C)   = (this%sic_out_r1+this%sic_out_r2)/2

#ifdef NUM_NEIGHBORS
    this%cut_nc_l(:)      = 0.0_DP
    this%cut_nc_l(C_C)    = this%cc_nc_r1
    this%cut_nc_l(C_H)    = this%ch_nc_r1
    this%cut_nc_l(H_H)    = this%hh_nc_r1
    this%cut_nc_l(Si_Si)  = this%sisi_nc_r1
    this%cut_nc_l(Si_H)   = this%sih_nc_r1
    this%cut_nc_l(C_Si)   = this%sic_nc_r1
    this%cut_nc_l(Si_C)   = this%sic_nc_r1

    this%cut_nc_h(:)      = 0.0_DP
    this%cut_nc_h(C_C)    = this%cc_nc_r2
    this%cut_nc_h(C_H)    = this%ch_nc_r2
    this%cut_nc_h(H_H)    = this%hh_nc_r2
    this%cut_nc_h(Si_Si)  = this%sisi_nc_r2
    this%cut_nc_h(Si_H)   = this%sih_nc_r2
    this%cut_nc_h(C_Si)   = this%sic_nc_r2
    this%cut_nc_h(Si_C)   = this%sic_nc_r2

    this%cut_nc_h2(:)     = 0.0_DP
    this%cut_nc_h2(C_C)   = this%cc_nc_r2 ** 2
    this%cut_nc_h2(C_H)   = this%ch_nc_r2 ** 2
    this%cut_nc_h2(H_H)   = this%hh_nc_r2 ** 2
    this%cut_nc_h2(Si_Si) = this%sisi_nc_r2 ** 2
    this%cut_nc_h2(Si_H)  = this%sih_nc_r2 ** 2
    this%cut_nc_h2(C_Si)  = this%sic_nc_r2 ** 2
    this%cut_nc_h2(Si_C)  = this%sic_nc_r2 ** 2

    this%cut_nc_m(:)      = 0.0_DP
    this%cut_nc_m(C_C)    = (this%cc_nc_r1+this%cc_nc_r2)/2
    this%cut_nc_m(C_H)    = (this%ch_nc_r1+this%ch_nc_r2)/2
    this%cut_nc_m(H_H)    = (this%hh_nc_r1+this%hh_nc_r2)/2
    this%cut_nc_m(Si_Si)  = (this%sisi_nc_r1+this%sisi_nc_r2)/2
    this%cut_nc_m(Si_H)   = (this%sih_nc_r1+this%sih_nc_r2)/2
    this%cut_nc_m(C_Si)   = (this%sic_nc_r1+this%sic_nc_r2)/2
    this%cut_nc_m(Si_C)   = (this%sic_nc_r1+this%sic_nc_r2)/2

    do i = 1, 10
       this%max_cut_sq(i) = max(max(this%cut_in_h2(i), this%cut_out_h2(i)), &
            this%cut_nc_h2(i))
    enddo
#else
    do i = 1, 10
       this%max_cut_sq(i) = max(this%cut_in_h2(i), this%cut_out_h2(i))
    enddo
#endif
#else
    do i = 1, 10
       this%max_cut_sq(i) = this%cut_in_h2(i)
    enddo
#endif

    call prlog("     C-C cut-off = " // sqrt(this%max_cut_sq(C_C)))
    call prlog("     C-H cut-off = " // sqrt(this%max_cut_sq(C_H)))
    call prlog("     H-H cut-off = " // sqrt(this%max_cut_sq(H_H)))
    call prlog("     Si-Si cut-off = " // sqrt(this%max_cut_sq(Si_Si)))
    call prlog("     Si-H cut-off = " // sqrt(this%max_cut_sq(Si_H)))
    call prlog("     Si-C cut-off = " // sqrt(this%max_cut_sq(Si_C)))

    !
    ! Generate the coefficients for
    ! the bi- and tri- cubic interpolation functions.
    !

    call rebo2x_db_make_cc_g_spline(this)
    call rebo2x_db_make_sisi_g_spline(this)

    !
    ! Initialize look-up tables
    !
    
    call prlog
    call init_f(this%Fcc, N_NI_NJ_NCONJ, &
         in_Fcc, in_dFccdi, in_dFccdj, in_dFccdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Fcc:")
    call table4d_prlog(this%Fcc, indent=5)
    call init_f(this%Fch, N_NI_NJ_NCONJ, &
         in_Fch, in_dFchdi, in_dFchdj, in_dFchdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Fch:")
    call table4d_prlog(this%Fch, indent=5)
    call init_f(this%Fhh, N_NI_NJ_NCONJ, &
         in_Fhh, in_dFhhdi, in_dFhhdj, in_dFhhdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Fhh:")
    call table4d_prlog(this%Fhh, indent=5)
    call init_f(this%Fsic, N_NI_NJ_NCONJ, &
         in_Fsic, in_dFsicdi, in_dFsicdj, in_dFsicdk,&
         error=error)
    PASS_ERROR(error)
    call prlog("     Fsic:")
    call table4d_prlog(this%Fsic, indent=5)
    call init_f(this%Fsih, N_NI_NJ_NCONJ, &
         in_Fsih, in_dFsihdi, in_dFsihdj, in_dFsihdk,&
         error=error)
    PASS_ERROR(error)
    call prlog("     Fsih:")
    call table4d_prlog(this%Fsih, indent=5)
    call init_f(this%Fsisi, N_NI_NJ_NCONJ, &
         in_Fsisi, in_dFsisidi, in_dFsisidj, &
         in_dFsisidk, error=error)
    PASS_ERROR(error)
    call prlog("     Fsisi:")
    call table4d_prlog(this%Fsisi, indent=5)

    call init(this%Pcc, N_NH_NC_NSI, in_Pcc, in_dPccdi, in_dPccdj, in_dPccdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pcc:")
    call table3d_prlog(this%Pcc, indent=5)
    call init(this%Pch, N_NH_NC_NSI, in_Pch, in_dPchdi, in_dPchdj, in_dPchdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pch:")
    call table3d_prlog(this%Pch, indent=5)
    call init(this%Pcsi, N_NH_NC_NSI, in_Pcsi, in_dPcsidi, in_dPcsidj, in_dPcsidk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pcsi:")
    call table3d_prlog(this%Pcsi, indent=5)
    call init(this%Psic, N_NH_NC_NSI, in_Psic, in_dPsicdi, in_dPsicdj, in_dPsicdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Psic:")
    call table3d_prlog(this%Psic, indent=5)
    call init(this%Psih, N_NH_NC_NSI, in_Psih, in_dPsihdi, in_dPsihdj, in_dPsihdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Psih:")
    call table3d_prlog(this%Psih, indent=5)
    call init(this%Psisi, N_NH_NCL_NSI, in_Psisi, in_dPsisidi, in_dPsisidj, &
         in_dPsisidk, error=error)
    PASS_ERROR(error)
    call prlog("     Psisi:")
    call table3d_prlog(this%Psisi, indent=5)
    call init(this%Tcc, N_NI_NJ_NCONJ, in_Tcc, error=error)
    PASS_ERROR(error)
    call prlog("     Tcc:")
    call table3d_prlog(this%Tcc, indent=5)

    !
    ! Make splines for attractive, repulsive functions
    !

    call rebo2x_db_make_splines(this)

    call prlog

  endsubroutine rebo2x_db_init_with_parameters


  !>
  !! Free all resources
  !<
  subroutine rebo2x_db_del(this)
    implicit none

    type(BOP_TYPE), intent(inout)  :: this

    ! ---

    if (this%neighbor_list_allocated) then
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
       deallocate(this%sneb_seed)
       deallocate(this%sneb_last)
       deallocate(this%sneb)
       deallocate(this%sbnd)
       deallocate(this%sfacbo)
       deallocate(this%sfacnc)
       deallocate(this%cutdrik)
       deallocate(this%cutdrjk)
#endif

       this%neighbor_list_allocated = .false.
    endif

    call del(this%Fcc)
    call del(this%Fch)
    call del(this%Fhh)
    call del(this%Fsic)
    call del(this%Fsih)
    call del(this%Fsisi)
    call del(this%Pcc)
    call del(this%Pch)
    call del(this%Pcsi)
    call del(this%Psic)
    call del(this%Psih)
    call del(this%Psisi)
    call del(this%Tcc)

    call del(this%spl_VA(C_C))
    call del(this%spl_VA(C_H))
    call del(this%spl_VA(H_H))
    call del(this%spl_VA(C_Si))
    call del(this%spl_VA(Si_C))
    call del(this%spl_VA(Si_H))
    call del(this%spl_VA(Si_Si))

    call del(this%spl_VR(C_C))
    call del(this%spl_VR(C_H))
    call del(this%spl_VR(H_H))
    call del(this%spl_VR(C_Si))
    call del(this%spl_VR(Si_C))
    call del(this%spl_VR(Si_H))
    call del(this%spl_VR(Si_Si))

    call del(this%spl_fCin(C_C))
    call del(this%spl_fCin(C_H))
    call del(this%spl_fCin(H_H))
    call del(this%spl_fCin(C_Si))
    call del(this%spl_fCin(Si_C))
    call del(this%spl_fCin(Si_H))
    call del(this%spl_fCin(Si_Si))

#ifdef SCREENING
    call del(this%spl_fCout(C_C))
    call del(this%spl_fCout(C_H))
    call del(this%spl_fCout(H_H))
    call del(this%spl_fCout(C_Si))
    call del(this%spl_fCout(Si_C))
    call del(this%spl_fCout(Si_H))
    call del(this%spl_fCout(Si_Si))
#ifdef NUM_NEIGHBORS
    call del(this%spl_fCnc(C_C))
    call del(this%spl_fCnc(C_H))
    call del(this%spl_fCnc(H_H))
    call del(this%spl_fCnc(C_Si))
    call del(this%spl_fCnc(Si_C))
    call del(this%spl_fCnc(Si_H))
    call del(this%spl_fCnc(Si_Si))
#endif

#endif

  endsubroutine rebo2x_db_del


  !>
  !! Compute the coefficients for the g(cos(theta)) spline
  !! for C-C interaction
  !<
  subroutine rebo2x_db_make_cc_g_spline(this)
    implicit none

    type(BOP_TYPE), intent(inout)  :: this

    ! ---

    real(DP)  :: A(6, 6), Asave(6, 6)
    real(DP)  :: B(6)

    real(DP)  :: z

    integer   :: i, j, k

    integer   :: ipiv(6)

!    real(DP)  :: h, dh

    ! ---

    !
    ! Third interval
    !

    do i = 3, 6
!       z = (g_theta(i)-g_theta(3))/(g_theta(6)-g_theta(3))
       z = this%cc_g_theta(i)

       do j = 1, 6
          A(i-2, j) = z**(j-1)
       enddo
    enddo

    z = this%cc_g_theta(3)
    A(5, :) = 0.0
    A(6, :) = 0.0
    A(5, 2) = 1.0
    A(6, 3) = 2.0
    do j = 3, 6
                    A(5, j) = (j-1)*z**(j-2)        ! First derivative on left boundary
       if (j >= 4)  A(6, j) = (j-2)*(j-1)*z**(j-3)  ! Second derivative on left boundary
    enddo

    B(1:4) = this%cc_g_g1(3:6)
    B(5)   = this%cc_g_dg1(3)
    B(6)   = this%cc_g_d2g1(3)

!    write (*, *)  1

    Asave = A
    call dgesv(6, 1, A, 6, ipiv, B, 6, i)

    if (i /= 0) then
       write (*, '(A,I5)')  "[rebo2x_make_cc_g_spline] dgesv failed. info = ", i
       stop
    endif

    this%cc_g1_coeff%c(:, 3) = B(:)

    B(1:4) = this%cc_g_g2(3:6)
    B(5)   = this%cc_g_dg1(3)
    B(6)   = this%cc_g_d2g1(3)

!    write (*, *)  2

    A = Asave
    call dgesv(6, 1, A, 6, ipiv, B, 6, i)

    if (i /= 0) then
       write (*, '(A,I5)')  "[rebo2x_make_cc_g_spline] dgesv failed. info = ", i
       stop
    endif

    this%cc_g2_coeff%c(:, 3) = B(:)


    !
    ! First interval and second interval
    !

    do k = 0, 1

       A = 0.0

       do i = 0, 1
          z = this%cc_g_theta(1+k)*(1-i) + this%cc_g_theta(2+k)*i

          A(3*i+1, 1) = 1.0
          A(3*i+2, 2) = 1.0
          A(3*i+3, 3) = 2.0
          do j = 2, 6
                           A(3*i+1, j) = z**(j-1)
             if (j >= 3)   A(3*i+2, j) = (j-1)*z**(j-2)
             if (j >= 4)   A(3*i+3, j) = (j-2)*(j-1)*z**(j-3)
          enddo
       enddo

       B(1)   = this%cc_g_g1(1+k)
       B(2)   = this%cc_g_dg1(1+k)
       B(3)   = this%cc_g_d2g1(1+k)
       B(4)   = this%cc_g_g1(2+k)
       B(5)   = this%cc_g_dg1(2+k)
       B(6)   = this%cc_g_d2g1(2+k)

!       write (*, *)  3

       call dgesv(6, 1, A, 6, ipiv, B, 6, i)

       if (i /= 0) then
          write (*, '(A,I5)')  "[rebo2x_make_cc_g_spline] dgesv failed. info = ", i
          stop
       endif

       this%cc_g1_coeff%c(:, 1+k) = B(:)
       this%cc_g2_coeff%c(:, 1+k) = B(:)

    enddo

  endsubroutine rebo2x_db_make_cc_g_spline


  !>
  !! Compute the coefficients for the g(cos(theta)) spline
  !! for Si-Si interaction
  !<
  subroutine rebo2x_db_make_sisi_g_spline(this)
    implicit none

    type(BOP_TYPE), intent(inout)  :: this

    ! ---

    real(DP)  :: A(6, 6)
    real(DP)  :: B(6)

    real(DP)  :: z

    integer   :: i, j, k

    integer   :: ipiv(6)

#if 0
    real(DP)  :: v, dv
#endif

    ! ---

    !
    ! First, second and third interval
    !

    do k = 0, 2

       A = 0.0_DP

       do i = 0, 1
          z = this%sisi_g_theta(1+k)*(1-i) + this%sisi_g_theta(2+k)*i

          A(3*i+1, 1) = 1.0
          A(3*i+2, 2) = 1.0
          A(3*i+3, 3) = 2.0
          do j = 2, 6
                           A(3*i+1, j) = z**(j-1)
             if (j >= 3)   A(3*i+2, j) = (j-1)*z**(j-2)
             if (j >= 4)   A(3*i+3, j) = (j-2)*(j-1)*z**(j-3)
          enddo
       enddo

       B(1)   = this%sisi_g_g(1+k)
       B(2)   = this%sisi_g_dg(1+k)
       B(3)   = this%sisi_g_d2g(1+k)
       B(4)   = this%sisi_g_g(2+k)
       B(5)   = this%sisi_g_dg(2+k)
       B(6)   = this%sisi_g_d2g(2+k)

       call dgesv(6, 1, A, 6, ipiv, B, 6, i)

       if (i /= 0) then
          write (*, '(A,I5)')  "[rebo2x_make_sisi_g_spline] dgesv failed. info = ", i
          stop
       endif

       this%sisi_g_coeff%c(:, 1+k) = B(:)

    enddo

#if 0
    do i = -100, 100
       call g_from_spline(this%sisi_g_theta, this%sisi_g_coeff, i/100.0_DP, v, dv)
       write (1000, *)  i/100.0_DP, v, dv
    enddo
#endif

  endsubroutine rebo2x_db_make_sisi_g_spline


! --- Functions ---

  function cc_VA(dr, cc_B1, cc_B2, cc_B3, cc_beta1, cc_beta2, cc_beta3) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: cc_B1
    real(DP), intent(in)  :: cc_B2
    real(DP), intent(in)  :: cc_B3
    real(DP), intent(in)  :: cc_beta1
    real(DP), intent(in)  :: cc_beta2
    real(DP), intent(in)  :: cc_beta3
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, exp2, exp3

    ! ---

    exp1 = cc_B1*exp(-cc_beta1*dr)
    exp2 = cc_B2*exp(-cc_beta2*dr)
    exp3 = cc_B3*exp(-cc_beta3*dr)

    val  = - ( exp1 + exp2 + exp3 )

  endfunction cc_VA


  function cc_VR(dr, cc_A, cc_Q, cc_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: cc_A
    real(DP), intent(in)  :: cc_Q
    real(DP), intent(in)  :: cc_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = cc_A*exp(-cc_alpha*dr)
    hlp1 = 1+cc_Q/dr

    val  = hlp1*exp1

  endfunction cc_VR


  function ch_VA(dr, ch_B1, ch_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: ch_B1
    real(DP), intent(in)  :: ch_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = ch_B1*exp(-ch_beta1*dr)

    val  = - exp1

  endfunction ch_VA


  function ch_VR(dr, ch_A, ch_Q, ch_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: ch_A
    real(DP), intent(in)  :: ch_Q
    real(DP), intent(in)  :: ch_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = ch_A*exp(-ch_alpha*dr)
    hlp1 = 1+ch_Q/dr

    val  = hlp1*exp1

  endfunction ch_VR


  function hh_VA(dr, hh_B1, hh_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: hh_B1
    real(DP), intent(in)  :: hh_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = hh_B1*exp(-hh_beta1*dr)

    val  = - exp1

  endfunction hh_VA


  function hh_VR(dr, hh_A, hh_Q, hh_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: hh_A
    real(DP), intent(in)  :: hh_Q
    real(DP), intent(in)  :: hh_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = hh_A*exp(-hh_alpha*dr)
    hlp1 = 1+hh_Q/dr

    val  = hlp1*exp1

  endfunction hh_VR


  function sisi_VA(dr, sisi_B1, sisi_B2, sisi_B3, sisi_beta1, sisi_beta2, sisi_beta3) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: sisi_B1
    real(DP), intent(in)  :: sisi_B2
    real(DP), intent(in)  :: sisi_B3
    real(DP), intent(in)  :: sisi_beta1
    real(DP), intent(in)  :: sisi_beta2
    real(DP), intent(in)  :: sisi_beta3
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, exp2, exp3

    ! ---

    exp1 = sisi_B1*exp(-sisi_beta1*dr)
    exp2 = sisi_B2*exp(-sisi_beta2*dr)
    exp3 = sisi_B3*exp(-sisi_beta3*dr)

    val  = - ( exp1 + exp2 + exp3 )

  endfunction sisi_VA

  function sisi_VR(dr, sisi_A, sisi_Q, sisi_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: sisi_A
    real(DP), intent(in)  :: sisi_Q
    real(DP), intent(in)  :: sisi_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = sisi_A*exp(-sisi_alpha*dr)
    hlp1 = 1+sisi_Q/dr

    val  = hlp1*exp1

  endfunction sisi_VR


  function sih_VA(dr, sih_B1, sih_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: sih_B1
    real(DP), intent(in)  :: sih_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = sih_B1*exp(-sih_beta1*dr)

    val  = - exp1

  endfunction sih_VA


  function sih_VR(dr, sih_A, sih_Q, sih_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: sih_A
    real(DP), intent(in)  :: sih_Q
    real(DP), intent(in)  :: sih_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = sih_A*exp(-sih_alpha*dr)
    hlp1 = 1+sih_Q/dr

    val  = hlp1*exp1

  endfunction sih_VR

 function sic_VA(dr, sic_B1, sic_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: sic_B1
    real(DP), intent(in)  :: sic_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = sic_B1*exp(-sic_beta1*dr)

    val  = - exp1

  endfunction sic_VA


  function sic_VR(dr, sic_A, sic_Q, sic_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: sic_A
    real(DP), intent(in)  :: sic_Q
    real(DP), intent(in)  :: sic_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = sic_A*exp(-sic_alpha*dr)
    hlp1 = 1+sic_Q/dr

    val  = hlp1*exp1

  endfunction sic_VR



#ifdef EXP_CUT

  function cutoff_f(dr, l, h, m) result(val)
    implicit none
    
    real(DP), intent(in)  :: dr, l, h, m
    real(DP)              :: val

    ! ---

    real(DP) :: dval

    ! ---

    call exp_cutoff(l, h, dr, val, dval)

  endfunction cutoff_f

  subroutine cutoff_f_and_df(dr, l, h, val, dval)
    implicit none
    
    real(DP), intent(in)  :: dr, l, h
    real(DP), intent(out) :: val, dval

    ! ---

    call exp_cutoff(l, h, dr, val, dval)

  endsubroutine cutoff_f_and_df

#else

  function cutoff_f(dr, l, h, m) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: l
    real(DP), intent(in)  :: h
    real(DP), intent(in)  :: m
    real(DP)              :: val

    ! ---

    real(DP) :: dval

    ! ---

    call trig_off(l, h, dr, val, dval)

  endfunction cutoff_f

  subroutine cutoff_f_and_df(dr, l, h, val, dval)
    implicit none

    real(DP), intent(in)  :: dr, l, h
    real(DP), intent(out) :: val, dval

    ! ---

    call trig_off(l, h, dr, val, dval)

  endsubroutine cutoff_f_and_df

#endif


  !>
  !! Make splines for attractive, repulsive functions
  !<
  subroutine rebo2x_db_make_splines(this)
    implicit none

    type(BOP_TYPE), intent(inout)  :: this

    ! ---

    !
    ! Attractive potential
    !

    call init( &
         this%spl_VA(C_C), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%cc_out_r2, &
#else
         this%cc_in_r2, &
#endif
         cc_VA, this%cc_B1, this%cc_B2, this%cc_B3, &
         this%cc_beta1, this%cc_beta2, this%cc_beta3)
    call init( &
         this%spl_VA(C_H), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%ch_out_r2, &
#else
         this%ch_in_r2, &
#endif
         ch_VA, this%ch_B1, this%ch_beta1)
    call init( &
         this%spl_VA(H_H), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%hh_out_r2, &
#else
         this%hh_in_r2, &
#endif
         hh_VA, this%hh_B1, this%hh_beta1)
    call init( &
         this%spl_VA(Si_Si), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sisi_out_r2, &
#else
         this%sisi_in_r2, &
#endif
         sisi_VA, this%sisi_B1, this%sisi_B2, this%sisi_B3, &
         this%sisi_beta1, this%sisi_beta2, this%sisi_beta3)
    call init( &
         this%spl_VA(Si_H), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sih_out_r2, &
#else
         this%sih_in_r2, &
#endif
         sih_VA, this%sih_B1, this%sih_beta1)
    call init( &
         this%spl_VA(C_Si), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sic_out_r2, &
#else
         this%sic_in_r2, &
#endif
         sic_VA, this%sic_B1, this%sic_beta1)
    call init( &
         this%spl_VA(Si_C), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sic_out_r2, &
#else
         this%sic_in_r2, &
#endif
         sic_VA, this%sic_B1, this%sic_beta1)

    !
    ! Repulsive potential
    !

    call init( &
         this%spl_VR(C_C), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%cc_out_r2, &
#else
         this%cc_in_r2, &
#endif
         cc_VR, this%cc_A, this%cc_Q, this%cc_alpha)
    call init( &
         this%spl_VR(C_H), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%ch_out_r2, &
#else
         this%ch_in_r2, &
#endif
         ch_VR, this%ch_A, this%ch_Q, this%ch_alpha)
    call init( &
         this%spl_VR(H_H), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%hh_out_r2, &
#else
         this%hh_in_r2, &
#endif
         hh_VR, this%hh_A, this%hh_Q, this%hh_alpha)
    call init( & 
         this%spl_VR(Si_Si), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sisi_out_r2, & 
#else
         this%sisi_in_r2, &
#endif
         sisi_VR, this%sisi_A,this%sisi_Q, this%sisi_alpha)
    call init( & 
         this%spl_VR(Si_H), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sih_out_r2, &
#else
         this%sih_in_r2, &
#endif
         sih_VR, this%sih_A, this%sih_Q, this%sih_alpha)
    call init(& 
         this%spl_VR(C_Si), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sic_out_r2, & 
#else
         this%sic_in_r2, &
#endif
         sic_VR, this%sic_A, this%sic_Q, this%sic_alpha)
    call init(& 
         this%spl_VR(Si_C), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%sic_out_r2, & 
#else
         this%sic_in_r2, &
#endif
         sic_VR, this%sic_A, this%sic_Q, this%sic_alpha)

    !
    ! Inner cut-off
    !

    call init( &
         this%spl_fCin(C_C), &
         this%spl_n, this%cc_in_r1, this%cc_in_r2, &
         cutoff_f, this%cut_in_l(C_C), this%cut_in_h(C_C), &
         this%cut_in_m(C_C))
    call init( &
         this%spl_fCin(C_H), &
         this%spl_n, this%ch_in_r1, this%ch_in_r2, &
         cutoff_f, this%cut_in_l(C_H), this%cut_in_h(C_H), &
         this%cut_in_m(C_H))
    call init( &
         this%spl_fCin(H_H), &
         this%spl_n, this%hh_in_r1, this%hh_in_r2, &
         cutoff_f, this%cut_in_l(H_H), this%cut_in_h(H_H), &
         this%cut_in_m(H_H))
    call init( &
         this%spl_fCin(Si_Si), & 
         this%spl_n, this%sisi_in_r1, this%sisi_in_r2, & 
         cutoff_f, this%cut_in_l(Si_Si), this%cut_in_h(Si_Si), &
         this%cut_in_m(Si_Si))
    call init( &
         this%spl_fCin(Si_H), &
         this%spl_n, this%sih_in_r1, this%sih_in_r2, &
         cutoff_f, this%cut_in_l(Si_H), this%cut_in_h(Si_H), &
         this%cut_in_m(Si_H))
    call init( &
         this%spl_fCin(C_Si), &
         this%spl_n, this%sic_in_r1, this%sic_in_r2, &
         cutoff_f, this%cut_in_l(C_Si), this%cut_in_h(C_Si), &
         this%cut_in_m(C_Si))
    call init( &
         this%spl_fCin(Si_C), &
         this%spl_n, this%sic_in_r1, this%sic_in_r2, &
         cutoff_f, this%cut_in_l(Si_C), this%cut_in_h(Si_C), &
         this%cut_in_m(Si_C))

#ifdef SCREENING

    !
    ! Outer cut-off
    !

    call init( &
         this%spl_fCout(C_C), &
         this%spl_n, this%cc_out_r1, this%cc_out_r2, &
         cutoff_f, this%cut_out_l(C_C), this%cut_out_h(C_C), &
         this%cut_out_m(C_C))
    call init( &
         this%spl_fCout(C_H), &
         this%spl_n, this%ch_out_r1, this%ch_out_r2, &
         cutoff_f, this%cut_out_l(C_H), this%cut_out_h(C_H), &
         this%cut_out_m(C_H))
    call init( &
         this%spl_fCout(H_H), &
         this%spl_n, this%hh_out_r1, this%hh_out_r2, &
         cutoff_f, this%cut_out_l(H_H), this%cut_out_h(H_H), &
         this%cut_out_m(H_H))
    call init( &
         this%spl_fCout(Si_Si), & 
         this%spl_n, this%sisi_out_r1, this%sisi_out_r2, & 
         cutoff_f, this%cut_out_l(Si_Si), this%cut_out_h(Si_Si), &
         this%cut_out_m(Si_Si))
    call init( &
         this%spl_fCout(Si_H), &
         this%spl_n, this%sih_out_r1, this%sih_out_r2, &
         cutoff_f, this%cut_out_l(Si_H), this%cut_out_h(Si_H), &
         this%cut_out_m(Si_H))
    call init( &
         this%spl_fCout(C_Si), &
         this%spl_n, this%sic_out_r1, this%sic_out_r2, &
         cutoff_f, this%cut_out_l(C_Si), this%cut_out_h(C_Si), &
         this%cut_out_m(C_Si))
    call init( &
         this%spl_fCout(Si_C), &
         this%spl_n, this%sic_out_r1, this%sic_out_r2, &
         cutoff_f, this%cut_out_l(Si_C), this%cut_out_h(Si_C), &
         this%cut_out_m(Si_C))

#ifdef NUM_NEIGHBORS

    !
    ! Neighbor and conjugation cut-off
    !

    call init( &
         this%spl_fCnc(C_C), &
         this%spl_n, this%cc_nc_r1, this%cc_nc_r2, &
         cutoff_f, this%cut_nc_l(C_C), this%cut_nc_h(C_C), &
         this%cut_nc_m(C_C))
    call init( &
         this%spl_fCnc(C_H), &
         this%spl_n, this%ch_nc_r1, this%ch_nc_r2, &
         cutoff_f, this%cut_nc_l(C_H), this%cut_nc_h(C_H), &
         this%cut_nc_m(C_H))
    call init( &
         this%spl_fCnc(H_H), &
         this%spl_n, this%hh_nc_r1, this%hh_nc_r2, &
         cutoff_f, this%cut_nc_l(H_H), this%cut_nc_h(H_H), &
         this%cut_nc_m(H_H))
    call init( &
         this%spl_fCnc(Si_Si), & 
         this%spl_n, this%sisi_nc_r1, this%sisi_nc_r2, & 
         cutoff_f, this%cut_nc_l(Si_Si), this%cut_nc_h(Si_Si), &
         this%cut_nc_m(Si_Si))
    call init( &
         this%spl_fCnc(Si_H), &
         this%spl_n, this%sih_nc_r1, this%sih_nc_r2, &
         cutoff_f, this%cut_nc_l(Si_H), this%cut_nc_h(Si_H), &
         this%cut_nc_m(Si_H))
    call init( &
         this%spl_fCnc(C_Si), &
         this%spl_n, this%sic_nc_r1, this%sic_nc_r2, &
         cutoff_f, this%cut_nc_l(C_Si), this%cut_nc_h(C_Si), &
         this%cut_nc_m(C_Si))
    call init( &
         this%spl_fCnc(Si_C), &
         this%spl_n, this%sic_nc_r1, this%sic_nc_r2, &
         cutoff_f, this%cut_nc_l(Si_C), this%cut_nc_h(Si_C), &
         this%cut_nc_m(Si_C))

#endif

#endif

  endsubroutine rebo2x_db_make_splines



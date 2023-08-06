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

!
! Functions for the bond-order potential, i.e. attractive, repulsive
! parts, etc.
!


!>
!! Conjugation counter for carbon
!<
!elemental subroutine fconj(this, x, fx, dfx)
subroutine fconj_C(this, x, fx, dfx)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  real(DP),       intent(in)  :: x
  real(DP),       intent(out) :: fx
  real(DP),       intent(out) :: dfx

  ! ---

  real(DP)  :: arg

  ! ---

  if ( x .le. 2.0_DP ) then
     fx   = 1.0_DP
     dfx  = 0.0_DP
  else if( x .ge. 3.0_DP ) then
     fx   = 0.0_DP
     dfx  = 0.0_DP
  else
     arg  = pi  * ( x - 2.0_DP )
     fx   = 0.5_DP * ( 1.0_DP + cos( arg ) )
     dfx  =-0.5_DP * pi * sin( arg )
  endif

endsubroutine fconj_C


!>
!! Conjugation counter for oxygen
!<
subroutine fconj_O(this, x, fx, dfx)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  real(DP),       intent(in)  :: x
  real(DP),       intent(out) :: fx
  real(DP),       intent(out) :: dfx

  ! ---

  real(DP)  :: arg

  ! ---

  if( x .ge. 1.0_DP ) then
     fx   = 0.0_DP
     dfx  = 0.0_DP
  else
     arg  = pi * x
     fx   = 0.5_DP * ( 1.0_DP + cos( arg ) )
     dfx  =-0.5_DP * pi * sin( arg )
  endif

endsubroutine fconj_O


!>
!! Cut-off function: fCin(r), dfCin(r)
!<
subroutine fCin(this, ijpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: ijpot
  real(DP), intent(in)        :: dr
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval

  ! ---

  if (dr > this%cut_in_h(ijpot)) then
     val   = 0.0_DP
     dval  = 0.0_DP
  else if (dr < this%cut_in_l(ijpot)) then
     val   = 1.0_DP
     dval  = 0.0_DP
  else
     call f_and_df(this%spl_fCin(ijpot), dr, val, dval)
  endif

endsubroutine fCin

#ifdef SCREENING

!>
!! Cut-off function: fCout(r), dfCout(r)
!<
subroutine fCout(this, ijpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: ijpot
  real(DP), intent(in)        :: dr
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval

  ! ---

  if (this%no_outer_cutoff) then
     val  = 1.0_DP
     dval = 0.0_DP
  else
     if (dr > this%cut_out_h(ijpot)) then
        val   = 0.0_DP
        dval  = 0.0_DP
     else if (dr < this%cut_out_l(ijpot)) then
        val   = 1.0_DP
        dval  = 0.0_DP
     else
        call f_and_df(this%spl_fCout(ijpot), dr, val, dval)
     endif
  endif

endsubroutine fCout


!**********************************************************************
! Cut-off function: fCbo(r), dfCbo(r)
!**********************************************************************
subroutine fCbo(this, ijpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: ijpot
  real(DP), intent(in)        :: dr
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval

  ! ---

  if (dr > this%cut_bo_h(ijpot)) then
     val   = 0.0_DP
     dval  = 0.0_DP
  else if (dr < this%cut_bo_l(ijpot)) then
     val   = 1.0_DP
     dval  = 0.0_DP
  else
     call f_and_df(this%spl_fCbo(ijpot), dr, val, dval)
  endif

endsubroutine fCbo


#ifdef NUM_NEIGHBORS

!**********************************************************************
! Cut-off function: fCnc(r), dfCnc(r)
!**********************************************************************
subroutine fCnc(this, ijpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer,        intent(in)  :: ijpot
  real(DP),       intent(in)  :: dr
  real(DP),       intent(out) :: val
  real(DP),       intent(out) :: dval

  ! ---

  if (dr > this%cut_nc_h(ijpot)) then
     val   = 0.0_DP
     dval  = 0.0_DP
  else if (dr < this%cut_nc_l(ijpot)) then
     val   = 1.0_DP
     dval  = 0.0_DP
  else
     call f_and_df(this%spl_fCnc(ijpot), dr, val, dval)
  endif

endsubroutine fCnc

#endif

#endif

!>
!! Attractive potential: VA(r), dVA(r)
!<
subroutine VA(this, ijpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: ijpot
  real(DP), intent(in)        :: dr
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval

  ! ---

  real(DP)  :: exp1, exp2, exp3

  ! --- 

  if (dr > this%spl_VA(ijpot)%x0 .and. dr < this%spl_VA(ijpot)%cut) then

     call f_and_df(this%spl_VA(ijpot), dr, val, dval)

  else

     if (ijpot == C_C) then

        exp1 = this%cc_B1*exp(-this%cc_beta1*dr)
        exp2 = this%cc_B2*exp(-this%cc_beta2*dr)
        exp3 = this%cc_B3*exp(-this%cc_beta3*dr)

        val  = - ( exp1 + exp2 + exp3 )
        dval = - ( -this%cc_beta1*exp1 - this%cc_beta2*exp2 - this%cc_beta3*exp3 )

     else if (ijpot == C_H) then

        exp1 = this%ch_B1*exp(-this%ch_beta1*dr)

        val  = - exp1
        dval =   this%ch_beta1*exp1

     else if (ijpot == O_C) then

        exp1 = this%oc_B1*exp(-this%oc_beta1*dr)

        val  = - exp1
        dval =   this%oc_beta1*exp1

     else if (ijpot == O_H) then

        exp1 = this%oh_B1*exp(-this%oh_beta1*dr)

        val  = - exp1
        dval =   this%oh_beta1*exp1

     else if (ijpot == O_O) then
         
        exp1 = this%oo_B1*exp(-this%oo_beta1*dr)

        val  = - exp1
        dval = this%oo_beta1*exp1

     else ! if (ijpot == H_H) then                                                                                                                                                    
        exp1 = this%hh_B1*exp(-this%hh_beta1*dr)

        val  = - exp1
        dval =   this%hh_beta1*exp1

     endif

  endif

endsubroutine VA


!>
!! Repulsive potential: VA(r), dVA(r)
!<
subroutine VR(this, ijpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: ijpot
  real(DP), intent(in)        :: dr
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval

  ! ---

  real(DP)  :: exp1, hlp1

  ! ---

  if (dr > this%spl_VR(ijpot)%x0 .and. dr < this%spl_VR(ijpot)%cut) then

     call f_and_df(this%spl_VR(ijpot), dr, val, dval)

  else

     if (ijpot == C_C) then

        exp1 = this%cc_A*exp(-this%cc_alpha*dr)
        hlp1 = 1+this%cc_Q/dr

        val  = hlp1*exp1
        dval = ( -this%cc_Q/(dr**2) - hlp1*this%cc_alpha ) * exp1

     else if (ijpot == C_H) then

        exp1 = this%ch_A*exp(-this%ch_alpha*dr)
        hlp1 = 1+this%ch_Q/dr

        val  = hlp1*exp1
        dval = ( -this%ch_Q/(dr**2) - hlp1*this%ch_alpha ) * exp1

     else if (ijpot == O_C) then

        exp1 = this%oc_A*exp(-this%oc_alpha*dr)
        hlp1 = 1+this%oc_Q/dr

        val  = hlp1*exp1
        dval = ( -this%oc_Q/(dr**2) - hlp1*this%oc_alpha ) * exp1

     else if (ijpot == O_H) then

        exp1 = this%oh_A*exp(-this%oh_alpha*dr)
        hlp1 = 1+this%oh_Q/dr

        val  = hlp1*exp1
        dval = ( -this%oh_Q/(dr**2) - hlp1*this%oh_alpha ) * exp1

     else if (ijpot == O_O) then

        exp1 = this%oo_A*exp(-this%oo_alpha*dr)
        hlp1 = 1+this%oo_Q/dr

        val  = hlp1*exp1
        dval = ( -this%oo_Q/(dr**2) - hlp1*this%oo_alpha ) * exp1

     else ! if (ijpot == H_H) then

        exp1 = this%hh_A*exp(-this%hh_alpha*dr)
        hlp1 = 1+this%hh_Q/dr

        val  = hlp1*exp1
        dval = ( -this%hh_Q/(dr**2) - hlp1*this%hh_alpha ) * exp1

     endif

  endif

endsubroutine VR


!>
!! Angular contribution to the bond order: g(cos(theta)), dg(cos(theta))
!<
subroutine g(this, ktypi, ktypj, ktypk, costh, n, val, dval_dcosth, dval_dN)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: ktypi
  integer, intent(in)         :: ktypj
  integer, intent(in)         :: ktypk
  real(DP), intent(in)        :: costh
  real(DP), intent(in)        :: n
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval_dcosth
  real(DP), intent(out)       :: dval_dN

  ! ---

  real(DP)  :: v1, v2, dv1, dv2, s, ds, arg, h
  integer   :: i, ig

  ! ---



  val         = 0.0_DP
  dval_dcosth = 0.0_DP
  dval_dN     = 0.0_DP


  if (ktypi == rebo2_C_ .and. ktypk /= rebo2_O_) then

     if (this%c_g > -0.5_DP) then
        
        val = this%c_g
        dval_dcosth = 0.0_DP
        dval_dN = 0.0_DP

     else

        if (n < 3.2_DP) then

           call g_from_spline(this%cc_g_theta, this%cc_g2_coeff, costh, val, dval_dcosth)
           dval_dN = 0.0_DP

        else if (n > 3.7_DP) then
           
           call g_from_spline(this%cc_g_theta, this%cc_g1_coeff, costh, val, dval_dcosth)
           dval_dN = 0.0_DP

        else

           call g_from_spline(this%cc_g_theta, this%cc_g1_coeff, costh, v1, dv1)
           call g_from_spline(this%cc_g_theta, this%cc_g2_coeff, costh, v2, dv2)

           arg = 2*PI*(n-3.2_DP)
           s  = (1+cos(arg))/2
           ds = -PI*sin(arg)

           val          =  v1*(1-s) +  v2*s
           dval_dcosth  = dv1*(1-s) + dv2*s
           dval_dN      = (v2-v1)*ds

        endif

     endif

  else if (ktypi == rebo2_O_ .and. ktypk == rebo2_O_) then

     h           = this%oo_d**2 + (this%oo_h+costh)**2
     val         = this%oo_gamma * (1.0 + this%oo_c**2/this%oo_d**2 - this%oo_c**2/h)
     dval_dcosth = 2.0 * this%oo_gamma * this%oo_c**2 * (this%oo_h+costh)/(h**2)
     dval_dN     = 0.0_DP

  else if ((ktypi == rebo2_O_ .and. ktypk == rebo2_C_) .or. &
           (ktypi == rebo2_C_ .and. ktypk == rebo2_O_)) then

     h           = this%oc_d**2 + (this%oc_h+costh)**2
     val         = this%oc_gamma * (1.0 + this%oc_c**2/this%oc_d**2 - this%oc_c**2/h)
     dval_dcosth = 2.0 * this%oc_gamma * this%oc_c**2 * (this%oc_h+costh)/(h**2)
     dval_dN     = 0.0_DP

  else if ((ktypi == rebo2_O_ .and. ktypk == rebo2_H_) .or. &
           (ktypi == rebo2_H_ .and. ktypk == rebo2_O_)) then

     h           = this%oh_d**2 + (this%oh_h+costh)**2
     val         = this%oh_gamma * (1.0 + this%oh_c**2/this%oh_d**2 - this%oh_c**2/h)
     dval_dcosth = 2.0 * this%oh_gamma * this%oh_c**2 * (this%oh_h+costh)/(h**2)
     dval_dN     = 0.0_DP

  else if (ktypi == rebo2_H_ .and. ktypk /= rebo2_O_) then

     if (this%h_g > -0.5_DP) then
        
        val = this%h_g
        dval_dcosth = 0.0_DP
        dval_dN = 0.0_DP
        
     else

        ig = this%igh(int(-costh*12.0D0)+13)
        
        val          = this%spgh(1, ig) + this%spgh(2, ig)*costh
        dval_dcosth  = this%spgh(2, ig)
        do i = 3, 6
           val          = val  + this%spgh(i, ig)*costh**(i-1)
           dval_dcosth  = dval_dcosth + (i-1)*this%spgh(i, ig)*costh**(i-2)
        enddo
        dval_dN = 0.0_DP

     endif

  endif

endsubroutine g


!>
!! Angular contribution to the bond order: g(cos(theta)), dg(cos(theta))
!<
pure subroutine g_from_spline(theta, coeff, costh, val, dval)
  implicit none

  real(DP),        intent(in)   :: theta(:)
  type(g_coeff_t), intent(in)   :: coeff
  real(DP),        intent(in)   :: costh
  real(DP),        intent(out)  :: val
  real(DP),        intent(out)  :: dval

  ! ---

  integer   :: i, j
  real(DP)  :: h, dh

  ! ---

  !    if (costh >= theta(1)) then

  if (costh < theta(2)) then
     j = 1
  else if (costh < theta(3)) then
     j = 2
  else ! if (costh <= theta(6)) then
     j = 3
     !       else
     !          write (*, '(A,ES20.10,A)')  "[g] value ", costh, " outside the region for which the spline is defined."
     !          stop
  endif

  h   = coeff%c(1, j) + coeff%c(2, j)*costh
  dh  = coeff%c(2, j)
  do i = 3, 6
     h   = h  + coeff%c(i, j)*costh**(i-1)
     dh  = dh + (i-1)*coeff%c(i, j)*costh**(i-2)
  enddo

  val   = h
  dval  = dh

  !    else
  !       write (*, '(A,ES20.10,A)')  "[g] value ", costh, " outside the region for which the spline is defined."
  !       stop
  !    endif

endsubroutine g_from_spline


!>
!! Bond order function
!<
!pure subroutine bo(this, eli, ijpot, zij, fcij, faij, bij, dfbij)
subroutine bo(this, eli, ijpot, zij, fcij, faij, bij, dfbij)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: eli
  integer, intent(in)         :: ijpot
  real(DP), intent(in)        :: zij
  real(DP), intent(in)        :: fcij
  real(DP), intent(in)        :: faij
  real(DP), intent(out)       :: bij
  real(DP), intent(out)       :: dfbij

  ! ---

  real(DP) :: arg

  ! ---

  if (this%bo_override(ijpot) > -0.5_DP) then

     bij = this%bo_override(ijpot)
     dfbij = 0.0_DP

  else

     if (this%const_bo) then

        bij   = 0.0_DP
        dfbij = 0.0_DP

     else

        arg    = 1.0 + zij
        bij    = arg ** this%conpe(eli)
        dfbij  = this%conan(eli) * fcij * faij * arg ** this%conpf(eli)
        
     endif

  endif

endsubroutine bo


!>
!! Length dependent contribution to the bond order: h(dr), dh(dr)
!<
! FIXME: Code for SEPARATE_H_ARGUMENTS has been removed
subroutine h(this, elj, eli, elk, ijpot, ikpot, dr, val, dval)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: elj
  integer, intent(in)         :: eli
  integer, intent(in)         :: elk
  integer, intent(in)         :: ijpot
  integer, intent(in)         :: ikpot
  real(DP), intent(in)        :: dr
  real(DP), intent(out)       :: val
  real(DP), intent(out)       :: dval

  ! ---

  real(DP)  :: arg
  real(DP)  :: fac
  integer   :: m

  integer :: i,j,k
  ! ---

  val       = 1.0_DP
  dval      = 0.0_DP


  fac = this%lambda(eli,elj,elk)
  arg = fac*(dr-this%re(ijpot)+this%re(ikpot))
  m = this%m(eli,elj,elk)
  if (m == 0) then
     val  = 1.0_DP
     dval = 0.0_DP
  else if (m == 1) then
     val  = exp(arg)
     dval = fac * val
  else if (m == 3) then
     val  = exp(arg*arg*arg)
     dval = 3*fac * arg*arg * val
  else
     val  = exp(arg**m)
     dval = m*fac * arg**(m-1) * val
  endif

endsubroutine h


!>
!! Generate an index for this *pair* of elements
!<
elemental function Z2pair(this, eli, elj)
  implicit none

  type(BOP_TYPE), intent(in)  :: this
  integer, intent(in)         :: eli
  integer, intent(in)         :: elj
  integer                     :: Z2pair


  if (eli == rebo2_C_) then
     if (elj == rebo2_O_) then
        Z2pair = 7
     else
        Z2pair = elj
     end if
  else if (elj == rebo2_C_) then
     Z2pair = eli
  else 
     Z2pair = eli + elj
  endif

endfunction Z2pair

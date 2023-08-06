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
  subroutine rebo2coh_db_init_with_parameters( &
       this, &
       in_Fcc,   in_dFccdi,   in_dFccdj,   in_dFccdk, &
       in_Fch,   in_dFchdi,   in_dFchdj,   in_dFchdk, &
       in_Fhh,   in_dFhhdi,   in_dFhhdj,   in_dFhhdk, &
       in_Foc,   in_dFocdi,   in_dFocdj,   in_dFocdk, &
       in_Foh,   in_dFohdi,   in_dFohdj,   in_dFohdk, &
       in_Foo,   in_dFoodi,   in_dFoodj,   in_dFoodk, & 
       in_Pcc,   in_dPccdi,   in_dPccdj,   in_dPccdk, &
       in_Pch,   in_dPchdi,   in_dPchdj,   in_dPchdk, &
       in_Phh,   in_dPhhdi,   in_dPhhdj,   in_dPhhdk, &
       in_Poc,   in_dPocdi,   in_dPocdj,   in_dPocdk, &
       in_Pco,   in_dPcodi,   in_dPcodj,   in_dPcodk, &
       in_Poh,   in_dPohdi,   in_dPohdj,   in_dPohdk, &
       in_Pho,   in_dPhodi,   in_dPhodj,   in_dPhodk, &
       in_Poo,   in_dPoodi,   in_dPoodj,   in_dPoodk, &
       in_Tcc,   in_dTccdi,   in_dTccdj,   in_dTccdk, &
       error)
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
    real(DP), intent(in)          :: in_Foc(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFocdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFocdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFocdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Foh(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFohdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFohdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFohdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Foo(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFoodi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFoodj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dFoodk(0:, 0:, 0:)

    real(DP), intent(in)          :: in_Pcc(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPccdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPccdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPccdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Pch(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPchdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPchdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPchdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Phh(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPhhdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPhhdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPhhdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Poc(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPocdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPocdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPocdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Pco(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPcodi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPcodj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPcodk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Poh(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPohdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPohdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPohdk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Pho(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPhodi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPhodj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPhodk(0:, 0:, 0:)
    real(DP), intent(in)          :: in_Poo(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPoodi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPoodj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dPoodk(0:, 0:, 0:)

    real(DP), intent(in)          :: in_Tcc(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dTccdi(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dTccdj(0:, 0:, 0:)
    real(DP), intent(in)          :: in_dTccdk(0:, 0:, 0:)

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
       write (ilog, '(5X,A,F20.10)')  "oo_A        = ", this%oo_A
       write (ilog, '(5X,A,F20.10)')  "oo_Q        = ", this%oo_Q
       write (ilog, '(5X,A,F20.10)')  "oo_alpha    = ", this%oo_alpha
       write (ilog, '(5X,A,F20.10)')  "oo_B1       = ", this%oo_B1
       write (ilog, '(5X,A,F20.10)')  "oo_beta1    = ", this%oo_beta1
       write (ilog, '(5X,A,F20.10)')  "oh_A        = ", this%oh_A
       write (ilog, '(5X,A,F20.10)')  "oh_Q        = ", this%oh_Q
       write (ilog, '(5X,A,F20.10)')  "oh_alpha    = ", this%oh_alpha
       write (ilog, '(5X,A,F20.10)')  "oh_B1       = ", this%oh_B1
       write (ilog, '(5X,A,F20.10)')  "oh_beta1    = ", this%oh_beta1
       write (ilog, '(5X,A,F20.10)')  "oc_A        = ", this%oc_A
       write (ilog, '(5X,A,F20.10)')  "oc_Q        = ", this%oc_Q
       write (ilog, '(5X,A,F20.10)')  "oc_alpha    = ", this%oc_alpha
       write (ilog, '(5X,A,F20.10)')  "oc_B1       = ", this%oc_B1
       write (ilog, '(5X,A,F20.10)')  "oc_beta1    = ", this%oc_beta1

       call prlog("     Parameters for angular function:")
       write (ilog, '(5X,A,F20.10)')  "oo_gamma    = ", this%oo_gamma
       write (ilog, '(5X,A,F20.10)')  "oo_c        = ", this%oo_c
       write (ilog, '(5X,A,F20.10)')  "oo_d        = ", this%oo_d
       write (ilog, '(5X,A,F20.10)')  "oo_h        = ", this%oo_h
       write (ilog, '(5X,A,F20.10)')  "oh_gamma    = ", this%oh_gamma
       write (ilog, '(5X,A,F20.10)')  "oh_c        = ", this%oh_c
       write (ilog, '(5X,A,F20.10)')  "oh_d        = ", this%oh_d
       write (ilog, '(5X,A,F20.10)')  "oh_h        = ", this%oh_h
       write (ilog, '(5X,A,F20.10)')  "oc_gamma    = ", this%oc_gamma
       write (ilog, '(5X,A,F20.10)')  "oc_c        = ", this%oc_c
       write (ilog, '(5X,A,F20.10)')  "oc_d        = ", this%oc_d
       write (ilog, '(5X,A,F20.10)')  "oc_h        = ", this%oc_h

       call prlog("     Cutoff parameters:")
       write (ilog, '(5X,A,F20.10)')  "cc_in_r1    = ", this%cc_in_r1
       write (ilog, '(5X,A,F20.10)')  "cc_in_r2    = ", this%cc_in_r2
       write (ilog, '(5X,A,F20.10)')  "ch_in_r1    = ", this%ch_in_r1
       write (ilog, '(5X,A,F20.10)')  "ch_in_r2    = ", this%ch_in_r2
       write (ilog, '(5X,A,F20.10)')  "hh_in_r1    = ", this%hh_in_r1
       write (ilog, '(5X,A,F20.10)')  "hh_in_r2    = ", this%hh_in_r2
       write (ilog, '(5X,A,F20.10)')  "oo_in_r1    = ", this%oo_in_r1
       write (ilog, '(5X,A,F20.10)')  "oo_in_r2    = ", this%oo_in_r2
       write (ilog, '(5X,A,F20.10)')  "oh_in_r1    = ", this%oh_in_r1
       write (ilog, '(5X,A,F20.10)')  "oh_in_r2    = ", this%oh_in_r2
       write (ilog, '(5X,A,F20.10)')  "oc_in_r1    = ", this%oc_in_r1
       write (ilog, '(5X,A,F20.10)')  "oc_in_r2    = ", this%oc_in_r2

#ifdef SCREENING
       call prlog("     Outer cutoff parameters:")
       write (ilog, '(5X,A,F20.10)')  "cc_out_r1   = ", this%cc_out_r1
       write (ilog, '(5X,A,F20.10)')  "cc_out_r2   = ", this%cc_out_r2
       write (ilog, '(5X,A,F20.10)')  "ch_out_r1   = ", this%ch_out_r1
       write (ilog, '(5X,A,F20.10)')  "ch_out_r2   = ", this%ch_out_r2
       write (ilog, '(5X,A,F20.10)')  "hh_out_r1   = ", this%hh_out_r1
       write (ilog, '(5X,A,F20.10)')  "hh_out_r2   = ", this%hh_out_r2
       write (ilog, '(5X,A,F20.10)')  "oo_out_r1   = ", this%oo_out_r1
       write (ilog, '(5X,A,F20.10)')  "oo_out_r2   = ", this%oo_out_r2
       write (ilog, '(5X,A,F20.10)')  "oh_out_r1   = ", this%oh_out_r1
       write (ilog, '(5X,A,F20.10)')  "oh_out_r2   = ", this%oh_out_r2
       write (ilog, '(5X,A,F20.10)')  "oc_out_r1   = ", this%oc_out_r1
       write (ilog, '(5X,A,F20.10)')  "oc_out_r2   = ", this%oc_out_r2

       call prlog("     Neighbor/conjugation parameters:")
       write (ilog, '(5X,A,F20.10)')  "cc_nc_r1    = ", this%cc_nc_r1
       write (ilog, '(5X,A,F20.10)')  "cc_nc_r2    = ", this%cc_nc_r2
       write (ilog, '(5X,A,F20.10)')  "ch_nc_r1    = ", this%ch_nc_r1
       write (ilog, '(5X,A,F20.10)')  "ch_nc_r2    = ", this%ch_nc_r2
       write (ilog, '(5X,A,F20.10)')  "hh_nc_r1    = ", this%hh_nc_r1
       write (ilog, '(5X,A,F20.10)')  "hh_nc_r2    = ", this%hh_nc_r2
       write (ilog, '(5X,A,F20.10)')  "oo_nc_r1    = ", this%oo_nc_r1
       write (ilog, '(5X,A,F20.10)')  "oo_nc_r2    = ", this%oo_nc_r2
       write (ilog, '(5X,A,F20.10)')  "oh_nc_r1    = ", this%oh_nc_r1
       write (ilog, '(5X,A,F20.10)')  "oh_nc_r2    = ", this%oh_nc_r2
       write (ilog, '(5X,A,F20.10)')  "oc_nc_r1    = ", this%oc_nc_r1
       write (ilog, '(5X,A,F20.10)')  "oc_nc_r2    = ", this%oc_nc_r2

       call prlog("     Additional screening parameters:")
       write (ilog, '(5X,A,F20.10)')  "h_C_min     = ", this%h_Cmin
       write (ilog, '(5X,A,F20.10)')  "h_C_max     = ", this%h_Cmax
       write (ilog, '(5X,A,F20.10)')  "c_C_min     = ", this%c_Cmin
       write (ilog, '(5X,A,F20.10)')  "c_C_max     = ", this%c_Cmax
       write (ilog, '(5X,A,F20.10)')  "o_C_min     = ", this%o_Cmin
       write (ilog, '(5X,A,F20.10)')  "o_C_max     = ", this%o_Cmax
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
    this%Cmin(rebo2_H_)  = this%h_Cmin
    this%Cmax(rebo2_H_)  = this%h_Cmax
    this%Cmin(rebo2_C_)  = this%c_Cmin
    this%Cmax(rebo2_C_)  = this%c_Cmax
    this%Cmin(rebo2_O_)  = this%o_Cmin
    this%Cmax(rebo2_O_)  = this%o_Cmax
    this%dC              = this%Cmax-this%Cmin
    this%C_dr_cut        = this%Cmax**2/(4*(this%Cmax-1))
#endif

    !
    ! bond order constants.
    !

    this%conpe(rebo2_C_) = - 0.5_DP
    this%conpe(rebo2_H_) = - 0.5_DP
    this%conpe(rebo2_O_) = - 0.5_DP
    this%conan(rebo2_C_) = 0.5_DP * this%conpe(rebo2_C_)
    this%conan(rebo2_H_) = 0.5_DP * this%conpe(rebo2_H_)
    this%conan(rebo2_O_) = 0.5_DP * this%conpe(rebo2_O_)
    this%conpf(rebo2_C_) = this%conpe(rebo2_C_) - 1.0_DP
    this%conpf(rebo2_H_) = this%conpe(rebo2_H_) - 1.0_DP
    this%conpf(rebo2_O_) = this%conpe(rebo2_O_) - 1.0_DP

    !
    ! bond order penalty function constants
    !

#define H_ rebo2_H_
#define C_ rebo2_C_
#define O_ rebo2_O_
    this%lambda          = 0.0_DP

    this%lambda(H_,H_,H_) = this%HHH_lambda
    this%lambda(H_,C_,H_) = this%HCH_lambda
    this%lambda(H_,H_,C_) = this%HHC_lambda
    this%lambda(H_,C_,C_) = this%HCC_lambda
    this%lambda(H_,O_,H_) = this%HOH_lambda
    this%lambda(H_,H_,O_) = this%HHO_lambda
    this%lambda(H_,O_,O_) = this%HOO_lambda
    this%lambda(H_,C_,O_) = this%HCO_lambda
    this%lambda(H_,O_,C_) = this%HOC_lambda

    this%lambda(C_,H_,H_) = this%CHH_lambda
    this%lambda(C_,C_,H_) = this%CCH_lambda
    this%lambda(C_,H_,C_) = this%CHC_lambda
    this%lambda(C_,C_,C_) = this%CCC_lambda
    this%lambda(C_,O_,H_) = this%COH_lambda
    this%lambda(C_,H_,O_) = this%CHO_lambda
    this%lambda(C_,O_,O_) = this%COO_lambda
    this%lambda(C_,C_,O_) = this%CCO_lambda
    this%lambda(C_,O_,C_) = this%COC_lambda

    this%lambda(O_,H_,H_) = this%OHH_lambda
    this%lambda(O_,C_,H_) = this%OCH_lambda
    this%lambda(O_,H_,C_) = this%OHC_lambda
    this%lambda(O_,C_,C_) = this%OCC_lambda
    this%lambda(O_,O_,H_) = this%OOH_lambda
    this%lambda(O_,H_,O_) = this%OHO_lambda
    this%lambda(O_,O_,O_) = this%OOO_lambda
    this%lambda(O_,C_,O_) = this%OCO_lambda
    this%lambda(O_,O_,C_) = this%OOC_lambda

    this%m(H_,H_,H_) = this%HHH_m
    this%m(H_,C_,H_) = this%HCH_m
    this%m(H_,H_,C_) = this%HHC_m
    this%m(H_,C_,C_) = this%HCC_m
    this%m(H_,O_,H_) = this%HOH_m
    this%m(H_,H_,O_) = this%HHO_m
    this%m(H_,O_,O_) = this%HOO_m
    this%m(H_,C_,O_) = this%HCO_m
    this%m(H_,O_,C_) = this%HOC_m

    this%m(C_,H_,H_) = this%CHH_m
    this%m(C_,C_,H_) = this%CCH_m
    this%m(C_,H_,C_) = this%CHC_m
    this%m(C_,C_,C_) = this%CCC_m
    this%m(C_,O_,H_) = this%COH_m
    this%m(C_,H_,O_) = this%CHO_m
    this%m(C_,O_,O_) = this%COO_m
    this%m(C_,C_,O_) = this%CCO_m
    this%m(C_,O_,C_) = this%COC_m

    this%m(O_,H_,H_) = this%OHH_m
    this%m(O_,C_,H_) = this%OCH_m
    this%m(O_,H_,C_) = this%OHC_m
    this%m(O_,C_,C_) = this%OCC_m
    this%m(O_,O_,H_) = this%OOH_m
    this%m(O_,H_,O_) = this%OHO_m
    this%m(O_,O_,O_) = this%OOO_m
    this%m(O_,C_,O_) = this%OCO_m
    this%m(O_,O_,C_) = this%OOC_m

    this%re      = 1.0_DP
    this%re(H_H) = this%HH_re
    this%re(C_H) = this%CH_re
    this%re(O_H) = this%OH_re
    this%re(C_C) = this%CC_re

    do i = 1, 5, 2
       do j = 1, 5, 2
          do k = 1, 5, 2
             call prlog("     lambda(" // rebo2_el_strs(i) // ", " // &
                  rebo2_el_strs(j) // ", " // rebo2_el_strs(k) // ") = " // &
                  this%lambda(i,j,k))
          enddo
       enddo
    enddo

    do i = 1, 5, 2
       do j = 1, 5, 2
          do k = 1, 5, 2
             call prlog("     m(" // rebo2_el_strs(i) // ", " // &
                  rebo2_el_strs(j) // ", " // rebo2_el_strs(k) // ") = " // &
                  this%m(i,j,k))
          enddo
       enddo
    enddo

    do j = 1, 5, 2
       do k = 1, 5, 2
          call prlog("     re(" // rebo2_el_strs(j) // ", " // &
               rebo2_el_strs(k) // ") = " // this%re(Z2pair(this, j, k)))
       enddo
    enddo

#undef H_
#undef C_
#undef O_

    this%bo_override = -1.0_DP
    this%bo_override(H_H) = this%hh_bo
    this%bo_override(C_C) = this%cc_bo
    this%bo_override(C_H) = this%ch_bo

!   
!   Need to add in the Silicon penalty functions - MTK

    !
    ! cutoff constants.
    !

    this%cut_in_l(:)     = 0.0_DP
    this%cut_in_l(C_C)   = this%cc_in_r1
    this%cut_in_l(C_H)   = this%ch_in_r1
    this%cut_in_l(H_H)   = this%hh_in_r1
    this%cut_in_l(O_O)   = this%oo_in_r1
    this%cut_in_l(O_H)   = this%oh_in_r1
    this%cut_in_l(C_O)   = this%oc_in_r1
    this%cut_in_l(O_C)   = this%oc_in_r1

    this%cut_in_h(:)     = 0.0_DP
    this%cut_in_h(C_C)   = this%cc_in_r2
    this%cut_in_h(C_H)   = this%ch_in_r2
    this%cut_in_h(H_H)   = this%hh_in_r2
    this%cut_in_h(O_O)   = this%oo_in_r2
    this%cut_in_h(O_H)   = this%oh_in_r2
    this%cut_in_h(C_O)   = this%oc_in_r2
    this%cut_in_h(O_C)   = this%oc_in_r2

    this%cut_in_h2(:)    = 0.0_DP
    this%cut_in_h2(C_C)  = this%cc_in_r2 ** 2
    this%cut_in_h2(C_H)  = this%ch_in_r2 ** 2
    this%cut_in_h2(H_H)  = this%hh_in_r2 ** 2
    this%cut_in_h2(O_O)  = this%oo_in_r2 ** 2
    this%cut_in_h2(O_H)  = this%oh_in_r2 ** 2
    this%cut_in_h2(C_O)  = this%oc_in_r2 ** 2
    this%cut_in_h2(O_C)  = this%oc_in_r2 ** 2

    this%cut_in_m(:)     = 0.0_DP
    this%cut_in_m(C_C)   = (this%cc_in_r1+this%cc_in_r2)/2
    this%cut_in_m(C_H)   = (this%ch_in_r1+this%ch_in_r2)/2
    this%cut_in_m(H_H)   = (this%hh_in_r1+this%hh_in_r2)/2
    this%cut_in_m(O_O)   = (this%oo_in_r1+this%oo_in_r2)/2
    this%cut_in_m(O_H)   = (this%oh_in_r1+this%oh_in_r2)/2
    this%cut_in_m(C_O)   = (this%oc_in_r1+this%oc_in_r2)/2
    this%cut_in_m(O_C)   = (this%oc_in_r1+this%oc_in_r2)/2

#ifdef SCREENING
    this%cut_out_l(:)    = 0.0_DP
    this%cut_out_l(C_C)  = this%cc_out_r1
    this%cut_out_l(C_H)  = this%ch_out_r1
    this%cut_out_l(H_H)  = this%hh_out_r1
    this%cut_out_l(O_O)  = this%oo_out_r1
    this%cut_out_l(O_H)  = this%oh_out_r1
    this%cut_out_l(C_O)  = this%oc_out_r1
    this%cut_out_l(O_C)  = this%oc_out_r1

    this%cut_out_h(:)    = 0.0_DP
    this%cut_out_h(C_C)  = this%cc_out_r2
    this%cut_out_h(C_H)  = this%ch_out_r2
    this%cut_out_h(H_H)  = this%hh_out_r2
    this%cut_out_h(O_O)  = this%oo_out_r2
    this%cut_out_h(O_H)  = this%oh_out_r2
    this%cut_out_h(C_O)  = this%oc_out_r2
    this%cut_out_h(O_C)  = this%oc_out_r2

    this%cut_out_h2(:)   = 0.0_DP
    this%cut_out_h2(C_C) = this%cc_out_r2 ** 2
    this%cut_out_h2(C_H) = this%ch_out_r2 ** 2
    this%cut_out_h2(H_H) = this%hh_out_r2 ** 2
    this%cut_out_h2(O_O) = this%oo_out_r2 ** 2
    this%cut_out_h2(O_H) = this%oh_out_r2 ** 2
    this%cut_out_h2(C_O) = this%oc_out_r2 ** 2
    this%cut_out_h2(O_C) = this%oc_out_r2 ** 2

    this%cut_out_m(:)    = 0.0_DP
    this%cut_out_m(C_C)  = (this%cc_out_r1+this%cc_out_r2)/2
    this%cut_out_m(C_H)  = (this%ch_out_r1+this%ch_out_r2)/2
    this%cut_out_m(H_H)  = (this%hh_out_r1+this%hh_out_r2)/2
    this%cut_out_m(O_O)  = (this%oo_out_r1+this%oo_out_r2)/2
    this%cut_out_m(O_H)  = (this%oh_out_r1+this%oh_out_r2)/2
    this%cut_out_m(C_O)  = (this%oc_out_r1+this%oc_out_r2)/2
    this%cut_out_m(O_C)  = (this%oc_out_r1+this%oc_out_r2)/2

    this%cut_bo_l(:)     = 0.0
    this%cut_bo_l(C_C)   = this%cc_bo_r1
    this%cut_bo_l(C_H)   = this%ch_bo_r1
    this%cut_bo_l(H_H)   = this%hh_bo_r1
    this%cut_bo_l(O_O)   = this%oo_bo_r1
    this%cut_bo_l(O_H)   = this%oh_bo_r1
    this%cut_bo_l(C_O)   = this%oc_bo_r1
    this%cut_bo_l(O_C)   = this%oc_bo_r1

    this%cut_bo_h(:)     = 0.0
    this%cut_bo_h(C_C)   = this%cc_bo_r2
    this%cut_bo_h(C_H)   = this%ch_bo_r2
    this%cut_bo_h(H_H)   = this%hh_bo_r2
    this%cut_bo_h(O_O)   = this%oo_bo_r2
    this%cut_bo_h(O_H)   = this%oh_bo_r2
    this%cut_bo_h(C_O)   = this%oc_bo_r2
    this%cut_bo_h(O_C)   = this%oc_bo_r2

    this%cut_bo_h2(:)    = 0.0
    this%cut_bo_h2(C_C)  = this%cc_bo_r2 ** 2
    this%cut_bo_h2(C_H)  = this%ch_bo_r2 ** 2
    this%cut_bo_h2(H_H)  = this%hh_bo_r2 ** 2
    this%cut_bo_h2(O_O)  = this%oo_bo_r2 ** 2
    this%cut_bo_h2(O_H)  = this%oh_bo_r2 ** 2
    this%cut_bo_h2(C_O)  = this%oc_bo_r2 ** 2
    this%cut_bo_h2(O_C)  = this%oc_bo_r2 ** 2

    this%cut_bo_m(:)     = 0.0
    this%cut_bo_m(C_C)   = (this%cc_bo_r1+this%cc_bo_r2)/2
    this%cut_bo_m(C_H)   = (this%ch_bo_r1+this%ch_bo_r2)/2
    this%cut_bo_m(H_H)   = (this%hh_bo_r1+this%hh_bo_r2)/2
    this%cut_bo_m(O_O)   = (this%oo_bo_r1+this%oo_bo_r2)/2
    this%cut_bo_m(O_H)   = (this%oh_bo_r1+this%oh_bo_r2)/2
    this%cut_bo_m(C_O)   = (this%oc_bo_r1+this%oc_bo_r2)/2
    this%cut_bo_m(O_C)   = (this%oc_bo_r1+this%oc_bo_r2)/2

#ifdef NUM_NEIGHBORS
    this%cut_nc_l(:)    = 0.0_DP
    this%cut_nc_l(C_C)  = this%cc_nc_r1
    this%cut_nc_l(C_H)  = this%ch_nc_r1
    this%cut_nc_l(H_H)  = this%hh_nc_r1
    this%cut_nc_l(O_O)  = this%oo_nc_r1
    this%cut_nc_l(O_H)  = this%oh_nc_r1
    this%cut_nc_l(C_O)  = this%oc_nc_r1
    this%cut_nc_l(O_C)  = this%oc_nc_r1

    this%cut_nc_h(:)    = 0.0_DP
    this%cut_nc_h(C_C)  = this%cc_nc_r2
    this%cut_nc_h(C_H)  = this%ch_nc_r2
    this%cut_nc_h(H_H)  = this%hh_nc_r2
    this%cut_nc_h(O_O)  = this%oo_nc_r2
    this%cut_nc_h(O_H)  = this%oh_nc_r2
    this%cut_nc_h(C_O)  = this%oc_nc_r2
    this%cut_nc_h(O_C)  = this%oc_nc_r2

    this%cut_nc_h2(:)   = 0.0_DP
    this%cut_nc_h2(C_C) = this%cc_nc_r2 ** 2
    this%cut_nc_h2(C_H) = this%ch_nc_r2 ** 2
    this%cut_nc_h2(H_H) = this%hh_nc_r2 ** 2
    this%cut_nc_h2(O_O) = this%oo_nc_r2 ** 2
    this%cut_nc_h2(O_H) = this%oh_nc_r2 ** 2
    this%cut_nc_h2(C_O) = this%oc_nc_r2 ** 2
    this%cut_nc_h2(O_C) = this%oc_nc_r2 ** 2

    this%cut_nc_m(:)    = 0.0_DP
    this%cut_nc_m(C_C)  = (this%cc_nc_r1+this%cc_nc_r2)/2
    this%cut_nc_m(C_H)  = (this%ch_nc_r1+this%ch_nc_r2)/2
    this%cut_nc_m(H_H)  = (this%hh_nc_r1+this%hh_nc_r2)/2
    this%cut_nc_m(O_O)  = (this%oo_nc_r1+this%oo_nc_r2)/2
    this%cut_nc_m(O_H)  = (this%oh_nc_r1+this%oh_nc_r2)/2
    this%cut_nc_m(C_O)  = (this%oc_nc_r1+this%oc_nc_r2)/2
    this%cut_nc_m(O_C)  = (this%oc_nc_r1+this%oc_nc_r2)/2

    do i = 1, 10
       this%max_cut_sq(i) = maxval( (/ this%cut_in_h2(i), this%cut_out_h2(i), this%cut_bo_h2(i), this%cut_nc_h2(i) /) )
    enddo
#else
    do i = 1, 10
       this%max_cut_sq(i) = maxval( (/ this%cut_in_h2(i), this%cut_out_h2(i), this%cut_bo_h2(i) /) )
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
    call prlog("     O-O cut-off = " // sqrt(this%max_cut_sq(O_O)))
    call prlog("     O-H cut-off = " // sqrt(this%max_cut_sq(O_H)))
    call prlog("     O-C cut-off = " // sqrt(this%max_cut_sq(O_C)))

    !
    ! Generate the coefficients for
    ! the bi- and tri- cubic interpolation functions.
    !

    call rebo2coh_db_make_cc_g_spline(this)

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
    call init_f(this%Foc, N_NI_NJ_NCONJ, &
         in_Foc, in_dFocdi, in_dFocdj, in_dFocdk,&
         error=error)
    PASS_ERROR(error)
    call prlog("     Foc:")
    call table4d_prlog(this%Foc, indent=5)
    call init_f(this%Foh, N_NI_NJ_NCONJ, &
         in_Foh, in_dFohdi, in_dFohdj, in_dFohdk,&
         error=error)
    PASS_ERROR(error)
    call prlog("     Foh:")
    call table4d_prlog(this%Foh, indent=5)
    call init_f(this%Foo, N_NI_NJ_NCONJ, &
         in_Foo, in_dFoodi, in_dFoodj, &
         in_dFoodk, error=error)
    PASS_ERROR(error)
    call prlog("     Foo:")
    call table4d_prlog(this%Foo, indent=5)

    call init(this%Pcc, N_NHC_NO, &
         in_Pcc, in_dPccdi, in_dPccdj, in_dPccdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pcc:")
    call table3d_prlog(this%Pcc, indent=5)
    call init(this%Pch, N_NHC_NO, &
         in_Pch, in_dPchdi, in_dPchdj, in_dPchdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pch:")
    call table3d_prlog(this%Pch, indent=5)
    call init(this%Phh, N_NHC_NO, &
         in_Phh, in_dPhhdi, in_dPhhdj, in_dPhhdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Phh:")
    call table3d_prlog(this%Phh, indent=5)
    call init(this%Poc, N_NHC_NO, &
         in_Poc, in_dPocdi, in_dPocdj, in_dPocdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Poc:")
    call table3d_prlog(this%Poc, indent=5)
    call init(this%Pco, N_NHC_NO, &
         in_Pco, in_dPcodi, in_dPcodj, in_dPcodk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pco:")
    call table3d_prlog(this%Pco, indent=5)
    call init(this%Poh, N_NHC_NO, &
         in_Poh, in_dPohdi, in_dPohdj, in_dPohdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Poh:")
    call table3d_prlog(this%Poh, indent=5)
    call init(this%Pho, N_NHC_NO, &
         in_Pho, in_dPhodi, in_dPhodj, in_dPhodk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Pho:")
    call table3d_prlog(this%Pho, indent=5)
    call init(this%Poo, N_NHC_NO, &
         in_Poo, in_dPoodi, in_dPoodj, in_dPoodk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Poo:")
    call table3d_prlog(this%Poo, indent=5)

    call init(this%Tcc, N_NI_NJ_NCONJ, &
         in_Tcc, in_dTccdi, in_dTccdj, in_dTccdk, &
         error=error)
    PASS_ERROR(error)
    call prlog("     Tcc:")
    call table3d_prlog(this%Tcc, indent=5)


    !
    ! Make splines for attractive, repulsive functions
    !

    call rebo2coh_db_make_splines(this)

    call prlog

  endsubroutine rebo2coh_db_init_with_parameters


  !>
  !! Free all resources
  !<
  subroutine rebo2coh_db_del(this)
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
       deallocate(this%cutfcnbo)
       deallocate(this%sneb_seed)
       deallocate(this%sneb_last)
       deallocate(this%sneb)
       deallocate(this%sbnd)
       deallocate(this%sfacbo)
       deallocate(this%sfacnc)
       deallocate(this%cutdrik)
       deallocate(this%cutdrjk)
       deallocate(this%cutdrboik)
       deallocate(this%cutdrbojk)
#endif

       this%neighbor_list_allocated = .false.
    endif

    call del(this%Fcc)
    call del(this%Fch)
    call del(this%Fhh)
    call del(this%Foc)
    call del(this%Foh)
    call del(this%Foo)
    call del(this%Pcc)
    call del(this%Pch)
    call del(this%Phh)
    call del(this%Poc)
    call del(this%Pco)
    call del(this%Poh)
    call del(this%Pho)
    call del(this%Poo)
    call del(this%Tcc)

    call del(this%spl_VA(C_C))
    call del(this%spl_VA(C_H))
    call del(this%spl_VA(H_H))
    call del(this%spl_VA(C_O))
    call del(this%spl_VA(O_C))
    call del(this%spl_VA(O_H))
    call del(this%spl_VA(O_O))

    call del(this%spl_VR(C_C))
    call del(this%spl_VR(C_H))
    call del(this%spl_VR(H_H))
    call del(this%spl_VR(C_O))
    call del(this%spl_VR(O_C))
    call del(this%spl_VR(O_H))
    call del(this%spl_VR(O_O))

    call del(this%spl_fCin(C_C))
    call del(this%spl_fCin(C_H))
    call del(this%spl_fCin(H_H))
    call del(this%spl_fCin(C_O))
    call del(this%spl_fCin(O_C))
    call del(this%spl_fCin(O_H))
    call del(this%spl_fCin(O_O))

#ifdef SCREENING
    call del(this%spl_fCout(C_C))
    call del(this%spl_fCout(C_H))
    call del(this%spl_fCout(H_H))
    call del(this%spl_fCout(C_O))
    call del(this%spl_fCout(O_C))
    call del(this%spl_fCout(O_H))
    call del(this%spl_fCout(O_O))

    call del(this%spl_fCbo(C_C))
    call del(this%spl_fCbo(C_H))
    call del(this%spl_fCbo(H_H))
    call del(this%spl_fCbo(C_O))
    call del(this%spl_fCbo(O_C))
    call del(this%spl_fCbo(O_H))
    call del(this%spl_fCbo(O_O))

#ifdef NUM_NEIGHBORS
    call del(this%spl_fCnc(C_C))
    call del(this%spl_fCnc(C_H))
    call del(this%spl_fCnc(H_H))
    call del(this%spl_fCnc(C_O))
    call del(this%spl_fCnc(O_C))
    call del(this%spl_fCnc(O_H))
    call del(this%spl_fCnc(O_O))
#endif

#endif

  endsubroutine rebo2coh_db_del


  !>
  !! Compute the coefficients for the g(cos(theta)) spline
  !! for C-C interaction
  !<
  subroutine rebo2coh_db_make_cc_g_spline(this)
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
       write (*, '(A,I5)')  "[rebo2coh_make_cc_g_spline] dgesv failed. info = ", i
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
       write (*, '(A,I5)')  "[rebo2coh_make_cc_g_spline] dgesv failed. info = ", i
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
          write (*, '(A,I5)')  "[rebo2coh_make_cc_g_spline] dgesv failed. info = ", i
          stop
       endif

       this%cc_g1_coeff%c(:, 1+k) = B(:)
       this%cc_g2_coeff%c(:, 1+k) = B(:)

    enddo

  endsubroutine rebo2coh_db_make_cc_g_spline



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


  function oo_VA(dr, oo_B1, oo_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: oo_B1
    real(DP), intent(in)  :: oo_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = oo_B1*exp(-oo_beta1*dr)

    val  = - exp1

  endfunction oo_VA

  function oo_VR(dr, oo_A, oo_Q, oo_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: oo_A
    real(DP), intent(in)  :: oo_Q
    real(DP), intent(in)  :: oo_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = oo_A*exp(-oo_alpha*dr)
    hlp1 = 1+oo_Q/dr

    val  = hlp1*exp1

  endfunction oo_VR


  function oh_VA(dr, oh_B1, oh_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: oh_B1
    real(DP), intent(in)  :: oh_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = oh_B1*exp(-oh_beta1*dr)

    val  = - exp1

  endfunction oh_VA


  function oh_VR(dr, oh_A, oh_Q, oh_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: oh_A
    real(DP), intent(in)  :: oh_Q
    real(DP), intent(in)  :: oh_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = oh_A*exp(-oh_alpha*dr)
    hlp1 = 1+oh_Q/dr

    val  = hlp1*exp1

  endfunction oh_VR

 function oc_VA(dr, oc_B1, oc_beta1) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: oc_B1
    real(DP), intent(in)  :: oc_beta1
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1

    ! ---

    exp1 = oc_B1*exp(-oc_beta1*dr)

    val  = - exp1

  endfunction oc_VA


  function oc_VR(dr, oc_A, oc_Q, oc_alpha) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: oc_A
    real(DP), intent(in)  :: oc_Q
    real(DP), intent(in)  :: oc_alpha
    real(DP)              :: val

    ! ---

    real(DP)  :: exp1, hlp1

    ! ---

    exp1 = oc_A*exp(-oc_alpha*dr)
    hlp1 = 1+oc_Q/dr

    val  = hlp1*exp1

  endfunction oc_VR



#ifdef EXP_CUT

  function cutoff_f(dr, l, h, m) result(val)
    implicit none
    
    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: l
    real(DP), intent(in)  :: h
    real(DP), intent(in)  :: m
    real(DP)              :: val

    ! ---

!    if (dr < m) then 
!       val = 2**(-(2*(dr-l)/(h-l))**cutoff_k)
!    else
!       val = 1-2**(-(2*(h-dr)/(h-l))**cutoff_k)
!    endif

    val = exp(-(2*(dr-l)/(h-l))**3)

  endfunction cutoff_f

#else

  function cutoff_f(dr, l, h, m) result(val)
    implicit none

    real(DP), intent(in)  :: dr
    real(DP), intent(in)  :: l
    real(DP), intent(in)  :: h
    real(DP), intent(in)  :: m
    real(DP)              :: val

    ! ---

    real(DP)  :: fca

    ! ---

    fca = pi / ( h - l )

    val   = 0.5 *  ( 1.0 + cos( fca*( dr-l ) ) )

  endfunction cutoff_f

#endif


  !>
  !! Make splines for attractive, repulsive functions
  !<
  subroutine rebo2coh_db_make_splines(this)
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
         this%spl_VA(O_O), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oo_out_r2, &
#else
         this%oo_in_r2, &
#endif
         oo_VA, this%oo_B1, this%oo_beta1)
    call init( &
         this%spl_VA(O_H), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oh_out_r2, &
#else
         this%oh_in_r2, &
#endif
         oh_VA, this%oh_B1, this%oh_beta1)
    call init( &
         this%spl_VA(C_O), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oc_out_r2, &
#else
         this%oc_in_r2, &
#endif
         oc_VA, this%oc_B1, this%oc_beta1)
    call init( &
         this%spl_VA(O_C), &
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oc_out_r2, &
#else
         this%oc_in_r2, &
#endif
         oc_VA, this%oc_B1, this%oc_beta1)

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
         this%spl_VR(O_O), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oo_out_r2, & 
#else
         this%oo_in_r2, &
#endif
         oo_VR, this%oo_A,this%oo_Q, this%oo_alpha)
    call init( & 
         this%spl_VR(O_H), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oh_out_r2, &
#else
         this%oh_in_r2, &
#endif
         oh_VR, this%oh_A, this%oh_Q, this%oh_alpha)
    call init(& 
         this%spl_VR(C_O), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oc_out_r2, & 
#else
         this%oc_in_r2, &
#endif
         oc_VR, this%oc_A, this%oc_Q, this%oc_alpha)
    call init(& 
         this%spl_VR(O_C), & 
         this%spl_n, this%spl_x0, &
#ifdef SCREENING
         this%oc_out_r2, & 
#else
         this%oc_in_r2, &
#endif
         oc_VR, this%oc_A, this%oc_Q, this%oc_alpha)

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
         this%spl_fCin(O_O), & 
         this%spl_n, this%oo_in_r1, this%oo_in_r2, & 
         cutoff_f, this%cut_in_l(O_O), this%cut_in_h(O_O), &
         this%cut_in_m(O_O))
    call init( &
         this%spl_fCin(O_H), &
         this%spl_n, this%oh_in_r1, this%oh_in_r2, &
         cutoff_f, this%cut_in_l(O_H), this%cut_in_h(O_H), &
         this%cut_in_m(O_H))
    call init( &
         this%spl_fCin(C_O), &
         this%spl_n, this%oc_in_r1, this%oc_in_r2, &
         cutoff_f, this%cut_in_l(C_O), this%cut_in_h(C_O), &
         this%cut_in_m(C_O))
    call init( &
         this%spl_fCin(O_C), &
         this%spl_n, this%oc_in_r1, this%oc_in_r2, &
         cutoff_f, this%cut_in_l(O_C), this%cut_in_h(O_C), &
         this%cut_in_m(O_C))

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
         this%spl_fCout(O_O), & 
         this%spl_n, this%oo_out_r1, this%oo_out_r2, & 
         cutoff_f, this%cut_out_l(O_O), this%cut_out_h(O_O), &
         this%cut_out_m(O_O))
    call init( &
         this%spl_fCout(O_H), &
         this%spl_n, this%oh_out_r1, this%oh_out_r2, &
         cutoff_f, this%cut_out_l(O_H), this%cut_out_h(O_H), &
         this%cut_out_m(O_H))
    call init( &
         this%spl_fCout(C_O), &
         this%spl_n, this%oc_out_r1, this%oc_out_r2, &
         cutoff_f, this%cut_out_l(C_O), this%cut_out_h(C_O), &
         this%cut_out_m(C_O))
    call init( &
         this%spl_fCout(O_C), &
         this%spl_n, this%oc_out_r1, this%oc_out_r2, &
         cutoff_f, this%cut_out_l(O_C), this%cut_out_h(O_C), &
         this%cut_out_m(O_C))


    !
    ! Bond-order cut-off
    !

    call init( &
         this%spl_fCbo(C_C), &
         this%spl_n, this%cc_bo_r1, this%cc_bo_r2, &
         cutoff_f, this%cut_bo_l(C_C), this%cut_bo_h(C_C), this%cut_bo_m(C_C))
    call init( &
         this%spl_fCbo(C_H), &
         this%spl_n, this%ch_bo_r1, this%ch_bo_r2, &
         cutoff_f, this%cut_bo_l(C_H), this%cut_bo_h(C_H), this%cut_bo_m(C_H))
    call init( &
         this%spl_fCbo(H_H), &
         this%spl_n, this%hh_bo_r1, this%hh_bo_r2, &
         cutoff_f, this%cut_bo_l(H_H), this%cut_bo_h(H_H), this%cut_bo_m(H_H))
    call init( &
         this%spl_fCbo(C_O), &
         this%spl_n, this%oc_bo_r1, this%oc_bo_r2, &
         cutoff_f, this%cut_bo_l(C_O), this%cut_bo_h(C_O), this%cut_bo_m(C_O))
    call init( &
         this%spl_fCbo(O_C), &
         this%spl_n, this%oc_bo_r1, this%oc_bo_r2, &
         cutoff_f, this%cut_bo_l(O_C), this%cut_bo_h(O_C), this%cut_bo_m(O_C))
    call init( &
         this%spl_fCbo(O_H), &
         this%spl_n, this%oh_bo_r1, this%oh_bo_r2, &
         cutoff_f, this%cut_bo_l(O_H), this%cut_bo_h(O_H), this%cut_bo_m(O_H))
    call init( &
         this%spl_fCbo(O_O), &
         this%spl_n, this%oo_bo_r1, this%oo_bo_r2, &
         cutoff_f, this%cut_bo_l(O_O), this%cut_bo_h(O_O), this%cut_bo_m(O_O))

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
         this%spl_fCnc(O_O), & 
         this%spl_n, this%oo_nc_r1, this%oo_nc_r2, & 
         cutoff_f, this%cut_nc_l(O_O), this%cut_nc_h(O_O), &
         this%cut_nc_m(O_O))
    call init( &
         this%spl_fCnc(O_H), &
         this%spl_n, this%oh_nc_r1, this%oh_nc_r2, &
         cutoff_f, this%cut_nc_l(O_H), this%cut_nc_h(O_H), &
         this%cut_nc_m(O_H))
    call init( &
         this%spl_fCnc(C_O), &
         this%spl_n, this%oc_nc_r1, this%oc_nc_r2, &
         cutoff_f, this%cut_nc_l(C_O), this%cut_nc_h(C_O), &
         this%cut_nc_m(C_O))
    call init( &
         this%spl_fCnc(O_C), &
         this%spl_n, this%oc_nc_r1, this%oc_nc_r2, &
         cutoff_f, this%cut_nc_l(O_C), this%cut_nc_h(O_C), &
         this%cut_nc_m(O_C))

#endif

#endif

  endsubroutine rebo2coh_db_make_splines



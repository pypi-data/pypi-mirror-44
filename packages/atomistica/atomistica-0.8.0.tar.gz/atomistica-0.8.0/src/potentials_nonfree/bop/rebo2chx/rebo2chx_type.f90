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
! Declaration of the datatype which contains the materials parameters
! and local neighbor lists.
!

  !
  ! Atom types
  !

  !>
  !! Maximum internal element number - Note this not the number of elements
  !! since some element numbers are unused. See rebo2_*_ element definitions
  !! below.
  !! REFACTOR: Fix this, make element numbers continuous.
  !<
  integer, parameter       :: rebo2_MAX_ELS = 5

  !>
  !! Maximum internal pair number = 10
  !<
  integer, parameter       :: rebo2_MAX_PAIRS = 10

  integer, parameter       :: rebo2_C_  = 1
  integer, parameter       :: rebo2_H_  = 3
  integer, parameter       :: rebo2_O_  = 5

  character(2), parameter  :: rebo2_el_strs(rebo2_MAX_ELS) = &
       (/ "C ", "  ", "H ", "  ", "Fe" /)

  integer, parameter       :: possible_elements(3) = &
       (/ rebo2_C_, rebo2_H_, rebo2_O_ /)

  integer, parameter       :: C_C = 1
  integer, parameter       :: C_H = 3
  integer, parameter       :: H_H = 6
  integer, parameter       :: O_O = 10
  integer, parameter       :: O_C = 5
  integer, parameter       :: C_O = 7
  integer, parameter       :: O_H = 8

  integer, parameter       :: H_ = 1
  integer, parameter       :: C_ = 6
  integer, parameter       :: O_ = 26

  type g_coeff_t
     real(DP)  :: c(6, 3)
  endtype g_coeff_t

  public :: BOP_TYPE
  type BOP_TYPE

     character(MAX_EL_STR)  :: elements = "C,H,Fe"
     integer                :: els

     integer, allocatable   :: internal_el(:)

     !
     ! === THIS SECTION CONTAINS PARAMETERS ===
     !

#ifdef SCREENING

     !
     ! Screening parameters
     !

     real(DP)             :: H_Cmin = 1.0_DP
     real(DP)             :: H_Cmax = 2.0_DP
     real(DP)             :: C_Cmin = 1.0_DP
     real(DP)             :: C_Cmax = 2.0_DP
     real(DP)             :: O_Cmin = 1.0_DP
     real(DP)             :: O_Cmax = 3.0_DP

     real(DP)             :: Cmin(rebo2_MAX_ELS)  = 1.00_DP
     real(DP)             :: Cmax(rebo2_MAX_ELS)  = 3.00_DP

     real(DP)             :: screening_threshold  = log(1d-6)
     real(DP)             :: dot_threshold        = 1e-10

#endif

     !
     ! ============ C-C interaction ============
     !

     !
     ! Attractive function (C-C)
     ! [ Table 2 from Brenner2002 ]
     !

     real(DP)             :: CC_B1     = 12388.79197798_DP
     real(DP)             :: CC_B2     = 17.56740646509_DP
     real(DP)             :: CC_B3     = 30.71493208065_DP
     real(DP)             :: CC_beta1  = 4.7204523127_DP
     real(DP)             :: CC_beta2  = 1.4332132499_DP
     real(DP)             :: CC_beta3  = 1.3826912506_DP

     !
     ! Repulsive function (C-C)
     ! [ Table 2 from Brenner2002 ]
     !

     real(DP)             :: CC_Q     = 0.3134602960833_DP
     real(DP)             :: CC_A     = 10953.544162170_DP
     real(DP)             :: CC_alpha = 4.7465390606595_DP
     
     !
     ! g(cos(theta))  (C-C)
     ! [ Table 3 from Brenner2002 ]
     !
     
     !                                            ----------|----------|----------|----------|----------|----------|
     real(DP)             :: CC_g_theta(6)   = (/    -1.0_DP, -1.0_DP/2, -1.0_DP/3,    0.0_DP,  1.0_DP/2,    1.0_DP  /)
     real(DP)             :: CC_g_g1(6)      = (/      -0.01,   0.05280,   0.09733,   0.37545,    2.0014,       8.0  /)
     real(DP)             :: CC_g_dg1(6)     = (/    0.10400,   0.17000,   0.40000,       0.0,       0.0,       0.0  /)
     real(DP)             :: CC_g_d2g1(6)    = (/    0.00000,   0.37000,   1.98000,       0.0,       0.0,       0.0  /)
     real(DP)             :: CC_g_g2(6)      = (/        0.0,       0.0,   0.09733,  0.271856,  0.416335,       1.0  /)

     !
     ! ============ C-H interaction ============
     !

     !
     ! Attractive function (C-H)
     ! [ Table 7 from Brenner2002 ]
     !

     real(DP)             :: CH_B1     = 32.3551866587_DP
     real(DP)             :: CH_beta1  = 1.43445805925_DP

     !
     ! Repulsive function (C-H)
     ! [ Table 7 from Brenner2002 ]
     !

     real(DP)             :: CH_Q     = 0.340775728_DP
     real(DP)             :: CH_A     = 149.94098723_DP
     real(DP)             :: CH_alpha = 4.10254983_DP

     !
     ! ============ H-H interaction ============
     !

     !
     ! Attractive function (H-H)
     ! [ Table 6 from Brenner2002 ]
     !

     real(DP)             :: HH_B1     = 29.632593_DP
     real(DP)             :: HH_beta1  = 1.71589217_DP

     !
     ! Repulsive function (H-H)
     ! [ Table 6 from Brenner2002 ]
     !

     real(DP)             :: HH_Q     = 0.370471487045_DP
     real(DP)             :: HH_A     = 32.817355747_DP
     real(DP)             :: HH_alpha = 3.536298648_DP

     !
     ! g(cos(theta))  (H-H)
     ! [ Table 6 from Brenner2002 ]
     !

     !                                            ----------------|----------------|----------------|----------------|----------------|----------------|
     !  real(DP)             :: HH_g_theta(6)   = (/          -1.0_DP, -0.866025403_DP,       -1.0_DP/2,          0.0_DP,        1.0_DP/2,          1.0_DP  /)
     !  real(DP)             :: HH_g_g(6)       = (/        11.235870,       12.164186,       16.811574,       19.065124,       19.704059,       19.991787  /)
     
     ! This is directly from the MD code of Brenner's group...
     ! ...there is no way to get this from the paper.

     real(DP)  :: SPGH(6,3) = &
          reshape( &
          (/ 270.467795364007301_DP ,1549.701314596994564_DP  &
          ,3781.927258631323866_DP,4582.337619544424228_DP,2721.538161662818368_DP, &
          630.658598136730774_DP,16.956325544514659_DP,-21.059084522755980_DP, &
          -102.394184748124742_DP,-210.527926707779059_DP,-229.759473570467513_DP, &
          -94.968528666251945_DP,19.065031149937783_DP,2.017732531534021_DP, &
          -2.566444502991983_DP,3.291353893907436_DP,-2.653536801884563_DP, &
          0.837650930130006_DP /), &
          (/ 6, 3 /) )
     integer  :: IGH(25) = &
          (/ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, &
             2, 2, 2, 2, &
             1, 1, 1 /)

!     integer   :: IGH(25) = &
!          (/18*3,4*2,3*1/)

!     DATA SPGH / 270.467795364007301,1549.701314596994564  &
!          ,3781.927258631323866,4582.337619544424228,2721.538161662818368, &
!          630.658598136730774,16.956325544514659,-21.059084522755980, &
!          -102.394184748124742,-210.527926707779059,-229.759473570467513, &
!          -94.968528666251945,19.065031149937783,2.017732531534021, &
!          -2.566444502991983,3.291353893907436,-2.653536801884563, &
!          0.837650930130006/

!     DATA IGH/18*3,4*2,3*1/

     !  real(DP)             :: HH_g_coeff(6)

     !
     ! Attractive function (Fe-Fe)
     ! [ Henriksson, table 3 ]
     !

     real(DP)           :: OO_B1      = 67.864772279855899_DP
     real(DP)           :: OO_beta1   = 1.3763540363137268_DP

     !
     ! Repulsive Term (Fe-Fe)
     ! [ Henriksson, table 3 ]
     !

     real(DP)           :: OO_Q       = 0.0_DP
     real(DP)           :: OO_A       = 953.9485925552151_DP
     real(DP)           :: OO_alpha   = 2.8481044096029908_DP

     !
     ! g(cos(theta)) (Fe-Fe)
     ! [ Henriksson, table 3 ]
     !

     real(DP) :: OO_gamma =  0.0115751_DP
     real(DP) :: OO_c     =  1.2898716_DP
     real(DP) :: OO_d     =  0.3413219_DP
     real(DP) :: OO_h     = -0.26_DP


     !
     ! Attractive function (Fe-H)
     ! [ Kuopanportti, table 1 ]
     !

     real(DP)             :: OH_B1     = 17.867766823732843_DP
     real(DP)             :: OH_beta1  = 1.3258252147247767_DP

     !
     ! Repulsive function (Fe-H)
     ! [ Kuopanportti, table 1 ]
     !

     real(DP)             :: OH_Q     = 0.0_DP
     real(DP)             :: OH_A     = 2482.2304027819637_DP
     real(DP)             :: OH_alpha = 5.3033008588991066_DP

     !
     ! g(cos(theta)) (Fe-H)
     ! [ Kuopanportti, table 1 ]
     !

     real(DP) :: OH_gamma =  0.01332_DP
     real(DP) :: OH_c     =  424.5_DP
     real(DP) :: OH_d     =  7.282_DP
     real(DP) :: OH_h     = -0.1091_DP


     !
     ! Attractive function (Fe-C)
     ! [ Henriksson, table 3 ]
     !

     real(DP)             :: OC_B1     = 276.92542457736567_DP
     real(DP)             :: OC_beta1  = 1.9292314964325725_DP

     !
     ! Repulsive function (Fe-C)
     ! [ Henriksson, table 3 ]
     !

     real(DP)             :: OC_Q     = 0.0_DP
     real(DP)             :: OC_A     = 661.52630736011349_DP
     real(DP)             :: OC_alpha = 2.7614007758015964_DP

     !
     ! g(cos(theta)) (Fe-C)
     ! [ Kuopanportti, table 1 ]
     !

     real(DP) :: OC_gamma =  0.00205862_DP
     real(DP) :: OC_c     =  8.95583221_DP
     real(DP) :: OC_d     =  0.72062047_DP
     real(DP) :: OC_h     =  0.87099874_DP


     !
     ! Other parameters
     !
     
     real(DP)             :: HHH_lambda = 4.0_DP
     real(DP)             :: HCH_lambda = 4.0_DP
     real(DP)             :: HHC_lambda = 4.0_DP
     real(DP)             :: HCC_lambda = 4.0_DP
     real(DP)             :: HOH_lambda = 0.0_DP
     real(DP)             :: HHO_lambda = 0.0_DP
     real(DP)             :: HOO_lambda = 0.0_DP
     real(DP)             :: HCO_lambda = 0.0_DP
     real(DP)             :: HOC_lambda = 0.0_DP

     real(DP)             :: CHH_lambda = 4.0_DP
     real(DP)             :: CCH_lambda = 0.0_DP
     real(DP)             :: CHC_lambda = 0.0_DP
     real(DP)             :: CCC_lambda = 0.0_DP
     real(DP)             :: COH_lambda = 0.0_DP
     real(DP)             :: CHO_lambda = 0.0_DP
     real(DP)             :: COO_lambda = 0.0_DP
     real(DP)             :: CCO_lambda = 0.0_DP
     real(DP)             :: COC_lambda = 0.0_DP

     real(DP)             :: OHH_lambda = 0.0_DP
     real(DP)             :: OCH_lambda = 0.0_DP
     real(DP)             :: OHC_lambda = 0.0_DP
     real(DP)             :: OCC_lambda = 0.0_DP
     real(DP)             :: OOH_lambda = 0.0_DP
     real(DP)             :: OHO_lambda = 0.0_DP
     real(DP)             :: OOO_lambda = 0.0_DP
     real(DP)             :: OCO_lambda = 0.0_DP
     real(DP)             :: OOC_lambda = 0.0_DP

     integer              :: HHH_m = 1
     integer              :: HCH_m = 1
     integer              :: HHC_m = 1
     integer              :: HCC_m = 1
     integer              :: HOH_m = 0
     integer              :: HHO_m = 0
     integer              :: HOO_m = 0
     integer              :: HCO_m = 0
     integer              :: HOC_m = 0

     integer              :: CHH_m = 1
     integer              :: CCH_m = 1
     integer              :: CHC_m = 1
     integer              :: CCC_m = 1
     integer              :: COH_m = 0
     integer              :: CHO_m = 0
     integer              :: COO_m = 0
     integer              :: CCO_m = 0
     integer              :: COC_m = 0

     integer              :: OHH_m = 0
     integer              :: OCH_m = 0
     integer              :: OHC_m = 0
     integer              :: OCC_m = 0
     integer              :: OOH_m = 0
     integer              :: OHO_m = 0
     integer              :: OOO_m = 0
     integer              :: OCO_m = 0
     integer              :: OOC_m = 0

     real(DP)             :: CC_re = 1.4_DP
     real(DP)             :: CH_re = 1.09_DP
     real(DP)             :: HH_re = 0.7415886997_DP
     real(DP)             :: OH_re = 0.0_DP


     !
     ! Debugging
     !

     logical(C_BOOL)      :: const_bo = .false.
     logical(C_BOOL)      :: const_nconj = .false.
     logical(C_BOOL)      :: no_outer_cutoff = .false.

     !
     ! Set angular terms to a constant if > 0.0
     !
     
     real(DP) :: H_g = -1.0_DP
     real(DP) :: C_g = -1.0_DP

     real(DP) :: HH_bo = -1.0_DP
     real(DP) :: CC_bo = -1.0_DP
     real(DP) :: CH_bo = -1.0_DP

     real(DP) :: bo_override(rebo2_MAX_PAIRS)

     !
     ! Cutoff radii
     !
#ifndef SCREENING
     real(DP)             :: CC_in_r1 = 1.70_DP
     real(DP)             :: CC_in_r2 = 2.00_DP

     real(DP)             :: CH_in_r1 = 1.30_DP
     real(DP)             :: CH_in_r2 = 1.80_DP

     real(DP)             :: HH_in_r1 = 1.10_DP
     real(DP)             :: HH_in_r2 = 1.70_DP

     real(DP)             :: OO_in_r1 = 2.95_DP
     real(DP)             :: OO_in_r2 = 3.35_DP

     real(DP)             :: OH_in_r1 = 2.2974_DP
     real(DP)             :: OH_in_r2 = 2.6966_DP

     real(DP)             :: OC_in_r1 = 2.30_DP
     real(DP)             :: OC_in_r2 = 2.70_DP

#else

     real(DP)             :: CC_in_r1 = 1.95_DP
     real(DP)             :: CC_in_r2 = 2.25_DP

     real(DP)             :: CH_in_r1 = 1.30_DP
     real(DP)             :: CH_in_r2 = 1.80_DP

     real(DP)             :: HH_in_r1 = 1.10_DP
     real(DP)             :: HH_in_r2 = 1.70_DP

     real(DP)             :: OO_in_r1 = 2.95_DP
     real(DP)             :: OO_in_r2 = 3.35_DP

     real(DP)             :: OH_in_r1 = 2.2974_DP
     real(DP)             :: OH_in_r2 = 2.6966_DP

     real(DP)             :: OC_in_r1 = 2.30_DP
     real(DP)             :: OC_in_r2 = 2.70_DP

     !
     ! Outer screening cutoff radii
     !

     real(DP)             :: CC_out_r1 = 2.179347_DP
     real(DP)             :: CC_out_r2 = 2.819732_DP

     real(DP)             :: CH_out_r1 = 1.30_DP
     real(DP)             :: CH_out_r2 = 1.80_DP

     real(DP)             :: HH_out_r1 = 1.10_DP
     real(DP)             :: HH_out_r2 = 1.70_DP

     real(DP)             :: OO_out_r1 = 2.95_DP
     real(DP)             :: OO_out_r2 = 3.35_DP

     real(DP)             :: OH_out_r1 = 2.2974_DP
     real(DP)             :: OH_out_r2 = 2.6966_DP

     real(DP)             :: OC_out_r1 = 2.30_DP
     real(DP)             :: OC_out_r2 = 2.70_DP


     !
     ! b_ij and dihedral cutoff radii
     !

     real(DP)             :: CC_bo_r1 = 1.866344_DP
     real(DP)             :: CC_bo_r2 = 2.758372_DP

     real(DP)             :: CH_bo_r1 = 1.30_DP
     real(DP)             :: CH_bo_r2 = 1.80_DP

     real(DP)             :: HH_bo_r1 = 1.10_DP
     real(DP)             :: HH_bo_r2 = 1.70_DP

     real(DP)             :: OO_bo_r1 = 2.95_DP
     real(DP)             :: OO_bo_r2 = 3.35_DP

     real(DP)             :: OH_bo_r1 = 2.2974_DP
     real(DP)             :: OH_bo_r2 = 2.6966_DP

     real(DP)             :: OC_bo_r1 = 2.30_DP
     real(DP)             :: OC_bo_r2 = 2.70_DP

#ifdef NUM_NEIGHBORS

     !
     ! Neighbor and conjugation cutoff radii
     !

     real(DP)             :: CC_nc_r1 = 1.217335_DP
     real(DP)             :: CC_nc_r2 = 4.000000_DP

     real(DP)             :: CH_nc_r1 = 1.30_DP
     real(DP)             :: CH_nc_r2 = 1.80_DP

     real(DP)             :: HH_nc_r1 = 1.10_DP
     real(DP)             :: HH_nc_r2 = 1.70_DP

     real(DP)             :: OO_nc_r1 = 2.95_DP
     real(DP)             :: OO_nc_r2 = 3.35_DP

     real(DP)             :: OH_nc_r1 = 2.2974_DP
     real(DP)             :: OH_nc_r2 = 2.6966_DP

     real(DP)             :: OC_nc_r1 = 2.30_DP
     real(DP)             :: OC_nc_r2 = 2.70_DP

#endif

#endif

     logical(C_BOOL)      :: with_dihedral = .true.

     !
     ! === THIS SECTION CONTAINS *DERIVED* DATA
     !

#ifdef SCREENING
     real(DP)  :: dC(rebo2_MAX_ELS)
     real(DP)  :: C_dr_cut(rebo2_MAX_ELS)
#endif

     type(g_coeff_t)  :: CC_g1_coeff
     type(g_coeff_t)  :: CC_g2_coeff

     type(g_coeff_t)  :: OO_g_coeff

     real(DP)  :: re(rebo2_MAX_PAIRS)

     real(DP)  :: lambda(rebo2_MAX_ELS,rebo2_MAX_ELS,rebo2_MAX_ELS)
     integer   :: m(rebo2_MAX_ELS,rebo2_MAX_ELS,rebo2_MAX_ELS)
     real(DP)  :: conpe(rebo2_MAX_ELS), conan(rebo2_MAX_ELS)
     real(DP)  :: conpf(rebo2_MAX_ELS)
     real(DP)  :: cut_in_h(rebo2_MAX_PAIRS), cut_in_h2(rebo2_MAX_PAIRS)
     real(DP)  :: cut_in_m(rebo2_MAX_PAIRS), cut_in_l(rebo2_MAX_PAIRS)
#ifdef SCREENING
     real(DP)  :: cut_out_h(rebo2_MAX_PAIRS), cut_out_h2(rebo2_MAX_PAIRS)
     real(DP)  :: cut_out_m(rebo2_MAX_PAIRS), cut_out_l(rebo2_MAX_PAIRS)
     real(DP)  :: cut_bo_h(rebo2_MAX_PAIRS),  cut_bo_h2(rebo2_MAX_PAIRS)
     real(DP)  :: cut_bo_m(rebo2_MAX_PAIRS),  cut_bo_l(rebo2_MAX_PAIRS)
#ifdef NUM_NEIGHBORS
     real(DP)  :: cut_nc_h(rebo2_MAX_PAIRS), cut_nc_h2(rebo2_MAX_PAIRS)
     real(DP)  :: cut_nc_m(rebo2_MAX_PAIRS), cut_nc_l(rebo2_MAX_PAIRS)
#endif
#endif

     real(DP)  :: max_cut_sq(rebo2_MAX_PAIRS)

     !
     ! Lookup tables
     !

#ifdef SEP_NCONJ
     type(table4d_t)  :: Fcc
     type(table4d_t)  :: Fch
     type(table4d_t)  :: Fhh
     type(table4d_t)  :: Foh
     type(table4d_t)  :: Foc
     type(table4d_t)  :: Foo
#else
     type(table3d_t)  :: Fcc
     type(table3d_t)  :: Fch
     type(table3d_t)  :: Fhh
     type(table3d_t)  :: Foh
     type(table3d_t)  :: Foc
     type(table3d_t)  :: Foo
#endif

     type(table3d_t)  :: Pcc
     type(table3d_t)  :: Pch
     type(table3d_t)  :: Phh
     type(table3d_t)  :: Poc
     type(table3d_t)  :: Pco
     type(table3d_t)  :: Poh
     type(table3d_t)  :: Pho
     type(table3d_t)  :: Poo

     type(table3d_t)  :: Tcc



     !
     ! Splines
     !

     integer                :: spl_n = 1000
     real(DP)               :: spl_x0 = 0.1
     type(simple_spline_t)  :: spl_VA(rebo2_MAX_PAIRS)
     type(simple_spline_t)  :: spl_VR(rebo2_MAX_PAIRS)
     type(simple_spline_t)  :: spl_fCin(rebo2_MAX_PAIRS)
#ifdef SCREENING
     type(simple_spline_t)  :: spl_fCout(rebo2_MAX_PAIRS)
     type(simple_spline_t)  :: spl_fCbo(rebo2_MAX_PAIRS)
#ifdef NUM_NEIGHBORS
     type(simple_spline_t)  :: spl_fCnc(rebo2_MAX_PAIRS)
#endif
#endif

     !
     ! Counters
     !

     logical  :: neighbor_list_allocated  = .false.
     integer  :: it                       = 0

#ifdef NUM_NEIGHBORS
     ! Precomputed number of neighbors
     real(DP), allocatable  :: nn(:, :)
#endif

     !
     ! Internal neighbor lists
     !

     integer                :: nebmax = 20
     integer                :: nebavg = 20

     integer, allocatable   :: neb_seed(:)
     integer, allocatable   :: neb_last(:)

     integer, allocatable   :: neb(:)
     integer, allocatable   :: nbb(:)
#ifndef LAMMPS
     integer, allocatable   :: dcell(:)
#endif

     integer, allocatable   :: bndtyp(:)
     real(DP), allocatable  :: bndlen(:)
     real(DP), allocatable  :: bndnm(:, :)
     real(DP), allocatable  :: cutfcn(:), cutdrv(:)

#ifdef SCREENING
     real(DP), allocatable  :: cutfcnbo(:), cutdrvbo(:)
     ! "screened" neighbor list (all neighbors of a bond which sit in the
     ! screening cutoff)
     integer, allocatable   :: sneb_seed(:)
     integer, allocatable   :: sneb_last(:)
     integer, allocatable   :: sneb(:)
#ifdef LAMMPS
     integer(C_INTPTR_T), allocatable   :: sbnd(:)
#else
     integer, allocatable   :: sbnd(:)
#endif

     ! for force calculation
     real(DP), allocatable  :: sfacbo(:)
     real(DP), allocatable  :: sfacnc(:)

     real(DP), allocatable  :: cutdrik(:), cutdrjk(:)
     real(DP), allocatable  :: cutdrboik(:), cutdrbojk(:)

#ifdef NUM_NEIGHBORS
     real(DP), allocatable  :: cutfcnnc(:), cutdrvnc(:)
     real(DP), allocatable  :: cutdrncik(:), cutdrncjk(:)
#endif
#endif

     !
     ! From the input file
     !
     
     logical(C_BOOL) :: zero_tables = .false.

#define R_NHC_NO 0:5, 0:5, 0:5
#define R_NI_NJ_NCONJ 0:4, 0:4, 0:9

#define N_NHC_NO 5, 5, 5
#define N_NI_NJ_NCONJ 4, 4, 9

     real(DP)  :: in_Fcc(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFccdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFccdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFccdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Fch(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFchdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFchdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFchdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Fhh(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFhhdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFhhdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFhhdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Foc(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFocdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFocdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFocdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Foh(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFohdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFohdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFohdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Foo(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFoodi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFoodj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFoodk(R_NI_NJ_NCONJ) = 0.0_DP


     real(DP)  :: in_Pcc(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPccdi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPccdj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPccdk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Pch(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPchdi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPchdj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPchdk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Phh(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPhhdi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPhhdj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPhhdk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Poc(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPocdi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPocdj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPocdk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Pco(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPcodi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPcodj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPcodk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Poh(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPohdi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPohdj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPohdk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Pho(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPhodi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPhodj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPhodk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Poo(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPoodi(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPoodj(R_NHC_NO) = 0.0_DP
     real(DP)  :: in_dPoodk(R_NHC_NO) = 0.0_DP

     real(DP)  :: in_Tcc(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dTccdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dTccdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dTccdk(R_NI_NJ_NCONJ) = 0.0_DP

  endtype BOP_TYPE

#if defined(MDCORE_MONOLITHIC) || defined(MDCORE_PYTHON) || defined(LAMMPS)

  public :: init
  interface init
     module procedure INIT_FUNC
  endinterface

#else

  public :: init_default
  interface init_default
     module procedure INIT_DEFAULT_FUNC
  endinterface

#endif

  public :: del
  interface del
     module procedure DEL_FUNC
  endinterface

  public :: bind_to
  interface bind_to
     module procedure BIND_TO_FUNC
  endinterface

  public :: energy_and_forces
  interface energy_and_forces
     module procedure COMPUTE_FUNC
  endinterface

  public :: init_default_database
  interface init_default_database
     module procedure rebo2coh_init_default_database
  endinterface init_default_database

  public :: register, REGISTER_FUNC
  interface register
     module procedure REGISTER_FUNC
  endinterface register

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
! Adding in Silicon Parameters - M. Todd Knippenberg 7/19/2012
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
  integer, parameter       :: rebo2_Si_ = 5

  character(2), parameter  :: rebo2_el_strs(rebo2_MAX_ELS) = &
       (/ "C ", "  ", "H ", "  ", "Si" /)

  integer, parameter       :: possible_elements(3) = &
       (/ rebo2_C_, rebo2_H_, rebo2_Si_ /)

  integer, parameter       :: C_C = 1
  integer, parameter       :: C_H = 3
  integer, parameter       :: H_H = 6
  integer, parameter       :: Si_Si = 10
  integer, parameter       :: Si_C = 5
  integer, parameter       :: C_Si = 7
  integer, parameter       :: Si_H = 8

  integer, parameter       :: H_ = 1
  integer, parameter       :: C_ = 6
  integer, parameter       :: Si_ = 14

  public :: BOP_TYPE
  type BOP_TYPE

     character(MAX_EL_STR)  :: elements = "C,H,Si"
     integer                :: els

     integer, allocatable   :: internal_el(:)

     !
     ! === THIS SECTION CONTAINS PARAMETERS ===
     !

#ifdef SCREENING

     !
     ! Screening parameters
     !

     real(DP) :: HH_Cmin = 0.0_DP
     real(DP) :: HH_Cmax = -1.0_DP
     real(DP) :: CH_Cmin = 0.0_DP
     real(DP) :: CH_Cmax = -1.0_DP
     real(DP) :: CC_Cmin = 1.0_DP
     real(DP) :: CC_Cmax = 2.0_DP
     real(DP) :: SiH_Cmin = 0.0_DP
     real(DP) :: SiH_Cmax = -1.0_DP
     real(DP) :: SiC_Cmin = 1.0_DP
     real(DP) :: SiC_Cmax = 2.0_DP
     real(DP) :: SiSi_Cmin = 1.0_DP
     real(DP) :: SiSi_Cmax = 2.0_DP

     real(DP) :: Cmin(rebo2_MAX_PAIRS)  = 1.0_DP
     real(DP) :: Cmax(rebo2_MAX_PAIRS)  = 2.0_DP

     real(DP) :: screening_threshold  = log(1d-6)
     real(DP) :: dot_threshold        = 1e-10

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

     !real(DP)             :: CC_g_theta(6)   = (/    -1.0_DP, -1.0_DP/2, -1.0_DP/3,    0.0_DP,  1.0_DP/2,    1.0_DP  /)
     !real(DP)             :: CC_g_g1(6)      = (/      -0.01,   0.05280,   0.09733,   0.37545,    2.0014,       8.0  /)
     !real(DP)             :: CC_g_dg1(6)     = (/    0.10400,   0.17000,   0.40000,       0.0,       0.0,       0.0  /)
     !real(DP)             :: CC_g_d2g1(6)    = (/    0.00000,   0.37000,   1.98000,       0.0,       0.0,       0.0  /)
     !real(DP)             :: CC_g_g2(6)      = (/        0.0,       0.0,   0.09733,  0.271856,  0.416335,       1.0  /)
     real(DP)             :: CC_g_theta(5) = (/       -1.0_DP,    -2.0_DP/3,    -1.0_DP/2,    -1.0_DP/3,       1.0_DP  /)
     real(DP)             :: CC_g_g1(5)    = (/  -0.010000_DP,  0.028207_DP,  0.052804_DP,  0.097321_DP,  1.000000_DP  /)
     real(DP)             :: CC_g_dg1(5)   = (/   0.104000_DP,  0.131443_DP,  0.170000_DP,  0.400000_DP,  2.834570_DP  /)
     real(DP)             :: CC_g_d2g1(5)  = (/   0.000000_DP,  0.140229_DP,  0.370000_DP,  1.980000_DP, 10.264700_DP  /)
     real(DP)             :: CC_g_g2(5)    = (/  -0.010000_DP,  0.028207_DP,  0.052804_DP,  0.097321_DP,  8.000000_DP  /)
     real(DP)             :: CC_g_dg2(5)   = (/   0.104000_DP,  0.131443_DP,  0.170000_DP,  0.400000_DP, 20.243600_DP  /)
     real(DP)             :: CC_g_d2g2(5)  = (/   0.000000_DP,  0.140229_DP,  0.370000_DP,  1.980000_DP, 43.933600_DP  /)

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

     real(DP)             :: HH_g_theta(4) = (/     -1.0_DP,   -5.0_DP/6,     -1.0_DP/2,        1.0_DP  /)
     real(DP)             :: HH_g_g(4)     = (/  11.2357_DP,  12.5953_DP,  16.811100_DP,  19.991800_DP  /)
     real(DP)             :: HH_g_dg(4)    = (/      0.0_DP,  13.8543_DP,   8.641230_DP,   0.333013_DP  /)
     real(DP)             :: HH_g_d2g(4)   = (/  115.115_DP,  32.3618_DP, -25.061700_DP,  -0.474189_DP  /)

     ! This is directly from the MD code of Brenner's group...
     ! ...there is no way to get this from the paper.

     !real(DP)  :: SPGH(6,3) = &
     !     reshape( &
     !     (/ 270.467795364007301_DP ,1549.701314596994564_DP  &
     !     ,3781.927258631323866_DP,4582.337619544424228_DP,2721.538161662818368_DP, &
     !     630.658598136730774_DP,16.956325544514659_DP,-21.059084522755980_DP, &
     !     -102.394184748124742_DP,-210.527926707779059_DP,-229.759473570467513_DP, &
     !     -94.968528666251945_DP,19.065031149937783_DP,2.017732531534021_DP, &
     !     -2.566444502991983_DP,3.291353893907436_DP,-2.653536801884563_DP, &
     !     0.837650930130006_DP /), &
     !     (/ 6, 3 /) )
     !integer  :: IGH(25) = &
     !     (/ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, &
     !        2, 2, 2, 2, &
     !        1, 1, 1 /)

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
     !  Attractive function (Si-Si)
     !  [ From Table 2 Schall2012 - added by MTK 7/2012 ]

     real(DP)           :: SiSi_B1      = 92.74551_DP
     real(DP)           :: SiSi_B2      = 255.329_DP
     real(DP)           :: SiSi_B3      = -3.4026_DP
     real(DP)           :: SiSi_beta1   = 1.72687_DP
     real(DP)           :: SiSi_beta2   = 1.64617_DP
     real(DP)           :: SiSi_beta3   = 132.454_DP

     ! Repulsive Term (Si-Si)
     ! [ From Table 2 Schall2012 - added by MTK 7/2012 ]
     !

     real(DP)           :: SiSi_Q       = 15.6614_DP
     real(DP)           :: SiSi_A       = 90.1964_DP
     real(DP)           :: SiSi_alpha   = 2.13083_DP

     !
     ! g(cos(theta))  (Si-Si)
     ! [ Table 3 from Schall2008 ]
     !

     real(DP)             :: SiSi_g_theta(4) = (/          -1.0_DP,       -1.0_DP/2,       -1.0_DP/3,     1.0_DP  /)
     real(DP)             :: SiSi_g_g(4)     = (/  -0.122736935_DP, -0.044734259_DP, -0.000223579_DP,  0.9800_DP  /)
     real(DP)             :: SiSi_g_dg(4)    = (/   0.065720000_DP,  0.249121746_DP,  0.308832492_DP,  1.8000_DP  /)
     real(DP)             :: SiSi_g_d2g(4)   = (/   0.320763152_DP,  0.380715536_DP,  1.125000000_DP,  2.6100_DP  /)



     ! Attractive function (Si-H)
     ! [ Table 2 from Schall2012 - added by MTK ]
     !

     real(DP)             :: SiH_B1     = 51.5687_DP
     real(DP)             :: SiH_beta1  = 1.4798_DP

     !
     ! Repulsive function (Si-H)
     ! [ Table 2 from Schall2012 - added by MTK ]
     !

     real(DP)             :: SiH_Q     = 1.48065_DP
     real(DP)             :: SiH_A     = 128.613_DP
     real(DP)             :: SiH_alpha = 3.14279_DP

     !
     ! Attractive function (Si-C)
     ! [ Table 2 from Schall2012 - added by MTK ]
     !

     real(DP)             :: SiC_B1     = 165.632_DP
     real(DP)             :: SiC_beta1  = 1.7044_DP

     !
     ! Repulsive function (Si-C)
     ! [ Table 2 from Schall2012 - added by MTK ]
     !

     real(DP)             :: SiC_Q     = 1.88794_DP
     real(DP)             :: SiC_A     = 499.015_DP
     real(DP)             :: SiC_alpha = 3.0_DP


     !
     ! Additional Si-C bond-order mixing factor
     !

     real(DP)             :: SiC_chi   = 1.0637634_DP


     !
     ! Other parameters
     !

     real(DP)             :: HHH_lambda    = 4.0_DP
     real(DP)             :: CHH_lambda    = 0.0_DP
     real(DP)             :: SiHH_lambda   = 0.0_DP

     real(DP)             :: HCC_lambda    = 4.0_DP
     real(DP)             :: CCC_lambda    = 0.0_DP
     real(DP)             :: SiCC_lambda   = 0.0_DP

     real(DP)             :: HSiSi_lambda  = 2.5_DP
     real(DP)             :: CSiSi_lambda  = 0.0_DP
     real(DP)             :: SiSiSi_lambda = 0.0_DP

     real(DP)             :: HCH_lambda    = 4.0_DP
     real(DP)             :: CCH_lambda    = 0.0_DP
     real(DP)             :: SiCH_lambda   = 0.0_DP

     real(DP)             :: HHC_lambda    = 4.0_DP
     real(DP)             :: CHC_lambda    = 0.0_DP
     real(DP)             :: SiHC_lambda   = 0.0_DP

     real(DP)             :: HSiH_lambda   = 3.2_DP
     real(DP)             :: CSiH_lambda   = 0.0_DP
     real(DP)             :: SiSiH_lambda  = 0.0_DP

     real(DP)             :: HHSi_lambda   = 3.6_DP
     real(DP)             :: CHSi_lambda   = 0.0_DP
     real(DP)             :: SiHSi_lambda  = 0.0_DP

     real(DP)             :: HCSi_lambda   = 4.0_DP
     real(DP)             :: CCSi_lambda   = 0.0_DP
     real(DP)             :: SiCSi_lambda  = 0.0_DP

     real(DP)             :: HSiC_lambda   = 4.0_DP
     real(DP)             :: CSiC_lambda   = 0.0_DP
     real(DP)             :: SiSiC_lambda  = 0.0_DP


#ifdef SCREENING
#define M 0
#else
#define M 0
#endif

     ! Note: m = 0 below means h(rij, rik)=1
     integer              :: HHH_m    = 1
     integer              :: CHH_m    = M
     integer              :: SiHH_m   = M

     integer              :: HCC_m    = 1
     integer              :: CCC_m    = M
     integer              :: SiCC_m   = M

     integer              :: HSiSi_m  = 1
     integer              :: CSiSi_m  = M
     integer              :: SiSiSi_m = M

     integer              :: HCH_m    = 1
     integer              :: CCH_m    = M
     integer              :: SiCH_m   = M

     integer              :: HHC_m    = 1
     integer              :: CHC_m    = M
     integer              :: SiHC_m   = M

     integer              :: HSiH_m   = 1
     integer              :: CSiH_m   = M
     integer              :: SiSiH_m  = M

     integer              :: HHSi_m   = 1
     integer              :: CHSi_m   = M
     integer              :: SiHSi_m  = M

     integer              :: HCSi_m   = 1
     integer              :: CCSi_m   = M
     integer              :: SiCSi_m  = M

     integer              :: HSiC_m   = 1
     integer              :: CSiC_m   = M
     integer              :: SiSiC_m  = M


     real(DP)             :: CC_re  = 1.4_DP
     real(DP)             :: CH_re  = 1.09_DP
     real(DP)             :: HH_re  = 0.7415887_DP
     real(DP)             :: SiH_re = 1.48065165_DP

     !
     ! New parameters, required for bond-order cutoff
     !

     real(DP)             :: SiSi_re = 2.1_DP
     real(DP)             :: SiC_re  = 1.8_DP

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
     real(DP) :: Si_g = -1.0_DP

     real(DP) :: HH_bo = -1.0_DP
     real(DP) :: CC_bo = -1.0_DP
     real(DP) :: CH_bo = -1.0_DP
     real(DP) :: SiSi_bo = -1.0_DP

     real(DP) :: bo_override(rebo2_MAX_PAIRS)

     !
     ! Cutoff radii
     !

#ifdef SCREENING
     real(DP)             :: CC_in_r1 = 1.95_DP
     real(DP)             :: CC_in_r2 = 2.25_DP
#else
     real(DP)             :: CC_in_r1   = 1.80_DP
     real(DP)             :: CC_in_r2   = 2.10_DP
#endif

     real(DP)             :: CH_in_r1   = 1.30_DP
     real(DP)             :: CH_in_r2   = 1.80_DP

     real(DP)             :: HH_in_r1   = 1.10_DP
     real(DP)             :: HH_in_r2   = 1.70_DP

     real(DP)             :: SiSi_in_r1 = 2.5_DP
     real(DP)             :: SiSi_in_r2 = 3.05_DP

     real(DP)             :: SiH_in_r1  = 1.66_DP
     real(DP)             :: SiH_in_r2  = 2.28_DP

     real(DP)             :: SiC_in_r1  = 2.06_DP
     real(DP)             :: SiC_in_r2  = 2.47_DP

#ifdef SCREENING

     !
     ! Outer screening cutoff radii
     !

     real(DP)             :: CC_out_r1 = 1.95_DP
     real(DP)             :: CC_out_r2 = 3.45_DP
     real(DP)             :: SiC_out_r1 = 2.05_DP
     real(DP)             :: SiC_out_r2 = 5.40_DP
     real(DP)             :: SiSi_out_r1 = 2.50_DP
     real(DP)             :: SiSi_out_r2 = 3.70_DP

     real(DP)             :: CH_out_r1   = 1.80_DP
     real(DP)             :: CH_out_r2   = 2*1.80_DP
     real(DP)             :: HH_out_r1   = 1.70_DP
     real(DP)             :: HH_out_r2   = 2.50_DP
     real(DP)             :: SiH_out_r1  = 2.28_DP
     real(DP)             :: SiH_out_r2  = 2*2.28_DP


     real(DP)             :: CC_bo_r1 = 1.95_DP
     real(DP)             :: CC_bo_r2 = 2.75_DP
     real(DP)             :: SiC_bo_r1 = 2.05_DP
     real(DP)             :: SiC_bo_r2 = 5.00_DP
     real(DP)             :: SiSi_bo_r1 = 2.50_DP
     real(DP)             :: SiSi_bo_r2 = 5.55_DP

     real(DP)             :: CH_bo_r1   = 0.6_DP*1.80_DP
     real(DP)             :: CH_bo_r2   = 2*1.80_DP
     real(DP)             :: HH_bo_r1   = 0.6_DP*1.70_DP
     real(DP)             :: HH_bo_r2   = 2.5_DP
     real(DP)             :: SiH_bo_r1  = 0.6_DP*2.28_DP
     real(DP)             :: SiH_bo_r2  = 2*2.28_DP

#ifdef NUM_NEIGHBORS

     !
     ! Neighbor and conjugation cutoff radii
     !

     real(DP)             :: CC_nc_r1 = 1.74_DP
     real(DP)             :: CC_nc_r2 = 4.00_DP
     real(DP)             :: SiC_nc_r1 = 1.00_DP
     real(DP)             :: SiC_nc_r2 = 5.00_DP
     real(DP)             :: SiSi_nc_r1 = 3.45_DP
     real(DP)             :: SiSi_nc_r2 = 6.00_DP


     real(DP)             :: CH_nc_r1   = 0.6_DP*1.80_DP
     real(DP)             :: CH_nc_r2   = 2*1.80_DP
     real(DP)             :: HH_nc_r1   = 0.6_DP*1.70_DP
     real(DP)             :: HH_nc_r2   = 2.5_DP
     real(DP)             :: SiH_nc_r1  = 0.6_DP*2.28_DP
     real(DP)             :: SiH_nc_r2  = 2*2.28_DP

#endif

#endif

     real(DP)             :: dh_sin1 = 0.1_DP
     real(DP)             :: dh_sin2 = 0.5_DP

     logical(C_BOOL)      :: with_dihedral = .true.

     !
     ! === THIS SECTION CONTAINS *DERIVED* DATA
     !

#ifdef SCREENING
     real(DP)  :: dC(rebo2_MAX_PAIRS)
     real(DP)  :: C_dr_cut(rebo2_MAX_PAIRS)
#endif

     real(DP)  :: CC_g1_coeff(6, 4)
     reaL(DP)  :: CC_g2_coeff(6, 4)

     reaL(DP)  :: HH_g_coeff(6, 3)

     real(DP)  :: SiSi_g_coeff(6, 3)

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
     real(DP)  :: cut_bo_h(rebo2_MAX_PAIRS), cut_bo_h2(rebo2_MAX_PAIRS)
     real(DP)  :: cut_bo_m(rebo2_MAX_PAIRS), cut_bo_l(rebo2_MAX_PAIRS)
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
     type(table4d_t)  :: Fsih
     type(table4d_t)  :: Fsic
     type(table4d_t)  :: Fsisi
#else
     type(table3d_t)  :: Fcc
     type(table3d_t)  :: Fch
     type(table3d_t)  :: Fhh
     type(table3d_t)  :: Fsih
     type(table3d_t)  :: Fsic
     type(table3d_t)  :: Fsisi
#endif

     type(table3d_t)  :: Pcc
     type(table3d_t)  :: Pch
     type(table3d_t)  :: Psic
     type(table3d_t)  :: Pcsi
     type(table3d_t)  :: Psih
     type(table3d_t)  :: Psisi

#ifdef SEP_NCONJ
     type(table4d_t)  :: Tcc
#else
     type(table3d_t)  :: Tcc
#endif

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
     real(DP), allocatable  :: cutdrik(:), cutdrjk(:)

     real(DP), allocatable  :: sfacbo(:)
     real(DP), allocatable  :: cutfcnbo(:), cutdrvbo(:)
     real(DP), allocatable  :: cutdrboik(:), cutdrbojk(:)

#ifdef NUM_NEIGHBORS
     real(DP), allocatable  :: sfacnc(:)
     real(DP), allocatable  :: cutfcnnc(:), cutdrvnc(:)
     real(DP), allocatable  :: cutdrncik(:), cutdrncjk(:)
#endif
#endif

     real(DP), allocatable  :: VA(:)
     real(DP), allocatable  :: VR(:)
     real(DP), allocatable  :: bij(:)
     real(DP), allocatable  :: bji(:)
     real(DP), allocatable  :: baveij(:)
     real(DP), allocatable  :: Fij(:)
     real(DP), allocatable  :: Pij(:)
     real(DP), allocatable  :: Pji(:)

     real(DP), allocatable  :: packed_VA(:)
     real(DP), allocatable  :: packed_VR(:)
     real(DP), allocatable  :: packed_bij(:)
     real(DP), allocatable  :: packed_bji(:)
     real(DP), allocatable  :: packed_baveij(:)
     real(DP), allocatable  :: packed_Fij(:)
     real(DP), allocatable  :: packed_Pij(:)
     real(DP), allocatable  :: packed_Pji(:)

     !
     ! From the input file
     !

     logical(C_BOOL) :: zero_tables = .false.
     logical(C_BOOL) :: introspection = .false.

#define R_NI_NJ_NCONJ 0:4, 0:4, 0:9
#define R_NH_NC_NSI 0:5, 0:5, 0:5
#define R_NH_NCL_NSI 0:5, 0:9, 0:5

#define N_NI_NJ_NCONJ 4, 4, 9
#define N_NH_NC_NSI 5, 5, 5
#define N_NH_NCL_NSI 5, 9, 5

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

     real(DP)  :: in_Fsic(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsicdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsicdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsicdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Fsih(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsihdi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsihdj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsihdk(R_NI_NJ_NCONJ) = 0.0_DP

     real(DP)  :: in_Fsisi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsisidi(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsisidj(R_NI_NJ_NCONJ) = 0.0_DP
     real(DP)  :: in_dFsisidk(R_NI_NJ_NCONJ) = 0.0_DP


     real(DP)  :: in_Pcc(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPccdi(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPccdj(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPccdk(R_NH_NC_NSI) = 0.0_DP

     real(DP)  :: in_Pch(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPchdi(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPchdj(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPchdk(R_NH_NC_NSI) = 0.0_DP

     real(DP)  :: in_Psic(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPsicdi(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPsicdj(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPsicdk(R_NH_NC_NSI) = 0.0_DP

     real(DP)  :: in_Pcsi(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPcsidi(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPcsidj(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPcsidk(R_NH_NC_NSI) = 0.0_DP

     real(DP)  :: in_Psih(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPsihdi(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPsihdj(R_NH_NC_NSI) = 0.0_DP
     real(DP)  :: in_dPsihdk(R_NH_NC_NSI) = 0.0_DP

     real(DP)  :: in_Psisi(R_NH_NCL_NSI) = 0.0_DP
     real(DP)  :: in_dPsisidi(R_NH_NCL_NSI) = 0.0_DP
     real(DP)  :: in_dPsisidj(R_NH_NCL_NSI) = 0.0_DP
     real(DP)  :: in_dPsisidk(R_NH_NCL_NSI) = 0.0_DP

     real(DP)  :: in_Tcc(R_NI_NJ_NCONJ) = 0.0_DP

  endtype BOP_TYPE

  public :: init
  interface init
     module procedure INIT_FUNC
  endinterface

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
     module procedure rebo2sich_init_default_database
  endinterface init_default_database

  public :: register, REGISTER_FUNC
  interface register
     module procedure REGISTER_FUNC
  endinterface register

  public :: get_dict
  interface get_dict
     module procedure GET_DICT_FUNC
  endinterface get_dict

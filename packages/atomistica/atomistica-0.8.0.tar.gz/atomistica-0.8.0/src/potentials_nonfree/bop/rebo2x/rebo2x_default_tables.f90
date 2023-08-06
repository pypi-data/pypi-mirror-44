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

!#define CHECK_TABLES
#define ZERO_TABLES

module rebo2x_default_tables
  use supplib

  implicit none

contains

  !>
  ! Construct the Fcc-table
  !<
  subroutine rebo2x_default_Fcc_table(F, dFdi, dFdj, dFdk)
    implicit none

    real(DP), intent(out)  :: F(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdk(0:, 0:, 0:)

    ! ---

    real(DP)  :: x
    integer   :: i, j, k,n

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP

    !
    ! Values from Table 4
    !

    F(1, 1,   0)  =  0.105000_DP
    F(1, 1,   1)  = -0.0041775_DP
    F(1, 1, 2:8)  = -0.0160856_DP
    F(2, 2,   0)  =  0.09444957_DP
    F(2, 2,   1)  =  0.02200000_DP
    F(2, 2,   2)  =  0.03970587_DP
    F(2, 2,   3)  =  0.03308822_DP
    F(2, 2,   4)  =  0.02647058_DP
    F(2, 2,   5)  =  0.01985293_DP
    F(2, 2,   6)  =  0.01323529_DP
    F(2, 2,   7)  =  0.00661764_DP
    F(2, 2,   8)  =  0.0_DP
    F(0, 1,   0)  =  0.04338699_DP
    F(0, 1,   1)  =  0.0099172158_DP

!--
    F(0, 1, 1:8)  =  0.0099172158_DP
!--

    F(0, 2,   0)  =  0.0493976637_DP
    F(0, 2,   1)  = -0.011942669_DP

!--
    F(0, 2, 2:8)  = F(0, 1, 1)
!--

    F(0, 3, 0:8)  = -0.119798935_DP

!--
    F(0, 3, 0:1)  = -0.119798935_DP
    F(0, 3, 2:8)  =  F(0, 1, 1)
!--

    F(1, 2,   0)  =  0.0096495698_DP
    F(1, 2,   1)  =  0.030_DP
    F(1, 2,   2)  = -0.0200_DP
    F(1, 2,   3)  = -0.0233778774_DP
    F(1, 2,   4)  = -0.0267557548_DP
    F(1, 2, 5:8)  = -0.030133632_DP
!-- Refit for proper graphene elastic constants
!    F(1, 2, 5:8)  = -0.030133632_DP - 2*0.09968441349_DP
!--
    F(1, 3, 1:8)  = -0.124836752_DP
    F(2, 3, 0:8)  = -0.044709383_DP

!-- Refit for proper graphene elastic constants
!    F(2, 2,   8)  = g_graphene_F
!    F(2, 2,   8)  = 0.0_DP

    do i = 3, 7
       F(2, 2, i) = F(2, 2, 2) + (i-2)*( F(2, 2, 8) - F(2, 2, 2) )/6
    enddo

    do i = 3, 4
       F(1, 2, i) = F(1, 2, 2) + (i-2)*( F(1, 2, 5) - F(1, 2, 2) )/3
!       write (*, *) i, F(1, 2, i)
    enddo
!--

    ! Schall, Harrison, 2012
    F(1, 1, 2:8) = -0.30_DP

    dFdi(2, 1,   0)  = -0.052500_DP
    dFdi(2, 1, 4:8)  = -0.054376_DP
    dFdi(2, 3,   0)  =  0.0_DP
    dFdi(2, 3, 1:5)  =  0.062418_DP
    dFdk(2, 2, 3:7)  = -0.006618_DP
    dFdi(2, 3, 6:8)  =  0.062418_DP
    dFdk(1, 1,   1)  = -0.060543_DP
    dFdk(1, 2,   3)  = -0.020044_DP
    dFdk(1, 2,   4)  = -0.020044_DP

!*************************************************************
!     This value does not appear in DWB's paper, but should:
	dFdj(3,1,1) = 0.0375447764_DP
        dFdj(3,2, 1:8) = 0.062418_DP
!*************************************************************

    !
    ! Symmetrize values
    !

    do k = 0, 8
       do i = 0, 2
          do j = i+1, 3
             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

             x = dFdi(i, j, k) + dFdj(j, i, k)
             dFdi(i, j, k) = x
             dFdj(j, i, k) = x

             x = dFdi(j, i, k) + dFdj(i, j, k)
             dFdi(j, i, k) = x
             dFdj(i, j, k) = x

             x = dFdk(i, j, k) + dFdk(j, i, k)
             dFdk(i, j, k) = x
             dFdk(j, i, k) = x
          enddo
       enddo
    enddo

#ifdef CHECK_TABLES
    call assert_equal(F, "FijkCC.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP
#endif

  endsubroutine rebo2x_default_Fcc_table


  !>
  ! Construct the Fch-table
  !<
  subroutine rebo2x_default_Fch_table(F, dFdi, dFdj, dFdk)
    implicit none

    real(DP), intent(out)  :: F(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdk(0:, 0:, 0:)

    ! ---

    real(DP)  :: x
    integer   :: i, j, k

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP


    !
    ! Values from Table 9
    !

    F(0, 2, 4:8)  = -0.0090477875161288110_DP
    F(1, 3, 0:8)  = -0.213_DP
    F(1, 2, 0:8)  = -0.25_DP
    F(1, 1, 0:8)  = -0.5_DP


    !
    ! Symmetrize values
    !

    do k = 0, 8
       do i = 0, 2
          do j = i+1, 3

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo

#ifdef CHECK_TABLES
    call assert_equal(F, "FijkCH.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F    = 0.0_DP
    dFdi = 0.0_DP
    dFdj = 0.0_DP
    dFdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Fch_table


  !>
  ! Construct the Fhh-table
  !<
  subroutine rebo2x_default_Fhh_table(F, dFdi, dFdj, dFdk)
    implicit none

    real(DP), intent(out)  :: F(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdk(0:, 0:, 0:)

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP

    !
    ! Values from Table 6
    !

    F(1, 1, 0)  = 0.249831916_DP

! Derivatives from dFijkHH.dat (already symmetric) Schall-2013
 	dFdi(0,1,0) = 0.124915958_DP
 	dFdj(1,0,0) = 0.124915958_DP
 	dFdk(1,1,1) = -0.124915958_DP
 	dFdj(1,2,0) = -0.124915958_DP
 	dFdi(2,1,0) = -0.124915958_DP

#ifdef ZERO_TABLES
    F    = 0.0_DP
    dFdi = 0.0_DP
    dFdj = 0.0_DP
    dFdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Fhh_table


  !>
  ! Construct the Fsic-table
  !<
  subroutine rebo2x_default_Fsic_table(F, dFdi, dFdj, dFdk)
    implicit none

    real(DP), intent(out)  :: F(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdk(0:, 0:, 0:)

    ! ---

    real(DP)  :: x
    integer   :: i, j, k

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP

    !
    ! Values from Table 5 - Schall2012
    !

    F(3, 1, 0)   = -0.217547_DP
    F(3, 1, 1)   = -0.194939_DP
    F(2, 1, 0)   = -0.167218_DP
    F(2, 1, 1)   = 0.0254016_DP

    F(1, 0, 1)   = 0.170371_DP
    F(1, 0, 0)   = -0.0579748_DP
    F(3, 0, 0)   = -0.408163_DP
    F(3, 2, 0)   = -0.03_DP
    F(3, 3, 1)   = -0.01_DP
    F(2, 0, 0)   = 0.203986_DP
    F(1, 1, 0:8) = -0.2_DP
    F(2, 1, 0:8) = -0.2_DP
    F(3, 1, 0:8) = -0.2_DP

    ! Schall, Harrison --- from datafile
    F(3, 1, 0)   = -0.2175470_DP
    F(3, 1, 1)   = -0.1949390_DP
    F(2, 1, 1)   = 0.0254016_DP

    !
    ! Symmetrize values
    !

    do k = 0, 8
       do i = 0, 2
          do j = i+1, 3

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo

! Derivatives from dFijkSiC.dat Schall 2013

dFdi(0,2,0)=-0.083609_DP
dFdi(0,3,0)=-0.1087735_DP
dFdi(1,0,0)=0.101993_DP
dFdi(1,2,0)=-0.101993_DP
dFdi(1,3,0)=0.1890815_DP
dFdi(2,0,0)=-0.1750941_DP
dFdi(2,1,0)=-0.1087735_DP
dFdi(2,1,1)=-0.0974695_DP
dFdi(2,3,0)=0.1087735_DP
dFdi(3,0,0)=-0.101993_DP
dFdi(3,1,0)=0.083609_DP
dFdi(3,1,1)=-0.0127008_DP

dFdj(0,1,0)=0.101993_DP
dFdj(0,2,0)=-0.1750941_DP
dFdj(0,3,0)=-0.101993_DP
dFdj(1,2,0)=-0.1087735_DP
dFdj(1,2,1)=-0.0974695_DP
dFdj(1,3,0)=0.083609_DP
dFdj(1,3,1)=-0.0127008_DP
dFdj(2,0,0)=-0.083609_DP
dFdj(2,1,0)=-0.101993_DP
dFdj(3,0,0)=-0.1087735_DP
dFdj(3,1,0)=0.1890815_DP
dFdj(3,2,0)=0.1087735_DP

dFdk(0,1,0)=0.0851855_DP
dFdk(0,1,1)=0.0289874_DP
dFdk(1,0,0)=0.0851855_DP
dFdk(1,0,1)=0.0289874_DP
dFdk(1,2,0)=0.0127008_DP
dFdk(1,2,1)=0.083609_DP
dFdk(1,3,0)=-0.0974695_DP
dFdk(1,3,1)=0.1087735_DP
dFdk(2,1,0)=0.0127008_DP
dFdk(2,1,1)=0.083609_DP
dFdk(3,1,0)=-0.0974695_DP
dFdk(3,1,1)=0.1087735_DP


#ifdef CHECK_TABLES
    call assert_equal(F, "FijkSiC.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F    = 0.0_DP
    dFdi = 0.0_DP
    dFdj = 0.0_DP
    dFdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Fsic_table


  !>
  ! Construct the Fsih-table
  !<
  subroutine rebo2x_default_Fsih_table(F, dFdi, dFdj, dFdk)
    implicit none

    real(DP), intent(out)  :: F(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdk(0:, 0:, 0:)

    ! ---

    real(DP)  :: x
    integer   :: i, j, k

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP


    !
    ! Values from Table 5 - Schall2012
    !

    F(1, 0, 1)    = -0.102203_DP
    F(2, 0, 0)    = -0.103822_DP
    F(2, 0, 4:8)  = -0.00287431_DP
    F(3, 1, 0:8)  = -0.173718_DP
    F(3, 0, 1)    = -0.015_DP
! This gives wrong energies for SiSiH2
!    F(2, 0, 1)    = -0.0602798_DP

    !
    ! Symmetrize values
    !

    do k = 0, 8
       do i = 0, 2
          do j = i+1, 3

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo

! Derivatives from dFijkSiH.dat Schall 2013
!dFdi
dFdi(0,3,1) = -0.086859_DP
dFdi(1,3,1) = 0.0075_DP

!dFdj
dFdj(3,0,1) = -0.086859_DP
dFdj(3,1,1) = 0.0075_DP

!dFdk
dFdk(0,2,4) = -0.001437155_DP
dFdk(1,3,0) = -0.086859_DP
dFdk(2,0,4) = -0.001437155_DP
dFdk(3,1,0) = -0.086859_DP


#ifdef CHECK_TABLES
    call assert_equal(F, "FijkSiH.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F    = 0.0_DP
    dFdi = 0.0_DP
    dFdj = 0.0_DP
    dFdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Fsih_table


  !>
  ! Construct the Fsisi-table
  !<
  subroutine rebo2x_default_Fsisi_table(F, dFdi, dFdj, dFdk)
    implicit none

    real(DP), intent(out)  :: F(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dFdk(0:, 0:, 0:)

    ! ---

    real(DP)  :: x
    integer   :: i, j, k

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP

    !
    ! Values from Table 9
    !

    F(1, 1, 0)    = -0.204407_DP
    F(1, 0, 1)    = 0.213913_DP
    F(1, 1, 1:8)  = -0.273504_DP
    F(1, 0, 0)    = 0.13147_DP
!    F(2, 2, 2:8)  = -0.00287431_DP
    F(2, 2, 2:8)  = (/ ( -0.00287431_DP*(8-i)/6, i=2,8 ) /)
    F(2, 2, 3)    = -0.0023953_DP
!    F(2, 1, 2:5)  = -0.0492402_DP
    F(2, 1, 2:5)  = (/ ( -0.0492402_DP*(5-i)/3, i=2,5 ) /)
    F(2, 0, 0)    = 0.100364_DP
    F(3, 0, 0:8)  = 0.111018_DP
    F(2, 1, 0)    = -0.0666871_DP
    F(2, 1, 1)    = 0.071_DP
    F(3, 1, 1:8)  = -0.012773_DP
    F(3, 3, 4)    =  -0.012773_DP
    F(2, 2, 0)    =  -0.012773_DP
    F(3, 2, 0)    =  -0.012773_DP
    F(2, 2, 1)    =   -0.0666871_DP
    F(2, 0, 1)    =   0.0954453_DP
    F(3, 2, 4:8)  =   -0.0298937_DP
    F(3, 2, 0)    =   0.00619372_DP
! This gives wrong SiH3SiH=SiHSiH3
    F(3, 2, 1:3)  = (/ ( ((4-i)*F(3,2,0)+i*F(3,2,4))/4, i=1,3 ) /)

!    F(3, 2, 1)    = -0.012773_DP
!    F(3, 2, 1)    = -0.0028281_DP
!    F(3, 2, 2)    = -0.0118500_DP
!    F(3, 2, 3)    = -0.0208718_DP

    ! Schall, Harrison --- from datafile
    F(2, 2, 3)   = -0.0024637_DP

    !
    ! Symmetrize values
    !

    do k = 0, 8
       do i = 0, 2
          do j = i+1, 3

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo

! Derivatives from dFijkSiSi.dat Schall 2013

!dFdi
dFdi(0,1,0)=-0.1022035_DP
dFdi(0,1,1)=-0.136752_DP
dFdi(0,2,0)=-0.03334355_DP
dFdi(0,2,1)=0.0355_DP
dFdi(0,3,1)=-0.0063865_DP
dFdi(0,3,2)=-0.0063865_DP
dFdi(0,3,3)=-0.0063865_DP
dFdi(0,3,4)=-0.0063865_DP
dFdi(0,3,5)=-0.0063865_DP
dFdi(0,3,6)=-0.0063865_DP
dFdi(0,3,7)=-0.0063865_DP
dFdi(0,3,8)=-0.0063865_DP
dFdi(1,0,0)=0.050182_DP
dFdi(1,0,1)=0.04772265_DP
dFdi(1,1,0)=-0.09907855_DP
dFdi(1,1,1)=-0.0714565_DP
dFdi(1,1,2)=-0.0246201_DP
dFdi(1,1,3)=-0.0164134_DP
dFdi(1,1,4)=-0.0082067_DP
dFdi(1,2,0)=-0.0565685_DP
dFdi(1,2,1)=-0.0810662_DP
dFdi(1,2,2)=-0.001437155_DP
dFdi(1,2,3)=-0.001231845_DP
dFdi(1,2,4)=-0.0009581_DP
dFdi(1,3,1)=-0.056923065_DP
dFdi(1,3,2)=-0.061434_DP
dFdi(1,3,3)=-0.0659449_DP
dFdi(1,3,4)=-0.07045585_DP
dFdi(1,3,5)=-0.07045585_DP
dFdi(1,3,6)=-0.07045585_DP
dFdi(1,3,7)=-0.07045585_DP
dFdi(1,3,8)=-0.07045585_DP
dFdi(2,0,0)=-0.010226_DP
dFdi(2,0,1)=-0.0514475_DP
dFdi(2,1,0)=0.1022035_DP
dFdi(2,1,1)=0.1303655_DP
dFdi(2,1,2)=0.1303655_DP
dFdi(2,1,3)=0.1303655_DP
dFdi(2,1,4)=0.1303655_DP
dFdi(2,2,0)=0.03644041_DP
dFdi(2,2,1)=-0.036914065_DP
dFdi(2,2,2)=0.0186951_DP
dFdi(2,2,3)=0.0059775_DP
dFdi(2,2,4)=-0.00674015_DP
dFdi(2,2,5)=-0.01494685_DP
dFdi(2,2,6)=-0.01494685_DP
dFdi(2,2,7)=-0.01494685_DP
dFdi(2,3,1)=0.0063865_DP
dFdi(2,3,2)=0.0063865_DP
dFdi(2,3,3)=0.0063865_DP
dFdi(2,3,5)=0.0063865_DP
dFdi(2,3,6)=0.0063865_DP
dFdi(2,3,7)=0.0063865_DP
dFdi(2,3,8)=0.0063865_DP
dFdi(3,0,0)=-0.050182_DP
dFdi(3,0,1)=-0.04772265_DP
dFdi(3,1,1)=-0.0355_DP
dFdi(3,1,2)=0.0246201_DP
dFdi(3,1,3)=0.0164134_DP
dFdi(3,1,4)=0.0082067_DP
dFdi(3,2,0)=0.0063865_DP
dFdi(3,2,1)=0.03334355_DP
dFdi(3,2,2)=0.001437155_DP
dFdi(3,2,3)=0.001231845_DP
dFdi(3,2,4)=0.0009581_DP
dFdi(3,2,5)=0.000718575_DP
dFdi(3,2,6)=0.000479051_DP
dFdi(3,2,7)=0.0002395255_DP
dFdi(3,3,4)=0.01494685_DP

!dFdj
dFdj(0,1,0)=0.050182_DP
dFdj(0,1,1)=0.04772265_DP
dFdj(0,2,0)=-0.010226_DP
dFdj(0,2,1)=-0.0514475_DP
dFdj(0,3,0)=-0.050182_DP
dFdj(0,3,1)=-0.04772265_DP
dFdj(1,0,0)=-0.1022035_DP
dFdj(1,0,1)=-0.136752_DP
dFdj(1,1,0)=-0.09907855_DP
dFdj(1,1,1)=-0.0714565_DP
dFdj(1,1,2)=-0.0246201_DP
dFdj(1,1,3)=-0.0164134_DP
dFdj(1,1,4)=-0.0082067_DP
dFdj(1,2,0)=0.1022035_DP
dFdj(1,2,1)=0.1303655_DP
dFdj(1,2,2)=0.1303655_DP
dFdj(1,2,3)=0.1303655_DP
dFdj(1,2,4)=0.1303655_DP
dFdj(1,3,1)=-0.0355_DP
dFdj(1,3,2)=0.0246201_DP
dFdj(1,3,3)=0.0164134_DP
dFdj(1,3,4)=0.0082067_DP
dFdj(2,0,0)=-0.03334355_DP
dFdj(2,0,1)=0.0355_DP
dFdj(2,1,0)=-0.0565685_DP
dFdj(2,1,1)=-0.0810662_DP
dFdj(2,1,2)=-0.001437155_DP
dFdj(2,1,3)=-0.001231845_DP
dFdj(2,1,4)=-0.0009581_DP
dFdj(2,2,0)=0.03644041_DP
dFdj(2,2,1)=-0.036914065_DP
dFdj(2,2,2)=0.0186951_DP
dFdj(2,2,3)=0.0059775_DP
dFdj(2,2,4)=-0.00674015_DP
dFdj(2,2,5)=-0.01494685_DP
dFdj(2,2,6)=-0.01494685_DP
dFdj(2,2,7)=-0.01494685_DP
dFdj(2,3,0)=0.0063865_DP
dFdj(2,3,1)=0.03334355_DP
dFdj(2,3,2)=0.001437155_DP
dFdj(2,3,3)=0.001231845_DP
dFdj(2,3,4)=0.0009581_DP
dFdj(2,3,5)=0.000718575_DP
dFdj(2,3,6)=0.000479051_DP
dFdj(2,3,7)=0.0002395255_DP
dFdj(3,0,1)=-0.0063865_DP
dFdj(3,0,2)=-0.0063865_DP
dFdj(3,0,3)=-0.0063865_DP
dFdj(3,0,4)=-0.0063865_DP
dFdj(3,0,5)=-0.0063865_DP
dFdj(3,0,6)=-0.0063865_DP
dFdj(3,0,7)=-0.0063865_DP
dFdj(3,0,8)=-0.0063865_DP
dFdj(3,1,1)=-0.056923065_DP
dFdj(3,1,2)=-0.061434_DP
dFdj(3,1,3)=-0.0659449_DP
dFdj(3,1,4)=-0.07045585_DP
dFdj(3,1,5)=-0.07045585_DP
dFdj(3,1,6)=-0.07045585_DP
dFdj(3,1,7)=-0.07045585_DP
dFdj(3,1,8)=-0.07045585_DP
dFdj(3,2,1)=0.0063865_DP
dFdj(3,2,2)=0.0063865_DP
dFdj(3,2,3)=0.0063865_DP
dFdj(3,2,5)=0.0063865_DP
dFdj(3,2,6)=0.0063865_DP
dFdj(3,2,7)=0.0063865_DP
dFdj(3,2,8)=0.0063865_DP
dFdj(3,3,4)=0.01494685_DP

!dFdk
dFdk(0,1,0)=0.1069565_DP
dFdk(0,1,1)=-0.065735_DP
dFdk(0,2,0)=0.04772265_DP
dFdk(0,2,1)=-0.050182_DP
dFdk(0,3,0)=0.055509_DP
dFdk(1,0,0)=0.1069565_DP
dFdk(1,0,1)=-0.065735_DP
dFdk(1,1,0)=-0.136752_DP
dFdk(1,1,1)=-0.0345485_DP
dFdk(1,2,0)=0.0355_DP
dFdk(1,2,1)=0.00872345_DP
dFdk(1,2,2)=-0.0519134_DP
dFdk(1,2,3)=0.0164134_DP
dFdk(1,2,4)=0.0164134_DP
dFdk(1,3,1)=-0.0063865_DP
dFdk(2,0,0)=0.04772265_DP
dFdk(2,0,1)=-0.050182_DP
dFdk(2,1,0)=0.0355_DP
dFdk(2,1,1)=0.00872345_DP
dFdk(2,1,2)=-0.0519134_DP
dFdk(2,1,3)=0.0164134_DP
dFdk(2,1,4)=0.0164134_DP
dFdk(2,2,0)=-0.03334355_DP
dFdk(2,2,1)=0.004949345_DP
dFdk(2,2,2)=0.032111705_DP
dFdk(2,2,3)=0.000479055_DP
dFdk(2,2,4)=0.00051327_DP
dFdk(2,2,5)=0.000479049_DP
dFdk(2,2,6)=0.0004790495_DP
dFdk(2,2,7)=0.000479051_DP
dFdk(2,3,0)=-0.001414065_DP
dFdk(2,3,1)=-0.00902186_DP
dFdk(2,3,2)=-0.009021835_DP
dFdk(2,3,3)=-0.00902185_DP
dFdk(2,3,4)=-0.00451095_DP
dFdk(3,0,0)=0.055509_DP
dFdk(3,1,1)=-0.0063865_DP
dFdk(3,2,0)=-0.001414065_DP
dFdk(3,2,1)=-0.00902186_DP
dFdk(3,2,2)=-0.009021835_DP
dFdk(3,2,3)=-0.00902185_DP
dFdk(3,2,4)=-0.00451095_DP

#ifdef CHECK_TABLES
    call assert_equal(F, "FijkSiSi.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F    = 0.0_DP
    dFdi = 0.0_DP
    dFdj = 0.0_DP
    dFdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Fsisi_table



  !>
  ! Construct the Pcc-table
  !<
  subroutine rebo2x_default_Pcc_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP

    !
    ! Values from Table 8
    !

    P(1, 1, 0) = 0.003026697473481_DP
    P(2, 0, 0) = 0.007860700254745_DP
    P(3, 0, 0) = 0.016125364564267_DP
    P(1, 2, 0) = 0.003179530830731_DP
    P(2, 1, 0) = 0.006326248241119_DP

    ! New Silicon Pij values that affect C-C bonds - Table 3 Schall2012

    P(2, 0, 1) = 0.325945_DP
    P(0, 2, 1) = 0.832062_DP
    P(0, 0, 2) = 0.236272_DP
    P(0, 1, 2) = 0.57474_DP
    P(1, 0, 2) = 0.436777_DP
    P(0, 0, 3) = 0.740492_DP
    P(1, 1, 1) = 0.361792_DP
    P(0, 1, 1) = 0.160178_DP
    P(1, 0, 1) = 0.161117_DP
    P(0, 0, 1) = 0.1_DP

!-- Refit for proper graphen elastic constants
!    P(0, 2, 0 )  = g_graphene_P
!--

    ! For organosilicate molecules
    ! Table 4 of Schall, Harrison 2012
!    P(0, 2, 1) = 0.819496_DP
!    P(0, 0, 1) = -0.0428414_DP



! Insert dPCC derivatives here
! there are none.


#ifdef CHECK_TABLES
    call assert_equal(P, "PCC.dat", -1, -1, -1, .false.)
#endif

#ifdef ZERO_TABLES
    P    = 0.0_DP
    dPdi = 0.0_DP
    dPdj = 0.0_DP
    dPdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Pcc_table


  !>
  ! Construct the Pch-table
  !<
  subroutine rebo2x_default_Pch_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP

    !
    ! Values from Table 8
    !

    P(1, 0, 0)  =  0.2093367328250380_DP
    P(2, 0, 0)  = -0.064449615432525_DP
    P(3, 0, 0)  = -0.303927546346162_DP
    P(0, 1, 0)  =  0.01_DP
    P(0, 2, 0)  = -0.1220421462782555_DP
    P(1, 1, 0)  = -0.1251234006287090_DP
    P(2, 1, 0)  = -0.298905245783_DP
    P(0, 3, 0)  = -0.307584705066_DP
    P(1, 2, 0)  = -0.3005291724067579_DP

    !  Values from Table 3 - Schall2012
   
    P(0, 0, 1)  = 0.0389247_DP
    P(1, 0, 1)  = 0.0218147_DP
    P(2, 0, 1)  = -0.00706315_DP
    P(1, 0, 2)  = 0.0632173_DP
    P(1, 1, 1)  = 0.162972_DP
    P(0, 1, 2)  = 0.436777_DP
    P(0, 2, 1)  = 0.723583_DP
    P(0, 1, 1)  = 0.161117_DP

    ! For organosilicate molecules
    ! Table 4 of Schall, Harrison 2012
!    P(1, 0, 1)  = 0.0436295_DP
!    P(2, 0, 1)  = -0.0211895_DP

! Insert dPCH derivatives here
! there are none


#ifdef CHECK_TABLES
    call assert_equal(P, "PCH.dat", -1, -1, -1, .false.)
#endif

#ifdef ZERO_TABLES
    P    = 0.0_DP
    dPdi = 0.0_DP
    dPdj = 0.0_DP
    dPdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Pch_table


  !>
  ! Construct the Psic-table
  !<
  subroutine rebo2x_default_Psic_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP

    !
    ! Values from Table 3 - Schall2012
    !

    P(0, 0, 0) = -0.171604_DP
    P(1, 0, 0) = 0.0389247_DP
    P(2, 0, 0) = 0.0436295_DP
    P(3, 0, 0) = -0.0211895_DP
    P(2, 1, 0) = -0.0281849_DP
    P(2, 0, 1) = 0.0187852_DP
    P(0, 1, 0) = 0.493859_DP
! Does not exist in data file
!    P(0, 0, 1) = 0.166142_DP

    ! For organosilicate molecules
    ! Table 4 of Schall, Harrison 2012
!    P(2, 0, 0) = 0.0436295_DP
!    P(3, 0, 0) = -0.0211895_DP

! Insert the dPSiC derivatives here (type - 6)
dPdi(0,0,0)=0.01946235_DP
dPdi(1,0,0)=0.10761675_DP
dPdi(1,0,1)=0.0093926_DP
dPdi(1,1,0)=-0.26102195_DP
dPdi(2,0,0)=-0.0300571_DP
dPdi(3,0,0)=-0.02181475_DP
dPdi(3,0,1)=-0.0093926_DP
dPdi(3,1,0)=0.01409245_DP
dPdi(4,0,0)=0.01059475_DP

dPdj(0,0,0)=0.2469295_DP
dPdj(0,1,0)=0.085802_DP
dPdj(0,2,0)=-0.2469295_DP
dPdj(1,1,0)=-0.01946235_DP
dPdj(2,0,0)=-0.01409245_DP
dPdj(2,1,0)=-0.02181475_DP
dPdj(2,1,1)=-0.0093926_DP
dPdj(2,2,0)=0.01409245_DP
dPdj(3,1,0)=0.01059475_DP

dPdk(0,0,1)=0.085802_DP
dPdk(0,1,1)=-0.2469295_DP
dPdk(1,0,1)=-0.01946235_DP
dPdk(2,0,0)=0.0093926_DP
dPdk(2,0,1)=-0.02181475_DP
dPdk(2,0,2)=-0.0093926_DP
dPdk(2,1,1)=0.01409245_DP
dPdk(3,0,1)=0.01059475_DP

#ifdef CHECK_TABLES
    call assert_equal(P, "PSiC.dat", -1, -1, -1, .false.)
#endif

#ifdef ZERO_TABLES
    P    = 0.0_DP
    dPdi = 0.0_DP
    dPdj = 0.0_DP
    dPdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Psic_table


  !>
  ! Construct the Pcsi-table
  !<
  subroutine rebo2x_default_Pcsi_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP


    !
    ! Values from Table 3 - Schall2012
    !

    P(0, 0, 0) = -0.171604_DP
    P(1, 0, 0) =  0.0389247_DP
    P(2, 0, 0) =  0.0436295_DP
    P(3, 0, 0) = -0.0211895_DP
    P(2, 0, 1) =  0.0632173_DP
    P(2, 1, 0) =  0.325945_DP
    P(0, 3, 0) =  0.240817_DP
    P(0, 1, 1) =  0.118136_DP
    P(0, 2, 1) =  0.57474_DP
    P(1, 1, 1) =  0.218388_DP
    P(0, 1, 2) =  0.246831_DP
    P(1, 2, 0) =  0.723583_DP
    P(0, 2, 0) =  0.320357_DP
    P(1, 1, 0) =  0.161117_DP
    P(0, 1, 0) =  0.04_DP
    P(0, 0, 1) = -0.16218_DP

    ! For organosilicon molecules
    ! Table 4 of Schall, Harrison 2012
!    P(2, 0, 0) = 0.0436295_DP
!    P(3, 0, 0) = -0.0211895_DP
!    P(0, 3, 0) = 0.231988_DP
!    P(0, 1, 0) = -0.0428414_DP

! Insert dPCSi derivatives here, Schall 2013
dPdi(0,0,0)=0.01946235_DP
dPdi(0,1,0)=0.0805585_DP
dPdi(0,1,1)=0.109194_DP
dPdi(0,2,0)=0.3617915_DP
dPdi(1,0,0)=0.10761675_DP
dPdi(1,0,1)=0.11269865_DP
dPdi(1,1,0)=0.1629725_DP
dPdi(1,1,1)=-0.059068_DP
dPdi(1,1,2)=-0.1234155_DP
dPdi(1,2,0)=-0.1601785_DP
dPdi(1,2,1)=-0.28737_DP
dPdi(1,3,0)=-0.1204085_DP
dPdi(2,0,0)=-0.0300571_DP
dPdi(2,1,0)=-0.0805585_DP
dPdi(2,1,1)=-0.109194_DP
dPdi(2,2,0)=-0.3617915_DP
dPdi(3,0,0)=-0.02181475_DP
dPdi(3,0,1)=-0.03160865_DP
dPdi(3,1,0)=-0.1629725_DP
dPdi(4,0,0)=0.01059475_DP

dPdj(0,0,1)=0.059068_DP
dPdj(0,0,2)=0.1234155_DP
dPdj(0,1,0)=0.2459805_DP
dPdj(0,1,1)=0.36846_DP
dPdj(0,2,0)=0.1204085_DP
dPdj(0,2,1)=-0.059068_DP
dPdj(0,2,2)=-0.1234155_DP
dPdj(0,3,0)=-0.1601785_DP
dPdj(0,3,1)=-0.28737_DP
dPdj(0,4,0)=-0.1204085_DP
dPdj(1,0,0)=0.0805585_DP
dPdj(1,0,1)=0.109194_DP
dPdj(1,1,0)=0.34232915_DP
dPdj(1,2,0)=-0.0805585_DP
dPdj(1,2,1)=-0.109194_DP
dPdj(1,3,0)=-0.3617915_DP
dPdj(2,0,0)=0.1629725_DP
dPdj(2,1,0)=-0.02181475_DP
dPdj(2,1,1)=-0.03160865_DP
dPdj(2,2,0)=-0.1629725_DP
dPdj(3,1,0)=0.01059475_DP

dPdk(0,0,0)=-0.08109_DP
dPdk(0,0,1)=0.085802_DP
dPdk(0,0,2)=0.08109_DP
dPdk(0,1,0)=0.059068_DP
dPdk(0,1,1)=0.1234155_DP
dPdk(0,1,2)=-0.059068_DP
dPdk(0,1,3)=-0.1234155_DP
dPdk(0,2,0)=0.28737_DP
dPdk(0,2,1)=-0.1601785_DP
dPdk(0,2,2)=-0.28737_DP
dPdk(0,3,1)=-0.1204085_DP
dPdk(1,0,1)=-0.01946235_DP
dPdk(1,1,0)=0.109194_DP
dPdk(1,1,1)=-0.0805585_DP
dPdk(1,1,2)=-0.109194_DP
dPdk(1,2,1)=-0.3617915_DP
dPdk(2,0,0)=0.03160865_DP
dPdk(2,0,1)=-0.02181475_DP
dPdk(2,0,2)=-0.03160865_DP
dPdk(2,1,1)=-0.1629725_DP
dPdk(3,0,1)=0.01059475_DP

#ifdef CHECK_TABLES
    call assert_equal(P, "PCSi.dat", -1, -1, -1, .false.)
#endif

#ifdef ZERO_TABLES
    P    = 0.0_DP
    dPdi = 0.0_DP
    dPdj = 0.0_DP
    dPdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Pcsi_table


  !>
  ! Construct the Psih-table
  !<
  subroutine rebo2x_default_Psih_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP


    !
    ! Values from Table 3 - Schall2012
    !

    P(0, 0, 0) = 0.196923_DP
    P(1, 0, 0) = 0.217423_DP
    P(2, 0, 0) = 0.0426944_DP
    P(3, 0, 0) = 0.000670678_DP
    P(0, 0, 1) = 0.0423607_DP
    P(1, 0, 1) = 0.056059_DP
    P(2, 0, 1) = 0.0126435_DP
    P(1, 0, 2) = 0.0266661_DP
    P(0, 0, 3) = 0.0765396_DP
    P(0, 0, 2) = 0.101771_DP
    P(0, 1, 0) = 0.0389247_DP
    P(1, 1, 0) = 0.0218147_DP
    P(2, 1, 0) = -0.00706315_DP
    P(1, 1, 1) = 0.0093926_DP
    P(1, 2, 0) = -0.0281849_DP

    ! For organosilicate molecules
    ! Table 4 of Schall, Harrison 2012
!    P(1, 1, 0) = 0.0436295_DP
!    P(2, 1, 0) = -0.0211895_DP

! Insert dPSiH derivatives (type 5) here Schall 2013
dPdi(0,0,0)=0.1087115_DP
dPdi(0,0,1)=0.0280295_DP
dPdi(0,0,2)=0.01333305_DP
dPdi(0,1,0)=0.01090735_DP
dPdi(0,1,1)=0.0046963_DP
dPdi(0,2,0)=-0.01409245_DP
dPdi(1,0,0)=-0.0771143_DP
dPdi(1,0,1)=-0.0148586_DP
dPdi(1,0,2)=-0.0508855_DP
dPdi(1,0,3)=-0.0382698_DP
dPdi(1,1,0)=-0.022993925_DP
dPdi(2,0,0)=-0.108376161_DP
dPdi(2,0,1)=-0.0280295_DP
dPdi(2,0,2)=-0.01333305_DP
dPdi(2,1,0)=-0.01090735_DP
dPdi(2,1,1)=-0.0046963_DP
dPdi(2,2,0)=0.01409245_DP
dPdi(3,0,0)=-0.0213472_DP
dPdi(3,0,1)=-0.00632175_DP
dPdi(3,1,0)=0.003531575_DP
dPdi(4,0,0)=-0.000335339_DP

dPdj(0,0,0)=0.01946235_DP
dPdj(0,1,0)=-0.0984615_DP
dPdj(0,1,1)=-0.02118035_DP
dPdj(0,1,2)=-0.0508855_DP
dPdj(0,1,3)=-0.0382698_DP
dPdj(0,2,0)=-0.01946235_DP
dPdj(1,0,0)=0.01090735_DP
dPdj(1,0,1)=0.0046963_DP
dPdj(1,1,0)=-0.12280395_DP
dPdj(1,1,1)=-0.0280295_DP
dPdj(1,1,2)=-0.01333305_DP
dPdj(1,2,0)=-0.01090735_DP
dPdj(1,2,1)=-0.0046963_DP
dPdj(1,3,0)=0.01409245_DP
dPdj(2,0,0)=-0.003531575_DP
dPdj(2,1,0)=-0.0213472_DP
dPdj(2,1,1)=-0.00632175_DP
dPdj(2,2,0)=0.003531575_DP
dPdj(3,1,0)=-0.000335339_DP

dPdk(0,0,0)=0.02118035_DP
dPdk(0,0,1)=-0.047576_DP
dPdk(0,0,2)=0.01708945_DP
dPdk(0,0,3)=-0.0508855_DP
dPdk(0,0,4)=-0.0382698_DP
dPdk(0,1,1)=-0.01946235_DP
dPdk(1,0,0)=0.0280295_DP
dPdk(1,0,1)=-0.09537845_DP
dPdk(1,0,2)=-0.0280295_DP
dPdk(1,0,3)=-0.01333305_DP
dPdk(1,1,0)=0.0046963_DP
dPdk(1,1,1)=-0.01090735_DP
dPdk(1,1,2)=-0.0046963_DP
dPdk(1,2,1)=0.01409245_DP
dPdk(2,0,0)=0.00632175_DP
dPdk(2,0,1)=-0.0213472_DP
dPdk(2,0,2)=-0.00632175_DP
dPdk(2,1,1)=0.003531575_DP
dPdk(3,0,1)=-0.000335339_DP


#ifdef CHECK_TABLES
    call assert_equal(P, "PSiH.dat", -1, -1, -1, .false.)
#endif

#ifdef ZERO_TABLES
    P    = 0.0_DP
    dPdi = 0.0_DP
    dPdj = 0.0_DP
    dPdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Psih_table


  !>
  ! Construct the Psisi-table
  !<
  subroutine rebo2x_default_Psisi_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP

    !
    ! Values from Table 8
    !

    P(1, 0, 0)   = 0.0847214_DP
    P(2, 0, 0)   = 0.224236_DP
    P(3, 0, 0)   = 0.075861_DP
    P(2, 0, 1)   = 0.0533322_DP
    P(1, 0, 2)   = 0.0255132_DP
    P(1, 0, 1)   = 0.0508854_DP
    P(2, 1, 0)   = 0.0187852_DP
! This is missing from the data files
!    P(0, 1, 0)   = 0.166142_DP
    P(0, 4:6, 0) = -0.2_DP
    P(0, 3:5, 1) = -0.1_DP
    P(0, 2:4, 2) = -0.1_DP
    P(0, 1:3, 3) = -0.1_DP

! dP.dat type 4 PSiSi derivatives Schall 2013
dPdi(0,0,0)=0.0423607_DP
dPdi(0,0,1)=0.0254427_DP
dPdi(0,0,2)=0.0127566_DP
dPdi(1,0,0)=0.112118_DP
dPdi(1,0,1)=0.0266661_DP
dPdi(1,1,0)=0.0093926_DP
dPdi(2,0,0)=-0.0044302_DP
dPdi(2,0,1)=-0.0254427_DP
dPdi(2,0,2)=-0.0127566_DP
dPdi(3,0,0)=-0.112118_DP
dPdi(3,0,1)=-0.0266661_DP
dPdi(3,1,0)=-0.0093926_DP
dPdi(4,0,0)=-0.0379305_DP

dPdj(1,1,0)=-0.0423607_DP
dPdj(1,1,1)=-0.0254427_DP
dPdj(1,1,2)=-0.0127566_DP
dPdj(2,0,0)=0.0093926_DP
dPdj(2,1,0)=-0.112118_DP
dPdj(2,1,1)=-0.0266661_DP
dPdj(2,2,0)=-0.0093926_DP
dPdj(3,1,0)=-0.0379305_DP

dPdk(1,0,0)=0.0254427_DP
dPdk(1,0,1)=-0.0296041_DP
dPdk(1,0,2)=-0.0254427_DP
dPdk(1,0,3)=-0.0127566_DP
dPdk(2,0,0)=0.0266661_DP
dPdk(2,0,1)=-0.112118_DP
dPdk(2,0,2)=-0.0266661_DP
dPdk(2,1,1)=-0.0093926_DP
dPdk(3,0,1)=-0.0379305_DP


#ifdef CHECK_TABLES
    call assert_equal(P, "PSiSi.dat", -1, -1, -1, .false.)
#endif

#ifdef ZERO_TABLES
    P    = 0.0_DP
    dPdi = 0.0_DP
    dPdj = 0.0_DP
    dPdk = 0.0_DP
#endif

  endsubroutine rebo2x_default_Psisi_table


  !**********************************************************************
  ! Construct the Tcc-table
  !********************************************************************** 
  subroutine rebo2x_default_Tcc_table(T)
    implicit none

    real(DP), intent(out)  :: T(0:, 0:, 0:)

    ! ---

    T(0:, 0:, 0:)     = 0.0_DP


    !
    ! Values from Table 5
    !

    T(2, 2, 0)  = -0.070280085_DP
!    T(2, 2, 8)  = -0.00809675_DP

    T(2, 2, 1:8)  = -0.00809675_DP

#ifdef ZERO_TABLES
    T = 0.0_DP
#endif
    
  endsubroutine rebo2x_default_Tcc_table


  !>
  ! Check table against data stored in an external file
  !<
  subroutine assert_equal(tab, fn, o1, o2, o3, sym)
    implicit none

    real(DP),     intent(in)  :: tab(0:, 0:, 0:)
    character(*), intent(in)  :: fn
    integer,      intent(in)  :: o1, o2, o3
    logical,      intent(in)  :: sym

    ! ---

    integer  :: file
    integer  :: i, j, k
    real(DP) :: val

    logical  :: ex(0:size(tab,1)-1, 0:size(tab,2)-1, 0:size(tab,3)-1)

    ! ---

    file = fopen(fn, mode=F_READ)

    read (file, *)
    read (file, *)  i, j, k, val
    write (*, '(A)')  fn
    write (*, '(6I3)')  lbound(tab,1), ubound(tab,1), lbound(tab,2), ubound(tab,2), lbound(tab,3), ubound(tab,3)
    ex = .false.
    do while (i /= -1)
       write (*, '(3I3,3F15.7)')  i+o1, j+o2, k+o3, val, &
            tab(i+o1, j+o2, k+o3), val-tab(i+o1, j+o2, k+o3)
       if (ex(i+o1, j+o2, k+o3)) then
          write (*, '(A)')  "Warning: "//(i+o1)//" "//(j+o2)//" "//(k+o3)//" multiply defined."
       endif
       ex(i+o1, j+o2, k+o3) = .true.
       if (sym) then
          ex(j+o2, i+o1, k+o3) = .true.
       endif
       read (file, *)  i, j, k, val
    enddo

    do i = 0, size(tab,1)-1
       do j = 0, size(tab,2)-1
          do k = 0, size(tab,3)-1
             if (.not. ex(i,j,k) .and. tab(i,j,k) /= 0.0_DP) then
                write (*, '(A)')  "Entry "//(i-o1)//" "//(j-o2)//" "//(k-o3)//" has value "//tab(i,j,k)//" but does not exists in the file."
             endif
          enddo
       enddo
    enddo

    call fclose(file)

  endsubroutine assert_equal

endmodule rebo2x_default_tables

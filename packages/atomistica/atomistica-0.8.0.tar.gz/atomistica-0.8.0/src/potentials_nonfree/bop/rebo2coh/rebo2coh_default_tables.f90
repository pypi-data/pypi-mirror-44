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
!#define ZERO_TABLES

module rebo2coh_default_tables
  use supplib

  implicit none

contains

  !>
  ! Construct the Fcc-table
  !<
  subroutine rebo2coh_default_Fcc_table(F, dFdi, dFdj, dFdk)
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
    ! Some of these values are based on Table 4 in Brenner et al.,
    ! J. Phys. Condens. Matter 14 (2004) 783 but in many(!) cases there
    ! is no chance to get them from the literature. Reverse engineering
    ! the original code is the only possible way to get them...
    !

    F(0,0,2:8) =  0.0099172158_DP  ! reference code
    F(1,1,  0) =  0.105000_DP
    F(1,1,  1) = -0.0041775_DP
    F(1,1,2:8) = -0.0160856_DP
    F(2,2,  0) =  0.09444957_DP
    F(2,2,  1) =  0.02200000_DP
    F(2,2,  2) =  0.03970587_DP
    F(2,2,  3) =  0.03308822_DP
    F(2,2,  4) =  0.02647058_DP
    F(2,2,  5) =  0.01985293_DP
    F(2,2,  6) =  0.01323529_DP
    F(2,2,  7) =  0.00661764_DP
    F(2,2,  8) =  0.0_DP
    F(0,1,  0) =  0.04338699_DP
    F(0,1,1:8) =  0.0099172158_DP  ! reference code
    F(0,2,  0) =  0.0493976637_DP
    F(0,2,  1) = -0.011942669_DP
    F(0,2,2:8) =  0.0099172158_DP  ! reference code
    F(0,3,0:1) = -0.119798935_DP   ! reference code
    F(0,3,2:8) =  0.0099172158_DP  ! reference code
    F(0,4,0:1) = -0.119798935_DP   ! reference code
    F(0,4,2:8) =  0.0099172158_DP  ! reference code
    F(1,2,  0) =  0.0096495698_DP
    F(1,2,  1) =  0.030_DP
    F(1,2,  2) = -0.0200_DP
    F(1,2,  3) = -0.0233778774_DP
    F(1,2,  4) = -0.0267557548_DP
    F(1,2,5:8) = -0.030133632_DP
    F(1,3,1:8) = -0.124836752_DP
    ! F(2,1,6:8) --> see comment below
    F(2,3,0:8) = -0.044709383_DP

    dFdi(1,3,  1) = 0.03754477638199205_DP ! reference code
    dFdi(1,4,  1) = 0.03754477638199205_DP ! reference code
    dFdi(2,1,  0) = -0.052500_DP
    dFdi(2,1,4:8) = -0.054376_DP
    dFdi(2,3,  0) =  0.0_DP
    dFdi(2,3,1:5) =  0.062418_DP
    dFdi(2,4,1:8) =  0.062418_DP   ! reference code
    dFdk(2,2,3:7) = -0.006618_DP
    dFdi(2,3,6:8) =  0.062418_DP
    dFdk(1,1,  1) = -0.060543_DP
    dFdk(1,2,  3) = -0.020044_DP
    dFdk(1,2,  4) = -0.020044_DP

    !
    ! Symmetrize values
    !

    do k=0,8
       do i=0,2
          do j=i+1,4
             x = F(i,j,k) + F(j,i,k)
             F(i,j,k) = x
             F(j,i,k) = x

             x = dFdi(i,j,k) + dFdj(j,i,k)
             dFdi(i,j,k) = x
             dFdj(j,i,k) = x

             x = dFdi(j,i,k) + dFdj(i,j,k)
             dFdi(j,i,k) = x
             dFdj(i,j,k) = x

             x = dFdk(i,j,k) + dFdk(j,i,k)
             dFdk(i,j,k) = x
             dFdk(j,i,k) = x
          enddo
       enddo
    enddo

    do i=1,4
      do j=1,4
        do k=0,8
          if (i > 3) then
            F(i,j,k) = F(3,j,k)
          end if
        end do
      end do
    end do

    do i=1,4
      do j=1,4
        do k=0,8
          if (j > 3) then
            F(i,j,k) = F(i,3,k)
          end if
        end do
      end do
    end do


    !
    ! From the reference code:
    ! Values for F(2,1,6:8) differ from the symmetrizing
    ! scheme and are therefore set here...
    !
    F(2,1,6:8) = 0.0_DP


#ifdef CHECK_TABLES
    call assert_equal(F, "FijkCC.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Fcc_table


  !>
  ! Construct the Fch-table
  !<
  subroutine rebo2coh_default_Fch_table(F, dFdi, dFdj, dFdk)
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


    F(1,1,0:1) = -0.1_DP
    F(1,1,  2) = -0.6_DP
    F(1,1,3:8) = -0.1_DP
    F(1,2,1:2) = -0.5_DP
    F(1,3,  0) = -0.2_DP
    F(1,3,1:2) = -0.25_DP
    F(1,3,3:8) = -0.2_DP
    F(1,4,  0) = -0.2_DP
    F(1,4,1:2) = -0.25_DP
    F(1,4,3:8) = -0.2_DP

    F(0,2,4:8) = -0.0090477875161288110_DP


    !
    ! Symmetrize values
    !

    do k = 0, 8
       do i = 0, 2
          do j = i+1, 4

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
    F = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Fch_table


  !>
  ! Construct the Fhh-table
  !<
  subroutine rebo2coh_default_Fhh_table(F, dFdi, dFdj, dFdk)
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

#ifdef ZERO_TABLES
    F = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Fhh_table


  !>
  ! Construct the Foc-table
  !<
  subroutine rebo2coh_default_Foc_table(F, dFdi, dFdj, dFdk)
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


#ifdef CHECK_TABLES
    call assert_equal(F, "FijkOC.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Foc_table


  !>
  ! Construct the Foh-table
  !<
  subroutine rebo2coh_default_Foh_table(F, dFdi, dFdj, dFdk)
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



#ifdef CHECK_TABLES
    call assert_equal(F, "FijkOH.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Foh_table


  !>
  ! Construct the Foo-table
  !<
  subroutine rebo2coh_default_Foo_table(F, dFdi, dFdj, dFdk)
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


#ifdef CHECK_TABLES
    call assert_equal(F, "FijkOO.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Foo_table



  !>
  ! Construct the Pcc-table
  ! This function is used if there are no oxygen
  ! atoms in the vicinity of a C-C bond
  !<
  subroutine rebo2coh_default_Pcc_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP



    ! [ Brenner table 8 ]
    P(1,1) = 0.003026697473481309_DP
    P(2,0) = 0.007860700254745868_DP
    P(1,2) = 0.003179530830731258_DP
    P(2,1) = 0.006326248241119585_DP
    P(3,0) = 0.01612536456426738_DP


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pcc_table


  !>
  ! Construct the Pcc_o-table
  ! This function is used if there are oxygen
  ! atoms in the vicinity of a C-C bond
  !<
  subroutine rebo2coh_default_Pcc_o_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP



    ! [ reference code ]
    P(0,1) = 0.26322758289717174_DP
    P(0,2) = 0.18172173808666534_DP
    P(0,3) = -0.33812822082183042_DP
    P(1,1) = 0.0068975879892882921_DP
    P(1,2) = -0.14590703313216463_DP
    P(2,1) = -0.18833795634238631_DP

    ! [ reference code ]
    dPdi(1,1) = 0.5 * ( P(2,1) - P(0,1) )
    dPdi(1,0) = 0.5 * ( P(2,0) - P(0,0) )
    dPdi(2,0) = 0.5 * ( P(3,0) - P(1,0) )

    dPdj(1,1) = 0.5 * ( P(1,2) - P(1,0) )
    dPdj(0,1) = 0.5 * ( P(0,2) - P(0,0) )
    dPdj(0,2) = 0.5 * ( P(0,3) - P(0,1) )


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pcc_o_table


  !>
  ! Construct the Pch-table
  ! This function is used if there are no oxygen
  ! atoms in the vicinity of a C-H bond
  !<
  subroutine rebo2coh_default_Pch_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP


    ! [ Brenner table 8 ]
    P(0,1) = 0.01_DP
    P(0,2) = -0.122042146278256_DP
    P(0,3) = -0.307584705066552_DP
    P(1,0) = 0.209336732825038_DP
    P(1,1) = -0.125123400628709_DP
    P(2,1) = -0.298905249599898_DP  ! reference code
    P(1,2) = -0.300529172406758_DP
    P(2,0) = -0.06444961543252535_DP
    P(1,2) = -0.298905245782642_DP
    P(3,0) = -0.303927546346162_DP

    ! extracted from the reference code, not in the paper
    dPdi(1,1) = -0.154452622891321_DP
    dPdi(2,0) = -0.256632139585600_DP

    dPdj(0,2) = -0.158792352533276_DP
    dPdj(1,1) = -0.254932952615898_DP


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pch_table


  !>
  ! Construct the Pch_o-table
  ! This function is used if there are oxygen
  ! atoms in the vicinity of a C-H bond
  !<
  subroutine rebo2coh_default_Pch_o_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP


    ! [ reference code ]
    P(0, 1) = 0.33634981543859399_DP
    P(0, 2) = 0.63516806142203908_DP
    P(0, 3) = -0.50686982615829446_DP
    P(1, 1) = 0.19144348570035366_DP
    P(1, 2) = -0.14434919479893391_DP
    P(2, 1) = -0.35365613785081512_DP
    P(3, 1) = 1.0_DP

    ! [ reference code ]
    dPdi(1,1) = 0.5 * ( P(2,1) - P(0,1) )
    dPdi(1,0) = 0.5 * ( P(2,0) - P(0,0) )
    dPdi(2,0) = 0.5 * ( P(3,0) - P(1,0) )

    dPdj(1,1) = 0.5 * ( P(1,2) - P(1,0) )
    dPdj(0,1) = 0.5 * ( P(0,2) - P(0,0) )
    dPdj(0,2) = 0.5 * ( P(0,3) - P(0,1) )


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pch_o_table


  !>
  ! Construct the Phh-table
  !<
  subroutine rebo2coh_default_Phh_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP


    ! [ reference code ]
    P(0,1) =  0.01_DP
    P(0,2) = -0.122042153300129_DP
    P(0,3) = -0.307584728799839_DP
    P(1,0) =  0.209336733259995_DP
    P(1,1) = -0.125123428000094_DP
    P(1,2) = -0.300529121999318_DP
    P(2,0) = -0.06444960260022725_DP
    P(2,1) = -0.298905249599898_DP
    P(3,0) = -0.303927542800082_DP


    ! [ reference code ]
    dPdi(1,1) = -0.154452667200303_DP
    dPdi(2,0) = -0.256632129600170_DP

    dPdj(0,2) = -0.158792363300179_DP
    dPdj(1,1) = -0.254932972400184_DP


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Phh_table


  !>
  ! Construct the Poc-table
  !<
  subroutine rebo2coh_default_Poc_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---


    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP

    !
    ! [ Table 4 from Ni 2004 ]
    !

    P(:, :) = 19.057_DP                 ! Fix for overcoordinated oxygen
    P(0, 0) = -0.10215691047467139_DP   ! reference code
    P(0, 1) = 0.057125255608847153_DP   ! reference code
    P(0, 2) = 19.057_DP                 ! reference code
    P(0, 3) = 19.057_DP
    P(1, 0) = 0.37384717869475698_DP    ! reference code
    P(1, 1) = 19.057_DP
    P(1, 2) = 19.057_DP
    P(2, 0) = 19.057_DP
    P(2, 1) = 19.057_DP
    P(3, 0) = 19.057_DP

    ! [ reference code ]
    dPdi(1,1) = 0.5 * ( P(2,1) - P(0,1) )
    dPdi(2,0) = 0.5 * ( P(3,0) - P(1,0) )


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Poc_table


  !>
  ! Construct the Pco-table
  !<
  subroutine rebo2coh_default_Pco_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP


    ! [ reference code ]
    P(0, 0) = -0.49959316118488212_DP
    P(0, 1) = -0.13833764471605306_DP
    P(0, 2) = -0.11963189424243577_DP
    P(0, 3) = -0.19289035017487458_DP
    P(1, 0) = -0.20681692398078513_DP
    P(1, 1) = -0.24451392840821728_DP
    P(1, 2) = -0.075386271861458604_DP
    P(2, 0) = -0.18530763275453846_DP
    P(2, 1) = -0.20881444501255306_DP
    P(3, 0) = 0.58516357773566230_DP
    P(3, 1) = 12.5_DP

    ! [ reference code ]
    dPdi(1,1) = 0.5 * ( P(2,1) - P(0,1) )
    dPdi(1,0) = 0.5 * ( P(2,0) - P(0,0) )
    dPdi(2,0) = 0.5 * ( P(3,0) - P(1,0) )

    dPdj(1,1) = 0.5 * ( P(1,2) - P(1,0) )
    dPdj(0,1) = 0.5 * ( P(0,2) - P(0,0) )
    dPdj(0,2) = 0.5 * ( P(0,3) - P(0,1) )


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pco_table


  !>
  ! Construct the Poh-table
  !<
  subroutine rebo2coh_default_Poh_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    integer :: i,j,k

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP


    ! [ reference code ]
     P(0,0) = -0.02546910196542740_DP
     P(0,1) = -0.02210479229688644_DP
     P(0,2) =  0.07500000000000000_DP
     P(0,3) =  0.08200000000000000_DP
     P(1,0) = -0.01292102970182896_DP
     P(1,1) =  0.07500000000000000_DP
     P(1,2) =  0.08200000000000000_DP
     P(2,0) =  0.07500000000000000_DP
     P(2,1) =  0.08200000000000000_DP
     P(3,0) =  0.08200000000000000_DP

    ! [ reference code ]
    dPdi(1,1) = 0.5 * ( P(2,1) - P(0,1) )
    dPdi(1,0) = 0.5 * ( P(2,0) - P(0,0) )
    dPdi(2,0) = 0.5 * ( P(3,0) - P(1,0) )

    dPdj(1,1) = 0.5 * ( P(1,2) - P(1,0) )
    dPdj(0,1) = 0.5 * ( P(0,2) - P(0,0) )
    dPdj(0,2) = 0.5 * ( P(0,3) - P(0,1) )


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Poh_table


  !>
  ! Construct the Pho-table
  !<
  subroutine rebo2coh_default_Pho_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP


    ! [ reference code ]
    P(0,0) = -0.01900000000000000_DP


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pho_table


  !>
  ! Construct the Poo-table
  !<
  subroutine rebo2coh_default_Poo_table(P, dPdi, dPdj)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:)

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP

    !
    ! [ Table 4 from Ni 2004 ]
    !

    P(0,0)   = -0.031882500229465302_DP   ! reference code
    P(0,1)   = 0.019665671695954869_DP    ! reference code
    P(0,2)   = 0.062_DP
    P(0,3)   = 0.071_DP
    P(1,0)   = -0.0034852252855995043_DP  ! reference code
    P(1,1)   = 0.071_DP
    P(1,2)   = 0.071_DP
    P(2,0)   = 0.062_DP
    P(2,1)   = 0.071_DP
    P(3,0)   = 0.071_DP

     ! [ reference code ]
    dPdi(1,1) = 0.5 * ( P(2,1) - P(0,1) )
    dPdi(1,0) = 0.5 * ( P(2,0) - P(0,0) )
    dPdi(2,0) = 0.5 * ( P(3,0) - P(1,0) )

    dPdj(1,1) = 0.5 * ( P(1,2) - P(1,0) )
    dPdj(0,1) = 0.5 * ( P(0,2) - P(0,0) )
    dPdj(0,2) = 0.5 * ( P(0,3) - P(0,1) )


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Poo_table


  !**********************************************************************
  ! Construct the Tcc-table
  !********************************************************************** 
  subroutine rebo2coh_default_Tcc_table(T, dTdi, dTdj, dTdk)
    implicit none

    real(DP), intent(out)  :: T(0:, 0:, 0:)
    real(DP), intent(out)  :: dTdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dTdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dTdk(0:, 0:, 0:)

    ! ---

    T    = 0.0_DP
    dTdi = 0.0_DP
    dTdj = 0.0_DP
    dTdk = 0.0_DP


    !
    ! Values from Table 5
    !

    T(2, 2, 0)  = -0.070280085_DP
!    T(2, 2, 8)  = -0.00809675_DP

    T(2, 2, 1:8)  = -0.00809675_DP

     ! [ reference code ]
    dTdi(1,2,1) = -0.00404837500043698_DP
    dTdj(2,1,1) = -0.00404837500043698_DP

#ifdef ZERO_TABLES
    T = 0.0_DP
#endif
    
  endsubroutine rebo2coh_default_Tcc_table


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

endmodule rebo2coh_default_tables

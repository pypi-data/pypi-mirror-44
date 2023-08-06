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

module rebo2chx_default_tables
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


    ! [ Brenner table 4 ]
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
    F(0,1,  1) =  0.0099172158_DP
    F(0,1,1:8) =  0.0099172158_DP
    F(0,2,  0) =  0.0493976637_DP
    F(0,2,  1) = -0.011942669_DP
    F(0,2,2:8) = F(0, 1, 1)
    F(0,3,0:8) = -0.119798935_DP
    F(0,3,0:1) = -0.119798935_DP
    F(0,3,2:8) =  F(0, 1, 1)
    F(1,2,  0) =  0.0096495698_DP
    F(1,2,  1) =  0.030_DP
    F(1,2,  2) = -0.0200_DP
    F(1,2,  3) = -0.0233778774_DP
    F(1,2,  4) = -0.0267557548_DP
    F(1,2,5:8) = -0.030133632_DP
    F(1,3,1:8) = -0.124836752_DP
    F(2,3,0:8) = -0.044709383_DP


    do i = 3, 7
       F(2, 2, i) = F(2, 2, 2) + (i-2)*( F(2, 2, 8) - F(2, 2, 2) )/6
    enddo

    do i = 3, 4
       F(1, 2, i) = F(1, 2, 2) + (i-2)*( F(1, 2, 5) - F(1, 2, 2) )/3
    enddo

    dFdi(2,1,  0) = -0.052500_DP
    dFdi(2,1,4:8) = -0.054376_DP
    dFdi(2,3,  0) =  0.0_DP
    dFdi(2,3,1:5) =  0.062418_DP
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


    ! [ Brenner table 9 ]
    F(0,2,4:8) = -0.0090477875161288110_DP
    F(1,3,0:8) = -0.213_DP
    F(1,2,0:8) = -0.25_DP
    F(1,1,0:8) = -0.5_DP


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

    ! [ Brenner table 6 ]
    F(1,1,0) = 0.249831916_DP

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
    integer   :: stat

    ! ---

    F     = 0.0_DP
    dFdi  = 0.0_DP
    dFdj  = 0.0_DP
    dFdk  = 0.0_DP



    !
    ! Symmetrize values
    !

    do k = 0, 9
       do i = 0, 4
          do j = i+1, 4

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo


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



    !
    ! Symmetrize values
    !

    do k = 0, 9
       do i = 0, 4
          do j = i+1, 4

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo


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



    !
    ! Symmetrize values
    !

    do k = 0, 9
       do i = 0, 4
          do j = i+1, 4

             x = F(i, j, k) + F(j, i, k)
             F(i, j, k) = x
             F(j, i, k) = x

          enddo
       enddo
    enddo


#ifdef CHECK_TABLES
    call assert_equal(F, "FijkOO.dat", 0, 0, -1, .true.)
#endif

#ifdef ZERO_TABLES
    F = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Foo_table



  !>
  ! Construct the Pcc-table
  !<
  subroutine rebo2coh_default_Pcc_table(P, dPdi, dPdj, dPdk)
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


    ! [ Brenner table 8 ]
    P(1,1,0) = 0.003026697473481_DP
    P(2,0,0) = 0.007860700254745_DP
    P(3,0,0) = 0.016125364564267_DP
    P(1,2,0) = 0.003179530830731_DP
    P(2,1,0) = 0.006326248241119_DP

#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pcc_table



  !>
  ! Construct the Pch-table
  !<
  subroutine rebo2coh_default_Pch_table(P, dPdi, dPdj, dPdk)
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


    ! [ Brenner table 8 ]
    P(1,0,0) =  0.2093367328250380_DP
    P(2,0,0) = -0.064449615432525_DP
    P(3,0,0) = -0.303927546346162_DP
    P(0,1,0) =  0.01_DP
    P(0,2,0) = -0.1220421462782555_DP
    P(1,1,0) = -0.1251234006287090_DP
    P(2,1,0) = -0.298905245783_DP
    P(0,3,0) = -0.307584705066_DP
    P(1,2,0) = -0.3005291724067579_DP


#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pch_table



  !>
  ! Construct the Phh-table
  !<
  subroutine rebo2coh_default_Phh_table(P, dPdi, dPdj, dPdk)
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



#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Phh_table


  !>
  ! Construct the Poc-table
  !<
  subroutine rebo2coh_default_Poc_table(P, dPdi, dPdj, dPdk)
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



#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Poc_table


  !>
  ! Construct the Pco-table
  !<
  subroutine rebo2coh_default_Pco_table(P, dPdi, dPdj, dPdk)
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



#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pco_table


  !>
  ! Construct the Poh-table
  !<
  subroutine rebo2coh_default_Poh_table(P, dPdi, dPdj, dPdk)
    implicit none

    real(DP), intent(out)  :: P(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdi(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdj(0:, 0:, 0:)
    real(DP), intent(out)  :: dPdk(0:, 0:, 0:)

    ! ---

    integer :: i,j,k

    ! ---

    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP



#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Poh_table


  !>
  ! Construct the Pho-table
  !<
  subroutine rebo2coh_default_Pho_table(P, dPdi, dPdj, dPdk)
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



#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
#endif

  endsubroutine rebo2coh_default_Pho_table


  !>
  ! Construct the Poo-table
  !<
  subroutine rebo2coh_default_Poo_table(P, dPdi, dPdj, dPdk)
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



#ifdef ZERO_TABLES
    P     = 0.0_DP
    dPdi  = 0.0_DP
    dPdj  = 0.0_DP
    dPdk  = 0.0_DP
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


    ! [ Brenner table 5 ]
    T(2,2,0)   = -0.070280085_DP
    T(2,2,1:8) = -0.00809675_DP


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

endmodule rebo2chx_default_tables

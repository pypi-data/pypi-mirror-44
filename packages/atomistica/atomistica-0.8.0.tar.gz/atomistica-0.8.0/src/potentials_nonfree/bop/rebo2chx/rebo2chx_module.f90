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

  !>
  ! Initialize all input tables (this%in_*) with default values
  !<
  subroutine rebo2coh_init_default_database(this)
    implicit none

    type(BOP_TYPE), intent(inout) :: this

    ! ---

    if (.not. this%zero_tables) then
       call rebo2coh_default_Fcc_table(this%in_Fcc, this%in_dFccdi, this%in_dFccdj, &
            this%in_dFccdk)
       call rebo2coh_default_Fch_table(this%in_Fch, this%in_dFchdi, this%in_dFchdj, &
            this%in_dFchdk)
       call rebo2coh_default_Fhh_table(this%in_Fhh, this%in_dFhhdi, this%in_dFhhdj, &
            this%in_dFhhdk)
       call rebo2coh_default_Foc_table(this%in_Foc, this%in_dFocdi, &
            this%in_dFocdj, this%in_dFocdk)
       call rebo2coh_default_Foh_table(this%in_Foh, this%in_dFohdi, &
            this%in_dFohdj, this%in_dFohdk)
       call rebo2coh_default_Foo_table(this%in_Foo, this%in_dFoodi, &
            this%in_dFoodj, this%in_dFoodk)

       call rebo2coh_default_Pcc_table(this%in_Pcc, this%in_dPccdi, &
            this%in_dPccdj, this%in_dPccdk)
       call rebo2coh_default_Pch_table(this%in_Pch, this%in_dPchdi, &
            this%in_dPchdj, this%in_dPchdk)
       call rebo2coh_default_Phh_table(this%in_Phh, this%in_dPhhdi, &
            this%in_dPhhdj, this%in_dPhhdk)
       call rebo2coh_default_Poc_table(this%in_Poc, this%in_dPocdi, &
            this%in_dPocdj, this%in_dPocdk)
       call rebo2coh_default_Pco_table(this%in_Pco, this%in_dPcodi, &
            this%in_dPcodj, this%in_dPcodk)
       call rebo2coh_default_Poh_table(this%in_Poh, this%in_dPohdi, &
            this%in_dPohdj, this%in_dPohdk)
       call rebo2coh_default_Pho_table(this%in_Pho, this%in_dPhodi, &
            this%in_dPhodj, this%in_dPhodk)
       call rebo2coh_default_Poo_table(this%in_Poo, this%in_dPoodi, &
            this%in_dPoodj, this%in_dPoodk)

       call rebo2coh_default_Tcc_table(this%in_Tcc, this%in_dTccdi, this%in_dTccdj, &
            this%in_dTccdk)

    endif

  endsubroutine rebo2coh_init_default_database


#if defined(MDCORE_MONOLITHIC) || defined(MDCORE_PYTHON) || defined(LAMMPS)

  !>
  !! Constructor
  !!
  !! Constructor
  !<
  subroutine INIT_FUNC(this)
    implicit none

    type(BOP_TYPE), intent(inout)   :: this

    ! ---
    
    if (this%zero_tables) then
        this%in_Fcc = 0.0_DP
        this%in_dFccdi = 0.0_DP
        this%in_dFccdj = 0.0_DP
        this%in_dFccdk = 0.0_DP

        this%in_Fch = 0.0_DP
        this%in_dFchdi = 0.0_DP
        this%in_dFchdj = 0.0_DP
        this%in_dFchdk = 0.0_DP

        this%in_Fhh = 0.0_DP
        this%in_dFhhdi = 0.0_DP
        this%in_dFhhdj = 0.0_DP
        this%in_dFhhdk = 0.0_DP

        this%in_Foc = 0.0_DP
        this%in_dFocdi = 0.0_DP
        this%in_dFocdj = 0.0_DP
        this%in_dFocdk = 0.0_DP

        this%in_Foh = 0.0_DP
        this%in_dFohdi = 0.0_DP
        this%in_dFohdj = 0.0_DP
        this%in_dFohdk = 0.0_DP

        this%in_Foo = 0.0_DP
        this%in_dFoodi = 0.0_DP
        this%in_dFoodj = 0.0_DP
        this%in_dFoodk = 0.0_DP


        this%in_Pcc = 0.0_DP
        this%in_dPccdi = 0.0_DP
        this%in_dPccdj = 0.0_DP
        this%in_dPccdk = 0.0_DP

        this%in_Pch = 0.0_DP
        this%in_dPchdi = 0.0_DP
        this%in_dPchdj = 0.0_DP
        this%in_dPchdk = 0.0_DP

        this%in_Phh = 0.0_DP
        this%in_dPhhdi = 0.0_DP
        this%in_dPhhdj = 0.0_DP
        this%in_dPhhdk = 0.0_DP

        this%in_Poc = 0.0_DP
        this%in_dPocdi = 0.0_DP
        this%in_dPocdj = 0.0_DP
        this%in_dPocdk = 0.0_DP

        this%in_Pco = 0.0_DP
        this%in_dPcodi = 0.0_DP
        this%in_dPcodj = 0.0_DP
        this%in_dPcodk = 0.0_DP

        this%in_Poh = 0.0_DP
        this%in_dPohdi = 0.0_DP
        this%in_dPohdj = 0.0_DP
        this%in_dPohdk = 0.0_DP

        this%in_Pho = 0.0_DP
        this%in_dPhodi = 0.0_DP
        this%in_dPhodj = 0.0_DP
        this%in_dPhodk = 0.0_DP

        this%in_Poo = 0.0_DP
        this%in_dPoodi = 0.0_DP
        this%in_dPoodj = 0.0_DP
        this%in_dPoodk = 0.0_DP

        this%in_Tcc = 0.0_DP
        this%in_dTccdi = 0.0_DP
        this%in_dTccdj = 0.0_DP
        this%in_dTccdk = 0.0_DP
    endif

  endsubroutine INIT_FUNC

#else

  !>
  !! Constructor
  !!
  !! Constructor
  !<
  subroutine INIT_DEFAULT_FUNC(this, Fcc, dFdi, dFdj, dFdk, Fch, Fhh, Foc, &
       Foh, Foo, Pcc, Pch, Phh, Poc, Pco, Poh, Pho, Poo, Tcc, dTccdi, dTccdj, dTccdk, ierror)
    implicit none

    type(BOP_TYPE),  intent(inout)    :: this

    real(DP), optional, intent(in)    :: Fcc(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: dFdi(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: dFdj(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: dFdk(0:4, 0:4, 0:9)

    real(DP), optional, intent(in)    :: Fch(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: Fhh(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: Foc(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: Foh(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: Foo(0:4, 0:4, 0:9)

    real(DP), optional, intent(in)    :: Pcc(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Pch(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Phh(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Poc(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Pco(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Poh(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Pho(0:5, 0:5, 0:5)
    real(DP), optional, intent(in)    :: Poo(0:5, 0:5, 0:5)

    real(DP), optional, intent(in)    :: Tcc(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: dTccdi(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: dTccdj(0:4, 0:4, 0:9)
    real(DP), optional, intent(in)    :: dTccdk(0:4, 0:4, 0:9)

    integer,  optional, intent(inout) :: ierror


    ! ---

    call prlog("Warning: rebox2_*_init_default cannot yet accept derivatives for all tables. Please fix.")

    if (present(Fcc)) then
       if (present(dFdi)) then
          if (present(dFdj)) then
             if (present(dFdk)) then
                this%in_Fcc     = Fcc
                this%in_dFccdi  = dFdi
                this%in_dFccdj  = dFdj
                this%in_dFccdk  = dFdk
             else
                RAISE_ERROR("Please provide dFdi, dFdj and dFdk along Fcc.", ierror)
             endif
          else
             RAISE_ERROR("Please provide dFdi, dFdj and dFdk along Fcc.", ierror)
          endif
       else
          RAISE_ERROR("Please provide dFdi, dFdj and dFdk along Fcc.", ierror)
       endif
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Fcc_table(this%in_Fcc, this%in_dFccdi, &
               this%in_dFccdj, this%in_dFccdk)
       endif
    endif
    if (present(Fch)) then
       this%in_Fch  = Fch
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Fch_table(this%in_Fch, this%in_dFchdi, &
               this%in_dFchdj, this%in_dFchdk)
       endif
    endif
    if (present(Fhh)) then
       this%in_Fhh  = Fhh
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Fhh_table(this%in_Fhh, this%in_dFhhdi, &
               this%in_dFhhdj, this%in_dFhhdk)
       endif
    endif
    if (present(Foc)) then
       this%in_Foc = Foc
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Foc_table(this%in_Foc, this%in_dFocdi, &
               this%in_dFocdj, this%in_dFocdk)
       endif
    endif
   if (present(Foh)) then
       this%in_Foh = Foh
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Foh_table(this%in_Foh, this%in_dFohdi, &
               this%in_dFohdj, this%in_dFohdk)
       endif
    endif
   if (present(Foo)) then
       this%in_Foo = Foo
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Foo_table(this%in_Foo, this%in_dFoodi, &
               this%in_dFoodj, this%in_dFoodk)
       endif
    endif

    if (present(Pcc)) then
       this%in_Pcc  = Pcc
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Pcc_table(this%in_Pcc, this%in_dPccdi, &
               this%in_dPccdj, this%in_dPccdk)
       endif
    endif
    if (present(Pch)) then
       this%in_Pch  = Pch
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Pch_table(this%in_Pch, this%in_dPchdi, &
               this%in_dPchdj, this%in_dPchdk)
       endif
    endif
    if (present(Phh)) then
       this%in_Phh  = Phh
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Phh_table(this%in_Phh, this%in_dPhhdi, &
               this%in_dPhhdj, this%in_dPhhdk)
       endif
    endif
    if (present(Poc)) then
       this%in_Poc  = Poc
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Poc_table(this%in_Poc, this%in_dPocdi, &
               this%in_dPocdj, this%in_dPocdk)
       endif
    endif
    if (present(Pco)) then
       this%in_Pco  = Pco
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Pco_table(this%in_Pco, this%in_dPcodi, &
               this%in_dPcodj, this%in_dPcodk)
       endif
    endif
    if (present(Poh)) then
       this%in_Poh  = Poh
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Poh_table(this%in_Poh, this%in_dPohdi, &
               this%in_dPohdj, this%in_dPohdk)
       endif
    endif
    if (present(Pho)) then
       this%in_Pho  = Pho
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Pho_table(this%in_Pho, this%in_dPhodi, &
               this%in_dPhodj, this%in_dPhodk)
       endif
    endif
    if (present(Poo)) then
       this%in_Poo  = Poo
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Poo_table(this%in_Poo, this%in_dPoodi, &
               this%in_dPoodj, this%in_dPoodk)
       endif
    endif

    if (present(Tcc)) then
       this%in_Tcc    = Tcc
       this%in_dTccdi = dTccdi
       this%in_dTccdj = dTccdj
       this%in_dTccdk = dTccdk
    else
       if (.not. this%zero_tables) then
          call rebo2coh_default_Tcc_table(this%in_Tcc, this%in_dTccdi, &
               this%in_dTccdj, this%in_dTccdk)
       endif
    endif

  endsubroutine INIT_DEFAULT_FUNC

#endif


  !>
  !! Destructor
  !!
  !!
  !<
  subroutine DEL_FUNC(this)
    implicit none

    type(BOP_TYPE), intent(inout) :: this

    ! ---

    call rebo2coh_db_del(this)

    if (allocated(this%internal_el)) then
       deallocate(this%internal_el)
    endif

  endsubroutine DEL_FUNC


  subroutine BIND_TO_FUNC(this, p, nl, ierror)
    implicit none

    type(BOP_TYPE),    intent(inout) :: this
    type(particles_t), intent(inout) :: p
    type(neighbors_t), intent(inout) :: nl
    integer, optional, intent(inout) :: ierror

    ! ---

    integer   :: i, j
    real(DP)  :: c_cc, c_ch, c_hh, c_oc, c_oh, c_oo, c

    ! ---

    this%els = filter_from_string(this%elements, p, ierror)
    PASS_ERROR(ierror)

    call rebo2coh_db_init_with_parameters( &
         this, &
         this%in_Fcc,   this%in_dFccdi,   this%in_dFccdj,   this%in_dFccdk, &
         this%in_Fch,   this%in_dFchdi,   this%in_dFchdj,   this%in_dFchdk, &
         this%in_Fhh,   this%in_dFhhdi,   this%in_dFhhdj,   this%in_dFhhdk, &
         this%in_Foc,   this%in_dFocdi,   this%in_dFocdj,   this%in_dFocdk, &
         this%in_Foh,   this%in_dFohdi,   this%in_dFohdj,   this%in_dFohdk, &
         this%in_Foo,   this%in_dFoodi,   this%in_dFoodj,   this%in_dFoodk, &
         this%in_Pcc,   this%in_dPccdi,   this%in_dPccdj,   this%in_dPccdk, &
         this%in_Pch,   this%in_dPchdi,   this%in_dPchdj,   this%in_dPchdk, &
         this%in_Phh,   this%in_dPhhdi,   this%in_dPhhdj,   this%in_dPhhdk, &
         this%in_Poc,   this%in_dPocdi,   this%in_dPocdj,   this%in_dPocdk, &
         this%in_Pco,   this%in_dPcodi,   this%in_dPcodj,   this%in_dPcodk, &
         this%in_Poh,   this%in_dPohdi,   this%in_dPohdj,   this%in_dPohdk, &
         this%in_Pho,   this%in_dPhodi,   this%in_dPhodj,   this%in_dPhodk, &
         this%in_Poo,   this%in_dPoodi,   this%in_dPoodj,   this%in_dPoodk, & 
         this%in_Tcc,   this%in_dTccdi,   this%in_dTccdj,   this%in_dTccdk, &
         error=ierror)
    PASS_ERROR(ierror)

#ifdef SCREENING
    c_cc = sqrt(maxval(this%Cmax)) * maxval( [ this%cc_in_r2, this%cc_out_r2, this%cc_bo_r2, this%cc_nc_r2 ] )
    c_ch = sqrt(maxval(this%Cmax)) * maxval( [ this%ch_in_r2, this%ch_out_r2, this%ch_bo_r2, this%ch_nc_r2 ] )
    c_hh = sqrt(maxval(this%Cmax)) * maxval( [ this%hh_in_r2, this%hh_out_r2, this%hh_bo_r2, this%hh_nc_r2 ] )
    c_oc = sqrt(maxval(this%Cmax)) * maxval( [ this%oc_in_r2, this%oc_out_r2, this%oc_bo_r2, this%oc_nc_r2 ] )
    c_oh = sqrt(maxval(this%Cmax)) * maxval( [ this%oh_in_r2, this%oh_out_r2, this%oh_bo_r2, this%oh_nc_r2 ] )
    c_oo = sqrt(maxval(this%Cmax)) * maxval( [ this%oo_in_r2, this%oo_out_r2, this%oo_bo_r2, this%oo_nc_r2 ] )
!    c_cc = maxval(sqrt(this%C_dr_cut)) * maxval( [ this%cc_in_r2, this%cc_out_r2, this%cc_bo_r2, this%cc_nc_r2 ] )
!    c_ch = maxval(sqrt(this%C_dr_cut)) * maxval( [ this%ch_in_r2, this%ch_out_r2, this%ch_bo_r2, this%ch_nc_r2 ] )
!    c_hh = maxval(sqrt(this%C_dr_cut)) * maxval( [ this%hh_in_r2, this%hh_out_r2, this%hh_bo_r2, this%hh_nc_r2 ] )
!    c_oc = maxval(sqrt(this%C_dr_cut)) * maxval( [ this%oc_in_r2, this%oc_out_r2, this%oc_bo_r2, this%oc_nc_r2 ] )
!    c_oh = maxval(sqrt(this%C_dr_cut)) * maxval( [ this%oh_in_r2, this%oh_out_r2, this%oh_bo_r2, this%oh_nc_r2 ] )
!    c_oo = maxval(sqrt(this%C_dr_cut)) * maxval( [ this%oo_in_r2, this%oo_out_r2, this%oo_bo_r2, this%oo_nc_r2 ] )
#else
    c_cc = this%cc_in_r2
    c_ch = this%ch_in_r2
    c_hh = this%hh_in_r2
    c_oc = this%oc_in_r2
    c_oh = this%oh_in_r2
    c_oo = this%oo_in_r2
#endif

    do i = 1, p%nel
       do j = i, p%nel
          if (p%el2Z(i) == C_ .and. p%el2Z(j) == C_) then
             call request_interaction_range(nl, c_cc, i, j)
          else if ( &
               (p%el2Z(i) == C_ .and. p%el2Z(j) == H_) .or. &
               (p%el2Z(i) == H_ .and. p%el2Z(j) == C_) &
               ) then
             call request_interaction_range(nl, c_ch, i, j)
          else if (p%el2Z(i) == H_ .and. p%el2Z(j) == H_) then
             call request_interaction_range(nl, c_hh, i, j)
          else if ( &
               (p%el2Z(i) == O_ .and. p%el2Z(j) == C_) .or. &
               (p%el2Z(i) == C_ .and. p%el2Z(j) == O_) &
               ) then
             call request_interaction_range(nl, c_oc, i, j)
          else if ( &
               (p%el2Z(i) == O_ .and. p%el2Z(j) == H_) .or. &
               (p%el2Z(i) == H_ .and. p%el2Z(j) == O_) &
               ) then
             call request_interaction_range(nl, c_oh, i, j)
          else if (p%el2Z(i) == O_ .and. p%el2Z(j) == O_) then
             call request_interaction_range(nl, c_oo, i, j)
          endif
       enddo
    enddo

#ifdef SCREENING
    c = (2+maxval(sqrt(this%C_dr_cut)))*maxval( [ c_cc, c_ch, c_hh, c_oc, &
         c_oh, c_oo ] )
#else
    c = 3*maxval( [ c_cc, c_ch, c_hh, c_oc, c_oh, c_oo ] )
#endif
    call request_border(p, c)

    if (allocated(this%internal_el))  deallocate(this%internal_el)
    
    allocate(this%internal_el(p%maxnatloc))

  endsubroutine BIND_TO_FUNC


  !>
  !! Compute the force
  !!
  !! Compute the force
  !<
  subroutine COMPUTE_FUNC(this, p, nl, epot, f, wpot, epot_per_at, &
       epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, ierror)
    implicit none

    type(BOP_TYPE),     intent(inout) :: this
    type(particles_t),  intent(inout) :: p
    type(neighbors_t),  intent(inout) :: nl
    real(DP),           intent(inout) :: epot
    real(DP),           intent(inout) :: f(3, p%maxnatloc)  !< forces
    real(DP),           intent(inout) :: wpot(3, 3)
    real(DP), optional, intent(inout) :: epot_per_at(p%maxnatloc)
    real(DP), optional, intent(inout) :: epot_per_bond(nl%neighbors_size)
    real(DP), optional, intent(inout) :: f_per_bond(3, nl%neighbors_size)
#ifdef LAMMPS
    real(DP), optional, intent(inout) :: wpot_per_at(6, p%maxnatloc)
    real(DP), optional, intent(inout) :: wpot_per_bond(6, nl%neighbors_size)
#else
    real(DP), optional, intent(inout) :: wpot_per_at(3, 3, p%maxnatloc)
    real(DP), optional, intent(inout) :: wpot_per_bond(3, 3, nl%neighbors_size)
#endif
    integer,  optional, intent(inout) :: ierror

    ! ---

    integer  :: i

    ! ---

    call timer_start(BOP_NAME_STR // "_force")

    call update(nl, p, ierror)
    PASS_ERROR(ierror)

    if (size(this%internal_el) < p%maxnatloc) then
       deallocate(this%internal_el)
       allocate(this%internal_el(p%maxnatloc))
    endif

    this%internal_el = 0
    do i = 1, p%nat
       if (IS_EL(this%els, p, i)) then
          if (p%el2Z(p%el(i)) == C_) then
             this%internal_el(i) = rebo2_C_
          else if (p%el2Z(p%el(i)) == H_) then
             this%internal_el(i) = rebo2_H_
          else if (p%el2Z(p%el(i)) == O_) then
             this%internal_el(i) = rebo2_O_
           endif
       endif
    enddo


#ifdef LAMMPS
    call BOP_KERNEL( &
         this, &
         p%maxnatloc, p%natloc, p%nat, p%r_non_cyc, &
         p%tag, this%internal_el, &
         nl%seed, nl%last, nl%neighbors, nl%neighbors_size, &
         epot, f, wpot, &
         epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
         ierror)
#else
    call BOP_KERNEL( &
         this, p%Abox, &
         p%maxnatloc, p%natloc, p%nat, p%r_non_cyc, &
         this%internal_el, &
         nl%seed, nl%last, nl%neighbors, nl%neighbors_size, nl%dc, &
#ifndef PYTHON
         p%shear_dx, &
#endif
         epot, f, wpot, &
         epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
         ierror)
#endif
    PASS_ERROR(ierror)

    call timer_stop(BOP_NAME_STR // "_force")

  endsubroutine COMPUTE_FUNC


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
  subroutine rebo2sich_init_default_database(this)
    implicit none

    type(BOP_TYPE), intent(inout) :: this

    ! ---

    if (.not. this%zero_tables) then
       call rebo2sich_default_Fcc_table(this%in_Fcc, this%in_dFccdi, this%in_dFccdj, &
            this%in_dFccdk)
       call rebo2sich_default_Fch_table(this%in_Fch, this%in_dFchdi, this%in_dFchdj, &
            this%in_dFchdk)
       call rebo2sich_default_Fhh_table(this%in_Fhh, this%in_dFhhdi, this%in_dFhhdj, &
            this%in_dFhhdk)
       call rebo2sich_default_Fsic_table(this%in_Fsic, this%in_dFsicdi, &
            this%in_dFsicdj, this%in_dFsicdk)
       call rebo2sich_default_Fsih_table(this%in_Fsih, this%in_dFsihdi, &
            this%in_dFsihdj, this%in_dFsihdk)
       call rebo2sich_default_Fsisi_table(this%in_Fsisi, this%in_dFsisidi, &
            this%in_dFsisidj, this%in_dFsisidk)

       call rebo2sich_default_Pcc_table(this%in_Pcc, this%in_dPccdi, this%in_dPccdj, &
            this%in_dPccdk)
       call rebo2sich_default_Pch_table(this%in_Pch, this%in_dPchdi, this%in_dPchdj, &
            this%in_dPchdk)
       call rebo2sich_default_Pcsi_table(this%in_Pcsi, this%in_dPcsidi, &
            this%in_dPcsidj, this%in_dPcsidk)
       call rebo2sich_default_Psic_table(this%in_Psic, this%in_dPsicdi, &
            this%in_dPsicdj, this%in_dPsicdk)
       call rebo2sich_default_Psih_table(this%in_Psih, this%in_dPsihdi, &
            this%in_dPsihdj, this%in_dPsihdk)
       call rebo2sich_default_Psisi_table(this%in_Psisi, this%in_dPsisidi, &
            this%in_dPsisidj, this%in_dPsisidk)

       call rebo2sich_default_Tcc_table(this%in_Tcc)
    endif

  endsubroutine rebo2sich_init_default_database


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

        this%in_Fsic = 0.0_DP
        this%in_dFsicdi = 0.0_DP
        this%in_dFsicdj = 0.0_DP
        this%in_dFsicdk = 0.0_DP

        this%in_Fsih = 0.0_DP
        this%in_dFsihdi = 0.0_DP
        this%in_dFsihdj = 0.0_DP
        this%in_dFsihdk = 0.0_DP

        this%in_Fsisi = 0.0_DP
        this%in_dFsisidi = 0.0_DP
        this%in_dFsisidj = 0.0_DP
        this%in_dFsisidk = 0.0_DP


        this%in_Pcc = 0.0_DP
        this%in_dPccdi = 0.0_DP
        this%in_dPccdj = 0.0_DP
        this%in_dPccdk = 0.0_DP

        this%in_Pch = 0.0_DP
        this%in_dPchdi = 0.0_DP
        this%in_dPchdj = 0.0_DP
        this%in_dPchdk = 0.0_DP

        this%in_Psic = 0.0_DP
        this%in_dPsicdi = 0.0_DP
        this%in_dPsicdj = 0.0_DP
        this%in_dPsicdk = 0.0_DP

        this%in_Pcsi = 0.0_DP
        this%in_dPcsidi = 0.0_DP
        this%in_dPcsidj = 0.0_DP
        this%in_dPcsidk = 0.0_DP

        this%in_Psih = 0.0_DP
        this%in_dPsihdi = 0.0_DP
        this%in_dPsihdj = 0.0_DP
        this%in_dPsihdk = 0.0_DP

        this%in_Psisi = 0.0_DP
        this%in_dPsisidi = 0.0_DP
        this%in_dPsisidj = 0.0_DP
        this%in_dPsisidk = 0.0_DP

        this%in_Tcc = 0.0_DP
    endif

  endsubroutine INIT_FUNC


  !>
  !! Destructor
  !!
  !!
  !<
  subroutine DEL_FUNC(this)
    implicit none

    type(BOP_TYPE), intent(inout) :: this

    ! ---

    call rebo2sich_db_del(this)

    if (allocated(this%internal_el)) then
       deallocate(this%internal_el)
    endif

    if (allocated(this%Fij)) then
       deallocate(this%Fij)
    endif
    if (allocated(this%packed_Fij)) then
       deallocate(this%packed_Fij)
    endif
    if (allocated(this%Pij)) then
       deallocate(this%Pij)
    endif
    if (allocated(this%packed_Pij)) then
       deallocate(this%packed_Pij)
    endif
    if (allocated(this%Pji)) then
       deallocate(this%Pji)
    endif
    if (allocated(this%packed_Pji)) then
       deallocate(this%packed_Pji)
    endif
    if (allocated(this%bij)) then
       deallocate(this%bij)
    endif
    if (allocated(this%packed_bij)) then
       deallocate(this%packed_bij)
    endif
    if (allocated(this%bji)) then
       deallocate(this%bji)
    endif
    if (allocated(this%packed_bji)) then
       deallocate(this%packed_bji)
    endif
    if (allocated(this%baveij)) then
       deallocate(this%baveij)
    endif
    if (allocated(this%packed_baveij)) then
       deallocate(this%packed_baveij)
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
    real(DP)  :: c_cc, c_ch, c_hh, c_sic, c_sih, c_sisi, c

    ! ---

    this%els = filter_from_string(this%elements, p, ierror)
    PASS_ERROR(ierror)

    call rebo2sich_db_init_with_parameters( &
         this, &
         this%in_Fcc, this%in_dFccdi, this%in_dFccdj, this%in_dFccdk, &
         this%in_Fch, this%in_dFchdi, this%in_dFchdj, this%in_dFchdk, &
         this%in_Fhh, this%in_dFhhdi, this%in_dFhhdj, this%in_dFhhdk, &
         this%in_Fsic, this%in_dFsicdi, this%in_dFsicdj, this%in_dFsicdk, &
         this%in_Fsih, this%in_dFsihdi, this%in_dFsihdj, this%in_dFsihdk, &
         this%in_Fsisi, this%in_dFsisidi, this%in_dFsisidj, this%in_dFsisidk, &
         this%in_Pcc, this%in_dPccdi, this%in_dPccdj, this%in_dPccdk, &
         this%in_Pch, this%in_dPchdi, this%in_dPchdj, this%in_dPchdk, &
         this%in_Psic, this%in_dPsicdi, this%in_dPsicdj, this%in_dPsicdk, &
         this%in_Pcsi, this%in_dPcsidi, this%in_dPcsidj, this%in_dPcsidk, &
         this%in_Psih, this%in_dPsihdi, this%in_dPsihdj, this%in_dPsihdk, &
         this%in_Psisi, this%in_dPsisidi, this%in_dPsisidj, this%in_dPsisidk, & 
         this%in_Tcc, error=ierror)
    PASS_ERROR(ierror)

#ifdef SCREENING
    c_cc = max(maxval(sqrt(this%C_dr_cut)*this%cc_out_r2), maxval(sqrt(this%C_dr_cut)*this%cc_bo_r2), maxval(sqrt(this%C_dr_cut)*this%cc_nc_r2))
    c_ch = max(maxval(sqrt(this%C_dr_cut)*this%ch_out_r2), maxval(sqrt(this%C_dr_cut)*this%ch_bo_r2), maxval(sqrt(this%C_dr_cut)*this%ch_nc_r2))
    c_hh = max(maxval(sqrt(this%C_dr_cut)*this%hh_out_r2), maxval(sqrt(this%C_dr_cut)*this%hh_bo_r2), maxval(sqrt(this%C_dr_cut)*this%hh_nc_r2))
    c_sic = max(maxval(sqrt(this%C_dr_cut)*this%sic_out_r2), maxval(sqrt(this%C_dr_cut)*this%sic_bo_r2), maxval(sqrt(this%C_dr_cut)*this%sic_nc_r2))
    c_sih = max(maxval(sqrt(this%C_dr_cut)*this%sih_out_r2), maxval(sqrt(this%C_dr_cut)*this%sih_bo_r2), maxval(sqrt(this%C_dr_cut)*this%sih_nc_r2))
    c_sisi = max(maxval(sqrt(this%C_dr_cut)*this%sisi_out_r2), maxval(sqrt(this%C_dr_cut)*this%sisi_bo_r2), maxval(sqrt(this%C_dr_cut)*this%sisi_nc_r2))
#else
    c_cc = this%cc_in_r2
    c_ch = this%ch_in_r2
    c_hh = this%hh_in_r2
    c_sic = this%sic_in_r2
    c_sih = this%sih_in_r2
    c_sisi = this%sisi_in_r2
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
               (p%el2Z(i) == Si_ .and. p%el2Z(j) == C_) .or. &
               (p%el2Z(i) == C_ .and. p%el2Z(j) == Si_) &
               ) then
             call request_interaction_range(nl, c_sic, i, j)
          else if ( &
               (p%el2Z(i) == Si_ .and. p%el2Z(j) == H_) .or. &
               (p%el2Z(i) == H_ .and. p%el2Z(j) == Si_) &
               ) then
             call request_interaction_range(nl, c_sisi, i, j)
          else if (p%el2Z(i) == Si_ .and. p%el2Z(j) == Si_) then
             call request_interaction_range(nl, c_sisi, i, j)
          endif
       enddo
    enddo

#ifdef SCREENING
    c = (2+maxval(sqrt(this%C_dr_cut)))*maxval( [ c_cc, c_ch, c_hh, c_sic, &
         c_sih, c_sisi ] )
#else
    c = 3*maxval( [ c_cc, c_ch, c_hh, c_sic, c_sih, c_sisi ] )
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

    integer  :: i, nebmax, nebavg

    ! ---

    call timer_start(BOP_NAME_STR // "_force")

    call update(nl, p, ierror)
    PASS_ERROR(ierror)

    if (size(this%internal_el) < p%maxnatloc) then
       deallocate(this%internal_el)
       allocate(this%internal_el(p%maxnatloc))
    endif

    this%internal_el = 0
    nebmax = 0
    nebavg = 0
    do i = 1, p%nat
       if (IS_EL(this%els, p, i)) then
          if (p%el2Z(p%el(i)) == C_) then
             this%internal_el(i) = rebo2_C_
          else if (p%el2Z(p%el(i)) == H_) then
             this%internal_el(i) = rebo2_H_
          else if (p%el2Z(p%el(i)) == Si_) then
             this%internal_el(i) = rebo2_Si_
           endif
       endif
       nebmax = max(nebmax, nl%last(i)-nl%seed(i)+1)
       nebavg = nebavg + nl%last(i)-nl%seed(i)+1
    enddo
    nebavg = (nebavg+1)/p%nat+1

    if (this%introspection) then
       call resize(this%VA, nl%neighbors_size)
       call resize(this%VR, nl%neighbors_size)
       call resize(this%bij, nl%neighbors_size)
       call resize(this%bji, nl%neighbors_size)
       call resize(this%baveij, nl%neighbors_size)
       call resize(this%Fij, nl%neighbors_size)
       call resize(this%Pij, nl%neighbors_size)
       call resize(this%Pji, nl%neighbors_size)

       this%VA = 0.0_DP
       this%VR = 0.0_DP
       this%bij = 0.0_DP
       this%bji = 0.0_DP
       this%baveij = 0.0_DP
       this%Fij = 0.0_DP
       this%Pij = 0.0_DP
       this%Pji = 0.0_DP
    endif

#ifdef LAMMPS
    call BOP_KERNEL( &
         this, &
         p%maxnatloc, p%natloc, p%nat, p%r_non_cyc, &
         p%tag, this%internal_el, &
         nebmax, nebavg, nl%seed, nl%last, nl%neighbors, nl%neighbors_size, &
         epot, f, wpot, &
         epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
         ierror=ierror)
#else
    if (this%introspection) then
       call BOP_KERNEL( &
            this, p%Abox, &
            p%maxnatloc, p%natloc, p%nat, p%r_non_cyc, &
            this%internal_el, &
            nebmax, nebavg, nl%seed, nl%last, nl%neighbors, nl%neighbors_size, nl%dc, &
#ifndef PYTHON
            p%shear_dx, &
#endif
            epot, f, wpot, &
            epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
            this%VA, this%VR, this%bij, this%bji, this%baveij, &
            this%Fij, this%Pij, this%Pji, &
            ierror=ierror)

       i = get_number_of_all_neighbors(nl)
       call resize(this%packed_VA, i)
       call resize(this%packed_VR, i)
       call resize(this%packed_bij, i)
       call resize(this%packed_bji, i)
       call resize(this%packed_baveij, i)
       call resize(this%packed_Fij, i)
       call resize(this%packed_Pij, i)
       call resize(this%packed_Pji, i)
       call pack(nl, this%VA, this%packed_VA)
       call pack(nl, this%VR, this%packed_VR)
       call pack(nl, this%bij, this%packed_bij)
       call pack(nl, this%bji, this%packed_bji)
       call pack(nl, this%baveij, this%packed_baveij)
       call pack(nl, this%Fij, this%packed_Fij)
       call pack(nl, this%Pij, this%packed_Pij)
       call pack(nl, this%Pji, this%packed_Pji)
    else
       call BOP_KERNEL( &
            this, p%Abox, &
            p%maxnatloc, p%natloc, p%nat, p%r_non_cyc, &
            this%internal_el, &
            nebmax, nebavg, nl%seed, nl%last, nl%neighbors, nl%neighbors_size, nl%dc, &
#ifndef PYTHON
            p%shear_dx, &
#endif
            epot, f, wpot, &
            epot_per_at, epot_per_bond, f_per_bond, wpot_per_at, wpot_per_bond, &
            ierror=ierror)
    endif
#endif
    PASS_ERROR(ierror)

    call timer_stop(BOP_NAME_STR // "_force")

  endsubroutine COMPUTE_FUNC


  !>
  !! Return result of object introspection
  !<
  subroutine GET_DICT_FUNC(this, dict, error)
    implicit none

    type(BOP_TYPE), target, intent(inout) :: this        !< BOP object
    type(ptrdict_t),        intent(inout) :: dict
    integer,      optional, intent(out)   :: error       !< Error signals

    ! ---

    INIT_ERROR(error)

    if (allocated(this%packed_VA)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_VA), &
                                              size(this%packed_VA), &
                                              CSTR("VA"), &
                                              CSTR("VA"))
    endif
    if (allocated(this%packed_VR)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_VR), &
                                              size(this%packed_VR), &
                                              CSTR("VR"), &
                                              CSTR("VR"))
    endif
    if (allocated(this%packed_bij)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_bij), &
                                              size(this%packed_bij), &
                                              CSTR("bij"), &
                                              CSTR("bij"))
    endif
    if (allocated(this%packed_bji)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_bji), &
                                              size(this%packed_bji), &
                                              CSTR("bji"), &
                                              CSTR("bji"))
    endif
    if (allocated(this%packed_baveij)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_baveij), &
                                              size(this%packed_baveij), &
                                              CSTR("baveij"), &
                                              CSTR("baveij"))
    endif
    if (allocated(this%packed_Fij)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_Fij), &
                                              size(this%packed_Fij), &
                                              CSTR("Fij"), &
                                              CSTR("Fij"))
    endif
    if (allocated(this%packed_Pij)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_Pij), &
                                              size(this%packed_Pij), &
                                              CSTR("Pij"), &
                                              CSTR("Pij"))
    endif
    if (allocated(this%packed_Pji)) then
       call ptrdict_register_array1d_property(dict%ptrdict, &
                                              c_loc1(this%packed_Pji), &
                                              size(this%packed_Pji), &
                                              CSTR("Pji"), &
                                              CSTR("Pji"))
    endif

  endsubroutine GET_DICT_FUNC

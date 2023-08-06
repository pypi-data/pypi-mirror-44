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

  subroutine REGISTER_FUNC(this, cfg, m)
    use, intrinsic :: iso_c_binding

    implicit none

    type(BOP_TYPE), target      :: this
    type(c_ptr),    intent(in)  :: cfg
    type(c_ptr),    intent(out) :: m

    ! ---

    call init_default_database(this)

#ifdef SCREENING
    m = ptrdict_register_section(cfg, CSTR(BOP_STR), &
         CSTR("The screened 2nd generation REBO (Brenner 2002) potential for O-C-H (Schall-Harrison)."))
#else
    m = ptrdict_register_section(cfg, CSTR(BOP_STR), &
         CSTR("The 2nd generation REBO (Brenner 2002) potential for O-C-H (Schall-Harrison)."))
#endif

    call ptrdict_register_string_property(m, c_loc(this%elements), MAX_EL_STR, &
         CSTR("elements"), &
         CSTR("Elements for which to use this potential (default: O,C,H)."))

#ifdef SCREENING
    call ptrdict_register_real_property(m, c_loc(this%h_Cmin), CSTR("H_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for H."))
    call ptrdict_register_real_property(m, c_loc(this%h_Cmax), CSTR("H_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for H."))
    call ptrdict_register_real_property(m, c_loc(this%c_Cmin), CSTR("C_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for C."))
    call ptrdict_register_real_property(m, c_loc(this%c_Cmax), CSTR("C_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for C."))
    call ptrdict_register_real_property(m, c_loc(this%o_Cmin), &
         CSTR("O_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for O."))
    call ptrdict_register_real_property(m, c_loc(this%o_Cmax), &
         CSTR("O_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for O."))
#endif

!! ============ hhh Exponential parameters for BO term

    call ptrdict_register_real_property(m, c_loc(this%HHH_lambda), &
         CSTR("HHH_lambda"), CSTR("Lambda for H-H-H triples."))
    call ptrdict_register_real_property(m, c_loc(this%HCH_lambda), &
         CSTR("HCH_lambda"), CSTR("Lambda for H-C-H triples.."))
    call ptrdict_register_real_property(m, c_loc(this%HHC_lambda), &
         CSTR("HHC_lambda"), CSTR("Lambda for H-H-C triples.."))
    call ptrdict_register_real_property(m, c_loc(this%HCC_lambda), &
         CSTR("HCC_lambda"), CSTR("Lambda for H-C-C triples.."))

    call ptrdict_register_real_property(m, c_loc(this%CHH_lambda), &
         CSTR("CHH_lambda"), CSTR("Lambda for C-H-H triples."))
    call ptrdict_register_real_property(m, c_loc(this%CCH_lambda), &
         CSTR("CCH_lambda"), CSTR("Lambda for C-C-H triples.."))
    call ptrdict_register_real_property(m, c_loc(this%CHC_lambda), &
         CSTR("CHC_lambda"), CSTR("Lambda for C-H-C triples.."))
    call ptrdict_register_real_property(m, c_loc(this%CCC_lambda), &
         CSTR("CCC_lambda"), CSTR("Lambda for C-C-C triples.."))

    call ptrdict_register_real_property(m, c_loc(this%OHH_lambda), &
         CSTR("OHH_lambda"), CSTR("Lambda for O-H-H triples."))
    call ptrdict_register_real_property(m, c_loc(this%OCH_lambda), &
         CSTR("OCH_lambda"), CSTR("Lambda for O-C-H triples.."))
    call ptrdict_register_real_property(m, c_loc(this%OHC_lambda), &
         CSTR("OHC_lambda"), CSTR("Lambda for O-H-C triples.."))
    call ptrdict_register_real_property(m, c_loc(this%OCC_lambda), &
         CSTR("OCC_lambda"), CSTR("Lambda for O-C-C triples.."))

    call ptrdict_register_integer_property(m, c_loc(this%HHH_m), &
         CSTR("HHH_m"), CSTR("M for H-H-H triples."))
    call ptrdict_register_integer_property(m, c_loc(this%HCH_m), &
         CSTR("HCH_m"), CSTR("M for H-C-H triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%HHC_m), &
         CSTR("HHC_m"), CSTR("M for H-H-C triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%HCC_m), &
         CSTR("HCC_m"), CSTR("M for H-C-C triples.."))

    call ptrdict_register_integer_property(m, c_loc(this%CHH_m), &
         CSTR("CHH_m"), CSTR("M for C-H-H triples."))
    call ptrdict_register_integer_property(m, c_loc(this%CCH_m), &
         CSTR("CCH_m"), CSTR("M for C-C-H triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%CHC_m), &
         CSTR("CHC_m"), CSTR("M for C-H-C triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%CCC_m), &
         CSTR("CCC_m"), CSTR("M for C-C-C triples.."))

    call ptrdict_register_integer_property(m, c_loc(this%OHH_m), &
         CSTR("OHH_m"), CSTR("M for O-H-H triples."))
    call ptrdict_register_integer_property(m, c_loc(this%OCH_m), &
         CSTR("OCH_m"), CSTR("M for O-C-H triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%OHC_m), &
         CSTR("OHC_m"), CSTR("M for O-H-C triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%OCC_m), &
         CSTR("OCC_m"), CSTR("M for O-C-C triples.."))

!! ================= Added Some Parameters H-H =================

    call ptrdict_register_real_property(m, c_loc(this%hh_Q), &
         CSTR("HH_Q"), CSTR("Q for H-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_A), &
         CSTR("HH_A"), CSTR("A for H-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_alpha), &
         CSTR("HH_alpha"), CSTR("alpha for H-H interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%hh_B1), &
         CSTR("HH_B1"), CSTR("B1 for H-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_beta1), &
         CSTR("HH_beta1"), CSTR("beta1 for H-H interaction (inner)."))

!! ================= C-H Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%ch_Q), &
         CSTR("CH_Q"), CSTR("Q for C-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_A), &
         CSTR("CH_A"), CSTR("A for C-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_alpha), &
         CSTR("CH_alpha"), CSTR("alpha for C-H interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%ch_B1), &
         CSTR("CH_B1"), CSTR("B1 for C-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_beta1), &
         CSTR("CH_beta1"), CSTR("beta1 for C-H interaction (inner)."))

!! ================= C-C Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%cc_Q), &
         CSTR("CC_Q"), CSTR("Q for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_A), &
         CSTR("CC_A"), CSTR("A for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_alpha), &
         CSTR("CC_alpha"), CSTR("alpha for C-C interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%cc_B1), &
         CSTR("CC_B1"), CSTR("B1 for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_B2), &
         CSTR("CC_B2"), CSTR("B2 for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_B3), &
         CSTR("CC_B3"), CSTR("B3 for C-C interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%cc_beta1), &
         CSTR("CC_beta1"), CSTR("beta1 for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_beta2), &
         CSTR("CC_beta2"), CSTR("beta2 for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_beta3), &
         CSTR("CC_beta3"), CSTR("beta3 for C-C interaction (inner)."))

!! ================= O-H Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%oh_Q), &
         CSTR("OH_Q"), CSTR("Q for O-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_A), &
         CSTR("OH_A"), CSTR("A for O-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_alpha), &
         CSTR("OH_alpha"), CSTR("alpha for O-H interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%oh_B1), &
         CSTR("OH_B1"), CSTR("B1 for O-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_beta1), &
         CSTR("OH_beta1"), CSTR("beta1 for O-H interaction (inner)."))

!! ================= O-C Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%oc_Q), &
         CSTR("OC_Q"), CSTR("Q for O-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_A), &
         CSTR("OC_A"), CSTR("A for O-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_alpha), &
         CSTR("OC_alpha"), CSTR("alpha for O-C interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%oc_B1), &
         CSTR("OC_B1"), CSTR("B1 for O-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_beta1), &
         CSTR("OC_beta1"), CSTR("beta1 for O-C interaction (inner)."))

!! ================= O-O Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%oo_Q), &
         CSTR("OO_Q"), CSTR("Q for O-O interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_A), &
         CSTR("OO_A"), CSTR("A for O-O interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_alpha), &
         CSTR("OO_alpha"), CSTR("alpha for O-O interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%oo_B1), &
         CSTR("OO_B1"), CSTR("B1 for O-O interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_beta1), &
         CSTR("OO_beta1"), CSTR("beta1 for O-O interaction (inner)."))

!!===============================================================

    call ptrdict_register_real_property(m, c_loc(this%cc_in_r1), &
         CSTR("CC_in_r1"), CSTR("r1 for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_in_r2), &
         CSTR("CC_in_r2"), CSTR("r2 for C-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_in_r1), &
         CSTR("CH_in_r1"), CSTR("r1 for C-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_in_r2), &
         CSTR("CH_in_r2"), CSTR("r2 for C-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_in_r1), &
         CSTR("HH_in_r1"), CSTR("r1 for H-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_in_r2), &
         CSTR("HH_in_r2"), CSTR("r2 for H-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_in_r1), &
         CSTR("OO_in_r1"), CSTR("r1 for O-O interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_in_r2), &
         CSTR("OO_in_r2"), CSTR("r2 for O-O interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_in_r1), &
         CSTR("OH_in_r1"), CSTR("r1 for O-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_in_r2), &
         CSTR("OH_in_r2"), CSTR("r2 for O-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_in_r1), &
         CSTR("OC_in_r1"), CSTR("r1 for O-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_in_r2), &
         CSTR("OC_in_r2"), CSTR("r2 for O-C interaction (inner)."))

#ifdef SCREENING
    call ptrdict_register_real_property(m, c_loc(this%cc_out_r1), &
         CSTR("CC_out_r1"), CSTR("r1 for C-C interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_out_r2), &
         CSTR("CC_out_r2"),  CSTR("r2 for C-C interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_out_r1), &
         CSTR("CH_out_r1"), CSTR("r1 for C-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_out_r2), &
         CSTR("CH_out_r2"),  CSTR("r2 for C-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_out_r1), &
         CSTR("HH_out_r1"), CSTR("r1 for H-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_out_r2), &
         CSTR("HH_out_r2"),  CSTR("r2 for H-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_out_r1), &
         CSTR("OO_out_r1"), CSTR("r1 for O-O interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_out_r2), &
         CSTR("OO_out_r2"),  CSTR("r2 for O-O interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_out_r1), &
         CSTR("OH_out_r1"), CSTR("r1 for O-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_out_r2), &
         CSTR("OH_out_r2"),  CSTR("r2 for O-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_out_r1), &
         CSTR("OC_out_r1"), CSTR("r1 for O-C interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_out_r2), &
         CSTR("OC_out_r2"),  CSTR("r2 for O-C interaction (outer)."))

#ifdef NUM_NEIGHBORS
    call ptrdict_register_real_property(m, c_loc(this%cc_nc_r1), &
         CSTR("CC_nc_r1"), CSTR("r1 for C-C interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_nc_r2), &
         CSTR("CC_nc_r2"),  CSTR("r2 for C-C interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_nc_r1), &
         CSTR("CH_nc_r1"), CSTR("r1 for C-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_nc_r2), &
         CSTR("CH_nc_r2"),  CSTR("r2 for C-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_nc_r1), &
         CSTR("HH_nc_r1"), CSTR("r1 for H-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_nc_r2), &
         CSTR("HH_nc_r2"),  CSTR("r2 for H-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_nc_r1), &
         CSTR("OO_nc_r1"), CSTR("r1 for O-O interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%oo_nc_r2), &
         CSTR("OO_nc_r2"),  CSTR("r2 for O-O interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_nc_r1), &
         CSTR("OH_nc_r1"), CSTR("r1 for O-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%oh_nc_r2), &
         CSTR("OH_nc_r2"),  CSTR("r2 for O-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_nc_r1), &
         CSTR("OC_nc_r1"), CSTR("r1 for O-C interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%oc_nc_r2), &
         CSTR("OC_nc_r2"),  CSTR("r2 for O-C interaction (nc)."))
#endif
#endif

    call ptrdict_register_real_property(m, c_loc(this%hh_re), &
         CSTR("HH_re"), CSTR("re for H-H interaction."))
    call ptrdict_register_real_property(m, c_loc(this%ch_re), &
         CSTR("CH_re"), CSTR("re for C-H interaction."))
    call ptrdict_register_real_property(m, c_loc(this%oh_re), &
         CSTR("OH_re"), CSTR("re for O-H interaction."))
    call ptrdict_register_real_property(m, c_loc(this%cc_re), &
         CSTR("CC_re"), CSTR("re for C-C interaction."))

    call ptrdict_register_boolean_property(m, c_loc(this%with_dihedral), &
         CSTR("dihedral"), CSTR("Include the dihedral term?"))

    call ptrdict_register_boolean_property(m, c_loc(this%const_bo), &
         CSTR("const_bo"), CSTR("Set bond-order to unity (for debugging)"))
    call ptrdict_register_boolean_property(m, c_loc(this%const_nconj), &
         CSTR("const_nconj"), CSTR("Set nconj to zero (for debugging)"))
    call ptrdict_register_boolean_property(m, c_loc(this%no_outer_cutoff), &
         CSTR("no_outer_cutoff"), CSTR("Switch off outer cutoff function."))
         
    call ptrdict_register_boolean_property(m, c_loc(this%zero_tables), &
         CSTR("zero_tables"), CSTR("Initialize all tables to zero."))

    call ptrdict_register_array3d_property(m, c_loc111(this%in_Fcc), 5, 5, 10, &
         CSTR("Fcc"), CSTR("Fcc-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFccdi), 5, 5, 10, &
         CSTR("dFccdi"), CSTR("dFccdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFccdj), 5, 5, 10, &
         CSTR("dFccdj"), CSTR("dFccdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFccdk), 5, 5, 10, &
         CSTR("dFccdk"), CSTR("dFccdk"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Fch), 5, 5, 10, &
         CSTR("Fch"), CSTR("Fch-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFchdi), 5, 5, 10, &
         CSTR("dFchdi"), CSTR("dFchdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFchdj), 5, 5, 10, &
         CSTR("dFchdj"), CSTR("dFchdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFchdk), 5, 5, 10, &
         CSTR("dFchdk"), CSTR("dFchdk"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Fhh), 5, 5, 10, &
         CSTR("Fhh"), CSTR("Fhh-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFhhdi), 5, 5, 10, &
         CSTR("dFhhdi"), CSTR("dFhhdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFhhdj), 5, 5, 10, &
         CSTR("dFhhdj"), CSTR("dFhhdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFhhdk), 5, 5, 10, &
         CSTR("dFhhdk"), CSTR("dFhhdk"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Tcc), 5, 5, 10, &
         CSTR("Tcc"), CSTR("Tcc-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dTccdi), 5, 5, 10, &
         CSTR("dTccdi"), CSTR("dTccdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dTccdj), 5, 5, 10, &
         CSTR("dTccdj"), CSTR("dTccdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dTccdk), 5, 5, 10, &
         CSTR("dTccdk"), CSTR("dTccdk"))

    call ptrdict_register_real_property(m, c_loc(this%h_g), &
         CSTR("H_g"), CSTR("Constant angular term for H (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%c_g), &
         CSTR("C_g"), CSTR("Constant angular term for C (for debugging purposes). Needs to be > -0.5."))

    call ptrdict_register_real_property(m, c_loc(this%hh_bo), &
         CSTR("HH_bo"), CSTR("Constant bond-order for H-H (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%cc_bo), &
         CSTR("CC_bo"), CSTR("Constant bond-order for C-C (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%ch_bo), &
         CSTR("CH_bo"), CSTR("Constant bond-order for C-H (for debugging purposes). Needs to be > -0.5."))

!    call ptrdict_register_integer_property(m, nebmax, CSTR("nebmax"), CSTR("Internal neighbor list size."))
!    call ptrdict_register_integer_property(m, nebavg, CSTR("nebavg"), CSTR("Internal neighbor list size."))

  endsubroutine REGISTER_FUNC

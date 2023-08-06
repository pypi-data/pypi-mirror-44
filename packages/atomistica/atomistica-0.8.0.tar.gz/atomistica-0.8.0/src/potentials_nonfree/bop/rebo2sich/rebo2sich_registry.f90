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
         CSTR("The screened 2nd generation REBO (Brenner 2002) potential for Si-C-H (Schall-Harrison)."))
#else
    m = ptrdict_register_section(cfg, CSTR(BOP_STR), &
         CSTR("The 2nd generation REBO (Brenner 2002) potential for Si-C-H (Schall-Harrison)."))
#endif

    call ptrdict_register_string_property(m, c_loc(this%elements), MAX_EL_STR, &
         CSTR("elements"), &
         CSTR("Elements for which to use this potential (default: Si,C,H)."))

#ifdef SCREENING
    call ptrdict_register_real_property(m, c_loc(this%hh_Cmin), &
         CSTR("HH_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for H."))
    call ptrdict_register_real_property(m, c_loc(this%hh_Cmax), &
         CSTR("HH_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for H."))
    call ptrdict_register_real_property(m, c_loc(this%ch_Cmin), &
         CSTR("CH_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for C."))
    call ptrdict_register_real_property(m, c_loc(this%ch_Cmax), &
         CSTR("CH_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for C."))
    call ptrdict_register_real_property(m, c_loc(this%cc_Cmin), &
         CSTR("CC_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for C."))
    call ptrdict_register_real_property(m, c_loc(this%cc_Cmax), &
         CSTR("CC_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for C."))
    call ptrdict_register_real_property(m, c_loc(this%sih_Cmin), &
         CSTR("SiH_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for Si."))
    call ptrdict_register_real_property(m, c_loc(this%sih_Cmax), &
         CSTR("SiH_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for Si."))
    call ptrdict_register_real_property(m, c_loc(this%sic_Cmin), &
         CSTR("SiC_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for Si."))
    call ptrdict_register_real_property(m, c_loc(this%sic_Cmax), &
         CSTR("SiC_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for Si."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_Cmin), &
         CSTR("SiSi_Cmin"), &
         CSTR("Lower screening cut-off (should be >= 1) for Si."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_Cmax), &
         CSTR("SiSi_Cmax"), &
         CSTR("Upper screening cut-off (should be <= 3) for Si."))
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
    call ptrdict_register_real_property(m, c_loc(this%CSiSi_lambda), &
         CSTR("CSiSi_lambda"), CSTR("Lambda for C-Si-Si triples.."))

    call ptrdict_register_real_property(m, c_loc(this%SiHH_lambda), &
         CSTR("SiHH_lambda"), CSTR("Lambda for Si-H-H triples."))
    call ptrdict_register_real_property(m, c_loc(this%SiCH_lambda), &
         CSTR("SiCH_lambda"), CSTR("Lambda for Si-C-H triples.."))
    call ptrdict_register_real_property(m, c_loc(this%SiHC_lambda), &
         CSTR("SiHC_lambda"), CSTR("Lambda for Si-H-C triples.."))
    call ptrdict_register_real_property(m, c_loc(this%SiCC_lambda), &
         CSTR("SiCC_lambda"), CSTR("Lambda for Si-C-C triples.."))
    call ptrdict_register_real_property(m, c_loc(this%SiSiSi_lambda), &
         CSTR("SiSiSi_lambda"), CSTR("Lambda for Si-Si-Si triples.."))

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
    call ptrdict_register_integer_property(m, c_loc(this%CSiSi_m), &
         CSTR("CSiSi_m"), CSTR("M for C-Si-Si triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%CCSi_m), &
         CSTR("CCSi_m"), CSTR("M for C-C-Si triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%CSiC_m), &
         CSTR("CSiC_m"), CSTR("M for C-Si-C triples.."))

    call ptrdict_register_integer_property(m, c_loc(this%SiHH_m), &
         CSTR("SiHH_m"), CSTR("M for Si-H-H triples."))
    call ptrdict_register_integer_property(m, c_loc(this%SiCH_m), &
         CSTR("SiCH_m"), CSTR("M for Si-C-H triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%SiHC_m), &
         CSTR("SiHC_m"), CSTR("M for Si-H-C triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%SiCC_m), &
         CSTR("SiCC_m"), CSTR("M for Si-C-C triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%SiCSi_m), &
         CSTR("SiCSi_m"), CSTR("M for Si-C-Si triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%SiSiC_m), &
         CSTR("SiSiC_m"), CSTR("M for Si-Si-C triples.."))
    call ptrdict_register_integer_property(m, c_loc(this%SiSiSi_m), &
         CSTR("SiSiSi_m"), CSTR("M for Si-Si-Si triples.."))

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

!! ================= Si-H Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%sih_Q), &
         CSTR("SiH_Q"), CSTR("Q for Si-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_A), &
         CSTR("SiH_A"), CSTR("A for Si-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_alpha), &
         CSTR("SiH_alpha"), CSTR("alpha for Si-H interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%sih_B1), &
         CSTR("SiH_B1"), CSTR("B1 for Si-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_beta1), &
         CSTR("SiH_beta1"), CSTR("beta1 for Si-H interaction (inner)."))

!! ================= Si-C Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%sic_Q), &
         CSTR("SiC_Q"), CSTR("Q for Si-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_A), &
         CSTR("SiC_A"), CSTR("A for Si-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_alpha), &
         CSTR("SiC_alpha"), CSTR("alpha for Si-C interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%sic_B1), &
         CSTR("SiC_B1"), CSTR("B1 for Si-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_beta1), &
         CSTR("SiC_beta1"), CSTR("beta1 for Si-C interaction (inner)."))

!! ================= Si-Si Parameters ====================

    call ptrdict_register_real_property(m, c_loc(this%sisi_Q), &
         CSTR("SiSi_Q"), CSTR("Q for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_A), &
         CSTR("SiSi_A"), CSTR("A for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_alpha), &
         CSTR("SiSi_alpha"), CSTR("alpha for Si-Si interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%sisi_B1), &
         CSTR("SiSi_B1"), CSTR("B1 for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_B2), &
         CSTR("SiSi_B2"), CSTR("B2 for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_B3), &
         CSTR("SiSi_B3"), CSTR("B3 for Si-Si interaction (inner)."))

    call ptrdict_register_real_property(m, c_loc(this%sisi_beta1), &
         CSTR("SiSi_beta1"), CSTR("beta1 for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_beta2), &
         CSTR("SiSi_beta2"), CSTR("beta2 for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_beta3), &
         CSTR("SiSi_beta3"), CSTR("beta3 for Si-Si interaction (inner)."))

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
    call ptrdict_register_real_property(m, c_loc(this%sisi_in_r1), &
         CSTR("SiSi_in_r1"), CSTR("r1 for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_in_r2), &
         CSTR("SiSi_in_r2"), CSTR("r2 for Si-Si interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_in_r1), &
         CSTR("SiH_in_r1"), CSTR("r1 for Si-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_in_r2), &
         CSTR("SiH_in_r2"), CSTR("r2 for Si-H interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_in_r1), &
         CSTR("SiC_in_r1"), CSTR("r1 for Si-C interaction (inner)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_in_r2), &
         CSTR("SiC_in_r2"), CSTR("r2 for Si-C interaction (inner)."))

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
    call ptrdict_register_real_property(m, c_loc(this%sisi_out_r1), &
         CSTR("SiSi_out_r1"), CSTR("r1 for Si-Si interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_out_r2), &
         CSTR("SiSi_out_r2"),  CSTR("r2 for Si-Si interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_out_r1), &
         CSTR("SiH_out_r1"), CSTR("r1 for Si-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_out_r2), &
         CSTR("SiH_out_r2"),  CSTR("r2 for Si-H interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_out_r1), &
         CSTR("SiC_out_r1"), CSTR("r1 for Si-C interaction (outer)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_out_r2), &
         CSTR("SiC_out_r2"),  CSTR("r2 for Si-C interaction (outer)."))

    call ptrdict_register_real_property(m, c_loc(this%cc_bo_r1), &
         CSTR("CC_bo_r1"), CSTR("r1 for C-C interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%cc_bo_r2), &
         CSTR("CC_bo_r2"),  CSTR("r2 for C-C interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_bo_r1), &
         CSTR("CH_bo_r1"), CSTR("r1 for C-H interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%ch_bo_r2), &
         CSTR("CH_bo_r2"),  CSTR("r2 for C-H interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_bo_r1), &
         CSTR("HH_bo_r1"), CSTR("r1 for H-H interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%hh_bo_r2), &
         CSTR("HH_bo_r2"),  CSTR("r2 for H-H interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_bo_r1), &
         CSTR("SiSi_bo_r1"), CSTR("r1 for Si-Si interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_bo_r2), &
         CSTR("SiSi_bo_r2"),  CSTR("r2 for Si-Si interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_bo_r1), &
         CSTR("SiH_bo_r1"), CSTR("r1 for Si-H interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_bo_r2), &
         CSTR("SiH_bo_r2"),  CSTR("r2 for Si-H interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_bo_r1), &
         CSTR("SiC_bo_r1"), CSTR("r1 for Si-C interaction (bo)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_bo_r2), &
         CSTR("SiC_bo_r2"),  CSTR("r2 for Si-C interaction (bo)."))

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
    call ptrdict_register_real_property(m, c_loc(this%sisi_nc_r1), &
         CSTR("SiSi_nc_r1"), CSTR("r1 for Si-Si interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_nc_r2), &
         CSTR("SiSi_nc_r2"),  CSTR("r2 for Si-Si interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_nc_r1), &
         CSTR("SiH_nc_r1"), CSTR("r1 for Si-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%sih_nc_r2), &
         CSTR("SiH_nc_r2"),  CSTR("r2 for Si-H interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_nc_r1), &
         CSTR("SiC_nc_r1"), CSTR("r1 for Si-C interaction (nc)."))
    call ptrdict_register_real_property(m, c_loc(this%sic_nc_r2), &
         CSTR("SiC_nc_r2"),  CSTR("r2 for Si-C interaction (nc)."))
#endif
#endif

    call ptrdict_register_real_property(m, c_loc(this%hh_re), &
         CSTR("HH_re"), CSTR("re for H-H interaction."))
    call ptrdict_register_real_property(m, c_loc(this%ch_re), &
         CSTR("CH_re"), CSTR("re for C-H interaction."))
    call ptrdict_register_real_property(m, c_loc(this%sih_re), &
         CSTR("SiH_re"), CSTR("re for Si-H interaction."))
    call ptrdict_register_real_property(m, c_loc(this%cc_re), &
         CSTR("CC_re"), CSTR("re for C-C interaction."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_re), &
         CSTR("SiSi_re"), CSTR("re for Si-Si interaction."))
    call ptrdict_register_real_property(m, c_loc(this%sic_re), &
         CSTR("SiC_re"), CSTR("re for Si-C interaction."))

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
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Fsisi), 5, 5, 10, &
         CSTR("Fsisi"), CSTR("Fsisi-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFsisidi), 5, 5, 10, &
         CSTR("dFsisidi"), CSTR("dFsisidi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFsisidj), 5, 5, 10, &
         CSTR("dFsisidj"), CSTR("dFsisidj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFsisidk), 5, 5, 10, &
         CSTR("dFsisidk"), CSTR("dFsisidk"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Fsih), 5, 5, 10, &
         CSTR("Fsih"), CSTR("Fsih-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFsihdi), 5, 5, 10, &
         CSTR("dFsihdi"), CSTR("dFsihdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFsihdj), 5, 5, 10, &
         CSTR("dFsihdj"), CSTR("dFsihdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dFsihdk), 5, 5, 10, &
         CSTR("dFsihdk"), CSTR("dFsihdk"))

    call ptrdict_register_array3d_property(m, c_loc111(this%in_Pcc), 6, 6, 6, &
         CSTR("Pcc"), CSTR("Pcc-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPccdi), 6, 6, 6, &
         CSTR("dPccdi"), CSTR("dPccdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPccdj), 6, 6, 6, &
         CSTR("dPccdj"), CSTR("dPccdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPccdk), 6, 6, 6, &
         CSTR("dPccdk"), CSTR("dPccdk"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Pch), 6, 6, 6, &
         CSTR("Pch"), CSTR("Pch-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPchdi), 6, 6, 6, &
         CSTR("dPchdi"), CSTR("dPchdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPchdj), 6, 6, 6, &
         CSTR("dPchdj"), CSTR("dPchdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPchdk), 6, 6, 6, &
         CSTR("dPchdk"), CSTR("dPchdk"))

    call ptrdict_register_array3d_property(m, c_loc111(this%in_Psisi), 6, 6, 6, &
         CSTR("Psisi"), CSTR("Psisi-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPsisidi), 6, 6, 6, &
         CSTR("dPsisidi"), CSTR("dPsisidi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPsisidj), 6, 6, 6, &
         CSTR("dPsisidj"), CSTR("dPsisidj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPsisidk), 6, 6, 6, &
         CSTR("dPsisidk"), CSTR("dPsisidk"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_Psih), 6, 6, 6, &
         CSTR("Psih"), CSTR("Psih-table"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPsihdi), 6, 6, 6, &
         CSTR("dPsihdi"), CSTR("dPsihdi"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPsihdj), 6, 6, 6, &
         CSTR("dPsihdj"), CSTR("dPsihdj"))
    call ptrdict_register_array3d_property(m, c_loc111(this%in_dPsihdk), 6, 6, 6, &
         CSTR("dPsihdk"), CSTR("dPsihdk"))

    call ptrdict_register_array3d_property(m, c_loc111(this%in_Tcc), 5, 5, 10, &
         CSTR("Tcc"), CSTR("Tcc-table"))

    call ptrdict_register_real_property(m, c_loc(this%h_g), &
         CSTR("H_g"), CSTR("Constant angular term for H (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%c_g), &
         CSTR("C_g"), CSTR("Constant angular term for C (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%si_g), &
         CSTR("Si_g"), CSTR("Constant angular term for Si (for debugging purposes). Needs to be > -0.5."))

    call ptrdict_register_real_property(m, c_loc(this%hh_bo), &
         CSTR("HH_bo"), CSTR("Constant bond-order for H-H (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%cc_bo), &
         CSTR("CC_bo"), CSTR("Constant bond-order for C-C (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%ch_bo), &
         CSTR("CH_bo"), CSTR("Constant bond-order for C-H (for debugging purposes). Needs to be > -0.5."))
    call ptrdict_register_real_property(m, c_loc(this%sisi_bo), &
         CSTR("SiSi_bo"), CSTR("Constant bond-order for C-C (for debugging purposes). Needs to be > -0.5."))

#ifdef DIHEDRAL_SIN_CUTOFF
    call ptrdict_register_real_property(m, c_loc(this%dh_sin1), &
         CSTR("dh_sin1"), CSTR("Min value where cutoff procedure start."))
    call ptrdict_register_real_property(m, c_loc(this%dh_sin2), &
         CSTR("dh_sin2"), CSTR("Max value where cutoff procedure stops."))
#endif

    call ptrdict_register_boolean_property(m, c_loc(this%introspection), &
         CSTR("introspection"), CSTR("Enable object introspection"))

!    call ptrdict_register_integer_property(m, nebmax, CSTR("nebmax"), CSTR("Internal neighbor list size."))
!    call ptrdict_register_integer_property(m, nebavg, CSTR("nebavg"), CSTR("Internal neighbor list size."))

  endsubroutine REGISTER_FUNC

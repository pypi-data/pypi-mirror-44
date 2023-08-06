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

! @meta
!    private
!    dependencies:rebo2coh_default_tables.f90
!    classtype:rebo2coh_scr_t classname:Rebo2cohScr interface:potentials
! @endmeta


#include "macros.inc"
#include "filter.inc"

module rebo2coh_scr
  use, intrinsic :: iso_c_binding

  use supplib

  use particles
  use filter
  use neighbors

  use table2d
  use table3d
  use table4d

  use rebo2coh_default_tables

  implicit none

  private

#define DIHEDRAL
#define SCREENING

!#define ALT_DIHEDRAL
!#define SEPARATE_H_ARGUMENTS

! Enable neighbor and conjugation count, i.e. enable P and F tables
#define NUM_NEIGHBORS
! Use separate conjugation variables for both atoms that participate in a bond
!#define SEP_NCONJ
! Use exponential cut-offs
!#define EXP_CUT

! The value below are replaced by the preprocessor. This makes it easier to
! compile the module with different setting into a single code.
#define BOP_NAME             rebo2coh_scr
#define BOP_NAME_STR         "rebo2coh_scr"
#define BOP_STR              "Rebo2cohScr"
#define BOP_KERNEL           rebo2coh_scr_kernel
#define BOP_TYPE             rebo2coh_scr_t

#define REGISTER_FUNC        rebo2coh_scr_register
#define INIT_FUNC            rebo2coh_scr_init
#define INIT_DEFAULT_FUNC    rebo2coh_scr_init_default
#define DEL_FUNC             rebo2coh_scr_del
#define BIND_TO_FUNC         rebo2coh_scr_bind_to
#define COMPUTE_FUNC         rebo2coh_scr_energy_and_forces

#include "rebo2coh_type.f90"

contains

#include "rebo2coh_db.f90"

#include "rebo2coh_module.f90"

#include "bop_kernel_rebo2coh.f90"

#include "rebo2coh_func.f90"

#include "rebo2coh_registry.f90"

endmodule rebo2coh_scr

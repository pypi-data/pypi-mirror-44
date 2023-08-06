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
!    dependencies:rebo2chx_default_tables.f90
!    classtype:rebo2chx_t classname:Rebo2chx interface:potentials
!    features:per_at,per_bond
! @endmeta


#include "macros.inc"
#include "filter.inc"

module rebo2chx
  use, intrinsic :: iso_c_binding

  use supplib

  use particles
  use filter
  use neighbors

  use table2d
  use table3d
  use table4d

  use rebo2chx_default_tables

#ifdef _MP
  use parallel_3d
#endif

  implicit none

  private

!#define DIHEDRAL

#define NUM_NEIGHBORS


! The value below are replaced by the preprocessor. This makes it easier to
! compile the module with different setting into a single code.
#define BOP_NAME       rebo2chx
#define BOP_NAME_STR   "rebo2chx"
#define BOP_STR        "Rebo2chx"
#define BOP_KERNEL     rebo2chx_kernel
#define BOP_TYPE       rebo2chx_t

#define REGISTER_FUNC        rebo2chx_register
#define INIT_FUNC            rebo2chx_init
#define INIT_DEFAULT_FUNC    rebo2chx_init_default
#define DEL_FUNC             rebo2chx_del
#define BIND_TO_FUNC         rebo2chx_bind_to
#define COMPUTE_FUNC         rebo2chx_energy_and_forces


#include "rebo2chx_type.f90"

contains

#include "rebo2chx_db.f90"

#include "rebo2chx_module.f90"

#include "bop_kernel_rebo2chx.f90"

#include "rebo2chx_func.f90"

#include "rebo2chx_registry.f90"

endmodule rebo2chx

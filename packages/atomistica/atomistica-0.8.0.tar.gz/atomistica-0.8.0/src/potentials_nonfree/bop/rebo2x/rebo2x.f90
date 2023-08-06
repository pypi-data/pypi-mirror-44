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
!    dependencies:rebo2x_default_tables.f90
!    classtype:rebo2x_t classname:Rebo2x interface:potentials
! @endmeta

!>
!! The screened second generation reactive empirical bond-order potential
!! (REBO2+S)
!!
!! The screened second generation reactive empirical bond-order potential
!! The screened second generation reactive empirical bond-order potential
!! (REBO2+S), including a parameterization for silicon.
!! See: Brenner et al., J. Phys.: Condens. Matter 14, 783 (2002)
!! Pastewka, Pou, Perez, Gumbsch, Moseler, Phys. Rev. B 78, 161402(R) (2008)
!! Schall, Harrison, J. Phys. Chem. C 117, 1323 (2013)
!! Pastewka, Klemenz, Gumbsch, Moseler, Phys. Rev. B 87, 205410 (2013)
!<

#include "macros.inc"
#include "filter.inc"

module rebo2x
  use, intrinsic :: iso_c_binding

  use supplib

  use particles
  use filter
  use neighbors

  use table2d
  use table3d
  use table4d

  use rebo2x_default_tables

  implicit none

  private

#define SCREENING

!#define ALT_DIHEDRAL
#define SEPARATE_H_ARGUMENTS

! Enable neighbor and conjugation count, i.e. enable P and F tables
#define NUM_NEIGHBORS
! Use separate conjugation variables for both atoms that participate in a bond
#define SEP_NCONJ
! Use exponential cut-offs
!#define EXP_CUT

! The value below are replaced by the preprocessor. This makes it easier to
! compile the module with different setting into a single code.
#define BOP_NAME             rebo2x
#define BOP_NAME_STR         "rebo2x"
#define BOP_STR              "Rebo2x"
#define BOP_KERNEL           rebo2x_kernel
#define BOP_TYPE             rebo2x_t

#define REGISTER_FUNC        rebo2x_register
#define INIT_FUNC            rebo2x_init
#define INIT_DEFAULT_FUNC    rebo2x_init_default
#define DEL_FUNC             rebo2x_del
#define BIND_TO_FUNC         rebo2x_bind_to
#define COMPUTE_FUNC         rebo2x_energy_and_forces

#include "rebo2x_type.f90"

contains

#include "rebo2x_db.f90"

#include "rebo2x_module.f90"

#define cut_bo_h cut_out_h
#include "bop_kernel_rebo2x.f90"

#include "rebo2x_func.f90"

#include "rebo2x_registry.f90"

endmodule rebo2x

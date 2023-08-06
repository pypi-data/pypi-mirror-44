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
!    dependencies:rebo2sich_default_tables.f90
!    classtype:rebo2sich_scr_t classname:Rebo2SiCHScr interface:potentials
!    features:per_at,per_bond
! @endmeta

!>
!! The screened second generation reactive empirical bond-order potential
!! (REBO2+S)
!!
!! The screened second generation reactive empirical bond-order potential
!! (REBO2+S), including a parameterization for silicon.
!! See: Brenner et al., J. Phys.: Condens. Matter 14, 783 (2002)
!! Pastewka, Pou, Perez, Gumbsch, Moseler, Phys. Rev. B 78, 161402(R) (2008)
!! Schall, Harrison, J. Phys. Chem. C 117, 1323 (2013)
!! Pastewka, Klemenz, Gumbsch, Moseler, Phys. Rev. B 87, 205410 (2013)
!<

#include "macros.inc"
#include "filter.inc"

module rebo2sich_scr
  use, intrinsic :: iso_c_binding

  use supplib

  use particles
  use filter
  use neighbors

  use table2d
  use table3d
  use table4d

  use rebo2sich_default_tables

  implicit none

  private

#define SCREENING

! Enable dihedral term
#define DIHEDRAL
! Use angular cutoffs for dihedral
#define DIHEDRAL_SIN_CUTOFF

! Enable neighbor and conjugation count, i.e. enable P and F tables
#define NUM_NEIGHBORS

! Use separate conjugation variables for both atoms that participate in a bond
#define SEP_NCONJ

! Use exponential cut-offs
!#define EXP_CUT

! The value below are replaced by the preprocessor. This makes it easier to
! compile the module with different setting into a single code.
#define BOP_NAME             rebo2sich_scr
#define BOP_NAME_STR         "rebo2sich_scr"
#define BOP_STR              "Rebo2SiCHScr"
#define BOP_KERNEL           rebo2sich_scr_kernel
#define BOP_TYPE             rebo2sich_scr_t

#define REGISTER_FUNC        rebo2sich_scr_register
#define INIT_FUNC            rebo2sich_scr_init
#define INIT_DEFAULT_FUNC    rebo2sich_scr_init_default
#define DEL_FUNC             rebo2sich_scr_del
#define BIND_TO_FUNC         rebo2sich_scr_bind_to
#define COMPUTE_FUNC         rebo2sich_scr_energy_and_forces
#define GET_DICT_FUNC        rebo2sich_scr_get_dict

#include "rebo2sich_type.f90"

contains

#include "rebo2sich_db.f90"

#include "rebo2sich_module.f90"

#include "bop_kernel_rebo2sich.f90"

#include "rebo2sich_func.f90"

#include "rebo2sich_registry.f90"

endmodule rebo2sich_scr

#! /usr/bin/env python

# ======================================================================
# Atomistica - Interatomic potential library
# https://github.com/pastewka/atomistica
# Lars Pastewka, lars.pastewka@iwm.fraunhofer.de, and others.
# See the AUTHORS file in the top-level Atomistica directory.
#
# Copyright (2005-2013) Fraunhofer IWM
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ======================================================================

import math
import sys

import unittest

import ase
from ase.units import mol

from ase.lattice.cubic import Diamond, FaceCenteredCubic, SimpleCubic
from ase.lattice.cubic import BodyCenteredCubic
from ase.lattice.compounds import B1, B2, B3, L1_2, NaCl

import atomistica.native as native
from atomistica import *
from atomistica.tests import test_forces, test_potential, test_virial

# import ase_ext_io as io

###

sx = 2
dx = 1e-6
tol = 1e-3

###

def random_solid(els, density):
    syms = [ ]
    nat = 0
    for sym, n in els:
        syms += n*[sym]
        nat += n
    r = np.random.rand(nat, 3)
    a = ase.Atoms(syms, positions=r, cell=[1,1,1], pbc=True)

    mass = np.sum(a.get_masses())
    a0 = ( 1e24*mass/(density*mol) )**(1./3)
    a.set_cell([a0,a0,a0], scale_atoms=True)

    return a

def assign_charges(a, els):
    syms = np.array(a.get_chemical_symbols())
    qs = np.zeros(len(a))
    for el, q in els.items():
        qs[syms==el] = q
    if hasattr(a, 'set_initial_charges'):
        a.set_initial_charges(qs)
    else:
        a.set_charges(qs)
    return a

def printdiff(f0, ffd, tol):
    for i, (_f0, _ffd) in enumerate(zip(f0, ffd)):
        if np.linalg.norm(_f0-_ffd) > tol:
            print('=== {} ==='.format(i))
            print('analytical: {} {} {}'.format(*_f0))
            print(' numerical: {} {} {}'.format(*_ffd))
            print('difference: {} {} {}'.format(*(_f0-_ffd)))

###

# Potential tests
tests  = [
    ( Rebo2SiCH, None,
      [ ( 'dia-C', Diamond('C', size=[sx,sx,sx]) ),
        ( 'random-C', random_solid( [('C', 60)], 3.0 ) ),
        ( 'random-C-H', random_solid( [('C',50),('H',10)], 3.0 ) ),
        ( 'dia-Si', Diamond('Si', size=[sx,sx,sx]) ),
        ( 'random-Si', random_solid( [('Si', 60)], 2.3 ) ),
        ( 'random-Si-H', random_solid( [('Si',50),('H',10)], 3.0 ) ),
        ( "dia-Si-C", B3( [ "Si", "C" ], latticeconstant=4.3596,
                          size=[sx,sx,sx]) ),
        ( 'random-Si-C', random_solid( [('Si',30),('C',30)], 3.2 ) ),
        ( 'random-Si-C-H', random_solid( [('Si',20),('C',20),('H',20)], 3.2 ) ),
       ] ),
    ( Rebo2SiCHScr, dict(Tcc=np.zeros([5,5,10])),
      [ ( 'dia-C', Diamond('C', size=[sx,sx,sx]) ),
        ( 'random-C', random_solid( [('C', 60)], 3.0 ) ),
        ( 'random-C-H', random_solid( [('C',50),('H',10)], 3.0 ) ),
        ( 'dia-Si', Diamond('Si', size=[sx,sx,sx]) ),
        ( 'random-Si', random_solid( [('Si', 60)], 2.3 ) ),
        ( 'random-Si-H', random_solid( [('Si',50),('H',10)], 3.0 ) ),
        ( "dia-Si-C", B3( [ "Si", "C" ], latticeconstant=4.3596,
                          size=[sx,sx,sx]) ),
        ( 'random-Si-C', random_solid( [('Si',30),('C',30)], 3.2 ) ),
        ( 'random-Si-C-H', random_solid( [('Si',20),('C',20),('H',20)], 3.2 ) ),
        ] ),
    ]

###

def run_forces_and_virial_test(test=None):
    for pot, par, mats in tests:
        if len(sys.argv) > 1:
            found = False
            if par is not None:
                for keyword in sys.argv[1:]:
                    if '__ref__' in par:
                        if par['__ref__'].lower().find(keyword.lower()) != -1:
                            found = True
            try:
                potname = pot.__name__
            except:
                potname = pot.__class__.__name__
            for keyword in sys.argv[1:]:
                if potname.lower().find(keyword.lower()) != -1:
                    found = True
            if not found:
                continue

        try:
            potname = pot.__name__
        except:
            potname = pot.__class__.__name__
        if test is None:
            print("--- %s ---" % potname)
        if par is None:
            c  = pot()
        else:
            c  = pot(**par)
            if test is None and '__ref__' in par:
                print("    %s" % par["__ref__"])

        for imat in mats:
            if isinstance(imat, tuple):
                name, a = imat
            else:
                name = imat['name']
                a = imat['struct']
            if test is None:
                print("Material:  ", name)
            a.translate([0.1,0.1,0.1])
            a.set_calculator(c)

            for dummy in range(2):
                if dummy == 0:
                    errmsg = 'potential: {0}; material: {1}; equilibrium' \
                        .format(potname, name)
                    if test is None:
                        print("...equilibrium...")
                else:
                    errmsg = 'potential: {0}; material: {1}; distorted' \
                        .format(potname, name)
                    if test is None:
                        print("...distorted...")

                ffd, f0, maxdf = test_forces(a, dx=dx)

                if test is None:
                    if abs(maxdf) < tol:
                        print("forces .ok.")
                    else:
                        print("forces .failed.")
                        print("max(df)  = %f" % maxdf)

                        printdiff(f0, ffd, tol)
                else:
                    test.assertTrue(abs(maxdf) < tol,
                                    msg=errmsg+'; forces')

                sfd, s0, maxds = test_virial(a, de=dx)

                if test is None:
                    if abs(maxds) < tol:
                        print("virial .ok.")
                    else:
                        print("virial .failed.")
                        print("max(ds)  = %f" % maxds)

                        print('analytical: {}'.format(s0))
                        print(' numerical: {}'.format(sfd))
                        print('difference: {}'.format(s0-sfd))
                else:
                    test.assertTrue(abs(maxds) < tol,
                                    msg=errmsg+'; virial')

                pfd, p0, maxdp = test_potential(a, dq=dx)

                if test is None:
                    if abs(maxdp) < tol:
                        print("potential .ok.")
                    else:
                        print("potential .failed.")
                        print("max(dp)  = %f" % maxdp)

                        printdiff(p0, pfd, tol)
                else:
                    test.assertTrue(abs(maxds) < tol,
                                    msg=errmsg+'; virial')

                a.rattle(0.5)

###

class TestForcesAndVirial(unittest.TestCase):

    def test_forces_and_virial(self):
        run_forces_and_virial_test(self)

###

if __name__ == '__main__':
    run_forces_and_virial_test()

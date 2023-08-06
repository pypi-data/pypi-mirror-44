from ase.build import molecule
from atomistica import Rebo2SiCH, Rebo2SiCHScr

###

a = molecule('CH4')
a.center(vacuum=100)
a.set_calculator(Rebo2SiCHScr())
print(a.get_potential_energy())

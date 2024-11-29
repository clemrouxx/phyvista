# Basic example only using the 'core' submodule, for first testing.

# phyvista adds useful on top of pyvista, which we need to import
import pyvista as pv
# Import everything from the 'core' submodule, which provides a few useful constants, functions and the Element and Group classes.
from phyvista.core import *

# Create the main plotter object (from pyvista)
p = pv.Plotter()

# Use the 'add' method added by phyvista to easily add objects with color/material
p.add(pv.Cube(),"yellow")

# Equivalent version of the previous line using explicitely the Element class. Useful for modyfiying the object before adding it for example.
my_object = Element(pv.Cube(center=2*U_X),"red")
p.add(my_object)

# Show the scene ("plot")
p.show()
import pyvista as pv
import numpy as np
from phyvista.core import *
from phyvista import constructors as constr
from phyvista import lattices as lat

p = pv.Plotter()

cr = lat.Crystal(ORIGIN,lat.hexagonalLatticeVectors())
# Adding the two atoms (when added in this way, their positions are given in the basis of lattice vectors, which is quite practical here)
cr.addNewElement(pv.Sphere(radius=0.1),"black",(0,0))
cr.addNewElement(pv.Sphere(radius=0.1),"black",(2/3,1/3))

atom_position = cr.point(2/3,1/3) # Position of the second C atom (the first one is at (0,0))

# Create the links between the second particle and its nearest neibourghs
cr.addNewElement(constr.CylinderStartEnd(cr.point(0,0),atom_position,0.03),"grey")
cr.addNewElement(constr.CylinderStartEnd(cr.point(1,1),atom_position,0.03),"grey")
cr.addNewElement(constr.CylinderStartEnd(cr.point(1,0),atom_position,0.03),"grey")

# Add the crystal to the scene
p.add(cr,(-4,4),(-4,4))
p.show()
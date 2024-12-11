import pyvista as pv
from phyvista.core import *
from phyvista import lattices as lat
from phyvista import materials as mat

p = pv.Plotter()

salt = lat.Crystal(ORIGIN,[U_X,U_Y,U_Z]) # Defining the crystal with position, 1 to 3 basis vectors and optionnally a pattern (empty by default)

# We now build the pattern by adding the different elements (another option is to provide the pattern as a Group in the Crystal constructor)
Cl = Element(pv.Sphere(radius=0.3),mat.SmoothMaterial("lime")) # Sphere that represents Cl atoms. Using SmoothMaterial gives a ... smoother result than the default.
pos_Cl = [(0,0,0),(0.5,0.5,0),(0,0.5,0.5),(0.5,0,0.5)] # Positions in the basis of unit cell vectors
for pos in pos_Cl:
    salt.addElement(Cl,pos)

# We also add Na atoms to the unit cell
Na = Element(pv.Sphere(radius=0.2),mat.SmoothMaterial("purple"))
pos_Na = [(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0.5)]
for pos in pos_Na:
    salt.addElement(Na,pos)

p.add(salt,(-1,1),(-1,1),(-1,1)) # Adding a 3x3x3 grid of unit cells to the scene (plot). The numbers are the indices ranges for the lattice translation vectors

p.show()
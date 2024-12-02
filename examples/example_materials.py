import pyvista as pv
from phyvista.core import *
from phyvista import materials as mat

# Demonstration of a few basic materials in light theme (default) and dark theme.

grid = pv.Sphere()

## Light theme

pv.set_plot_theme("default") # Optionnal line : default theme is light theme (white background)
mat.set_theme("default") # Idem

p = pv.Plotter()
materials = ["red","#00aaff",mat.SmoothMaterial("#00aaff"),mat.GLASS,mat.METAL,mat.METAL.variant(color="gold")]

for i in range(len(materials)):
    p.add(grid.translate(2*i*U_Y),materials[i])
p.show()

## Same, but in dark theme :

pv.set_plot_theme("dark") # Setting the pyvista theme to dark (black background)
mat.set_theme("dark") # Setting the material theme to dark : affects the values of materials.GLASS, materials.METAL...

p_dark = pv.Plotter() # Creating another plotter, after setting the theme. Will be shown after the first one. It is also possible to do some subplots, see pyvista documentation.
materials_dark = ["red","#00aaff",mat.SmoothMaterial("#00aaff"),mat.GLASS,mat.METAL,mat.METAL.variant(color="gold")] # Same expression as before, but we get different values because of 'mat.set_theme'

for i in range(len(materials_dark)):
    p_dark.add(grid.translate(2*i*U_Y),materials_dark[i])
p_dark.show()
import pyvista as pv
from phyvista.core import *
from phyvista import materials as mat

###
# Demonstration of a few basic materials in light theme (default) and dark theme.
###

grid = pv.Sphere() # Geometry of the example object

## Light theme

pv.set_plot_theme("default") # Optionnal line : default theme is light theme (called 'document', with white background)
p = pv.Plotter()
materials = ["red","#00aaff",mat.SmoothMaterial("#00aaff"),mat.getGLASS(),mat.getMETAL(),mat.getMETAL().variant(color="gold")] # Different material presets. The functions getGLASS and getMETAL take into account the current pyvista theme.
for i in range(len(materials)):
    p.add(grid.translate(2*i*U_Y),materials[i])
p.show()

## Same, but in dark theme

pv.set_plot_theme("dark") # Setting the pyvista theme to dark (black background)
p_dark = pv.Plotter() # Creating another plotter, after setting the theme. Will be shown after the first one. It is also possible to do some subplots, see pyvista documentation.
materials_dark = ["red","#00aaff",mat.SmoothMaterial("#00aaff"),mat.getGLASS(),mat.getMETAL(),mat.getMETAL().variant(color="gold")] # Same expression as before, but the results of getMETAL and getGLASS will be different.
for i in range(len(materials_dark)):
    p_dark.add(grid.translate(2*i*U_Y),materials_dark[i])
p_dark.show()
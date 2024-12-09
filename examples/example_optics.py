import pyvista as pv
from phyvista.core import *
from phyvista import light as light
from phyvista import optics as opt

pv.set_plot_theme("default") # Also try 'dark' !

p = pv.Plotter()

pos_PBS = ORIGIN
pos_plate = pos_PBS + 2*U_Y
pos_mirror = pos_plate + 2*U_Y
pos_lens = pos_PBS + 2*U_X

# Adding different optical elements to the scene
mirror = opt.Mirror(pos_mirror,-U_Y+U_Z,width=0.1)
cube = opt.CubicSplitter(pos_PBS,U_X,U_Y)
lens = opt.BiconvexLens(pos_lens,U_X,0.5,1,minimum_width=0.05)
p.add(mirror)
p.add(cube)
p.add(lens)
p.add(opt.Plate(pos_plate,U_Y,width=0.1)) # Directly added since we don't need the object for the beams

# Finally adding the laser beam(s).
# We can specify the start and ends of beams either with positions or with instances of OpticsElement; or a mix of both. 
# If an OpticsElement is provided for a StraightBeam, its end will be accordingly cut to the surface of the OpticsElement.
p.add(light.StraightBeam(mirror,pos_mirror + U_Z*5,0.3)) # Incoming beam
p.add(light.StraightBeam(mirror,cube,radius=0.3)) # Reflection off the mirror
p.add(light.StraightBeam(cube,pos_PBS - 2*U_Y,0.3,relative_intensity=0.3)) # Beam PBS-transmitted
p.add(light.StraightBeam(lens,cube,0.3,relative_intensity=0.5)) # Beam PBS-reflected
p.add(light.FocusedBeam(lens,pos_lens + 2*U_X,0.5,starting_radius=0.3,relative_intensity=0.5)) # Focused beam

p.show()
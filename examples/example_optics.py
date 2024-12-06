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
p.add(opt.Mirror(pos_mirror,-U_Y+U_Z,width=0.1))
p.add(opt.CubicSplitter(pos_PBS,U_X,U_Y))
p.add(opt.BiconvexLens(pos_lens,U_X,0.5,1,minimum_width=0.05))
p.add(opt.Plate(pos_plate,U_Y,width=0.1))

# Finally adding the laser beam(s)
p.add(light.StraightBeam(pos_mirror,pos_mirror+U_Z*5,0.3,clipping_normal_start=U_Y-U_Z)) # Incoming beam
p.add(light.StraightBeam(pos_mirror,pos_PBS,0.3,clipping_normal_start=U_Y-U_Z,clipping_normal_end=-U_X-U_Y)) # Reflection off the mirror
p.add(light.StraightBeam(pos_PBS,pos_PBS - 2*U_Y,0.3,clipping_normal_start=U_X+U_Y,relative_intensity=0.3)) # Beam PBS-transmitted
p.add(light.StraightBeam(pos_lens,pos_PBS,0.3,clipping_normal_end=-U_X-U_Y,relative_intensity=0.5)) # Beam PBS-reflected
p.add(light.FocusedBeam(pos_lens,pos_lens + 2*U_X,0.5,starting_radius=0.3,relative_intensity=0.5)) # Focused beam

p.show()
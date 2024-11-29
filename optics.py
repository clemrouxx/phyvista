import pyvista as pv
import numpy as np
import os
from phyvista.core import *
from phyvista.materials import GLASS,GLASS_LIGHT_THEME

def BiconvexLensGrid(position,direction,radius,curvature_radius,minimum_width=0,curvature_radius_back=None): 
    """Builds the geometry of a lens as an intersection of two spheres and a cylinder."""
    d1 = np.sqrt(curvature_radius**2-radius**2) - minimum_width/2 # Pythagoras
    s1 = pv.Sphere(center=position-d1*direction,radius=curvature_radius,theta_resolution=100,phi_resolution=50)
    if curvature_radius_back == None:
        curvature_radius_back = curvature_radius
    d2 = np.sqrt(curvature_radius_back**2-radius**2) - minimum_width/2
    s2 = pv.Sphere(center=position+d2*direction,radius=curvature_radius_back,theta_resolution=100,phi_resolution=50)
    if minimum_width == 0:
        return s1.boolean_intersection(s2)
    c = pv.Cylinder(center=position,direction=direction,radius=radius,height=2*(d1+d2)).triangulate(inplace=True)
    return s1.boolean_intersection(s2).boolean_intersection(c)

def BiconvexLens(position,direction,radius,curvature_radius,minimum_width=0,curvature_radius_back=None,style="semirealistic") -> Element:
    """Returns an Element representing a biconvex lens

    Args:
        position (3D vector): Center position
        direction (Nonzero 3D vector): Direction the lens is 'facing'
        radius (float): radius
        curvature_radius (float): Curvature of the lens face
        minimum_width (float, optional): Edge width. Defaults to 0.
        curvature_radius_back (float, optional): Curvature of the backface. If None, it will be the same as the front face. Defaults to None.
        style (str, optional): Dictates the material used for the lens. 'semirealistic' (GLASS material) or 'light_theme' (GLASS_LIGHT_THEME material). Defaults to "semirealistic".

    Returns:
        Element
    """
    
    grid = BiconvexLensGrid(position,direction,radius,curvature_radius,minimum_width,curvature_radius_back)
    if style=="semirealistic":
        material=GLASS
    elif style=="light_theme":
        material = GLASS_LIGHT_THEME
    else:
        raise ValueError(f"Unknwonw style for a lens : '{style}")
    return Element(grid,material)



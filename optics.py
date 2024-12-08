import pyvista as pv
import numpy as np
import os
from phyvista.core import *
from phyvista.materials import getGLASS, getMETAL

class OpticsElement(Element):
    def __init__(self,grid,material,center,normal):
        super().__init__(grid,material)
        self.center = np.array(center) # Position on which light beams can be transmitted/reflected
        self.normal = np.array(normal) # Normal of the reflective/transmissive surface

    def copy(self):
        return OpticsElement(self.grid.copy(),self.material.copy(),self.center,self.normal)

    def translate(self,vector,inplace=False):
        if inplace:
            super().translate(vector,True)
            self.center += vector
        else:
            new_elmt = self.copy()
            new_elmt.translate(vector,True)
            return new_elmt
    # TODO : also other transformations...

def BiconvexLensGrid(position,direction,radius,curvature_radius,minimum_width=0,curvature_radius_back=None): 
    """Builds the geometry of a lens as an intersection of two spheres and a cylinder."""
    position,direction = np.array(position), np.array(direction)
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

def BiconvexLens(position,direction,radius,curvature_radius,minimum_width=0,curvature_radius_back=None) -> OpticsElement:
    """Returns an Element representing a biconvex lens

    Args:
        position (3D vector): Center position
        direction (Nonzero 3D vector): Direction the lens is 'facing'
        radius (float): radius
        curvature_radius (float): Curvature of the lens face
        minimum_width (float, optional): Edge width. Defaults to 0.
        curvature_radius_back (float, optional): Curvature of the backface. If None, it will be the same as the front face. Defaults to None.

    Returns:
        Element
    """
    
    grid = BiconvexLensGrid(position,direction,radius,curvature_radius,minimum_width,curvature_radius_back)
    material = getGLASS()
    return OpticsElement(grid,material,position,direction)


def CubicSplitter(position,direction1,direction2,size=1.0) -> OpticsElement:
    """Creates an Element representing typically a polarized beam splitter

    Args:
        position (3D vector): center of the cube
        direction1 (Nonzero 3D vector): direction of one of the light beams in/out if the PBS
        direction2 (Nonzero 3D vector): direction of the other light beam (reflection of the first one)
        size (float): side length of the cube. Defaults to 1.0.

    Returns:
        Element: Element to be added to the plot
    """
    dir1 = normalized(np.array(direction1))
    dir2 = normalized(np.array(direction2))
    dir3 = np.cross(dir1,dir2)

    plane = [(dir1+dir2)/2,(dir1-dir2)/2,(-dir1-dir2)/2,(-dir1+dir2)/2]
    points = [pt - dir3/2 for pt in plane] + [pt + dir3/2 for pt in plane]

    cells = [(4,0,1,2,3),(4,0,1,5,4),(4,1,2,6,5),(4,2,3,7,6),(4,0,3,7,4),(4,1,3,7,5),(4,4,5,6,7)]

    grid = pv.UnstructuredGrid(cells, np.full(len(cells),pv.CellType.QUAD,dtype=np.uint), points)
    grid = grid.scale(size).translate(position)

    return OpticsElement(grid,getGLASS(),position,direction1+direction2)

def Plate(position,direction,radius=0.5,width=0.0) -> OpticsElement:
    """Creates an Element representing a waveplate or beamsplitter

    Args:
        position (3D vector): Center
        direction (Nonzero 3D vector): Main axis of the plate (beam direction)
        radius (float, optional): Defaults to 0.5.
        width (float, optional): Defaults to 0.0.

    Returns:
        Element : Element to be added to the plot
    """
    grid = pv.Cylinder(position,direction,radius,height=width)
    return OpticsElement(grid,getGLASS(),position,direction)

def Mirror(position,direction,radius=0.5,width=0.0) -> OpticsElement:
    """Creates an Element representing a circular flat mirror

    Args:
        position (3D vector): Center
        direction (Nonzero 3D vector): Normal vector to the mirror.
        radius (float, optional): Defaults to 0.5.
        width (float, optional): Defaults to 0.0.

    Returns:
        OpticsElement: Element to be added to the plot
    """
    direction = normalized(np.array(direction))
    grid = pv.Cylinder(center=position-width/2*direction,radius=radius,height=width,direction=direction)
    return OpticsElement(grid,getMETAL(),position,direction)
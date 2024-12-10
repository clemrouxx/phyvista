import pyvista as pv
import numpy as np
from phyvista.materials import plotGridWithMaterial,Material
from pyvista.core.utilities import transformations as transf


U_X = np.array((1.0,0,0))
U_Y = np.array((0,1.0,0))
U_Z = np.array((0,0,1.0))
ORIGIN = np.array((0.0,0,0))

def normalized(v):
    return v/np.linalg.norm(v)

def norm(v):
    return np.linalg.norm(v)

# New method for adding any object (Element,Group...) (or a grid with an associated material)
def add(self,obj,*args,**kwargs):
    """Adds an object to the plot.

    Args:
        obj (Element,Group,... or subclass of pyvista.DataSet): Object to be added. If it inherits from pyvista.DataSet, a Material or a color string is expected as second argument.
    """
    if issubclass(type(obj),pv.DataSet): # In this case, we expect a material as 2nd argument
        material = args[0]
        plotGridWithMaterial(self,obj,material)
    else:
        obj.plotSelf(self,*args,**kwargs)
pv.Plotter.add=add

class Element:
    def __init__(self,grid,material):
        self.grid = grid
        self.material = material
        if type(material) == str:
            self.material = Material(color=material)# Simple color material

    def plotSelf(self,plotter):
        plotGridWithMaterial(plotter,self.grid,self.material)

    def copy(self):
        return Element(self.grid.copy(),self.material.copy())

    def transform(self,transform,inplace=False):
        newgrid = self.grid.transform(transform,inplace=inplace)
        if not inplace:
            return Element(newgrid,self.material.copy())

    def translate(self,vector,inplace=False):
        matrix = np.eye(4)
        matrix[0:3,3] = vector # Create manually the translation 4x4 matrix
        return self.transform(matrix,inplace=inplace)

    def rotate_vector(self,vector,angle,point,inplace=False):
        return self.transform(transf.axis_angle_rotation(vector,angle,point),inplace=inplace)

    def rotate_x(self,angle,point=ORIGIN,inplace=False):
        return self.rotate_vector(U_X,angle,point,inplace)

    def rotate_y(self,angle,point=ORIGIN,inplace=False):
        return self.rotate_vector(U_Y,angle,point,inplace)

    def rotate_z(self,angle,point=ORIGIN,inplace=False):
        return self.rotate_vector(U_Z,angle,point,inplace)

    def reflect(self,normal,point,inplace=False):
        newgrid = self.grid.reflect(normal,point,inplace=inplace)
        if not inplace:
            return Element(newgrid,self.material.copy())

    def clip(self,normal,origin,inplace=False):
        newgrid = self.grid.clip(normal,origin,inplace=inplace)
        if not inplace:
            return Element(newgrid,self.material.copy())

class Group:
    def __init__(self,elements=[], grids = [],materials = []):
        if len(elements)==0:
            self.elements = [Element(grids[i],materials[i]) for i in range(len(grids))]
        else:
            self.elements = elements

    def append(self,element):
        self.elements.append(element)

    def plotSelf(self,plotter):
        for element in self.elements:
            element.plotSelf(plotter)

    def translate(self,vector,inplace=False):
        if not inplace:
            newgroup = Group()
        for elmt in self.elements:
            newelmt = elmt.translate(vector,inplace=inplace)
            if not inplace:
                newgroup.append(newelmt)
        if not inplace:
            return newgroup

    def rotate_vector(self,vector,angle,point,inplace=False):
        if not inplace:
            newgroup = Group()
        for elmt in self.elements:
            newelmt = elmt.rotate_vector(vector,angle,point,inplace=inplace)
            if not inplace:
                newgroup.append(newelmt)
        if not inplace:
            return newgroup

    def rotate_x(self,angle,point=ORIGIN,inplace=False):
        return self.rotate_vector(U_X,angle,point,inplace)

    def rotate_y(self,angle,point=ORIGIN,inplace=False):
        return self.rotate_vector(U_Y,angle,point,inplace)

    def rotate_z(self,angle,point=ORIGIN,inplace=False):
        return self.rotate_vector(U_Z,angle,point,inplace)

    def reflect(self,normal,point):# TODO : Make not inplace
        for elmt in self.elements:
            elmt.grid.reflect(normal,point,inplace=True)

    def extend(self,group):
        self.elements.extend(group.elements)

import pyvista as pv
import numpy as np
import os
from phyvista.core import *

class Crystal:
    def __init__(self,position,vectors,pattern=None):
        self.position = np.array(position,dtype=np.float64)
        self.vectors = [np.array(v,dtype=np.float64) for v in vectors]
        self.dimension = len(vectors)
        self.pattern = Group() if pattern == None else pattern
    
    def point(self,*indices):
        if len(indices) != self.dimension:
            raise ValueError("The number of indices should be the same of the dimension of the crystal.")
        r = self.position.copy()
        for i in range(self.dimension):
            r += indices[i]*self.vectors[i]
        return r

    def plotPattern(self,plotter,indices):
        pos = self.point(*indices)
        self.pattern.translate(pos).plotSelf(plotter)

    def plotSelf(self,plotter,*indices_ranges):
        if len(indices_ranges) != self.dimension:
            raise ValueError("The number of indices should be the same of the dimension of the crystal.")
        for i in range(indices_ranges[0][0],indices_ranges[0][1]+1):
            if self.dimension == 1:# I should be able to do it without 'if's
                self.plotPattern(plotter,(i,))
                continue
            for j in range(indices_ranges[1][0],indices_ranges[1][1]+1):
                if self.dimension == 2:
                    self.plotPattern(plotter,(i,j))
                    continue
                for k in range(indices_ranges[2][0],indices_ranges[2][1]+1):
                    self.plotPattern(plotter,(i,j,k))

    def addElement(self,element:Element,indices=None):# Add a particule with position defined by indices
        if type(indices)==type(None): # Default : no translation
            pos = np.zeros((3,))
        else:
            pos = self.point(*indices)
        self.pattern.append(element.translate(pos))

    def addNewElement(self,grid,material,indices=None):
        element = Element(grid,material)
        self.addElement(element,indices)

def hexagonalLatticeVectors(scale=1):#Returns base vectors for a hexagonal lattice (TODO : generalize)
    angle = 2*np.pi/3
    v1 = U_X
    v2 = np.cos(np.pi*2/3)*U_X + np.sin(np.pi*2/3)*U_Y
    return (v1,v2)
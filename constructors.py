import pyvista as pv
import numpy as np
from phyvista.core import norm,normalized

def CylinderStartEnd(start,end,radius,**kwargs):
    start = np.array(start)
    end = np.array(end)
    center = (start+end)/2
    axis = end-start
    height = norm(axis)
    return pv.Cylinder(center,axis,radius,height,**kwargs)


def ConeStartEnd(start,end,radius,resolution=100,**kwargs):
    start = np.array(start)
    end = np.array(end)
    center = (start+end)/2
    axis = end-start
    height = norm(axis)
    return pv.Cone(center,axis,height,radius,resolution=resolution,**kwargs)



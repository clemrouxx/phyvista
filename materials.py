import pyvista as pv
from matplotlib import colors

class Material:
    def __init__(self,renderingStyle="mesh",plottedField=None,**properties):
        self.renderingStyle = renderingStyle
        self.properties = properties
        self.plottedField = plottedField

    def modify(self,**properties):
        for key in properties.keys():
            self.properties[key] = properties[key]

    def copy(self):
        return Material(self.renderingStyle,self.plottedField,**(self.properties))

    def variant(self,**properties):
        newmat = self.copy()
        newmat.modify(**properties)
        return newmat

GLASS = Material(color="white",opacity=0.7,specular=1,diffuse=0.2,smooth_shading=True, split_sharp_edges=True,specular_power=20)
GLASS_LIGHT_THEME = Material(color="lightblue",opacity=0.2,specular=1,diffuse=0.2,ambient=1,smooth_shading=True, split_sharp_edges=True,specular_power=20)
METAL = Material(color="white",specular=1,diffuse=0.1,smooth_shading=True, split_sharp_edges=True,specular_power=10)
METAL_LIGHT_THEME = METAL.variant(diffuse=0.8)

def SmoothMaterial(color) -> Material:
    return Material(color=color,smooth_shading=True)

def plotGridWithMaterial(plotter,grid,material):
    if type(material) == Material:
        if material.renderingStyle == "mesh":
            plotter.add_mesh(grid,**(material.properties))
        elif material.renderingStyle == "volume":
            if material.plottedField != None:
                plotter.add_volume(grid,scalars=material.plottedField,**material.properties,show_scalar_bar=False)
            else:
                plotter.add_volume(grid,**material.properties,show_scalar_bar=False)
        else:
            raise ValueError(f"Unknown material renderingStyle : '{material.renderingStyle}'")
    else:
        plotter.add_mesh(grid,color=material)
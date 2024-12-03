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

GLASS_DARK_THEME = Material(color="white",opacity=0.6,specular=1,diffuse=0.1,smooth_shading=True, split_sharp_edges=True,specular_power=20)
GLASS_LIGHT_THEME = Material(color="lightblue",opacity=0.2,specular=1,diffuse=0.2,ambient=1,smooth_shading=True, split_sharp_edges=True,specular_power=20)
METAL_DARK_THEME = Material(color="white",specular=1,diffuse=0.1,smooth_shading=True, split_sharp_edges=True,specular_power=10)
METAL_LIGHT_THEME = METAL_DARK_THEME.variant(diffuse=0.8)

GLASS_BY_STYLE = {"light":GLASS_LIGHT_THEME,"dark":GLASS_DARK_THEME}
METAL_BY_STYLE = {"light":METAL_LIGHT_THEME,"dark":METAL_DARK_THEME}

def getAutoStyle():
    theme = pv.global_theme.name
    if theme == "document":
        return "light"
    elif theme == "dark":
        return "dark"
    raise ValueError(f"Theme '{theme}' unknown. Impossible to find an adequate style automatically.")
    
def getGLASS(style="auto"):
    if style == "auto":
        style = getAutoStyle()
    return GLASS_BY_STYLE[style]

def getMETAL(style="auto"):
    if style == "auto":
        style = getAutoStyle()
    return METAL_BY_STYLE[style]

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
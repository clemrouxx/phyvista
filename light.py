import numpy as np
from phyvista.core import *
from matplotlib import colors
from phyvista import materials

def StraightBeam(pos1,pos2,radius,style="simple",radial_fade_factor=2,color="red",opacity_unit_distance=0.4,relative_intensity=1.0,clipping_normal_start=None,clipping_normal_end=None) -> Element:
    """
    Returns an Element representing a straight (cylindrical) laser beam, going from pos1 to pos2 with a given beam radius.
    Optional Parameters :
        style : either 'semirealistic' for a volumic representation with gaussian cutoff, or 'simple' (semitransparent pipe)
        radial_fade_factor : used in the 'semirealistic' style, characterizes the gaussian curoff. default : 2.
        color : color of the beam. default : 'red'
        opacity_unit_distance : used in the 'semirealistic' style, distance of the view ray over which the laser beam seems totally opaque.
        relative_intensity : used in the both styles, changes the diffuse parameter or the opacity respectively. Defaults to 1.0.
        clipping_normal_start : normal vector of the plane according to which the laser beam should be clipped, at the first position. Facing outwards. No additionnal clipping if None (default).
        clipping_normal_end : idem for the second position.
    """
    if style=="semirealistic":
        grid = StraightBeamVolumeGrid(pos1,pos2,radius,radial_fade_factor,clipping_normal_start=clipping_normal_start,clipping_normal_end=clipping_normal_end)
        material = VolumicBeamMaterial(color,relative_intensity,opacity_unit_distance)
    elif style=="simple":
        grid = StraightBeamVolumeGrid(pos1,pos2,radius,radial_fade_factor,resolution_radius=2,surfacic_cells=True,clipping_normal_start=clipping_normal_start,clipping_normal_end=clipping_normal_end)
        material = SimpleBeamMaterial(color,relative_intensity)
    else:
        raise ValueError(f"Unkwnown beam style '{style}'")
    return Element(grid,material)

def FocusedBeam(pos1,pos2,focus_pos_param,starting_radius=None,divergence=None,radial_fade_factor=2,style="simple",color="red",opacity_unit_distance=0.1,relative_intensity=1.0) -> Element:
    """Creates an Element representing a light beam perfectly focused at a point.

    Args:
        pos1 (3Dvector-like): Starting point of the beam
        pos2 (3Dvector-like): Endpoint of the beam
        focus_pos_param (float): Relative distance from the starting point to the focusing point (relative to the beam length)
        starting_radius (float, optional): Beam radius at the starting point. If None, will be inferred from divergence. Defaults to None.
        divergence (float, optional): Beam divergence, in rad. If None, will be inferred from starting_radius. Defaults to None.
        radial_fade_factor (float, optional): Used in 'semirealistic' style, characterizes the radial fade-out of the beam. Defaults to 2.
        style (str, optional): 'semirealistic' (voluminc representation) or 'simple' (semitransparent pipe-like). Defaults to "semirealistic".
        color (str, optional): Color of the beam. Defaults to "red".
        opacity_unit_distance (float, optional): Used in 'semirealistic' style. Defaults to 0.1.
        opacity (float, optional): Used in 'simple' style. Defaults to 0.1.

    Returns:
        Element
    """
    if style=="semirealistic":
        material = VolumicBeamMaterial(color,relative_intensity,opacity_unit_distance,clim=[0,50])
        grid = FocusedBeamVolumeGrid(pos1,pos2,focus_pos_param,starting_radius,divergence,resolution_height=30,resolution_radius=25,radial_fade_factor=radial_fade_factor)
    elif style=="simple":
        material = SimpleBeamMaterial(color,relative_intensity)
        grid = FocusedBeamVolumeGrid(pos1,pos2,focus_pos_param,starting_radius,divergence,resolution_height=30,resolution_radius=2,radial_fade_factor=radial_fade_factor,surfacic_cells=True)
    else:
        raise ValueError(f"Unkwnown beam style '{style}'")
    return Element(grid,material)

def GlowingOrb(center,radius,color,saturation_color="white") -> Element:
    return Element(SphericalVolumeGrid(center,radius),GlowingOrbMaterial(color,saturation_color))

def StraightBeamVolumeGrid(pos1,pos2,radius,radial_fade_factor=2,resolution_height=10,resolution_theta=15,resolution_radius=10,surfacic_cells=False,clipping_normal_start=None,clipping_normal_end=None):
    pos1_modified = np.array(pos1)
    pos2_modified = np.array(pos2)
    axis = pos2_modified-pos1_modified

    # If we do additionnal clipping of the beam, we need to prolong the beam first
    if type(clipping_normal_start) != type(None):
        pos1_modified -= 3*radius*normalized(axis)
    if type(clipping_normal_end) != type(None):
        pos2_modified += 3*radius*normalized(axis)
    axis = pos2_modified-pos1_modified

    grid = CylindricalVolumeGrid(pos1_modified,axis,radius_profile=lambda p:radius,resolution_height=resolution_height,resolution_theta=resolution_theta,resolution_radius=resolution_radius,surfacic_cells=surfacic_cells)
    
    # We then do the eventual clipping of the beam on both ends
    if type(clipping_normal_start) != type(None):
        grid.clip(clipping_normal_start,pos1,inplace=True)
    if type(clipping_normal_end) != type(None):
        grid.clip(clipping_normal_end,pos2,inplace=True)

    # Adding the 'intensity' scalar field
    if radial_fade_factor == 0:
        intensity = np.ones(grid["r"].shape)
    else:
        intensity = np.exp(-(grid["r"]/(radius/radial_fade_factor))**2)
    grid["intensity"] = intensity

    return grid

def FocusedBeamVolumeGrid(pos1,pos2,focus_pos_param,starting_radius=None,divergence=None,resolution_height=30,resolution_radius=25,radial_fade_factor=2,surfacic_cells=False):
    if divergence==None and starting_radius==None:
        raise ValueError("Please provide either a divergence value or a starting_radius.")
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    length = np.sqrt(np.linalg.norm(pos1-pos2))
    if starting_radius == None:
        radius_factor = np.tan(divergence)*length
    else:
        radius_factor = starting_radius/focus_pos_param
    radius_profile = lambda p:np.maximum(abs(p-focus_pos_param),0.001)*radius_factor
    grid = CylindricalVolumeGrid(pos1,pos2-pos1,radius_profile,resolution_height,resolution_theta=15,resolution_radius=resolution_radius,include_parameter=focus_pos_param,surfacic_cells=surfacic_cells)
    profile = radius_profile(grid["axis_param"])
    if radial_fade_factor == 0:
        intensity = 1/(profile**2)
    else:
        intensity = np.exp(-(grid["r"]/(profile/radial_fade_factor))**2)/(profile**2)
    grid["intensity"] = intensity
    return grid

def GlowingOrbMaterial(color,saturation_color="white"):
    return materials.Material("volume",cmap=colors.LinearSegmentedColormap.from_list("",[saturation_color,color]),opacity="linear_r",opacity_unit_distance=0.7)

def VolumicBeamMaterial(color="red",relative_intensity=1,opacity_unit_distance=1,**parameters):
    return materials.Material("volume","intensity",cmap=[color],diffuse=relative_intensity,opacity_unit_distance=opacity_unit_distance,**parameters)

def SimpleBeamMaterial(color="red",relative_intensity=1.0):
    opacity = 0.1 if (materials.getAutoStyle() == "light") else 0.2 # Default opacity depending on the overall theme
    return materials.Material(color=color,opacity=opacity*relative_intensity,ambient=1,diffuse=1)

def CylindricalVolumeGrid(origin,axis,radius_profile,resolution_height=20,resolution_radius=20,resolution_theta=60,include_parameter=None,surfacic_cells=False):
    # radius_profile is a function of the axis parameter (from 0 to 1)
    # include_parameter has to be included in addition to the equidistant points
    # First, get a basis for the plane orthgonal to the axis
    U_temp = U_X if norm(np.cross(axis,U_X)) != 0 else U_Y
    U = normalized(np.cross(axis,U_temp))
    V = normalized(np.cross(axis,U))

    origin = np.array(origin)
    axis = np.array(axis)
    pointlist = []
    
    cells = []
    celltypes = []
    rlist = []
    paramlist = []
    # Build manually the different values of axis_param :
    axis_param_stops = []
    for i_h in range(resolution_height):
        next_axis_param = i_h/(resolution_height-1)
        if include_parameter != None and include_parameter < next_axis_param:
            axis_param_stops.append(include_parameter)
            include_parameter = None
        axis_param_stops.append(next_axis_param)

    i = -1
    points_per_cylinder = resolution_theta*len(axis_param_stops)

    # Start with the points on the central axis
    for axis_param in axis_param_stops:
        pt = origin + axis_param*axis
        pointlist.append(pt)
        paramlist.append(axis_param)
        rlist.append(0)
    i = len(pointlist)-1 # Index of the last point added

    # We build the grid from the inside out
    for i_r in range(1,resolution_radius):
        for i_axis,axis_param in enumerate(axis_param_stops):
            r = i_r*radius_profile(axis_param)/(resolution_radius-1)
            for i_theta in range(resolution_theta):
                theta = 2*np.pi*i_theta/resolution_theta
                pt = origin + axis_param*axis + (np.cos(theta)*U + np.sin(theta)*V)*r
                pointlist.append(pt)
                paramlist.append(axis_param)
                rlist.append(r)
                i += 1
                if i_r > 0 and i_axis > 0:
                    im1 = i-1
                    if i_theta == 0:
                        im1 += resolution_theta
                    if surfacic_cells:# Case where we only want 'leek' surfaces
                        cell = [4,i,im1,im1-resolution_theta,i-resolution_theta]
                        cells.append(cell)
                    else:
                        if i_r == 1: # First circle (wedges)
                            cell = [6,i,im1,i_axis,i-resolution_theta,im1-resolution_theta,i_axis-1]
                            cells.append(cell)
                        else: # Hexahedrons
                            # Changed into 2 wedges
                            cell1 = [6,i,im1-points_per_cylinder,i-points_per_cylinder,i-resolution_theta,im1-points_per_cylinder-resolution_theta,i-points_per_cylinder-resolution_theta]
                            cells.append(cell1)
                            cell2 = [6,i,im1,im1-points_per_cylinder,i-resolution_theta,im1-resolution_theta,im1-points_per_cylinder-resolution_theta]
                            cells.append(cell2)
    if surfacic_cells:
        usg = pv.UnstructuredGrid(cells, np.full(len(cells),pv.CellType.QUAD,dtype=np.uint), pointlist)
    else: 
        usg = pv.UnstructuredGrid(cells, np.full(len(cells),pv.CellType.WEDGE,dtype=np.uint), pointlist)
    usg["r"] = rlist
    usg["axis_param"] = paramlist
    return usg

def SphericalVolumeGrid(center,radius):
    """
    Builds a spherical volume grid based on pyvista.SolidSphere, but adds the scalar field 'r' (distance to the center) on the points.
    """
    s = pv.SolidSphere(outer_radius=radius,theta_resolution=20,phi_resolution=20)
    s["r"] = [norm(v) for v in s.points]
    return s.translate(center)
import numpy as np

def fromWavelength(wavelength: float) -> str:
    """Returns an approximate color corresponding to the given light wavelength

    Args:
        wavelength (float): wavelength (nm)

    Returns:
        str: color in RGB hex notation, in sRGB color space
    """
    r,g,b = CIEXYZtosRGB(wavelengthToCIEXYZ(wavelength))
    return fromRGB(r,g,b)

def fromRGB(r: float,g: float,b: float) -> str:
    """
    Converts an r,g,b float values (between 0 and 1) to a usable hex color string
    """
    return '#%02x%02x%02x' % (int(255*r),int(255*g),int(255*b))

def CIEXYZtosRGB(XYZ:np.array) -> np.array:
    matrix = np.array([3.2406,-1.5372,-0.4986,-0.9689,1.8758,0.0415,0.0557,-0.204,1.057]).reshape((3,3))
    RGB_linear = matrix @ XYZ
    def unlinearize(c):# Unlinearize and clamp
        if c <= 0.0031308:
            v = 12.92*c
        else:
            v = 1.055*np.power(c,1/2.4)-0.055
        return min(1,max(v,0))# This clamping leads to a very simple approximation of the real color that could be improved.
    RGB = np.array([unlinearize(c) for c in RGB_linear])
    return RGB

def wavelengthToCIEXYZ(wavelength: float) -> np.array:
    """Returns the CIE XYZ color for a monochromatic light. 
    Approximation taken from : Wyman, Chris; Sloan, Peter-Pike; Shirley, Peter (July 12, 2013). "Simple Analytic Approximations to the CIE XYZ Color Matching Functions". Journal of Computer Graphics Techniques.

    Args:
        wavelength (float): Wavelength (nm)

    Returns:
        numpy array (3D vector): X,Y,Z components of the CIE XYZ color
    """
    g = piecewiseGaussian # Just a shorthand
    x = 1.056*g(wavelength,599.8,0.0264,0.0323) + 0.362*g(wavelength,442,0.0624,0.0374) - 0.065*g(wavelength,501.1,0.049,0.0382)
    y = 0.821*g(wavelength,568.8,0.0213,0.0247) + 0.286*g(wavelength,530.9,0.0613,0.0322)
    z = 1.217*g(wavelength,437.0,0.0845,0.0278) + 0.681*g(wavelength,459,0.0385,0.0725)
    return np.array((x,y,z))

### HELPER FUNCTIONS
def gaussian(x,mu,tau):
    return np.exp(-(tau**2)*((x-mu)**2)/2)

def piecewiseGaussian(x,mu,tau1,tau2):
    if x < mu:
        return gaussian(x,mu,tau1)
    return gaussian(x,mu,tau2)
import numpy as np
import math
#from scipy import optimize
from scipy.optimize import curve_fit

boundsPhase = [-np.pi/2,np.pi/2] #really should be this [was in ouptup_normal]
#boundsPhase = [-np.pi,np.pi]

def my_sin(x, amplitude, phase):
    return np.sin(x + phase) * amplitude

def my_cosin(x, amplitude, phase):
    return np.cos(x - phase) * amplitude

def convertToRad(toRad):
    return list(map(lambda x: np.radians(x),toRad))

def makeCurve(anglesInDegrees,a,b):
    rads = convertToRad(anglesInDegrees)
    ys = []
    for each in rads:
        ys.append(my_cosin(each,a,b)) #originally my sin
    return ys

def get_mean(diff):
    return sum(diff)/len(diff)

def get_min(diff):
    return min(diff)

def get_max(diff):
    return max(diff)
        

def fit(angle,diff):
    rads = convertToRad(angle)
    p0 = [get_mean(diff),0]
    the_min = get_min(diff)
    the_max = get_max(diff)
    try: #added this
        fit = curve_fit(my_cosin, rads, diff, p0=p0,bounds=((get_min(diff),boundsPhase[0]),(get_max(diff),boundsPhase[1]))) #originally my sin
        return (fit[0][0],fit[0][1])
    except:
        return (0,0)

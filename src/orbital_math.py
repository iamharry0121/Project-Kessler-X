import numpy as np

GRAVITATIONAL_CONSTANT = 3.986004418e14
EARTH_RADIUS = 6378.1

def degToRad(deg):
    rad = np.radians(deg)
    return rad

def calculateSemiMajorAxis(mean_motion_per_day):
    """
    Converts Mean Motion (revs/day) into the Semi-Major Axis 'a' (meters)
    using Kepler's Third Law. 
    """
    # 1. Convert revolutions per day to radians per second
    # (2 * pi radians per revolution / 86400 seconds in a day)
    n_rad_per_sec = mean_motion_per_day * (2 * np.pi / 86400.0)
    
    # 2. Kepler's Third Law: a = (MU / n^2)^(1/3)
    # In Python, ** (1/3) calculates the cube root
    a = (GRAVITATIONAL_CONSTANT / (n_rad_per_sec ** 2)) ** (1/3)
    
    return a

def get3dPosition(semi_major_axis, inclination_rad, raan_rad, mean_anomaly_rad):
    """
    Transforms the orbital elements into simple X, Y, Z coordinates.
    """
    # For a perfect circular orbit baseline:
    # X points towards the prime meridian, Y points sideways, Z points through the North Pole.
    
    # 1. Calculate the position in the flat orbital plane
    x_plane = semi_major_axis * np.cos(mean_anomaly_rad)
    y_plane = semi_major_axis * np.sin(mean_anomaly_rad)
    
    # 2. Rotate that plane into 3D space using the inclination and RAAN angles
    X = x_plane * np.cos(raan_rad) - y_plane * np.sin(raan_rad) * np.cos(inclination_rad)
    Y = x_plane * np.sin(raan_rad) + y_plane * np.cos(raan_rad) * np.cos(inclination_rad)
    Z = y_plane * np.sin(inclination_rad)
    
    return X, Y, Z
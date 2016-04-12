# Trace.py

#####################################################
#    Written by: Christopher Davis and Ivy Wanta    #
#    Version: 0.0.2                                 #
#    12 April 2016                                  #
#    christopher.davis@yale.edu                     #
#####################################################

# This script generates muons and propagates them through the CUORE cryostat
# As muons pass through the muon panels, detectors, and shieldings, a flag will be recorded for the ratio of muons that pass through each


import os
import math
import numpy as np
import random


global muon_plane_starting_z
muon_plane_starting_z = 10.0 # height of muon plane in meters

global muon_bottom_z
muon_bottom_z = -10.0

global muon_plane_Xwidth
muon_plane_Xwidth = 20 # width of muon plane in meters
global muon_plane_Ywidth
muon_plane_Ywidth = 20 # width of muon plane in meters
global N_muons
N_muons = 1e6 # number of muons to generate

global theta_filename
theta_filename="Theta_Macro_tab_delim.txt"
global phi_filename
phi_filename="Phi_Macro_tab_delim.txt"


# Create muon class
class muon:
    def __init__(self, starting_x, starting_y, starting_z, angle_theta, angle_phi):
        self.x = starting_x
        self.y = starting_y
        self.z = starting_z
        self.theta = angle_theta
        self.phi = angle_phi

# Generate muon
def generate_muon():

    # Start random number generator
    random.seed()

    # Get random (x,y) position on plane for muon to start
    x = random.uniform(-muon_plane_Xwidth/2, muon_plane_Xwidth/2)
    y = random.uniform(-muon_plane_Ywidth/2, muon_plane_Ywidth/2)
    z = muon_plane_starting_z


    # Load theta distribution
    theta_data = np.loadtxt(theta_filename, delimiter = "\t", dtype = float)
    theta_values = theta_data[:,0]
    theta_probabilities = theta_data[:,1]

    # Load phi distribution
    phi_data = np.loadtxt(phi_filename, delimiter = "\t", dtype = float)
    phi_values = phi_data[:,0]
    phi_probabilities = phi_data[:,1]

    #print sum(theta_probabilities)
    #print sum(phi_probabilities)


    # Generate theta from distribution
    theta = np.random.choice(theta_values, p = theta_probabilities)
    
    # Generate phi from distribution
    phi = np.random.choice(phi_values, p = phi_probabilities)

    generated_muon = muon(x, y, z, theta, phi)
    return generated_muon


# "Draw" a line given a muon's theta phi. Note: Maybe this function is unnecessary? Might use up too much memory, but may save computation time
def propagate_muon(mu):

    x = mu.x
    y = mu.y
    z = mu.z

    print "Starting at (%.2f, %.2f, %.2f) at theta = %.2f degrees and phi = %.2f degrees)" %(x, y, z, mu.theta, mu.phi)


    # convert to radians
    theta = mu.theta * math.pi / 180.0
    phi = mu.phi * math.pi / 180.0


    # Solve for new displacements in x,y,z from spherical coordinates
    # x = r sin(theta) cos(phi)
    # y = r sin(theta) sin(phi)
    # z = r cos(theta)

    # start with a "delta_z" of 0.01 m, might need to use 0.001 m later
    delta_z = 0.001 # 1 mm step size

    # initialize array of (x,y,z) coordinates
    travel = [(x,y,z)]

    print "Starting propagation..."

    i = 1
    while (True):
        # Use delta_r as "time-step" for other variables
        x = x + (delta_z / math.cos(theta)) * math.sin(theta) * math.cos(phi)
        y = y + (delta_z / math.cos(theta)) * math.sin(theta) * math.sin(phi)
        z = z - delta_z

        #print "muon at point (%.2f, %.2f, %.2f)" %(x, y, z)

        # save the x,y,z of the muon as it passes down through the cryostat. Then use this array in the check() functions
        travel.append((x,y,z))
      
        # check to see if the muon goes out of the range (xmin, xmax, ymin, ymax, zmin)
        if (math.fabs(x) >= muon_plane_Xwidth or math.fabs(y) >= muon_plane_Ywidth or z <= muon_bottom_z):
            break

    return travel

def panel_check(travel):

    # generate test panel geometry
    muon_panel_Zwidth = 0.03  # 3 cm width
    muon_panel_Xwidth = 4 #4 m
    muon_panel_Ywidth = 4
    muon_panel_Xcenter = 0 # Start at (0,0,0)
    muon_panel_Ycenter = 0
    muon_panel_Zcenter = 0
    
    # For each z layer in panel, check to see if mu passes through
    for (x,y,z) in travel:
        if (z > (muon_panel_Zcenter - muon_panel_Zwidth) and z < (muon_panel_Zcenter + muon_panel_Zwidth)):
            if (x > (muon_panel_Xcenter - muon_panel_Xwidth) and x < (muon_panel_Zcenter + muon_panel_Zwidth) and y > (muon_panel_Ycenter - muon_panel_Ywidth) and y < (muon_panel_Ycenter + muon_panel_Ywidth)):
                return 1
            else:
                continue
        if (z < (muon_panel_Zcenter - muon_panel_Zwidth)):
            return 0

    # return 1 if hit
    # return 0 if no hit

# Check if passes through detectors
def detector_check():

    # Get geometry of detectors
    
    # First model as a bunch of rectangular prisms

    # return 1 if hit
    # return 0 if no hit


    pass

# Check if passes through lead shield
def lead_check():

    # Get geometry of lead shielding
    
    # First model as a thin walled hollow cylinder
    
    # return 1 if hit
    # return 0 if no hit
    pass



# Output Ratios
def Output():
    pass


while True:
    mu = generate_muon()

    Points = propagate_muon(mu)
    
    test = panel_check(Points)

    print test
    
    if (test):
        break

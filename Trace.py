# Trace.py

#####################################################
#    Written by: Christopher Davis and Ivy Wanta    #
#    Version: 0.0.1                                 #
#    11 April 2016                                  #
#    christopher.davis@yale.edu                     #
#####################################################

# This script generates muons and propagates them through the CUORE cryostat
# As muons pass through the muon panels, detectors, and shieldings, a flag will be recorded for the ratio of muons that pass through each


import os
import numpy as np
import random


global muon_plane_starting_z
muon_plane_starting_z = 10 # height of muon plane in meters
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

    # Generate theta from distribution
    theta = np.random.choice(theta_values, p = theta_probabilities)
    
    # Generate phi from distribution
    phi = np.random.choice(phi_values, p = phi_probabilities)

    generated_muon = muon(x, y, z, theta, phi)
    return generated_muon


# "Draw" a line given a muon's theta phi. Note: Maybe this function is unnecessary? Might use up too much memory, but may save computation time
def propagate_muon():
    # save the x,y,z of the muon as it passes down through the cryostat. Then use this array in the check() functions
    pass


# Check if passes through paddles
def paddle_check():

    # Get geometry of paddles

    pass

# Check if passes through detectors
def detector_check():

    # Get geometry of detectors
    
    # First model as a bunch of rectangular prisms

    pass

# Check if passes through lead shield
def lead_check():

    # Get geometry of lead shielding
    
    # First model as a thin walled hollow cylinder
    pass



# Output Ratios
def Output():
    pass

test_muon = generate_muon()
print test_muon.x
print test_muon.y
print test_muon.z
print test_muon.theta
print test_muon.phi

# Trace.py

#####################################################
#    Written by: Christopher Davis and Ivy Wanta    #
#    Version: 0.1.0                                 #
#    13 April 2016                                  #
#    christopher.davis@yale.edu                     #
#####################################################

# This script generates muons and propagates them through the CUORE cryostat
# As muons pass through the muon panels, detectors, and shieldings, a flag will be recorded for the ratio of muons that pass through each


import os
import math
import numpy as np
import random

global muon_plane_starting_z
muon_plane_starting_z = -2 # height of muon plane in meters

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

global output_file # .dat file to convert to ROOT later
output_file = "Trace_output.dat"

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
def propagate_muon(mu):

    x = mu.x
    y = mu.y
    z = mu.z

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

    i = 1
    while (True):
        # Use delta_r as "time-step" for other variables
        x = x + (delta_z / math.cos(theta)) * math.sin(theta) * math.cos(phi)
        y = y + (delta_z / math.cos(theta)) * math.sin(theta) * math.sin(phi)
        z = z - delta_z

        # save the x,y,z of the muon as it passes down through the cryostat. Then use this array in the check() functions
        travel.append((x,y,z))
      
        # check to see if the muon goes out of the range (xmin, xmax, ymin, ymax, zmin)
        if (math.fabs(x) >= muon_plane_Xwidth or math.fabs(y) >= muon_plane_Ywidth or z <= muon_bottom_z):
            break

    return travel

def panel_check(travel):

    # panels around the lead (.5 m away)

    muon_paddle_cylinder_innerDiameter = 1.50
    muon_paddle_cylinder_outerDiameter = 1.53
    muon_paddle_cylinder_height = 2.0 # 2 meter height
    muon_paddle_cylinder_Rcenter = 0
    muon_paddle_cylinder_Zbottom = -4.4 - 0.550

    (x,y,z) = travel.pop()
    if (z >= muon_paddle_cylinder_Zbottom + muon_paddle_cylinder_height):
        return 0
    else:
        travel.append((x,y,z))

    for (x,y,z) in travel:
        if (z >= muon_paddle_cylinder_Zbottom and z <= (muon_paddle_cylinder_Zbottom + muon_paddle_cylinder_height)):
            if ((x*x + y*y) >= muon_paddle_cylinder_innerDiameter and (x*x + y*y) <= muon_paddle_cylinder_outerDiameter):
                return 1
            
        if (z < muon_paddle_cylinder_Zbottom):
            return 0
    
    return 0

"""
    # generate test panel geometry
    muon_panel_Zwidth = 0.03  # 3 cm width
    muon_panel_Xwidth = 4.0 #4 m
    muon_panel_Ywidth = 4.0
    muon_panel_Xcenter = 0.0 # Start at (0,0,0)
    muon_panel_Ycenter = 0.0
    muon_panel_Zcenter = 0.0

    # Check if muon makes it to the panel
    (x,y,z) = travel.pop()
    if (z >= muon_panel_Zcenter + muon_panel_Zwidth/2):
        return 0
    else:
        travel.append((x,y,z))
    
    # For each z layer in panel, check to see if mu passes through
    for (x,y,z) in travel:
        if (z >= (muon_panel_Zcenter - muon_panel_Zwidth/2) and z <= (muon_panel_Zcenter + muon_panel_Zwidth/2)):
            if (x >= (muon_panel_Xcenter - muon_panel_Xwidth/2) and x <= (muon_panel_Zcenter + muon_panel_Zwidth/2) and y >= (muon_panel_Ycenter - muon_panel_Ywidth/2) and y <= (muon_panel_Ycenter + muon_panel_Ywidth/2)):
                return 1
            else:
                continue
        if (z <= (muon_panel_Zcenter - muon_panel_Zwidth/2)):
            return 0
    return 0
    # return 1 if hit
    # return 0 if no hit
"""
# Check if passes through detectors
def detector_check(travel):


    # Get geometry of detectors
    # First model as a box
    detector_box_Zwidth = 0.8  # 80 cm width
    detector_box_Xwidth = 1.0 #1 m width
    detector_box_Ywidth = 1.0
    detector_box_Xcenter = 0.0 # Start at (0,0,-4)
    detector_box_Ycenter = 0.0
    detector_box_Zcenter = -4.0

    # Check if muon makes it to the detectors
    (x,y,z) = travel.pop()
    if (z >= detector_box_Zcenter + detector_box_Zwidth/2):
        return 0
    else:
        travel.append((x,y,z))

    
    # For each z layer in panel, check to see if mu passes through
    for (x,y,z) in travel:
        if (z >= (detector_box_Zcenter - detector_box_Zwidth/2) and z <= (detector_box_Zcenter + detector_box_Zwidth/2)):
            if (x >= (detector_box_Xcenter - detector_box_Xwidth/2) and x <= (detector_box_Xcenter + detector_box_Xwidth/2) and y >= (detector_box_Ycenter - detector_box_Ywidth/2) and y <= (detector_box_Ycenter + detector_box_Ywidth/2)):
                return 1

        elif (z < (detector_box_Zcenter - detector_box_Zwidth/2)):
            return 0
    return 0

# Check if passes through lead shield
def lead_check(travel):

    
    # Get geometry of lead shielding
    
    ### Used MC to get geometry ###
    ### Lead shielding is an octogon ###

    # Lead shield is formed by intersection of two boxes with length R to create an octogon. Hollowed out by second intersection of two boxes
    lead_shield_ext_box = 1.1 
    lead_shield_int_box = 0.85

    lead_shield_height = 1.64
    # height of bottom part of lead
    lead_shield_bottom = 0.2

    # Distance from bottom of lead shield to bottom of detectors
    lead_shield_startZ = -4.4 - 0.550 

    ### begin checks if inside lead ###
     
    # check to see if muon reaches lead

    (x,y,z) = travel.pop()
    if (z > lead_shield_bottom + lead_shield_height + lead_shield_startZ):
        return 0
    else:
        travel.append((x,y,z))    

    # check to see if muon passes through "hollow" part of lead shield
    # octagon relations
    # check if inside outer layer

    for (x,y,z) in travel:

        if ((z <= lead_shield_bottom + lead_shield_height + lead_shield_startZ) and (z > lead_shield_bottom + lead_shield_startZ)):

            if ((y <= lead_shield_ext_box) and (y >= -lead_shield_ext_box) and (x <= lead_shield_ext_box) and (x >= -lead_shield_ext_box) and ((x + y) <= lead_shield_ext_box) and ((x - y) <= lead_shield_ext_box) and ((x + y) >= -lead_shield_ext_box) and ((x - y) >= -lead_shield_ext_box)):

                # now check if outside inner layer
                if not ((y <= lead_shield_int_box) and (y >= -lead_shield_int_box) and (x <= lead_shield_int_box) and (x >= -lead_shield_int_box) and ((x + y) <= lead_shield_int_box) and ((x - y) <= lead_shield_int_box) and ((x + y) >= -lead_shield_int_box) and ((x - y) >= -lead_shield_int_box)):

                    return 1
                
        # same check for the bottom part of the lead
        elif ((z <= lead_shield_bottom + lead_shield_startZ) and (z > lead_shield_bottom)):

            if ((y <= lead_shield_ext_box) and (y >= -lead_shield_ext_box) and (x <= lead_shield_ext_box) and (x >= -lead_shield_ext_box) and ((x + y) <= lead_shield_ext_box) and ((x - y) <= lead_shield_ext_box) and ((x + y) >= -lead_shield_ext_box) and ((x - y) >= -lead_shield_ext_box)):

                return 1

        # stop sooner if muon goes beyond the bottom w/o hitting lead
        elif (z <= lead_shield_bottom + lead_shield_startZ):

            return 0


    return 0

"""
    # Get geometry of lead shielding
    
    # First model as a thin walled hollow cylinder
    
    # cylinder part
    lead_cylinder_innerDiameter = 3.0 #3 meter diameter
    lead_cylinder_outerDiameter = 3.2 # 20 cm width
    lead_cylinder_height = 2.5 # 2.5 meter height
    lead_cylinder_cap = 0.2 # 10 cm height of the bottom cap
    
    lead_cylinder_Rcenter = 0 # centered at r = 0
    lead_cylinder_Zbottom = -5 # 60 cm below bottom of detector box


    # Check if muon makes it to the lead
    (x,y,z) = travel.pop()
    if (z >= lead_cylinder_Zbottom + lead_cylinder_height):
        return 0
    else:
        travel.append((x,y,z))

    for (x,y,z) in travel:
        # Check if muon goes through the cylinder's sides
        if (z >= lead_cylinder_Zbottom and z <= (lead_cylinder_Zbottom + lead_cylinder_height)):
            if ((x*x + y*y) <= lead_cylinder_outerDiameter and (x*x + y*y) >= lead_cylinder_innerDiameter): 
                return 1

        # Check if muon goes through the bottom cap
        if (z >= lead_cylinder_Zbottom and z<= (lead_cylinder_Zbottom + lead_cylinder_cap)):
            if ((x*x + y*y) <= lead_cylinder_outerDiameter):
                return 1

        # Check if muon goes past the bottom
        if (z <= lead_cylinder_Zbottom):
            return 0

    # Return 0 if the muon goes out of the World Volume
    return 0
"""

# Output Ratios
def Output():
    pass

paddles = 0
detectors = 0
lead = 0
paddles_detectors = 0
paddles_lead = 0
detectors_lead = 0
paddles_detectors_lead = 0

i = 1

# open file to write .dat output to
dat = open(output_file, 'w')

print "*" * 80
while i <= 50000:
    mu = generate_muon()

    # write mu x,y,z,theta,phi to file
    dat.write("%s\t%s\t%s\t%s\t%s\n" %(mu.x, mu.y, mu.z, mu.theta, mu.phi))


    Points = propagate_muon(mu)
    
    test1 = panel_check(Points)
    test2 = detector_check(Points)
    test3 = lead_check(Points)

    paddles = paddles + test1
    detectors = detectors + test2
    lead = lead + test3

    paddles_detectors = paddles_detectors + (test1 * test2)
    paddles_lead = paddles_lead + (test1 * test3)
    detectors_lead = detectors_lead + (test2 * test3)
    paddles_detectors_lead = paddles_detectors_lead + (test1 * test2 * test3)

    #print "iteration: %s \t paddles: %s \t detectors: %s" %(i, paddles, detectors)
    #print "paddles: %s \t detectors: %s" %(test1, test2)

    i = i + 1

    if (i % 1000 == 0):
        print "iteration: %s \t paddles: %s \t detectors: %s \t lead: %s" %(i, paddles, detectors, lead)
        print "pad + det: %s \t pad + lead: %s \t det + lead: %s \t pad + det + lead: %s" %(paddles_detectors, paddles_lead, detectors_lead, paddles_detectors_lead)
        print "*" * 80


#    if (test2 and test1):
#        break

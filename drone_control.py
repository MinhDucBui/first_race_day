import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

from keyboard_control import keyboard_mode
from coordinate_control import coordinate_mode
from checkpoint_reached import check_if_coordinates_reached


# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

threshold = 1
coordinate_point = [10, -10, -10]

keep_flying = True
while keep_flying:
    value = input("Please choose mode on how to fly the drone. 'coordinate_control' or 'keyboard_control'. To end and reset, enter 'end'. \n\n\n")

    if value == 'coordinate_control':
        coordinate_mode(client)
    elif value == 'keyboard_control':
        keyboard_mode(client)
    elif value == 'end':
        client.armDisarm(False)
        client.reset()
        keep_flying = False
    else:
        print("ERROR: Not an accepted input")
    
    
    coordinate_reached_check = check_if_coordinates_reached(client, coordinate_point, threshold)
    
    if coordinate_reached_check:
        print("Coordinate was reached")
    else:
        print("Coordinate was not reached")
    
    
client.enableApiControl(False)
    


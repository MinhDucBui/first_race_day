import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
from pyreadline import Readline
import readchar
#import readline
readline = Readline()
# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)


airsim.wait_key('Press any key to takeoff')
client.takeoffAsync()

print("\n\n\n")
print("Please choose direction to fly [wasd], 'o' to fly up, 'p' to fly down. Enter 'end' to reset drone\n")
while readchar.readchar():
    
    value = readchar.readkey()
    state = client.getMultirotorState()
    x_coordinate = state.kinematics_estimated.position.x_val
    y_coordinate = state.kinematics_estimated.position.y_val
    z_coordinate = state.kinematics_estimated.position.z_val

    if value == "k":
        client.armDisarm(False)
        client.reset()
        break
    elif value == "w":
        client.moveToPositionAsync(x_coordinate + 4, y_coordinate, z_coordinate, 5)
    elif value == "d":
        client.moveToPositionAsync(x_coordinate, y_coordinate + 4, z_coordinate, 5)
    elif value == "a":
        client.moveToPositionAsync(x_coordinate, y_coordinate - 4, z_coordinate, 5)
    elif value == "s":
        client.moveToPositionAsync(x_coordinate - 4, y_coordinate, z_coordinate, 5)
    elif value == "o":
        client.moveToPositionAsync(x_coordinate, y_coordinate , z_coordinate - 4, 5)
    elif value == "p":
        client.moveToPositionAsync(x_coordinate, y_coordinate, z_coordinate + 4, 5)
    elif value == "give_coordinates":
        state = client.getMultirotorState()
        drone_x = state.kinematics_estimated.position.x_val
        drone_y = state.kinematics_estimated.position.y_val
        drone_z = state.kinematics_estimated.position.z_val
        print("{}".format([drone_x, drone_y, drone_z]))
    
        
    print("\n\n\n")
    
    
    
    

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)

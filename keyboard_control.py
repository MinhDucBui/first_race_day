import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2


def keyboard_mode(client):


    client.takeoffAsync()
    print("\n\n\n")
    keep_flying = True
    while keep_flying:


        value = input("Please choose direction to fly [wasd], 'o' to fly up, 'p' to fly down. Enter 'end' to exit keyboard control and 'reset' to reset drone.\n")
        state = client.getMultirotorState()
        x_coordinate = state.kinematics_estimated.position.x_val
        y_coordinate = state.kinematics_estimated.position.y_val
        z_coordinate = state.kinematics_estimated.position.z_val
        print(z_coordinate)
        if value == "reset":
            client.reset()
            client.enableApiControl(True)
            client.armDisarm(True)
        elif value == "end":
            keep_flying = False
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
    
if __name__ == "__main__":
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    keyboard_mode(client)
    client.armDisarm(False)
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)

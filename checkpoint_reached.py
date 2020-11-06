import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import math


# checkpoint = [x, y, z]
def check_if_coordinates_reached(client, coordinate, threshold):

    state = client.getMultirotorState()
    drone_x = state.kinematics_estimated.position.x_val
    drone_y = state.kinematics_estimated.position.y_val
    drone_z = state.kinematics_estimated.position.z_val
    #print("\n\nPosition of Drone: {}".format([drone_x, drone_y, drone_z]))
    #print("Checkpoint Coordinates: {}".format(coordinate))
    
    checkpoint_x = coordinate[0]
    checkpoint_y = coordinate[1]
    checkpoint_z = coordinate[2]
    
    squared_dist = (checkpoint_x - drone_x)**2 + (checkpoint_y - drone_y)**2 + (checkpoint_z - drone_z)**2
    dist = math.sqrt(squared_dist)
    
    if dist <= threshold:
        return True
    else:
        return False
    

if __name__ == "__main__":
    print("check_if_coordinates_reached")

import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2



def coordinate_mode(client, user_input_mode = True, given_coordinates = [], take_off_drone = True, given_velocity = 5):
    keep_flying = True
    while keep_flying:
        if user_input_mode:
            user_coordinates = input("Please enter coordinates to fly to in the following format: 'x_coordinate, y_coordinate, z_coordinate'. Enter 'end' to exit coordinate control and 'reset' to reset drone.\n")
            
            if user_coordinates == "reset":
                client.armDisarm(False)
                client.reset()
            elif user_coordinates == "end":
                keep_flying = False
            else:
                user_velocity = input("\nPlease enter the velocity:\n")
                user_velocity = int(user_velocity)
                user_coordinates_split = user_coordinates.replace(" ", "").split(",")
                
            
        else:
            user_coordinates_split = given_coordinates
            user_velocity = given_velocity
            keep_flying = False
            
        if take_off_drone:
            print("\nTakeoff...\n")
            client.takeoffAsync().join()
            
        x_coordinate = float(user_coordinates_split[0])
        y_coordinate = float(user_coordinates_split[1])
        z_coordinate = float(user_coordinates_split[2])
        print("\nFlying to coordinates...\n")
        client.moveToPositionAsync(x_coordinate, y_coordinate, z_coordinate, user_velocity).join()
        


if __name__ == "__main__":
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    coordinate(client)
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)

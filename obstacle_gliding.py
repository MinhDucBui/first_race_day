import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time
from checkpoint_reached import check_if_coordinates_reached
import random


def give_relativ_direction(start, end, random_x):
    
    k = np.array(end) - np.array(start)
    x = random_x
    x -= x.dot(k) * k / np.linalg.norm(k)**2
    x /= np.linalg.norm(x)
    y = np.cross(k, x)
    return x, y, k



def obstacle_gliding_mode(client, user_input_mode = True, start_coordinates = [], given_coordinates = [], take_off_drone = True, given_velocity = 5, treshold = 2):
    keep_flying = True
    

    if take_off_drone:
        #print("\nTakeoff...\n")
        client.takeoffAsync()
        time.sleep(1)
    
    x_coordinate = float(given_coordinates[0])
    y_coordinate = float(given_coordinates[1])
    z_coordinate = float(given_coordinates[2])
    

    start_x_coordinate = float(start_coordinates[0])
    start_y_coordinate = float(start_coordinates[1])
    start_z_coordinate = float(start_coordinates[2])
    
    #print("\nFlying to {}...\n".format([x_coordinate, y_coordinate, z_coordinate]))
    
    
    previous_coordinates = [x_coordinate, y_coordinate, z_coordinate]

    reached_checkpoint = False
    

    
    index_added_coordinates = 0
    given_velocity = 10
    if_collided = True
    random_x = np.random.randn(3)
    index_collision_count = 0
    index_flew_past = 0
    while not reached_checkpoint:

        
        if if_collided:
            client.moveToPositionAsync(x_coordinate, y_coordinate, z_coordinate, given_velocity)
            if_collided = False
        else:
            index_flew_past += 1
            
        if index_flew_past > 40:
            client.moveToPositionAsync(start_x_coordinate, start_y_coordinate, start_z_coordinate, given_velocity)
            time.sleep(2)
            client.moveToPositionAsync(x_coordinate, y_coordinate, z_coordinate, given_velocity)
            index_flew_past = 0
            
        state = client.getMultirotorState()
        x_angular = state.kinematics_estimated.linear_velocity.x_val
        y_angular = state.kinematics_estimated.linear_velocity.y_val
        z_angular = state.kinematics_estimated.linear_velocity.z_val
        
        if x_angular == 0 and y_angular == 0 and z_angular == 0:
            time.sleep(1)
            state = client.getMultirotorState()
            x_angular = state.kinematics_estimated.linear_velocity.x_val
            y_angular = state.kinematics_estimated.linear_velocity.y_val
            z_angular = state.kinematics_estimated.linear_velocity.z_val
            if x_angular == 0 and y_angular == 0 and z_angular == 0:
                client.takeoffAsync()
                time.sleep(2)
                client.moveToPositionAsync(x_coordinate, y_coordinate, z_coordinate, given_velocity)
        state = client.getMultirotorState()
        current_x_coordinate = state.kinematics_estimated.position.x_val
        current_y_coordinate = state.kinematics_estimated.position.y_val
        current_z_coordinate = state.kinematics_estimated.position.z_val
        previous_coordinates = [current_x_coordinate, current_y_coordinate, current_z_coordinate]
        
        time.sleep(0.2)
        reached_checkpoint = check_if_coordinates_reached(client, given_coordinates, treshold)
        collision_info = client.simGetCollisionInfo()
        if_collided = collision_info.has_collided
            
        if if_collided:
            state = client.getMultirotorState()
            current_x_coordinate = state.kinematics_estimated.position.x_val
            current_y_coordinate = state.kinematics_estimated.position.y_val
            current_z_coordinate = state.kinematics_estimated.position.z_val
                    
            orth_1, orth_2, k = give_relativ_direction([current_x_coordinate, current_y_coordinate, current_z_coordinate], [x_coordinate, y_coordinate, z_coordinate], random_x)
            

            added_coordinates = [orth_1*10, -orth_1*10, orth_2*10, -orth_2*10]
           
            if_direction_collided = try_direction(client, [current_x_coordinate, current_y_coordinate, current_z_coordinate], added_coordinates[index_added_coordinates])
            if if_direction_collided:
                index_collision_count += 1
                if index_collision_count == 5:
                    index_collision_count = 0
                    index_added_coordinates = (index_added_coordinates + 1) % 4
            else:
                index_collision_count = 0
                
    return
                                                                        
        
            
        
        

        
def try_direction(client, previous_coordinates, added_coordinates):
    
    client.moveToPositionAsync(previous_coordinates[0] + added_coordinates[0], previous_coordinates[1] + added_coordinates[1], previous_coordinates[2] + added_coordinates[2], 10)
    time.sleep(0.5)

    collision_info = client.simGetCollisionInfo()
    if_collided = collision_info.has_collided
    return if_collided




if __name__ == "__main__":
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    coordinate(client)
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)

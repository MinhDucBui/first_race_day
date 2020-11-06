import time
from time import gmtime, strftime
import threading
import queue

import airsim
import numpy as np
import os
import tempfile
import pprint
import cv2
import readline



def coordinate(client):
    keep_flying = True
    while keep_flying:
    
        lock.acquire()
        user_coordinates = input("Please enter coordinates to fly to in the following format: 'x_coordinate, y_coordinate, z_coordinate'. Enter 'end' to exit coordinate control and 'reset' to reset drone.\n")
        lock.release()
        
        if user_coordinates == "reset":
            client.armDisarm(False)
            client.reset()
        elif user_coordinates == "end":
            keep_flying = False
        else:
            lock.acquire()
            user_velocity = input("\nPlease enter the velocity:\n")
            user_velocity = int(user_velocity)
            lock.release()
                    
            start_time = time.time()
            
            user_coordinates_split = user_coordinates.replace(" ", "").split(",")
            x_coordinate = int(user_coordinates_split[0])
            y_coordinate = int(user_coordinates_split[1])
            z_coordinate = int(user_coordinates_split[2])

            print("\nTakeoff...\n")
            client.takeoffAsync().join()
            print("\nFlying to coordinates...\n")
            client.moveToPositionAsync(x_coordinate, y_coordinate, z_coordinate, user_velocity)
            
            print ("\nFlight to checkpoint took", time.time() - start_time, "\n")
            
            
def timestamp():
    while True:
        while not lock.locked():

            print(strftime("%H:%M:%S", gmtime()))
            time.sleep(1)


if __name__ == "__main__":


    lock = threading.Lock()

    
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
#    coordinate(client)
    
    x = threading.Thread(target=timestamp)
    x.daemon = True
    x.start()
    
    y = threading.Thread(target = coordinate, args = (client,))
    y.start()
    

    
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)

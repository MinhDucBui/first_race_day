#!/usr/bin/env python

import airsim
import time

def teleport(client, x, y, z, ignore_collision=True):
    x, y, z = float(x), float(y), float(z)

    pose = client.simGetVehiclePose()

    pose.position.x_val = x
    pose.position.y_val = y
    pose.position.z_val = z

    client.simSetVehiclePose(pose=pose, ignore_collison=ignore_collision)
    
    

if __name__ == "__main__":
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Make sure drone didn't take off!
    # For some reason, the drone returns to it's initial position if has
    # already taken off.
    # client.takeoffAsync()

    while True:
        coordinates = input("Input coordinates as: x,y,z or hit return/enter to stop the script:\n")
        coordinates = coordinates.strip()

        if not coordinates:
            break

        teleport(client, *coordinates.split(","))

    client.armDisarm(False)
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)

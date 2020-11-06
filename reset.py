import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2


    
if __name__ == "__main__":
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    client.reset()
    client.enableApiControl(True)
    client.armDisarm(True)
    client.armDisarm(False)
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)

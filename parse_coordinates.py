import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

import numpy as np

def user_coordinates(raw_string):
    user_coordinates_data =raw_string.replace(" ", "").replace("\n", "").split(",")
    x_coordinate = float(user_coordinates_data[0])
    y_coordinate = float(user_coordinates_data[1])
    z_coordinate = float(user_coordinates_data[2])
    return (x_coordinate,y_coordinate,z_coordinate)

def coordinates_textfile(filename):
	f = open(filename, "r")
	coordinates = []
	while True:
		raw_string = f.readline()
		if not raw_string:
			break
		else:
			coordinates.append(user_coordinates(raw_string))
	return coordinates


def coordinates_cmd():
	current_checkpoint = 1
	coordinates = []   #list of tuples, each tuple having 3 elements (x,y,z coordinate)
	nr_checkpoints = int(input("Enter number of checkpoints:"))
	print("*checkpoints are separated with comma*")
	while current_checkpoint <= nr_checkpoints:
		raw_string = input("Checkpoint number" + str(current_checkpoint) + ": ")
		coordinates.append(user_coordinates(raw_string))
		current_checkpoint +=1
	return coordinates
	

if __name__ == "__main__":
    # connect to the AirSim simulator
	client = airsim.MultirotorClient()
	client.confirmConnection()
	client.enableApiControl(True)
	client.armDisarm(True)
	from_texfile = True
	filename = "coordinates.txt"
	if from_texfile:
		print(coordinates_textfile(filename))
	else:
		print(coordinates_cmd())

    # that's enough fun for now. let's quit cleanly
	client.enableApiControl(False)

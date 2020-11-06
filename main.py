import airsim
import sys, os
import codecs as codecs
import time

from parse_coordinates import coordinates_textfile, coordinates_cmd
from coordinate_control import coordinate_mode
from checkpoint_reached import check_if_coordinates_reached
from teleport_vehicle import teleport

from time import gmtime, strftime
import threading
import queue

from stopwatch import timestamp
from coordinate_control import coordinate_mode

from obstacle_gliding import obstacle_gliding_mode

import numpy as np
import random


def init_params(args):
    imports = "" #"import experiments.models\n"
    params_file = ''
    have_par_file = False
    if len(args) > 1:
        params_file = args[1]
        if os.path.exists(params_file):
            print('Loading par-file {}!'.format(params_file))
            # Load the parameters!
            parfile_locals = {}
            exec(imports + codecs.open(params_file, encoding='utf-8').read(), globals(), parfile_locals)
            have_par_file = True
            if 'params' not in parfile_locals:
                assert 0, 'Must at least specify params dictionary in parfile!'
    if not have_par_file:
        if len(args) > 1:
            print('The file {} does not exist or is not a valid parfile!\n'.format(params_file))
        else:
            print('Missing argument for parfile!\n')
        print('USAGE: {} <parfile>\n\n'.format(args[0]))
        sys.exit(1)
    
    return parfile_locals['params']
    
    
    
def start_drone_flying(client, get_coordinates, treshold, velocity):
    start_time = time.time()
    start_coordinates = list(get_coordinates[0])
    checkpoint_times = []
    for index, single_coordinate in enumerate(get_coordinates):
        if index == 0:
            teleport(client, *single_coordinate)
        else:
            single_coordinate = list(single_coordinate)

            drone_flying_mode(client, start_coordinates, single_coordinate, velocity, index, treshold)
            one_checkpoint_time = time.time() - start_time
            print("{}. Checkpoint reached in {} seconds.".format(index,  one_checkpoint_time))
            checkpoint_times.append(one_checkpoint_time)
        start_coordinates = list(single_coordinate)
        
    print("\n---------RACE SUCCESSFULLY FINISHED-----------\n")
    for index, i in enumerate(checkpoint_times):
        print("{}. Checkpoint reached in {} seconds.".format(index + 1, i))
        
    print("\n\nRace finished in {} seconds!".format(checkpoint_times[-1]))
    
    

        
        
 
    
    
def drone_flying_mode(client, start_coordinates, single_coordinate, velocity, index, treshold):
    
    if index == 0:
        obstacle_gliding_mode(client, start_coordinates = start_coordinates, given_coordinates = single_coordinate, take_off_drone = True, given_velocity = velocity, treshold = treshold)
        #coordinate_mode(client, user_input_mode = False, given_coordinates = single_coordinate, take_off_drone = True, given_velocity = velocity)
    else:
        obstacle_gliding_mode(client, start_coordinates = start_coordinates, given_coordinates = single_coordinate, take_off_drone = False, given_velocity = velocity, treshold = treshold)
        #coordinate_mode(client, user_input_mode = False, given_coordinates = single_coordinate, take_off_drone = False, given_velocity = velocity)
        
        
def reformatting_coordinates(coordinate_input):
    get_coordinates = []
    if isinstance(coordinate_input, str):
        if coordinate_input == "use_terminal":
            get_coordinates = coordinates_cmd()
        elif coordinate_input.split(".")[-1] == "txt":
            get_coordinates = coordinates_textfile(coordinate_input)
            
    elif isinstance(coordinate_input, list):
        get_coordinates = coordinate_input
    else:
        print("NO LEGAL INPUT")
        
    return get_coordinates

            

    
    



if __name__ == "__main__":
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    

    
    # PARAMETER
    params = init_params(sys.argv)
    coordinate_input = params["coordinate_input"]
    treshold = params["checkpoint_distance_treshold"]
    # TODO: VELOCITY HARD CODED
    velocity = 5
    
    get_coordinates = reformatting_coordinates(coordinate_input)
    
    
    
    messages = queue.Queue()
    lock = threading.Lock()
    x = threading.Thread(target=timestamp, args = (lock, messages,))
    x.daemon = True
    x.start()
    
    
    y = threading.Thread(target = start_drone_flying, args = (client, get_coordinates, treshold, velocity ))
    y.start()
    


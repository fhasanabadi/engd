import time

class CustomTimer:
    def __init__(self):
        try:
            self.timer = time.perf_counter
        except AttributeError:
            self.timer = time.time

    def time(self):
        return self.timer()

import glob
import os
import sys

try:
    sys.path.append(glob.glob('/home/fhasanabadi/Git/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import torch, cv2, sys

try:
    sys.path.append('/home/fhasanabadi/Git/carla/PythonAPI/examples/01_tutorials_Farshad/01_main/yolov5')
except IndexError:
    pass

import carla
import argparse
import random
import time
import numpy as np
from queue import Queue, Empty, PriorityQueue


# Sensor callback.
# This is where you receive the sensor data and
# process it as you liked and the important part is that,
# at the end, it should include an element into the sensor queue.
def sensor_callback(sensor_data, sensor_queue, sensor_name):
    # Do stuff with the sensor_data data like save it to disk
    # Then you just need to add to the queue
    sensor_queue.put((sensor_data.frame, sensor_name))

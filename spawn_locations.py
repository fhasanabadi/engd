from cv2 import transform
from utils_main import *

'''
this script is written to guarantee certain distance of spawning points from each other.

the file does not function properly now. 




'''
import random

def spawnLocations(client, number_of_locations, distanceLimitation = 2.0):

    world = client.get_world()
    spawn_transforms = []
    spawn_transforms.append(random.choice(world.get_map().get_spawn_points()))
    print(spawn_transforms, ' spawn transform inside spawn_locations functions')

    for _ in range(1, number_of_locations):

        while True:
            print('------------------ inside while loop: spawn_locatoins file', '\n')
            spawn_points = world.get_map().get_spawn_points()
            transform_candidate = random.choice(spawn_points)

            for _ in range(len(spawn_transforms)):
                print('inside for loop: spawn_location file' , '\n')
                if spawn_transforms[_].location.distance(transform_candidate.location) > distanceLimitation:
                #if carla.Vector3D(spawn_transforms[_]).distance(carla.Vector3D(transform_candidate)) < distanceLimitation:
                    

                    pass

                else:
                    break

                if _ == len(spawn_transforms) - 1:
                    spawn_transforms.append(transform_candidate)
                    
            if len(spawn_transforms) == number_of_locations:
                break
    
    return spawn_transforms

                    

        
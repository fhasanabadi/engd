from utils_main import *
from dsmanager import *

#transform = carla.Transform(carla.Location(x = -5.626226, y = 133.726013, z = 0.6), carla.Rotation(yaw = -179.647827))

#print(dir(location))
#print(location)
#print(location.location.x)
#transform.location.x +=5

#print(transform)

def incidentCreator2(client, transform, length):

    world = client.get_world()

    map = world.get_map()
    #waypoint = map.get_waypoint(location.location)
    incidentsList = []



    for _ in range(int(length)):
        incidentsList += incidentCreator(client, transform)
        waypoint = map.get_waypoint(transform.location)

        transform = waypoint.next(2.0)[0].transform



    return incidentsList

def centerFinder(world, location):
    
    map = world.get_map()
    waypoint = map.get_waypoint(location.location)


    location1 = waypoint.transform.location
    location2 = waypoint.next(1.0)[0].transform.location

    normal = (carla.Vector3D(location1) - carla.Vector3D(location2)).make_unit_vector()
    normal.x , normal.y = normal.y, normal.x
    laneWidth = waypoint.lane_width/2

    newLocation = carla.Transform(carla.Location(laneWidth * normal + location1), location.rotation)

    return newLocation


def incidentCreator(client, transform:carla.libcarla.Transform):

    world = client.get_world()
    if not isinstance(transform, carla.libcarla.Transform):
        print('location type is not correct')
        return 


    incident = None
    incident_list = []
    timer = CustomTimer()

    try:
        #get the world
        #world = client.get_world()
        original_settings = world.get_settings()




        bpCone = world.get_blueprint_library().filter('static.prop.constructioncone')[0]
        bpBarrier = world.get_blueprint_library().filter('static.prop.streetbarrier')[0]
        




        #incident01 = world.spawn_actor(bpCone, newTransform)
        #incident_list.append(incident01)
        newTransform = centerFinder(world, transform)
        #incident02 = world.spawn_actor(bpBarrier, newTransform)
        incident02 = world.spawn_actor(bpBarrier, newTransform)

        incident_list.append(incident02)

        return incident_list


    except:
        print('could not spawn the incidents')
        client.apply_batch([carla.command.DestroyActor(x) for x in incident_list])
        return []
        #world.apply_settings(original_settings)

def getPreviousTransform(world, transform, distance = 1.0):
    map = world.get_map()
    waypoint = map.get_waypoint(transform.location)
    waypoint = waypoint.previous(distance)[-1]

    transform = waypoint.transform

    return transform



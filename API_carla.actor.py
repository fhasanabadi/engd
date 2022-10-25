from incident_spawner import incidentCreator, centerFinder
from car_spawner import *

from utils_main import *
from dsmanager import *
import random

def run_simulation(args, client):

    display_manager = None
    vehicle = None
    vehicle_list = []
    timer = CustomTimer()

    try:
        #get the world
        i = 0
        world = client.get_world()
        original_settings = world.get_settings()

        if args.sync:
            traffic_manager = client.get_trafficmanager(8000)
            settings = world.get_settings()
            traffic_manager.set_synchronous_mode(True)
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            world.apply_settings(settings)

        bp = world.get_blueprint_library().filter('charger_2020')[0]
        bp_forActorAttribute = world.get_blueprint_library().filter('charger_2020')
        locations = random.choices(world.get_map().get_spawn_points(), k= 30)

        #print('actor attribute id: ' ,carla.ActorAttribute(bp_forActorAttribute))

        for _ in range(len(locations)):
            vehicle_list += incidentCreator(client, locations[_])
        location01 = carla.Transform(carla.Location(x = -5.626226, y = 133.726013, z = 0.6), carla.Rotation(yaw = -179.647827))
        map = world.get_map()
        #waypoints = map.get_waypoint(location01)[:1]

        locations_for_vehicles = random.choices(world.get_map().get_spawn_points(), k= 5)
        '''
        for _ in locations_for_vehicles:
            vehicle,sensor = vehicle_spawner(client = client , location = _)
            vehicle_list.append(vehicle)
        '''
        vehicle, sensors = vehicle_spawner(client = client, location = location01)
        vehicle_list.append(vehicle)
        '''
        sensors[0].listen(lambda image: image.save_to_disk('output/%6d.jpg'%image.frame))
        sensors[2].listen(lambda image: image.save_to_disk('output/%6dl.jpg'%image.frame))
        sensors[4].listen(lambda image: image.save_to_disk('output/%6dr.jpg'%image.frame))
        '''

        
        sensors['center_camera'].listen(lambda image: image.save_to_disk('output/%6d.jpg'%image.frame))
        sensors['left_camera'].listen(lambda image: image.save_to_disk('output/%6dl.jpg'%image.frame))
        sensors['right_camera'].listen(lambda image: image.save_to_disk('output/%6dr.jpg'%image.frame))
       

        #sensor[0].listen(lambda image: image.save_to_disk('tutorial/ %.6d.jpg' % image.frame))
        #sensor[1].listen(lambda image: image.save_to_disk('tutorial/ 01%.6d.jpg' % image.frame))
        

        


        #vehicle = world.spawn_actor(bp, location01)
        #vehicle.set_autopilot(True)

        #print('actor attribute id: ' , vehicle.ActorAttribute())
        #vehicle_list.append(vehicle)
        #transform = location01
        #transform.location.x +=3
        #incidentList = incidentCreator(client = client, transform = transform)
        #vehicle_list += incidentList
        #print(incidentList)
        #print(vehicle_list)



        time_init_sim = timer.time()

        while True:

            i+=1
            if args.sync:
                world.tick()
            
            if i%100==0:
                #sensor.listen(lambda image: image.save_to_disk('tutorial/ %.6d.jpg' % image.frame))

                '''
                #carla.Actor
                print(' type of the object: ', type(vehicle_list[0]) )
                print('attributes: ' , vehicle_list[0].attributes)
                print('id: ' , vehicle_list[0].id )
                print('is alive: ' , vehicle_list[0].is_alive)
                print('parent: ' , vehicle_list[0].parent)
                print('semantic tags: ', vehicle_list[0])
                print('type_id:  ', vehicle_list[0])
                print('show_debug_telemetry: ' , vehicle_list[0].show_debug_telemetry(enabled = True))
                #getters
                print('get acceleration: ', vehicle_list[0].get_acceleration())
                print('get angular velocity: ', vehicle_list[0].get_angular_velocity())
                print('get location: ', vehicle_list[0].get_location())
                print('get transform: ', vehicle_list[0].get_transform())
                print('get velocity: ', vehicle_list[0].get_velocity())
                print('get world: ', vehicle_list[0].get_world())
                #setters


                #carla.ActorBlueprint
                print('actorblueprint id: ' , vehicle_list[0].id)
                #does not have tags!
                # print('actor blueprint tags' , vehicle_list[0].tags)

                #print(client.ActorList.ActorList())
                #print('world.getactors(): ' ,world.get_actors())


                '''


                

    finally:
        

        client.apply_batch([carla.command.DestroyActor(x) for x in vehicle_list])
        world.apply_settings(original_settings)

def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Sensor tutorial')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Synchronous mode execution')
    argparser.add_argument(
        '--async',
        dest='sync',
        action='store_false',
        help='Asynchronous mode execution')
    argparser.set_defaults(sync=True)
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='window resolution (default: 1280x720)')

    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]
    print(args.host)
    print(' arg sync' , args.sync)

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(5.0)
        '''
        location01 = carla.Transform(carla.Location(x = -5.626226, y = 133.726013, z = 0.6), carla.Rotation(yaw = -179.647827))
        world = client.get_world()
        map = world.get_map()
        waypoint = map.get_waypoint(location01.location)

        waypoints = []
        waypoints.append(waypoint)
        print('lane width : ' , waypoint.lane_width)
        print('waypoint transform : ' , waypoint.transform)
        waypoints.append(waypoint.next(1.0))

        location1 = waypoint.transform.location
        location2 = waypoint.next(1.0)[0].transform.location
        normal = (carla.Vector3D(location1) - carla.Vector3D(location2)).make_unit_vector()
        print(normal)
        normal.x , normal.y = normal.y, normal.x
        print(normal)
        laneWidth = waypoint.lane_width/2
        print(laneWidth * normal)
        newLocation = carla.Transform(carla.Location(laneWidth*normal + location1), location01.rotation)
        bpCone = world.get_blueprint_library().filter('static.prop.constructioncone')[0]

        print(type(newLocation), newLocation)
        #vehicle = world.spawn_actor(bpCone, location01)
        #vehicle = world.spawn_actor(bpCone, newLocation)

        

        print('waypoint transform : ' , waypoint.next(1.0)[0].transform)


        #print([_.lane_width for _ in waypoints]) '''
        

        run_simulation(args, client)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()



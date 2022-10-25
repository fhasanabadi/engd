from incident_spawner import incidentCreator
from utils_main import *
from spawn_locations import *
import random







def run_simulation(args, client):

    display_manager = None
    vehicle = None
    vehicle_list = []
    timer = CustomTimer()

    try:
        #get the world
        world = client.get_world()
        original_settings = world.get_settings()

        if args.sync:
            traffic_manager = client.get_trafficmanager(8000)
            settings = world.get_settings()
            traffic_manager.set_synchronous_mode(True)
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            world.apply_settings(settings)

        #location01 = carla.Transform(carla.Location(x = -5.626226, y = 133.726013, z = 0.6), carla.Rotation(yaw = -179.647827))

        #vehicle_bp = world.get_blueprint_library().filter('charger_2020')[0]

        #vehicle = world.spawn_actor(vehicle_bp, location01)
        #vehicle_list.append(vehicle)

        locations = spawnLocations(client, 5)
        print('locations ; ; ; ' , locations)

        #print([print(_.location) for _ in locations])
        '''
        locations = random.choices(world.get_map().get_spawn_points(), k = 2)

        print([type(_) for _ in locations])
        print([print(_.location) for _ in locations])

        distance = locations[0].location.distance(locations[1].location)
        print(distance)
        '''        

        for _ in locations:
            vehicle_list+= incidentCreator(client, _)

        

        time_init_sim = timer.time()
        i = 0
        while True:

            i+=1

            if args.sync:
                world.tick()
            
            if i%100==0:
                #sensor.listen(lambda image: image.save_to_disk('tutorial/ %.6d.jpg' % image.frame))
            #    print(world.get_actors())
                #print(world.get_actors(), '\n')
                #print('length of the actors list' , len(world.get_actors()),'\n')
                #print('type of actors list', type(world.get_actors()),'\n')



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


        run_simulation(args, client)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
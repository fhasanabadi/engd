
from utils_main import *

#change map documentation:
#https://carla.readthedocs.io/en/latest/core_map/#changing-the-map

#list of maps:
listOfMaps = ['/Game/Carla/Maps/Town04', '/Game/Carla/Maps/Town10HD', '/Game/Carla/Maps/Town02_Opt', '/Game/Carla/Maps/Town10HD_Opt', '/Game/Carla/Maps/Town01_Opt', '/Game/Carla/Maps/Town01', '/Game/Carla/Maps/Town05', '/Game/Carla/Maps/Town03', '/Game/Carla/Maps/Town02', '/Game/Carla/Maps/Town05_Opt', '/Game/Carla/Maps/Town03_Opt', '/Game/Carla/Maps/Town04_Opt']
def changeMap(client, town = 'Town01'):
    world = client.load_world(town)

    return world


def run_simulation(args, client):

    display_manager = None
    vehicle = None
    vehicle_list = []
    sensor_list = []
    incident_list = []
    timer = CustomTimer()


    try:
        world = client.get_world()
        original_settings = world.get_settings()

        if args.sync:
            traffic_manager = client.get_trafficmanager(8000)
            settings = world.get_settings()
            traffic_manager.set_synchronous_mode(True)
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            world.apply_settings(settings)

       # changeWeather(world, weatherNum=0)
        print(client.get_available_maps())
        world = client.load_world('Town01')

        

        i = 0

        while True:

            i+=1

            if i%100 == 0:


                #print(world.get_weather())
                pass


 

            if args.sync:
                world.tick()

    finally:
        #print('cancelled by the user')
        #world.apply_settings(original_settings)
        #world.apply_settings(settings)
        pass
    

    


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


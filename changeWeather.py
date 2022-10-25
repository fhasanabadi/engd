from cProfile import run
from utils_main import *

#reference for weather parameters:
# https://carla.readthedocs.io/en/0.9.3/python_api/#carlaweatherparameters

weatherList = [carla.WeatherParameters.ClearNoon,
carla.WeatherParameters.CloudyNoon,
carla.WeatherParameters.WetNoon,
carla.WeatherParameters.WetCloudyNoon,
carla.WeatherParameters.MidRainyNoon,
carla.WeatherParameters.HardRainNoon,
carla.WeatherParameters.SoftRainNoon,
carla.WeatherParameters.ClearSunset,
carla.WeatherParameters.CloudySunset,
carla.WeatherParameters.WetSunset,
carla.WeatherParameters.WetCloudySunset,
carla.WeatherParameters.MidRainSunset,
carla.WeatherParameters.HardRainSunset,
carla.WeatherParameters.SoftRainSunset]

# number of weathers = 14


def changeWeather(world, weatherNum=0):

    #world.set_weather(carla.WeatherParameters.WetCloudySunset)
    world.set_weather(random.choice(weatherList))
    world.set_weather(weatherList[weatherNum])


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

        changeWeather(world, weatherNum=0)

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
        world.apply_settings(original_settings)
        world.apply_settings(settings)
    

    


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

from changeWeather import changeWeather
from incident_spawner import getPreviousTransform, incidentCreator, centerFinder, incidentCreator2
from car_spawner import *
import pickle
from utils_main import *
from dsmanager import *
from changeMap import changeMap
#from changeWeather import *
import random
from yolov5 import CV_model
from image_converter import to_rgb_array, depth_to_array 
#from object_detection import ObjectDetection
#from yolov5 import CV_model02
from yolov5.distanceCalculation import *
def run_simulation(args, client):


    ### Set the modes of the simulation
    #gnss false or true
    gnss = False
    sensors = True
    vehicles = True
    objectDetectionMode = True
    if objectDetectionMode:
        obj = CV_model.ObjectDetection()
        obj.init()
    display_manager = None
    vehicle = None
    vehicle_list = []
    sensor_list = []
    incident_list = []
    timer = CustomTimer()

    try:
        #get the world
        i = 0
        #world = changeMap(client, 'Town01')
        world = client.get_world()
        original_settings = world.get_settings()

        if args.sync:
            traffic_manager = client.get_trafficmanager(8000)
            settings = world.get_settings()
            traffic_manager.set_synchronous_mode(True)
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            world.apply_settings(settings)

        #changeWeather(world, weatherNum = 13)
        bp = world.get_blueprint_library().filter('charger_2020')[0]
        bp_forActorAttribute = world.get_blueprint_library().filter('charger_2020')
        locations = random.choices(world.get_map().get_spawn_points(), k= 50)

        #print('actor attribute id: ' ,carla.ActorAttribute(bp_forActorAttribute))

        #for _ in range(len(locations)):
        #    incident_list += incidentCreator(client, locations[_])
        town= 10
        #location for map 10: ------------------------------------------------------------------------------------
        if town == 10:
            location01_v = carla.Transform(carla.Location(x = 10.626226, y = 130.026013, z = 0.6), carla.Rotation(yaw = -179.647827))
            location01_i = carla.Transform(carla.Location(x = -14.626226, y = 133.726013, z = 0.6), carla.Rotation(yaw = -179.647827))

        #location for map 02: ------------------------------------------------------------------------------------
        if town == 2:
            location01_v = carla.Transform(carla.Location(x = 181.24, y = 187.776013, z = 0.6), carla.Rotation(yaw = -179.997827))
            location01_i = carla.Transform(carla.Location(x = 175.24, y = 188.776013, z = 0.6), carla.Rotation(yaw = -0.007827))

        location01_forIncidents = carla.Transform(carla.Location(x = 13.568643, y = 2.467965, z = 0.6), carla.Rotation(yaw = 0.0, roll = 0.0000000))
        location01_forVehicle = carla.Transform(carla.Location(x = 13.568643, y = 2.467965, z = 0.6), carla.Rotation(yaw = 0.0, roll = 0.00000001))
        #location01_forVehicle = carla.Transform(carla.Location(x=-49.406830, y=50.617756, z=-0.004063), carla.Rotation(pitch=0.0, yaw=0.0, roll=0.000177)) 
        ####just one incident:
        #incident_list += incidentCreator(location01_forIncidents)
        #incident_list += incidentCreator2(client, location01_forVehicle, 10.0)
        incident_list += incidentCreator2(client, location01_i,1)
        print('transforms of the incidents', [str(_.get_location()) for _ in incident_list])
        map = world.get_map()

        bpBarrier = world.get_blueprint_library().filter('static.prop.streetbarrier')[0]

        #the location of the objects detected in with the real distance
        '''
        location01_i = carla.Transform(carla.Location(x = -12.00, y = 134.6276013, z = 0.6), carla.Rotation(yaw = -179.647827))
        incident_list.append(world.spawn_actor(bpBarrier, location01_i))
        location01_i = carla.Transform(carla.Location(x = -12.8, y = 134.876013, z = 0.6), carla.Rotation(yaw = -179.647827))
        incident_list.append(world.spawn_actor(bpBarrier, location01_i))

        location01_i = carla.Transform(carla.Location(x = -13.37, y = 134.136013, z = 0.6), carla.Rotation(yaw = -179.647827))

        incident_list.append(world.spawn_actor(bpBarrier, location01_i))
        #waypoints = map.get_waypoint(location01)[:1]

        '''
        locations_for_vehicles = random.choices(world.get_map().get_spawn_points(), k= 5)

        '''
        for _ in locations_for_vehicles:
            vehicle,sensor = vehicle_spawner(client = client , location = _)
            vehicle_list.append(vehicle)
        '''
        transformForVehicle = getPreviousTransform(world, location01_forVehicle, 1.0)

        if vehicles:
            vehicle, sensors = vehicle_spawner(client = client, location = location01_v, sensor_tick=0.2, gnss=gnss)
            vehicle_list.append(vehicle)
        #--------------------------Training Set Image Creation -----------------
        '''
        sensors['center_camera'].listen(lambda image: image.save_to_disk('output/%6dc.jpg'%image.frame))
        sensors['center_depth_camera'].listen(lambda image: image.save_to_disk('output/%6dcd.jpg'%image.frame))
        sensors['left_camera'].listen(lambda image: image.save_to_disk('output/%6dl.jpg'%image.frame))
        #sensors['left_depth_camera'].listen(lambda image: image.save_to_disk('output/%6dld.jpg'%image.frame, color_converter = carla.colorConverter.Depth))
        sensors['left_depth_camera'].listen(lambda image: np.savetxt('output/%6dld.jpg'%image.frame, depth_to_array(image)))#.save(,))# color_converter = carla.colorConverter.Depth))
        sensors['right_camera'].listen(lambda image: image.save_to_disk('output/%6dr.jpg'%image.frame))
        sensors['right_depth_camera'].listen(lambda image: image.save_to_disk('output/%6drd.jpg'%image.frame))
        '''
        #---------------working obj working
        '''
        detection = lambda image: obj.detect(to_rgb_array(image))

        sensors['left_camera'].listen(detection)#image: image.save_to_disk('output/%6dr.jpg'%image.frame))
        '''
        #----------------------------------------Test for Lambdas ----------------------------------
        '''
        def det(image=''):
            print('doing the detection')
            return [1,2,3]

        detection = lambda sensors:det(img)
        def loc(img = '', bounding_box=''):
            print('loc function is working')
        '''    
        sensor_queue = PriorityQueue()
        detection_queue = Queue()
        import pandas as pd
        df =  pd.DataFrame(columns=('x','y','z'))
        
        ''' 
        sensors['left_camera'].listen(lambda image: sensor_queue.put((1,image)))#sensor_callback(image, sensor_queue))
        sensors['left_depth_camera'].listen(lambda image: sensor_queue.put((2,depth_to_array(image))))#sensor_callback(image, sensor_queue))
        '''
        if sensors:
            sensors['left_camera'].listen(lambda image: sensor_queue.put((1,image)))#sensor_callback(image, sensor_queue))
            sensors['left_depth_camera'].listen(lambda image: sensor_queue.put((2,depth_to_array(image))))#sensor_callback(image, sensor_queue))
        
        #sensors['left_depth_camera'].listen(lambda image: sensor_callback(image, sensor_queue))


        #sensors['left_camera'].listen(detection)#image: image.save_to_disk('output/%6dr.jpg'%image.frame))
        #sensors['left_camera','left_depth_camera'].listen(lambda image: obj.detect(to_rgb_array(image)))#image: image.save_to_disk('output/%6dr.jpg'%image.frame))

        #sensors['left_camera','left_depth_camera'].listen(lambda image: obj.detect(to_rgb_array(image)))#image: image.save_to_disk('output/%6dr.jpg'%image.frame))
       
        if sensors:
            for _ in list(sensors.keys()):
                sensor_list.append(sensors[_])
            if gnss:
                sensors['gnss'].listen(callback)
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
        #changeWeather(world)

        while True:

            i+=1
            #print(i,'\n')
            if args.sync:
                world.tick()
            if objectDetectionMode:
                while not sensor_queue.empty():
                    #print(type(sensor_queue.get()))
                    
                    leftImage = sensor_queue.get()[1]
                    leftImageD = sensor_queue.get()[1]
                    vehicleTransform = vehicle.get_transform()

                    print('first Q is ' , leftImage)
                    frames =[]
                    frames = obj.detect(to_rgb_array(leftImage), i = i)
                    if len(frames):
                        for _ in frames:
                            print('frame in the main function:  ', _)
                            print('distance of Obj  :')
                            ds = distanceFrame(leftImageD, _)
                            angleFOV = []
                            angleFOV = angleFromFOV(_)
                            print('angleFOV vertical is :   ', angleFOV[1])
                            if (angleFOV[1] < 20) or (angleFOV[1] > 40) :
                                continue
                            print('angleFOV:    ', angleFOV)
                            firstAngleFOV = angleFOV[0]
                            realdst = realDistance(distanceFromFrame=ds, horizontalAngle=firstAngleFOV)            
                            print('read dst     :', realdst)
                            
                            #normal calculations
                            #locationOfIncident = localization(vehicleTransform,realdst, angleFOV[1])
                            #instead of realdistance use the distance :ds
                            locationOfIncident = localization(vehicleTransform,ds , angleFOV[1])
                            print('location of the vehicle: ', vehicleTransform)
                            print('location of the Incident  ', locationOfIncident)

                            df.loc[len(df)] = [str(locationOfIncident.location.x), str(locationOfIncident.location.y),str(locationOfIncident.location.z)]
                            #detection_queue.put(locationOfIncident)
                            waypoints = map.get_waypoint(locationOfIncident.location)
                            print('road id :    ', waypoints.road_id)
                            print('section id:  ', waypoints.section_id)
                            print('lane_id:     ',waypoints.section_id)
                            print('s:           ',waypoints.s)



                        #distanceCalc(leftImageD, _)
                #print('second in the queue is :' ,sensor_queue))
                    sensor_queue.task_done()
                #frames = obj.detect(to_rgb_array(sensor_queue.get()))
                #distanceCalc(sensor_queue.get(),frames)
                #sensor_queue.task_done()
                #print(sensor_queue.qsize())

                #print('type of first element    :', type(sensor_queue.get()))
                #print('type of second element    :', type(sensor_queue.get()))
                #the order is not necessarily the order above
            '''
                if len(frames):
                    print(frames[0],'\n')
                    distanceCalc(sensor_queue.get(), frames[0])
            if not sensor_queue.empty():
                sensor_queue.task_done()
            '''
            if i%10==0:
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
        [x.destroy() for x in sensor_list]
        client.apply_batch([carla.command.DestroyActor(x) for x in sensor_list])
        client.apply_batch([carla.command.DestroyActor(x) for x in incident_list])
        world.apply_settings(original_settings)
        df.to_csv('detections.csv')

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



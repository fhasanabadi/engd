from utils_main import *
import random


def vehicle_spawner(client, location, sensor_tick = 1, right_camera = True, left_camera = True, gnss = True, pitch = -15):
    """
    The function spawns vehicles attached with the camera sensors on top of the vehicle
    Default used vehicle is 'charger_2020'
    Arguments:
        client: Carla client
        location: the location to spawn the vehicle
        right_camera: Boolean 
        left_camera: Boolean
        gnss: Bool
        pitch: degrees (negative for heading sensors toward the ground)
    
    """
    world = client.get_world()
    vehicle_bp = world.get_blueprint_library().filter('charger_2020')[0]
    camera_bp = world.get_blueprint_library().filter('sensor.camera.rgb')
    vehicle = world.spawn_actor(vehicle_bp, location)
    vehicle.set_autopilot(True)
    transform = carla.Transform(carla.Location(x = 0.8, z = 1.7))
    '''
    sensor = world.spawn_actor(camera_bp , transform , attach_to = vehicle)
    #return vehicle, sensor
    '''

    #sensor lists
    sensor_list = []
    sensor_dictionary = {}
    sensors_location = carla.Location(0.5,0,2)


    fov = True
    fov_value = 60
    camera_x_size = 600
    camera_y_size = 600
    #sensor_tick = 1
    # create the RGB camera BP
    cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    cam_bp.set_attribute("image_size_x",str(camera_x_size))
    cam_bp.set_attribute("image_size_y",str(camera_y_size))
    cam_bp.set_attribute('sensor_tick', str(sensor_tick))
    if fov:
        cam_bp.set_attribute("fov",str(fov_value))
    
    cam_location = carla.Location(0,0,2)
    cam_rotation = carla.Rotation(pitch,0,0)
    cam_transform = carla.Transform(sensors_location,cam_rotation)

    #depth camera bp
    cam_bp_depth = world.get_blueprint_library().find('sensor.camera.depth')
    cam_bp_depth.set_attribute('image_size_x', str(camera_x_size))
    cam_bp_depth.set_attribute('image_size_y', str(camera_y_size))
    cam_bp_depth.set_attribute('sensor_tick', str(sensor_tick))

    if fov:
        cam_bp_depth.set_attribute("fov",str(fov_value))
    

    ego_cam = world.spawn_actor(cam_bp, cam_transform, attach_to = vehicle, attachment_type = carla.AttachmentType.Rigid)
    sensor_dictionary['center_camera'] = ego_cam
    sensor_list.append(ego_cam)
    ego_cam_depth = world.spawn_actor(cam_bp_depth, cam_transform, attach_to = vehicle, attachment_type = carla.AttachmentType.Rigid)
    sensor_list.append(ego_cam_depth)
    sensor_dictionary['center_depth_camera'] = ego_cam_depth


    if left_camera:
        left_camera_transform = carla.Transform(sensors_location, carla.Rotation(pitch,-45,0))
        ego_cam_left = world.spawn_actor(cam_bp, left_camera_transform, attach_to = vehicle, attachment_type = carla.AttachmentType.Rigid)
        cam_bp_depth_left = world.spawn_actor(cam_bp_depth, left_camera_transform, attach_to = vehicle,
                                            attachment_type = carla.AttachmentType.Rigid)
        sensor_dictionary['left_camera'] = ego_cam_left
        sensor_list.append(ego_cam_left)
        sensor_dictionary['left_depth_camera'] = cam_bp_depth_left
        sensor_list.append(cam_bp_depth_left)
        

        

    if right_camera:
        right_camera_transform = carla.Transform(sensors_location, carla.Rotation(pitch,45,0))
        ego_cam_right = world.spawn_actor(cam_bp, right_camera_transform, attach_to = vehicle, attachment_type = carla.AttachmentType.Rigid)
        cam_bp_depth_right = world.spawn_actor(cam_bp_depth, right_camera_transform, attach_to = vehicle,
                                            attachment_type = carla.AttachmentType.Rigid)

        sensor_dictionary['right_camera'] = ego_cam_right
        sensor_list.append(ego_cam_right)
        sensor_dictionary['right_depth_camera'] = cam_bp_depth_right

        sensor_list.append(cam_bp_depth_right)

    if gnss:
        gnss_bp = world.get_blueprint_library().find('sensor.other.gnss')
        gnss_bp.set_attribute('sensor_tick', str(sensor_tick))
        gnss_sensor = world.spawn_actor(gnss_bp, cam_transform, attach_to = vehicle, attachment_type = carla.AttachmentType.Rigid)

        sensor_dictionary['gnss'] = gnss_sensor

    return vehicle, sensor_dictionary

def callback(data):
    print(data)


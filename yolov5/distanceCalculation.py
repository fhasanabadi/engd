from turtle import distance
import numpy as np
import sys, os, glob, math
#from utils_main import *
import matplotlib.pyplot as plt
path = './images_distance/25819ld.jpg'
path = './image/25819ld.jpg'
import cv2
from trianglesolver import solve, degree
#add carla path
try:
    sys.path.append(glob.glob('/home/fhasanabadi/Git/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla
#carlaImage = carla.Image(raw_data = path)
#https://github.com/carla-simulator/driving-benchmarks/blob/master/version084/carla/image_converter.py
def distanceFrame(arrpath, xyxy):
    
    
    #read the array of image depth values in grayscale
    #arr = np.loadtxt(arrpath)
    arr = arrpath
    #get the frame locations based on the xyxy detected by detect.py function    
    x1, y1, x2, y2 = [int(_) for _ in xyxy]
    #slicing the array
    depth = arr[y1:y2, x1:x2]
    print('distance from camera: ', depth.mean()*1000)
    return depth.mean()*1000

def centerFinder(xyxy):

    x1, y1, x2, y2 = [int(_) for _ in xyxy]
    return [ int((xyxy[0]+ xyxy[2]) / 2) , int((xyxy[1] + xyxy[3]) / 2) ]


def angleFromFOV(xyxy, px = 600, fov = 60, ):
    
    #calculate the center of the frame

    xyCenterLst = centerFinder(xyxy = xyxy) 

    #convert height and width to the relative angle of the frame
    #calculating the horizontal angle from top horizontal line
    h_angle = int(xyCenterLst[1]/ px * fov)

    #calculating the vertical angle of the point relative to left vertical line
    v_angle = int(xyCenterLst[0] / px * fov)

    return [h_angle, v_angle]

def realDistance(distanceFromFrame: float, horizontalAngle: int, pitch = -15):

    #calculate the first angle of the triangle
    B = 90 - pitch
    print('B in distanceCalc function:  ', B)
    print('horizontalAngle in distanceCalc function:    ', horizontalAngle)
    #calculate the other angle of the triangle
    C = B - horizontalAngle
    distance = math.sin(math.radians(C)) * distanceFromFrame
    return distance
#print('distance calcualtion :',distanceCalc(12.4, 45))

print(angleFromFOV([20,60,30,40]))

a,b,c,A,B,C = solve(b = 4, B = 105*degree, C = 45*degree)

print('a:',a,'\n', 'b:',b,'\n','c:',c,'\n','A:',A,'\n','B',B,'\n','C:',C,'\n')

def localization(transformOfVehicle: carla.Transform, distance: float, v_angle, camera = 'left', fov = 60, yaw = -45):
    rotation = transformOfVehicle.rotation
    if camera == 'left':
        rotation.yaw -= yaw - fov/2 +v_angle 
    vehicleToIncidentNormal = rotation.get_forward_vector()

    incidentLocation = transformOfVehicle.location + vehicleToIncidentNormal * distance
    incidentTransform = carla.Transform(incidentLocation, rotation)

    return incidentTransform






'''


    img = cv2.imread(imgpath, 1)
    print('inside main')
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #img1 = img1[0:300,0:100]
    r, g, b = cv2.split(img1)
    
    titles = ['Original Image', 'Red', 'Green', 'Blue']
    images = [cv2.merge((r, g, b)), r, g, b]
    print('r shape: ', r.shape)
    print('g shape: ', g.shape)
    print('b shape: ', b.shape)
    depth = r + np.multiply(g ,256) + np.multiply(b , 256^2)
    print('shape of depth:  ', depth.shape)
    depth= depth/(256*256*256-1) * 1000
    #xyxy = [796.0,598.0,523.0,409.0]
    x1, y1, x2, y2 = [int(_) for _ in xyxy]


    print('shape of depth:  ', depth.shape )
    frame = img1[y1:y2, x1:x2]

    print('frame maxmimum ', np.amax(frame))
    print('frame minimum  :', np.amin(frame))
    print('shape of frame :     ',frame.shape)
    print('shape of depth image:  ', depth.shape)

    print('average distance:  ', frame.sum()/frame.shape[0]/frame.shape[1])

    average_distance = frame.sum()/frame.shape[0]/frame.shape[1]
    #np.savetxt('average_distance.csv', depth, delimiter=',')

    

    frameDepth = depth[y1:y2, x1:x2]
    boxAverageDistance = frameDepth.sum()/frameDepth.shape[0]/frameDepth.shape[1]
    print('average depth map    :', frameDepth.sum()/frameDepth.shape[0]/frameDepth.shape[1])
    #print(depth[y1:y2,x1:x2])
    
    


    

    

    


    plt.subplot(2, 3, 1)
    plt.imshow(images[0])
    plt.title(titles[0])
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(2, 3, 2)
    plt.imshow(images[1], cmap='Reds')
    plt.title(titles[1])
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(2, 3, 3)
    plt.imshow(images[2], cmap='Greens')
    plt.title(titles[2])
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(2, 3, 4)
    plt.imshow(images[3], cmap='Blues')
    plt.title(titles[3])
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,3,5)
    plt.imshow(depth,)
    plt.title('depth')
    plt.xticks([])
    plt.yticks([])


    plt.subplot(2,3,6)
    plt.imshow(frame,)
    plt.title('frame')
    plt.xticks([])
    plt.yticks([])
    plt.show()  
    return boxAverageDistance

xyxy = [433.0, 309.0, 523.0, 409.0]
'''
'''
#xyxy = [166.0, 405.0, 372.0, 508.0]

#xyxy = [796.0,598.0,523.0,409.0]
x1, y1, x2, y2 = [int(_) for _ in xyxy]
area_of_the_box = abs((x2-x1) * (y2-y1))
if x1>x2:
    x1,x2 = x2, x1
if y1>y2:
    y1,y2 = y2, y1
    '''
#distanceCalc(path, xyxy)

#if __name__ =='__init__':
#  main(path) 
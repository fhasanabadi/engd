from turtle import distance
import numpy as np
import sys, os, glob, math, cv2


try:
    sys.path.append(glob.glob('/home/fhasanabadi/Git/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla


class instanceLocalization():

    def __init__(self, xyxy, imageDim = 600, imageFOV = 60, cameraYaw = -45, angleThresholdForDetection = 20):
        self.cameraYaw = cameraYaw
        self.angleThresholdForDetection = angleThresholdForDetection
        self.imageFOV = imageFOV
        self.xyxyToList(xyxy = xyxy) 

        #calculate the center of the frame: [h_angle, v_angle]
        self.centerFinder(self.xyxyList)
        self.angleFromFOV(imageDim = imageDim, imageFOV = imageFOV )


    def xyxyToList(self, xyxy):
        
        self.xyxy = xyxy        
        self.xyxyList = [int(_) for _ in xyxy]
    def distanceFrame(self,  arrayDepth):
        
        depthArray = arrayDepth[self.xyxyList[1]:self.xyxyList[3], self.xyxyList[0]: self.xyxyList[2]]
        print('distance from the camera:    ', depthArray.mean()*1000)

        return depthArray.mean()*1000
    
    def centerFinder(self, xyxyList):
        
        #calculate the center of the frame: [h_angle, v_angle]
        self.frameCenter = [ int((xyxyList[0] + xyxyList[2]) /2 ), int(( xyxyList[1] + xyxyList[3]) /2 )]
        
    def angleFromFOV(self, imageDim = 600, imageFOV = 60):

        #calculate horizontal angle; relative angle of the incident from the horizontal top 
        h_angle = int(self.frameCenter[1] / imageDim * imageFOV )

        #calculate the vertical angle; relative angle of the incident from the vertical left side of the image
        v_angle = int(self.frameCenter[0] / imageDim * imageFOV )
        self.incidentAngles = [h_angle, v_angle]


        #set the condition whether continue with localization of the image or not
        if (v_angle < self.angleThresholdForDetection ) or (v_angle > self.imageFOV - self.angleThresholdForDetection):
            self.Continue = False
        else:
            self.Continue = True
        

    def localization(self, transformOfVehicle: carla.Transform, depthArray,  camera = 'left'):

        rotationOfVehicle = transformOfVehicle.rotation
        newRotation = carla.Rotation()

        if camera == 'left':
            newRotationYaw = rotationOfVehicle.yaw - (abs(self.cameraYaw) + self.imageFOV / 2 - self.incidentAngles[1])

            if newRotationYaw > 180:
                newRotationYaw -= 360
            elif newRotationYaw < -180:
                newRotationYaw += 360
            
            newRotation.yaw = newRotationYaw
            print('new rotation:    ', newRotation)
        
        vehicleToIncidentNormalVector = newRotation.get_forward_vector()

        incidentLocation = transformOfVehicle.location + vehicleToIncidentNormalVector * self.distanceFrame(depthArray)
        incdentTransform = carla.Transform( incidentLocation, newRotation)

        return incdentTransform






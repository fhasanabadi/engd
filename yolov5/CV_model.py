import torch
import cv2, sys
try:
    sys.path.append('/home/fhasanabadi/Git/carla/PythonAPI/examples/01_tutorials_Farshad/01_main/yolov5')
    pass
except IndexError:
    pass
import matplotlib.pylab as plt
import numpy as np
from torchvision import transforms
from PIL import Image
#from os.path import dirname, realpath, sep, pardir
import sys
import glob, os
try:
    
    
    from utils.augmentations import letterbox
    #from yolov5.utils.general import check_img_size
    from utils.general import check_img_size, non_max_suppression, scale_coords

    yolov5_folder_path = '/home/fhasanabadi/Git/carla/PythonAPI/examples/01_tutorials_Farshad/01_main/yolov5'
    #print('system paths     :', sys.path)
    from models.common import DetectMultiBackend
    from utils.torch_utils import select_device
    from utils.dataloaders import LoadImages
    from utils.general import Profile, xyxy2xywh
    
except ImportError:

    from yolov5.utils.augmentations import letterbox
    #from yolov5.utils.general import check_img_size
    from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords

    yolov5_folder_path = '/home/fhasanabadi/Git/carla/PythonAPI/examples/01_tutorials_Farshad/01_main/yolov5'
    #print('system paths     :', sys.path)
    from yolov5.models.common import DetectMultiBackend
    from yolov5.utils.torch_utils import select_device
    from yolov5.utils.dataloaders import LoadImages
    from yolov5.utils.general import Profile, xyxy2xywh


from utils.augmentations import letterbox
device = select_device('')


npArr = 'yolov5/image/1005ld.txt'
arr = np.loadtxt(npArr)
img = '/image/1005l.jpg'
img = cv2.imread(yolov5_folder_path + img, )#cv2.COLOR_BGR2RGB)#[:,:,::-1]
#cv2.imshow('image' , img)
#cv2.waitKey(0)
print('type of the image loaded with cv2    :', type(img))
print('shape of the image read by cv2   ', img.shape)
#load model
class ObjectDetection():
    def __init__(self, dnn = False, fp16 = False, data = '', imgsz = 600,
                conf_thres = 0.5, iou_thres = 0.45, device = device):
        self.dnn = dnn
        self.device = device
        self.fp16 = fp16
        self.data = data
        self.imgsz = imgsz
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        print('class initialized')
    def init(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path = yolov5_folder_path+'/best/best.pt')
        #self.model = DetectMultiBackend(weights=  yolov5_folder_path+'/best/best.pt', device = self.device, dnn = self.dnn, data = self.data, fp16= self.fp16)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        print('stride: ', self.stride, '\n', 'names: ', self.names, '\n', 'pt: ', self.pt, '\n')
        self.imgsz =  check_img_size(self.imgsz, s = self.stride)
        print('image size after check_img_size  :', self.imgsz)
        bs = 1
        #model warmup ~ no warmup here
        #self.model.warmup(imgsz=(1 if self.pt else bs, 3, self.imgsz, self.imgsz))
        self.dt = (Profile(), Profile(), Profile())

    def detect(self, img):
        im0 = img.copy()
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

            
        print('original image shape     :', img.shape)
        im = letterbox(img, self.imgsz, stride= self.stride, auto = False)[0]
        im = im.transpose((2,0,1))[::-1]
        im = np.ascontiguousarray(im)
        print('type of the image    im[None]    :' , type(im))
        #cv2.imshow('first image' , im[0])
        #cv2.waitKey(0)

        #cv2.imwrite('./iixxx.jpg', im[0])
        
        with self.dt[0]:
            im = torch.from_numpy(im).to(device = device)
            im = im.float()
            im /= 255
            print('im shape ' , im.shape)
            im = im[None]
        
        with self.dt[1]:
            pred = self.model(im )#, augment = False, visualize = False)
        with self.dt[2]:
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, max_det = 3 )
        det = []
        #convert the coordinates to the original imagesize
        for i, det in enumerate(pred):
            if len(det):
                #det[:, :4] = scale_coords(im.shape[2:], det[:, :4], img.shape).round()
                det[:, :4] = scale_coords(  im.shape[2:],det[:, :4],img.shape).round()
                m = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                print('det one here' , det[:,:4])
            else:
                print('no detection')
        return det[:, :4].int().tolist()
        '''
        for *xyxy, conf, cls in reversed(det):
            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4) )/ gn ).view(-1).tolist()
            print('xywh: ' , xywh)
            print('xyxy' , xyxy)
            print('conf' , conf)
            print('cls : ', cls)
        print('the original ones: ', '\n', pred)
'''
obj = ObjectDetection()
obj.init()
m = obj.detect(img= img)
#m = m.int().tolist()
print('type of the return', type(m),'\n', len(m))
print(m[0])
print(m[1])
print(m[2])
from distanceCalculation import *

for _ in m:
    print('distance of Obj')
    ds = distanceFrame(arr, _)
    angleFOV = angleFromFOV(_)
    print('angleFOV :', angleFOV)
    realdst = distanceCalc(ds, angleFOV[0])
    print('realdst  :', realdst)
    

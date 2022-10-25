import torch, cv2, sys,os

'''

import os
mydir = os.getcwd()
print('os.getcwd()  :', os.getcwd())
newdir = mydir + '/yolov5'
mydir_new = os.chdir(newdir)
print('os.getcwd()  :', os.getcwd())
from yolov5.CV_model02 import ObjectDetection
'''
'''
try:
    sys.path.append('/home/fhasanabadi/Git/carla/PythonAPI/examples/01_tutorials_Farshad/01_main/yolov5')
except IndexError:
    pass
'''
sys.path.insert(1, '/home/fhasanabadi/Git/carla/PythonAPI/examplse/01_tutorials_Farshad/01_main/yolov5')
import numpy as np

#import yolov5.utils.augmentations
#from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords, Profile, xyxy2xywh

from yolov5 import CV_model02

obj = CV_model02.ObjectDetection()
obj.init()



'''
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device
from yolov5.utils.dataloaders import LoadImages



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
'''
import torch
import cv2
import numpy as np
from PIL import ImageGrab
import os
import argparse
import os
import sys
from pathlib import Path
from grabscreen import grab_screen
import cv2
import torch
import torch.backends.cudnn as cudnn
import random
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, save_one_box
from utils.torch_utils import select_device, time_sync
import torchvision.transforms.functional as T
import win32api
import win32con 

'''names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush']'''
names =  ['Pedestrian']
conf_thres=0.25
iou_thres=0.45
#classes = [0,1,2,3,5,6,7]
classes = None
agnostic_nms=False
max_det=1000
device=''
project=ROOT / 'runs/detect'
name='results'
exist_ok=False
save_txt=False
#weights=ROOT / 'yolov5s.pt'
weights=ROOT / 'best.pt'
imgsz=(1080, 1920)
half=False
augment=False
visualize=False
dnn=False
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
#data=ROOT / 'data/coco128.yaml'
data=ROOT / 'data/apex_Pedestrian.yaml'

def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)
    
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')+
device = select_device(device)
model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data)

view_img = check_imshow()
dt, seen = [0.0, 0.0, 0.0], 0
while True:
    img_rgb = grab_screen((0,0,1920,1080))
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
    img = letterbox(img_rgb)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device).unsqueeze(0)
    img = img.half() if half else img.float()
    img /= 255.0 

    #img_rgb = ImageGrab.grab()
    #img_rgb = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_BGR2RGB)
    #img_rgb = T.to_tensor(img_rgb)
    #img_rgb=img_rgb.unsqueeze(0)
    #print(img.shape)
    results = model(img, augment=augment, visualize=visualize)
    #print(type(results),':',results)
    results = non_max_suppression(results, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
    gn = torch.tensor(img_rgb.shape)[[1, 0, 1, 0]]
    results = results[0]
    if results is not None and len(results):
        # Rescale boxes from img_size to im0 size
        results[:, :4] = scale_coords(img.shape[2:], results[:, :4], img_rgb.shape).round()

        # Print results
        for c in results[:, -1].unique():
            n = (results[:, -1] == c).sum()  # detections per class

        img_object = []
        cls_object = []
        # Write results
        hero_conf = 0
        hero_index = 0
        for idx, (*xyxy, conf, cls) in enumerate(reversed(results)):
            # if save_txt:  # Write to file
            #     xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
            #     with open(txt_path + '.txt', 'a') as f:
            #         f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # label format

            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
            cls = int(cls)
            img_object.append(xywh)
            cls_object.append(names[cls])

            if view_img:  # Add bbox to image
                label = '%s %.2f' % (names[int(cls)], conf)
                plot_one_box(xyxy, img_rgb, label=label, color=colors[int(cls)], line_thickness=2)


        
    img_rgb = cv2.resize(img_rgb, (1920,1080))


    # Stream results
    if view_img:
        cv2.imshow('window', img_rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
            raise StopIteration


    #results.print()
    
    #cv2.imshow('video',np.squeeze(results.render()))
    #cv2.imshow('video',img_rgb)
    if cv2.waitKey(1) == ord('q'):
        break
    
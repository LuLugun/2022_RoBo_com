import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync
import numpy as np
import random
import pyimgur

names =  ['0','1','2','3']
conf_thres=0.25
iou_thres=0.45
classes = None
agnostic_nms=False
max_det=1000
device=''
project=ROOT / 'runs/detect'
name='results'
exist_ok=False
save_txt=False
weights='robo_V1.1.pt'
imgsz=(1080, 1920)
half=False
augment=False
visualize=False
dnn=False
data=ROOT / 'data/robo_com.yaml'
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
device = select_device()
model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data)


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

def jpg_to_url(path):
    client_id = "d71e4a049aa4219"
    client_secret = '8205a0eedeaaed605421c765665f70294d39da9f'
    api = pyimgur.Imgur(client_id,client_secret)
    upload_image = api.upload_image(path)
    return upload_image.link

def model_detect(img_path):
    frame = cv2.imread(img_path)
    img = letterbox(frame)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device).unsqueeze(0)
    img = img.half() if half else img.float()
    img /= 255.0 
    results = model(img, augment=augment, visualize=visualize)
    results = non_max_suppression(results, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
    gn = torch.tensor(frame.shape)[[1, 0, 1, 0]]
    results = results[0]
    results[:, :4] = scale_coords(img.shape[2:], results[:, :4], frame.shape).round()
    for c in results[:, -1].unique():
        n = (results[:, -1] == c).sum()
    hero_conf = 0
    hero_index = 0
    label_commit = []
    for idx, (*xyxy, conf, cls) in enumerate(reversed(results)):
        label = '%s %.2f' % (names[int(cls)], conf)
        label_commit.append(names[int(cls)])
        label_commit.append(conf.item())
        plot_one_box(xyxy, frame, label=label, color=colors[int(cls)], line_thickness=2)
    if label_commit == []:
        img_path = img_path.replace('original','need_train').replace('.jpg','_detect.jpg')
    #os.remove(img_path)
    else:
        img_path = img_path.replace('original','detect').replace('.jpg','_detect.jpg')
        if len(label_commit) > 2:
            if label_commit[1] > label_commit[3]:
                result_label = [label_commit[0],label_commit[1]]
            else:
                result_label = [label_commit[2],label_commit[3]]
        else:
            result_label = label_commit
    cv2.imwrite(img_path,frame)
    return result_label
    #img_url = jpg_to_url(img_path)

    #return img_url






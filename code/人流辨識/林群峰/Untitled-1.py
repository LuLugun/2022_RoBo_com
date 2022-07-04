
import torch
# Model
path_model = "./yolov5s.pt"
model = torch.load(path_model)

# Image
im = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(im)
results.print() 
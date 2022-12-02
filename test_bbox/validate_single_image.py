import warnings
warnings.filterwarnings("ignore")
import os, glob, json, cv2, tqdm
import pandas as pd
from collections import Counter
from PIL import Image




img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"

# name = "000015491.jpg"
name = "000011849.jpg"

# prese dai leggings....io non ci posso credere
dict_ciao = [{"photo": 11849, "product": 76, "bbox": {"width": 33, "top": 385, "height": 82, "left": 381}}, 
             {"photo": 11849, "product": 76, "bbox": {"width": 39, "top": 389, "height": 106, "left": 420}}, 
             {"photo": 11849, "product": 76, "bbox": {"width": 60, "top": 458, "height": 48, "left": 140}}, 
             {"photo": 11849, "product": 76, "bbox": {"width": 46, "top": 409, "height": 50, "left": 261}}]

img = Image.open(img_dir + name)

print(img)

for idx,el in enumerate(dict_ciao):
    bbox = el["bbox"]
    img_crop = img.copy()
    im_crop = img_crop.crop((bbox["left"], bbox["top"], bbox["left"]+bbox["width"], bbox["left"]+bbox["height"]))
    im_crop.save("test_crop_single_%s.jpg" % idx)
    break
    
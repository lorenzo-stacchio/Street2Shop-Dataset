import warnings
warnings.filterwarnings("ignore")
import os, glob, json, cv2, tqdm
import pandas as pd
from collections import Counter
from PIL import Image




img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"

name = "000015491.jpg"

img = Image.open(img_dir + name)
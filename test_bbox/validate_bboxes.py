''''
CHECK WHAT TYPE OF BBOXES CREATE NULL SAMPLES
'''
import warnings
warnings.filterwarnings("ignore")
import os, glob, json, cv2, tqdm
import pandas as pd
from collections import Counter
from PIL import Image

def get_original_code(code, final_length = 9):
    code = str(code)
    final_code = "0" * (final_length-len(code)) + code
    return final_code

modes = ["train", "test"]

img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"
plot_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/plot_images_partitions/test/"

tuple_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images/"

out_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/test_bbox/consumer_bbox_shop/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images), len(all_images_no_ext))

bbox_columns = ["cons_path", "left","width","top","height"]


for m in modes:
    for path in glob.glob(tuple_dir + "%s*" % m):
        # if "footwear" in path or "dresses" in path:
        df_bbox = pd.read_csv(path) #  id  left  width  top  height      cons_path      shop_path

        df_bbox = df_bbox.drop_duplicates(
                subset = bbox_columns,
                keep = 'first').reset_index(drop = True) # remove duplicates which are present in the tuples
        # print(df_bbox)
        for idx, row in tqdm.tqdm(df_bbox.iterrows(), total = len(df_bbox), desc="Elaborating %s" % path):
            try:
                img = Image.open(img_dir + row["cons_path"])
            except Exception as e:
                print("ERROR opening  %s %s" %  (row["id"], row["cons_path"]))
            
            try:
                left, width, top, height =  row["left"],row["width"],row["top"],row["height"]
                img = img.crop((left, top, left + width, top+height))
                if 0 in img.size:
                    print("error in bbox", row["cons_path"])
                    print(left, width, top, height)
                    print(row["id"])
            except Exception as e:
                print("ERROR cropping with %s %s" %  (row["id"], row["cons_path"]))
            # print(img.size, 0 in img.size)
            # print(0 in (0,5))
            # print(type(img.size)==type((0,5)))
            # exit()


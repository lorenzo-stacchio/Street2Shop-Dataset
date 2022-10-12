import warnings
warnings.filterwarnings("ignore")
import os, glob, json, cv2
import pandas as pd
from collections import Counter

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


# INCREDIBILE MA VERO PHOTO 5670 ha 12 bbox in test pairs dressess 

for m in modes:
    for path in glob.glob(tuple_dir + "%s*" % m):
        # print(path)
        # lines = []
        # with open(path) as f:
        #     for l in f.readlines():
        #         lines.append(l)
        
        # lines = lines[1:] # remove header --> id,cons,shop,left,width,top,height
        df_bbox = pd.read_csv(path) #  id  left  width  top  height      cons_path      shop_path

        df_bbox = df_bbox.drop_duplicates(
                subset = bbox_columns,
                keep = 'first').reset_index(drop = True) # remove duplicates which are present in the tuples
        dict_of_bbox = df_bbox[bbox_columns].groupby('cons_path').apply(lambda x: x.drop('cons_path',1).to_dict(orient='r')).to_dict()
        
        bbox_distribution = (dict(Counter([len(x) for x in list(dict_of_bbox.values())])))
        print("Category %s with distribution %s" % (os.path.basename(path), bbox_distribution))
        # print()
        # exit()
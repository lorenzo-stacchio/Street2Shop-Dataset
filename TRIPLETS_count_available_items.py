import os
import random
import json, glob
import shutil
import itertools
import pandas as pd 

def get_original_code(code, final_length=9):
    code = str(code)
    final_code = "0" * (final_length - len(code)) + code
    return final_code


def get_dict_products_id_and_photo_id(set_partition_dicts):
    dict_partition = {}
    for el_dict in set_partition_dicts:
        photo_id = el_dict["photo"]
        id_prod = el_dict["product"]
        if id_prod not in dict_partition.keys():
            dict_partition[id_prod] = []
        dict_partition[id_prod].append(photo_id)

    return dict_partition
    # print(dict_partition)
    # exit()


def write_partition_file(list_consumer, list_shop, filepath):
    with open(filepath, "w") as fw:
        fw.write("cons,shop/n")
        for c, s in zip(list_consumer, list_shop):
            fw.write("%s,%s/n" % (c, s))


product_prefix = "retrieval"
modes = ["train", "test"]

triplet_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images_wacv/"
img_dir = '/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/UNIMORE_RESIZED/'

all_images = os.listdir(img_dir)

all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images))

c = 0

items_correct = 0
total_images_top = 0
total_images = 0

image_id_already_tested = []

tot_images = 0
tot_pairs = 0

for m in modes:
    print(m)
    for path in glob.glob(triplet_dir + "%s*" % m):
        temp_item = 0
        path = path.replace("//", "/")
        list_image_cat_consumer, list_image_cat_shop = [], []
        filename = path.split("/")[-1].split(".")[0]
        cat = filename.split("_")[-1]
        df = pd.read_csv(path)
        tot_pairs += len(df)
        tot_images += len(set(df["cons_path"]))
        tot_images += len(set(df["shop_path"]))
        # print(len(df))
        # id,cons_path,shop_path
        # dict_data_cat, dict_data_cat_ret = json.load(open(path, "r")), json.load(open(retrieval_path, "r"))

print(tot_pairs)
print(tot_images)
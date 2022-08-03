import os
import random, tqdm
import json, glob
import shutil
import itertools
import pandas as pd 

def get_original_code(code, final_length = 9):
    code = str(code)
    final_code = "0" * (final_length-len(code)) + code
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


def write_partition_file(list_consumer, list_shop,filepath):
    with open(filepath,"w") as fw:
        fw.write("cons,shop\n")
        for c,s in zip(list_consumer,list_shop):
            fw.write("%s,%s\n"% (c,s))


product_prefix = "retrieval"

modes = ["train", "test"]

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples/"
img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images/"
tuple_out_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images))

c = 0


for path in tqdm.tqdm(glob.glob(dir_json + "*"), desc= "Erasing pairs with at least one non existent image"):
    print(path)
    df = pd.read_csv(path)
    df["cons_path"] = df["cons"].apply(lambda x: get_original_code(x))
    df["shop_path"] = df["shop"].apply(lambda x: get_original_code(x))
    df["both_exist"] = df.apply(lambda row: row["cons_path"] in all_images_no_ext and row["shop_path"] in all_images_no_ext, axis=1)

    # Remove non existent pairs
    print(len(df))
    df = df[df["both_exist"]==True]
    # Convert path to correct ones
    df["cons_path"] = df["cons_path"].apply(lambda x: all_images[all_images_no_ext.index(x)])
    df["shop_path"] = df["shop_path"].apply(lambda x: all_images[all_images_no_ext.index(x)])
    # Save final df
    df = df.drop(["cons", "shop", "both_exist"], axis = 1)
    df.to_csv(tuple_out_dir + "%s" % os.path.basename(path), index=False)
    # print(df)
    # exit()
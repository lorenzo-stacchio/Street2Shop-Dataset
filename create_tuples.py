import os
import random
import json, glob
import shutil
import itertools

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
    # print(dict_partition)
    # exit()


def write_partition_file(list_image_id, list_consumer, list_shop,filepath):
    with open(filepath,"w") as fw:
        fw.write("id,cons,shop\n")
        for id, c,s in zip(list_image_id, list_consumer,list_shop):
            fw.write("%s,%s,%s\n"% (id, c,s))


product_prefix = "retrieval"

modes = ["train", "test"]

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"
img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_mine_downloaded/"
plot_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/plot_images_partitions/test/"
tuple_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images))

c = 0

for m in modes:
    for path in glob.glob(dir_json + "%s*" % m):
        path = path.replace("\\", "/")
        list_image_id, list_image_cat_consumer, list_image_cat_shop = [],[],[]
        filename = path.split("/")[-1].split(".")[0]
        cat = filename.split("_")[-1]

        retrieval_path = dir_json + "%s_%s.json" % (product_prefix,cat)
        dict_data_cat,dict_data_cat_ret = json.load(open(path, "r")),json.load(open(retrieval_path, "r"))

        dict_data_cat_unique = get_dict_products_id_and_photo_id(dict_data_cat)
        dict_data_cat_ret_unique = get_dict_products_id_and_photo_id(dict_data_cat_ret)
        # print(dict_data_cat_ret_unique)
        intersection = set(list(dict_data_cat_unique.keys())).intersection(set(list(dict_data_cat_ret_unique.keys())))
        print("INTERSECTION ", path, len(dict_data_cat_unique.keys()), len(dict_data_cat_ret_unique.keys()), len(intersection))
        # Merge dicts
        dict_merged = {}
        for k in intersection:
            dict_merged[k] = {"consumer": dict_data_cat_unique[k],"shop": dict_data_cat_ret_unique[k]}
            # Creating pairs
        for id_product,dict_photos_id in dict_merged.items():
            for cons,shop in itertools.product(*[dict_photos_id["consumer"],dict_photos_id["shop"]]):
                #print(cons,shop)
                list_image_id.append(id_product)
                list_image_cat_consumer.append(cons)
                list_image_cat_shop.append(shop)
                #exit()
        #
        #     exit()
        print(len(list_image_cat_shop), len(list_image_cat_consumer))

        write_partition_file(list_image_id, list_image_cat_consumer, list_image_cat_shop, tuple_dir + "%s.txt" % filename)


        # exit()
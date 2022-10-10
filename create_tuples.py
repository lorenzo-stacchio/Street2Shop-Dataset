import os
from pickle import TRUE
import random
import json, glob
import shutil
import itertools

def get_original_code(code, final_length = 9):
    code = str(code)
    final_code = "0" * (final_length-len(code)) + code
    return final_code


def get_dict_products_id_and_photo_id(set_partition_dicts, bbox = TRUE):
    dict_partition = {}
    for el_dict in set_partition_dicts:
        photo_id = el_dict["photo"]
        id_prod = el_dict["product"]
        if bbox: # parsing consumer
            bbox = el_dict["bbox"]
            if id_prod not in dict_partition.keys():
                dict_partition[id_prod] = {photo_id:[bbox]}
            elif photo_id not in dict_partition[id_prod].keys():
                dict_partition[id_prod][photo_id] = [bbox]
            else:
                # dict_partition[id_prod]["images_id"].append(photo_id)
                dict_partition[id_prod][photo_id].append(bbox)
        else: # parsing shop
            if id_prod not in dict_partition.keys():
                dict_partition[id_prod] = [photo_id]
           
            else:
                dict_partition[id_prod].append(photo_id)

    return dict_partition


def write_partition_file(list_image_id, list_consumer, list_shop,list_bbox, filepath):
    with open(filepath,"w") as fw:
        fw.write("id,cons,shop,left,width,top,height\n")
        for id, c,s, bbox in zip(list_image_id, list_consumer,list_shop, list_bbox):
            fw.write("%s,%s,%s,%s,%s,%s,%s\n"% (id, c,s, bbox["left"],bbox["width"],bbox["top"],bbox["height"]))


product_prefix = "retrieval"

modes = ["train", "test"]

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"
img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"
plot_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/plot_images_partitions/test/"
tuple_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images))

c = 0

for m in modes:
    for path in glob.glob(dir_json + "%s*" % m):
        # print(path)
        path = path.replace("\\", "/")
        list_image_id, list_image_cat_consumer, list_image_cat_shop, list_bbox = [],[],[], []
        filename = path.split("/")[-1].split(".")[0]
        cat = filename.split("_")[-1]

        retrieval_path = dir_json + "%s_%s.json" % (product_prefix,cat)
        dict_data_category,dict_data_category_retrieval = json.load(open(path, "r")),json.load(open(retrieval_path, "r"))

        dict_data_category_unique_bbox = get_dict_products_id_and_photo_id(dict_data_category)
        # print(list(dict_data_category_unique_bbox.items())[0]) # not sorte ids


        dict_data_category_retrieval_unique = get_dict_products_id_and_photo_id(dict_data_category_retrieval, bbox = False)
        # print(list(dict_data_category_retrieval_unique.items())[0]) # it's ok if the ids are differents from the previous, the first are not sorted
        intersection = set(list(dict_data_category_unique_bbox.keys())).intersection(set(list(dict_data_category_retrieval_unique.keys())))
        print("INTERSECTION ", path, len(dict_data_category_unique_bbox.keys()), len(dict_data_category_retrieval_unique.keys()), len(intersection))


        ## test existance of images with more than one bbox
        # for k,v in dict_data_category_unique_bbox.items():
        #     if any([len(list_bbox)>1 for list_bbox in list(v.values())]):
        #         print("\n----------------------")
        #         for el in list(v.values()):
        #             print(len(el))
        #         # print(list(v.values())[0], len(list(v.values())[0]))
        #         print("MORE THAN ONE BBOX %s ---- %s" % (k,v))
        #         exit()
        

        # exit()
        # Merge dicts
        dict_merged = {}
        for k in intersection:
            dict_merged[k] = {"consumer": list(dict_data_category_unique_bbox[k].keys()),"shop": dict_data_category_retrieval_unique[k]}
            # Creating pairs


        # print(dict_merged)
        # exit()

        for id_product,dict_photos_id in dict_merged.items():
            for cons,shop in itertools.product(*[dict_photos_id["consumer"],dict_photos_id["shop"]]):
                #print(cons,shop)
                for bbox in dict_data_category_unique_bbox[id_product][cons]:
                    list_image_id.append(id_product)
                    list_image_cat_consumer.append(cons)
                    list_image_cat_shop.append(shop)
                    list_bbox.append(bbox)
                #exit()
        #
        #     exit()
        print(len(list_image_cat_shop), len(list_image_cat_consumer))

        write_partition_file(list_image_id, list_image_cat_consumer, list_image_cat_shop, list_bbox, tuple_dir + "%s.txt" % filename)


        # exit()
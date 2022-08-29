import os
import random
import json, glob
import shutil
import itertools


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

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json_wacv/"
# img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images/"
img_dir = '/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/UNIMORE_RESIZED/'

all_images = os.listdir(img_dir)

all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images))

c = 0

items_correct = 0
total_images_top = 0
total_images = 0

image_id_already_tested = []

for m in modes:

    for path in glob.glob(dir_json + "%s*" % m):
        temp_item = 0
        path = path.replace("//", "/")
        list_image_cat_consumer, list_image_cat_shop = [], []
        filename = path.split("/")[-1].split(".")[0]
        cat = filename.split("_")[-1]

        retrieval_path = dir_json + "%s_%s.json" % (product_prefix, cat)
        dict_data_cat, dict_data_cat_ret = json.load(open(path, "r")), json.load(open(retrieval_path, "r"))
        # print(len(dict_data_cat), len(dict_data_cat_ret))
        dict_data_cat_unique = get_dict_products_id_and_photo_id(dict_data_cat)
        dict_data_cat_ret_unique = get_dict_products_id_and_photo_id(dict_data_cat_ret)

        # print(sum([len(v) for v in dict_data_cat_unique.values()]))
        # print(sum([len(v) for v in dict_data_cat_ret_unique.values()]))

        # CALCULATE TOTAL EXISTING IMAGES
        tot_consumer_paths, tot_shop_paths = [], []
        for k,v in dict_data_cat_unique.items():
            tot_consumer_paths.extend([get_original_code(s) for s in v])

        for k,v in dict_data_cat_ret_unique.items():
            tot_shop_paths.extend([get_original_code(s) for s in v])
            # print(tot_shop_paths)
            # exit()

        image_id_already_tested.extend(set(tot_consumer_paths))
        image_id_already_tested.extend(set(tot_shop_paths))

        # print("---%s----" % path)
        # print(len(tot_consumer_paths), len(tot_shop_paths))
        # print(len(set(tot_consumer_paths)), len(set(tot_shop_paths)))

        # print((len(set(tot_consumer_paths).intersection(set(all_images_no_ext)))))
        # print((len(set(tot_shop_paths).intersection(set(all_images_no_ext)))))
        
        # total_images_top += (len(set(tot_consumer_paths).intersection(set(all_images_no_ext))))
        # total_images_top += (len(set(tot_shop_paths).intersection(set(all_images_no_ext))))
        # continue
        # exit()
        # print(len(tot_consumer_paths), len(tot_shop_paths))
        # print(total_images_top)
        # exit()
      

        # print(dict_data_cat_ret_unique)
        # exit()
        # print(dict_data_cat_ret_unique)
        intersection = set(list(dict_data_cat_unique.keys())).intersection(set(list(dict_data_cat_ret_unique.keys())))
        diff = set(list(dict_data_cat_ret_unique.keys())).intersection(set(list(dict_data_cat_unique.keys())))
        # print(list(set(list(dict_data_cat_ret_unique.keys())))[-10:])

        print("INTERSECTION ", path, len(dict_data_cat_unique.keys()), len(dict_data_cat_ret_unique.keys()),
              len(intersection))


        #print("DIFFERENCE ", diff)
        # exit()
        # Merge dicts
        dict_merged = {}
        for k in intersection:
            consumer_paths = [x for x in dict_data_cat_unique[k] if str(get_original_code(x)) in all_images_no_ext]
            shop_paths = [x for x in dict_data_cat_ret_unique[k] if str(get_original_code(x)) in all_images_no_ext]
            if len(shop_paths) > 0 and len(consumer_paths) > 0:
                dict_merged[k] = {"consumer": consumer_paths, "shop": shop_paths}
                # Creating pairs
                # print("---", consumer_paths, len(consumer_paths))
                # print("---", len(consumer_paths))
                items_correct += len(consumer_paths)
                temp_item += len(consumer_paths)
                total_images += (len(consumer_paths) + len(shop_paths))
            # print(len(dict_merged))
            # exit()
        print(temp_item, len(dict_data_cat))
        # write_partition_file(list_image_cat_consumer, list_image_cat_shop, tuple_dir + "%s.txt" % filename)

print("----------------FINAL RESULTS----------------")
# THIS COUNTS ALL THE CORRECTED ISEM USED IN TRAINING AND TESTING
print(items_correct)
print(total_images)
print(len(image_id_already_tested))

# THIS COUNTS ALL THE IMAGES LISTED IN THE TRAIN, TEST AND RETRIEVAL CLASSES, WITH NO INTERESECTION AND NO ID INTERSECTION CHECK
image_id_already_tested = set(image_id_already_tested)
print(len(image_id_already_tested.intersection(set(all_images_no_ext))))
# print(total_images_top)
# exit()

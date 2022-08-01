import json, glob, os, tqdm

def collect_good_items(list_of_dicts_category, all_images_without_ext, length_all_paths, category):
    # print(len(list_of_dicts_category))
    good_pairs = 0
    bad_filepaths = []
    for dict_ in tqdm.tqdm(list_of_dicts_category, desc = "Collecting for %s" % category):
        # print(dict_)
        #photo_id, product_id = dict_["photo"], dict_["product"]
        photo_id, product_id = str(dict_["photo"]),str(dict_["product"])

        #reformat photo id to match filename
        photo_id_full = ("0" * (length_all_paths-len(photo_id))) + photo_id
        product_id = ("0" * (length_all_paths-len(product_id))) + product_id

        # print(photo_id, photo_id_full)
        # print()
        # TODO: VALIDATE THAT THE PRODUCT ID IS REFERRED TO A PHOTO, FOR ME NO.
        if (photo_id_full in all_images_without_ext) and (product_id in all_images_without_ext):
            good_pairs +=1
        else:
            bad_filepaths.append(photo_id_full)
    # print("%s/%s check" % (good_pairs, len(list_of_dicts_category)))

    return good_pairs, len(list_of_dicts_category), bad_filepaths


meta_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"
images_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images/"

all_images_without_ext = [x.split(".")[0] for x in os.listdir(images_dir)]

length_all_paths = [len(x) for x in all_images_without_ext]
# print("SET LENGTH ALL PATHS", set(length_all_paths))
length_filepath = length_all_paths[0] # they are all the same


#modes = ["train", "test", "retrieval"]
modes = ["train", "test"]

errors_category_mode = {k:{} for k in modes}

train_total_sample, test_total_sample, retrieval_total_sample = 0,0,0

for mode in modes:

    for json_category_file in tqdm.tqdm(glob.glob(meta_dir + "%s_*" % mode), desc= "Checking categories for %s" % mode):
        # print(json_category_file)
        category = json_category_file.split("/")[-1].split(".")[0].split("_")[-1]
        if category not in errors_category_mode[mode].keys():
            errors_category_mode[mode][category] = {}

        list_of_dicts_category = json.load(open(json_category_file))
        if mode == "train":
            train_total_sample += len(list_of_dicts_category)
        elif mode == "test":
            test_total_sample += len(list_of_dicts_category)
        else:
            retrieval_total_sample += len(list_of_dicts_category)

        good_pairs, total, bad_filepaths = collect_good_items(list_of_dicts_category, all_images_without_ext, length_filepath, category)
        errors_category_mode[mode][category]["bad_filepaths"] = bad_filepaths
        errors_category_mode[mode][category]["good"] = good_pairs
        errors_category_mode[mode][category]["total"] = total
        errors_category_mode[mode][category]["percentage"] = round((good_pairs/total)*100,2)
        # print(errors_category_mode[mode][category])
    # exit()
    
# print(train_total_sample, test_total_sample, train_total_sample + test_total_sample, retrieval_total_sample)
# print(errors_category_mode)



for mode in modes:
    with open("%s_status_.json" % mode, "w") as fw:
        fw.write(json.dumps(errors_category_mode[mode], indent=4, separators=(',', ': ')))
    temp = errors_category_mode[mode]
    # for cat in temp.keys():
    #     print("%s-%s good: %s" % (mode.upper(), cat, temp[cat]["percentage"]))
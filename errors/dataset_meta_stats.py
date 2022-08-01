import json, glob, os, tqdm


meta_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"
images_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images/"

all_images_without_ext = [x.split(".")[0] for x in os.listdir(images_dir)]

length_all_paths = [len(x) for x in all_images_without_ext]
length_filepath = length_all_paths[0] # they are all the same


# modes = ["train", "test", "retrieval"]
modes = ["train", "test"]

errors_category_mode = {k:{} for k in modes}

train_total_sample, test_total_sample, retrieval_total_sample = 0,0,0

for mode in modes:
    for json_category_file in glob.glob(meta_dir + "%s_*" % mode):
        category = json_category_file.split("/")[-1].split(".")[0].split("_")[-1]
        list_of_dicts_category = json.load(open(json_category_file))
        if mode == "train":
            train_total_sample += len(list_of_dicts_category)
        elif mode == "test":
            test_total_sample += len(list_of_dicts_category)
        else:
            retrieval_total_sample += len(list_of_dicts_category)


print(train_total_sample, test_total_sample, train_total_sample + test_total_sample, retrieval_total_sample)


# CHECK MISSING FILEPATH TOTAL
for mode in ["train", "test"]:
    dict_data = json.load(open("/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/errors/%s_status_.json" % mode,"r"))
    acc = 0
    total = 0
    for k,v in dict_data.items():
        bads = dict_data[k]["total"]-dict_data[k]["good"]
        acc += bads
        total += dict_data[k]["total"]
        # print(bads)
    print("%s/%s" % (acc, total))

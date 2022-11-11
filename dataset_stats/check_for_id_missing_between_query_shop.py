import pandas as pd
import os, json, glob
import numpy as np 


json_folder = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"

# QUERY
train_acc, test_acc = {"n_items_real":[],"n_items_dataset":[], "percentage_items_loss": [], "category":[]}, {"n_items_real":[],"n_items_dataset":[], "percentage_items_loss": [], "category":[]}

for mode in ["train", "test"]:
    for basename in glob.glob(json_folder + "/%s*" % mode):
        real_basename = os.path.basename(basename).split(".")[0]
        # print("\n\nCurrent category %s" % real_basename)

        actual_json = json.load(open(json_folder + real_basename + ".json","r"))
        ids = list(set([json["product"] for json in actual_json]))

        # get retrieval json
        real_category = real_basename.split("_")[-1].split(".")[0]
        actual_json_retrieval = json.load(open(json_folder + "retrieval_%s.json" % real_category,"r"))
        actual_json_retrieval_filtered = list(filter(lambda x: (x["product"] in ids), actual_json_retrieval))
        # print(ids)
        print(real_basename, len(actual_json), len(ids), len(actual_json_retrieval),len(actual_json_retrieval_filtered))
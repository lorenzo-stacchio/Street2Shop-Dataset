import pandas as pd
import os, json
import numpy as np 


tuple_folder = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images/"
json_folder = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"

# QUERY
train_acc, test_acc = {"n_items_real":[],"n_items_dataset":[], "percentage_items_loss": [], "category":[]}, {"n_items_real":[],"n_items_dataset":[], "percentage_items_loss": [], "category":[]}


for basename in os.listdir(tuple_folder):
    real_basename = os.path.basename(basename).split(".")[0]
    # print("\n\nCurrent category %s" % real_basename)

    actual_df_tuple =  pd.read_csv(tuple_folder + real_basename + ".txt")

    actual_json = json.load(open(json_folder + real_basename + ".json","r"))
    ids = list(set([json["product"] for json in actual_json]))

    # get retrieval json
    real_category = real_basename.split("_")[-1].split(".")[0]
    actual_json_retrieval = json.load(open(json_folder + "retrieval_%s.json" % real_category,"r"))
    actual_json_retrieval_filtered = list(filter(lambda x: (x["product"] in ids), actual_json_retrieval))

    items_in_df = len(set(actual_df_tuple["shop_path"]))
    items_in_json = len(actual_json_retrieval_filtered)

    loss_percentage = 100 * (1 - (items_in_df/items_in_json))
    # print("Query in final dataframe %s ---- Query in json %s" % (items_in_df, items_in_json))

    target_dict = None

    if "train" in real_basename:
        target_dict = train_acc
       
    else:
        target_dict = test_acc

    target_dict["n_items_real"].append(items_in_df)
    target_dict["n_items_dataset"].append(items_in_json)
    target_dict["percentage_items_loss"].append(loss_percentage)
    target_dict["category"].append(real_basename)

df_train = pd.DataFrame.from_dict(train_acc)
df_test = pd.DataFrame.from_dict(test_acc)

df_train = df_train.append({"category": "train_total","n_items_real": sum(df_train["n_items_real"]),
"n_items_dataset": sum(df_train["n_items_dataset"]), "percentage_items_loss": np.mean(df_train["percentage_items_loss"]) }, ignore_index=True)


df_test = df_test.append({"category": "test_total","n_items_real": sum(df_test["n_items_real"]),
"n_items_dataset": sum(df_test["n_items_dataset"]), "percentage_items_loss": np.mean(df_test["percentage_items_loss"]) }, ignore_index=True)


print(df_train)
print(df_test)

df_train.to_csv("loss_items/df_train_shop.csv")
df_test.to_csv("loss_items/df_test_shop.csv")


# SHOP




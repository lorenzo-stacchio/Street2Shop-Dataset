import os, tqdm, glob
import pandas as pd 

def get_original_code(code, final_length = 9):
    code = str(code)
    final_code = "0" * (final_length-len(code)) + code
    return final_code


def write_partition_file(list_image_id, list_consumer, list_shop,filepath):
    with open(filepath,"w") as fw:
        fw.write("id,cons,shop\n")
        for id, c,s in zip(list_image_id, list_consumer,list_shop):
            fw.write("%s,%s,%s\n"% (id, c,s))


product_prefix = "retrieval"

modes = ["train", "test"]

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples/"
img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"

tuple_out_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images/"
error_tuple_out_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_erased/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images))

c = 0


for path in tqdm.tqdm(glob.glob(dir_json + "*"), desc= "Erasing pairs with at least one non existent image"):
    print(path)
    df = pd.read_csv(path)
    original_len = len(df)
    df["cons_path"] = df["cons"].apply(lambda x: get_original_code(x))
    df["shop_path"] = df["shop"].apply(lambda x: get_original_code(x))
    df["both_exist"] = df.apply(lambda row: row["cons_path"] in all_images_no_ext and row["shop_path"] in all_images_no_ext, axis=1)


    
    # Remove non existent pairs
    print(len(df))
    df_good_tuples = df[df["both_exist"]==True]
    # Convert path to correct ones --> ONLY VALID FOR EXISTING FILEPATHS!
    df_good_tuples["cons_path"] = df_good_tuples["cons_path"].apply(lambda x: all_images[all_images_no_ext.index(x)])
    df_good_tuples["shop_path"] = df_good_tuples["shop_path"].apply(lambda x: all_images[all_images_no_ext.index(x)])

    df_bad_tuples = df[df["both_exist"]==False]

    # Save final df
    df_good_tuples = df_good_tuples.drop(["cons", "shop", "both_exist"], axis = 1)
    df_bad_tuples = df_bad_tuples.drop(["cons", "shop", "both_exist"], axis = 1)

    # Ensure bboxes are integers
    for col in ["left","width","top","height"]:
        df_good_tuples[col] = df_good_tuples[col].astype(int)
        df_bad_tuples[col] = df_bad_tuples[col].astype(int)



    # df_good_tuples.to_csv(tuple_out_dir + "%s" % os.path.basename(path), index=False)
    df_bad_tuples.to_csv(error_tuple_out_dir + "%s" % os.path.basename(path), index=False)
    print("Reduced pairs from %s to %s" % (original_len, len(df)))

     # BAD TUPLES

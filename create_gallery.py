import json, glob, os
import pandas as pd 

def get_original_code(code, final_length=9):
    code = str(code)
    final_code = "0" * (final_length - len(code)) + code
    return final_code

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"

modes = ["retrieval"]
images_dir =  "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"
image_filename_list = [x for x in os.listdir(images_dir)]
print(len(image_filename_list))

av_samples_images = 0

for m in modes:
    for path in glob.glob(dir_json + "%s*" % m):
        cat = path.split("_")[-1].split(".")[0]
        df = pd.DataFrame(columns = ["id", "path", "category"])
        list_id, list_path, list_cat = [],[],[]
        path = path.replace("//", "/")
        print(path)
        dict_data_cat = json.load(open(path, "r"))
        print(len(dict_data_cat))
        for el in dict_data_cat:
            photo_id = get_original_code(el["photo"]) + ".jpg"
            id_prodotto = el["product"]
            list_path.append(photo_id)
            list_id.append(id_prodotto)
            list_cat.append(cat)
        df["id"] = list_id
        df["path"] = list_path
        df["category"] = list_cat
        df = df[df["path"].isin(image_filename_list)]
        df.to_csv("query_gallery/gallery/%s.csv" % cat, index=False)
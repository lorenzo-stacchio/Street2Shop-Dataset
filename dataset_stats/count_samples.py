import json, glob, os

def get_original_code(code, final_length=9):
    code = str(code)
    final_code = "0" * (final_length - len(code)) + code
    return final_code

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"

modes = ["train", "test", "retrieval"]
images_dir =  "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"
image_filename_list = [x for x in os.listdir(images_dir)]
print(len(image_filename_list))

dict_samples = {"train": 0, "test": 0, "retrieval":0}
av_samples_images = 0

for m in modes:
    for path in glob.glob(dir_json + "%s*" % m):
        temp_item = 0
        path = path.replace("//", "/")
        dict_data_cat = json.load(open(path, "r"))
        dict_samples[m]+=len(dict_data_cat)
        for el in dict_data_cat:
            photo_id = get_original_code(el["photo"]) + ".jpg"
            temp_item += photo_id in image_filename_list
        print(path, temp_item)
        av_samples_images += temp_item

print(dict_samples, sum(dict_samples.values()))
print("available images for query: %s" % av_samples_images)


# COUNT SAMPLE AVAILABLE IMAGES
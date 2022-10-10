import os, glob, json, cv2

def get_original_code(code, final_length = 9):
    code = str(code)
    final_code = "0" * (final_length-len(code)) + code
    return final_code

modes = ["train", "test"]

dir_json = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/meta/meta/json/"
img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"
plot_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/plot_images_partitions/test/"
tuple_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images), len(all_images_no_ext))


# Con bounding box multiple, il product è lo stesso!
# TODO stessa immagine query ha più bbox e non una sola, gestire questa cosa!


for m in modes:
    for path in glob.glob(dir_json + "%s*" % m):
        print(path)
        list_of_dicts = json.load(open(path))
        print(len(list_of_dicts))
        filepaths = list(map(lambda x: x["photo"], list_of_dicts))
        dict_accumulate = {f : {"bbox": [], "product": []}for f in set(filepaths)}
        for el in list_of_dicts:
            dict_accumulate[el["photo"]]["bbox"].append(el["bbox"])
            dict_accumulate[el["photo"]]["product"].append(el["product"])
        print(len(list_of_dicts), len(filepaths), len(set(filepaths)))
        # print(dict_accumulate)

        for k,v in dict_accumulate.items():
            # print(k)
            # exit()
            # print(k, len(v["product"]),len(v["bbox"]))
            img = cv2.imread(img_dir + all_images[all_images_no_ext.index(get_original_code(k))])
            if len(v["bbox"])>1:
                print(k,v)

                for idx, bbox in enumerate(v["bbox"]):
                    # save bbox for those images
                    top, h, left, w = bbox["top"],bbox["height"],bbox["left"],bbox["width"]
                    img_cropped = img[top: top+h, left: left+w]
                    cv2.imwrite("test_bbox/image_%s.jpg" % idx, img_cropped)
                exit()

        exit()

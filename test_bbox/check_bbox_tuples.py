import os, glob, json, cv2
import pandas as pd

def get_original_code(code, final_length = 9):
    code = str(code)
    final_code = "0" * (final_length-len(code)) + code
    return final_code

modes = ["train", "test"]

img_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images_download/"
plot_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/plot_images_partitions/test/"

tuple_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images/"

out_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/test_bbox/consumer_bbox_shop/"

all_images = os.listdir(img_dir)
all_images_no_ext = [str(x.split(".")[0]) for x in all_images]
print(len(all_images), len(all_images_no_ext))



for m in modes:
    for path in glob.glob(tuple_dir + "%s*" % m):
        print(path)
        # lines = []
        # with open(path) as f:
        #     for l in f.readlines():
        #         lines.append(l)
        
        # lines = lines[1:] # remove header --> id,cons,shop,left,width,top,height
        df = pd.read_csv(path) #  id  left  width  top  height      cons_path      shop_path

        for idx, row in df.iterrows():
            images_dirpath = out_dir + "/%s_%s_%s/" % (row["id"], row["cons_path"].split(".")[0], row["left"])
            if not os.path.exists(images_dirpath): os.mkdir(images_dirpath)
            cons_img, shop_img = cv2.imread(img_dir + row["cons_path"]),cv2.imread(img_dir + row["shop_path"])
            top, height, left, width = row["top"],row["height"],row["left"],row["width"]
            cons_img_cropped = cons_img[top:top+height, left:left+width]
            cv2.imwrite(images_dirpath + "cons_cropped.jpg", cons_img_cropped)
            cv2.imwrite(images_dirpath + "shop.jpg", shop_img)
            exit()
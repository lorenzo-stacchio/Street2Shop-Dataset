import cv2
import numpy as np
import os 

min_side_shape = 300

def crop_and_adapt_image(filepath, min_side_shape, replace = False):
    image = cv2.imread(filepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    shape_image_no_channel = image.shape[:-1]
    # print(shape_image_no_channel)
    min_side_current_image = np.argmin(shape_image_no_channel)# remove channel first
    # print(min_side_current_image)
    if shape_image_no_channel[min_side_current_image] > min_side_shape: # resize
        dim = [0,0]
        old_min_side = shape_image_no_channel[min_side_current_image]
        dim[min_side_current_image] = min_side_shape #height or width
        # Calculate factor for great size
        # print(shape_image_no_channel[min_side_current_image-1])
        # print(dim[min_side_current_image])
        # print(old_min_side)
       
        dim[min_side_current_image-1] = round((shape_image_no_channel[min_side_current_image-1] * dim[min_side_current_image])/old_min_side)

        # print("reshape size", dim)
        # exit()
        # dim[min_side_current_image-1] = # list indexing is cyclic so this works
        image = cv2.resize(image, dim[::-1]) 
        #resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        # print("Initial and final image shape %s - %s" % (shape_image_no_channel, image.shape[:-1]))
        if replace: # replace just if we reshaped
            cv2.imwrite(filepath, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    return image


if __name__ == "__main__":
    # m_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images/"
    # o_dir = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/test_crop/"
    # for idx, file in enumerate(os.listdir(m_dir)):
    #     image = crop_and_adapt_image(m_dir + file ,min_side_shape)
    #     cv2.imwrite(o_dir + file, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    #     if idx == 10:
    #         break

    image = crop_and_adapt_image("/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/images/000000001.jpg", min_side_shape, replace=True)

       
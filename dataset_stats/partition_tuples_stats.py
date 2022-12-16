import pandas as pd

file = "/data01/AEFFE/image_embeddings_pytorch/2021_WEB_CALL/VIT_CONFERENCE_2022/Street2Shop-Dataset/partitions_tuples_reduced_correct_images/test_pairs_dresses.txt"
print(file)
df = pd.read_csv(file)

df_calc_cons = df.drop(["id", "shop_path"], axis=1)
df_calc_cons = df_calc_cons.drop_duplicates()
print(len(df_calc_cons))
print(len(set(df["cons_path"])))
print(len(set(df["shop_path"])))
import tqdm
import os 
type_errors, names, urls = [],[],[]


if __name__ == '__main__':
    with open("errors_no_empty.txt", "r") as fr:
        acc = ""
        for line in tqdm.tqdm(fr.readlines(), desc="reading"):
            try:
                if line:
                    #print("LINE: ", line, line.split(","))
                    type_error, name, url = line.split(",")
                    type_errors.append(type_error)
                    names.append(name)
                    urls.append(url)
            except Exception as e:
                print(e)
                print(line)

# Calculate value counts on errors:
type_errors_value_counts = {k: 0 for k in set(type_errors)}
for type_error in type_errors:
    type_errors_value_counts[type_error]+=1

for k,v in type_errors_value_counts.items():
    print(k,v,"\n")
# exit()

# Other stats

downloaded_images = [x.split(".")[0] for x in os.listdir("../images/")]
# Check intersection
check_intersection_from_one_downlaod_to_another = len(set(downloaded_images).intersection(names))

len_downloaded_images  = len(downloaded_images)


# print correct length
print("%s + %s - %s: %s" % (len(type_errors),len_downloaded_images, check_intersection_from_one_downlaod_to_another, len(type_errors) + len_downloaded_images - check_intersection_from_one_downlaod_to_another))
import tqdm

real_lines = []


if __name__ == '__main__':
    with open("errors.txt", "r") as fr:
        acc = ""
        for line in tqdm.tqdm(fr.readlines(), desc="reading"):
            try:
                line = line.replace("\n", "")
                if acc:  # means throwing exception in previous iterate
                    line = acc + line
                    acc = ""
                if line:
                    type_error, name, url = line.split(",") # if this throw error
                    real_lines.append(line)
            except Exception as e:
                print(e)
                print(line)
                if "OpenCV(4.5.5) /io/opencv/modules/imgproc/src/color.cpp:182" in line:
                    acc = line


with open("errors_no_empty.txt", "w") as f:
    for line in real_lines:
        f.write(line+"\n")
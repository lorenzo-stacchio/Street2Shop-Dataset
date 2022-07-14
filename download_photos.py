import os
# import requests
import urllib.request
import tqdm
from time import sleep
from threading import Thread
import logging
import contextlib
from http.client import HTTPConnection  # py3

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
errors = []


# a custom function that blocks for a moment
def task(urls, errors, id):
    for url in tqdm.tqdm(urls, desc="Thread %s downloading" % id):
        try:
            filename = url.split(",")[0]
            real_url = url.split(",")[1]
        except Exception as e:
            errors.append(url)
        opener = urllib.request.URLopener()
        # opener.addheader(('User-Agent',
        #                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'))

        filepath = os.path.join(images_dir, filename + '.png')

        if not os.path.exists(filepath):
            try:
                filename, headers = opener.retrieve(real_url, filepath)
            except Exception as e:
                # print("%s ----- Error with %s --- %s" % (e,filepath, real_url))
                errors.append(real_url)


images_dir = 'D:/Lorenzo Stacchio/Datasets/street2shop/street2shop-dataset/images/'

with open('photos/photos.txt', "r") as f:
    lines = f.readlines()
    total_urls = []

    for each in tqdm.tqdm(lines, desc="Parsing file"):
        total_urls.append(each)

    # total_urls = ["ciao1,http://ecx.images-amazon.com/images/I/81gTZOlbIFL._UL1500_.jpg","ciao2,http://ecx.images-amazon.com/images/I/81GQFhMSDvL._UL1500_.jpg"]

    # divide urls and create threads
    threads = 10
    total_threads = []
    for idx, i_start in enumerate(range(0, len(total_urls), len(total_urls) // threads)):
        print(idx)
        end = i_start + (len(total_urls) // threads)
        if end > len(total_urls):
            end = len(total_urls)
        total_threads.append(Thread(target=task, args=(total_urls[i_start:end], errors, idx)))

    for idx, t in enumerate(total_threads):
        print("Start", t.name)
        t.start()

    for idx, t in enumerate(total_threads):
        t.join()

    with open("errors.txt", "w") as fw:
        for er in errors:
            fw.write(er + "\n")

    # print("ERRORS:"+"\n".join(errors))  # what sound does a metasyntactic locomotive make?

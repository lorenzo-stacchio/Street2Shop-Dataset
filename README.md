# Street2Shop-Dataset
<p align="right"><img src="https://visitor-badge.laobi.icu/badge?page_id=lorenzo-stacchio.Street2Shop-Dataset" alt="visitors"></p>

<!-- ![alt text](http://www.tamaraberg.com/street2shop/header.jpg) -->



Code to download Street2Shop Dataset from the paper [Where to Buy It: Matching Street Clothing Photos in Online Shops](https://openaccess.thecvf.com/content_iccv_2015/papers/Kiapour_Where_to_Buy_ICCV_2015_paper.pdf).


# Download meta files

* Download photo urls from [this](http://www.tamaraberg.com/street2shop/wheretobuyit/photos.tar)
* Download dataset triplets from [this](http://www.tamaraberg.com/street2shop/wheretobuyit/meta.zip)

Unpack both files. 

# Download with python script

It requires python version 3.x

> python download_photos.py 


# Search for troublesome images after download has finished

> python missing.py 


## Error found in dataset

In the original file, the image 000008288 labelled as bbox with id 4916 has no width and height. 

This gave the born to the ```validate_bboxes.py``` script.


## BROKEN LINKS

000098538.jpg was removed from pictures because of link contained a broken image.
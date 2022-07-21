import os
# import requests
import urllib.request
from urllib.request import urlopen


# working
real_url = "http://productshots2.modcloth.net/productshots/0148/4817/76ab989ea3f99870a33e6346e89a3a8e.jpg?1415640554"


# redirected 
real_url = "http://s3.amazonaws.com/media.modcloth/images/media/000/296/043/original/IMG_20140512_145445.jpg?1418208912"

# broken
real_url = "http://g.nordstromimage.com/imagegallery/store/product/Zoom/10/_9596350.jpg"

response = urlopen(real_url)
correct_url = response.geturl()
print(correct_url)
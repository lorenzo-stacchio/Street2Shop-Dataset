import os
# import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from urllib.request import Request, urlopen  # Python 3


# working
real_url = "http://productshots2.modcloth.net/productshots/0148/4817/76ab989ea3f99870a33e6346e89a3a8e.jpg?1415640554"


# redirected 
real_url = "http://s3.amazonaws.com/media.modcloth/images/media/000/296/043/original/IMG_20140512_145445.jpg?1418208912"

# broken
real_url = "http://g.nordstromimage.com/imagegallery/store/product/Zoom/10/_9596350.jpg"

real_url = "http://www.zappos.com/images/z/2/9/8/1/4/2/2981423-5-4x.jpg"


req = Request(real_url)
#req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
content = urlretrieve(real_url, "test.jpg")

response = urlopen(real_url)
correct_url = response.geturl()
print(real_url, correct_url)
# result = opener.retrieve(correct_url, "test.jpg")

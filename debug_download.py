import os
# import requests
import urllib.request
from urllib.request import urlopen


opener = urllib.request.URLopener()

real_url = "http://productshots2.modcloth.net/productshots/0148/4817/76ab989ea3f99870a33e6346e89a3a8e.jpg?1415640554"

html = urlopen(real_url)
print(html.read())

# filepath = os.path.join("test.jpg")

# result = opener.retrieve(real_url, filepath)

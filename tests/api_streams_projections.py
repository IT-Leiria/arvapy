""" Script to test the flask API
"""
from ast import literal_eval
import requests

# Base variables and methods
url_base_path = "http://zeus.itleiria.pt:5000/" 


# Get stream and print results
print("1.1 Get stream and print results")
r = requests.get(url_base_path + "get_stream_list")
for i, s in enumerate(literal_eval(r.content.decode())):
    print({"name": s[0], "width": s[1], "height": s[2], "bytes_per_pixel": s[3], "number_of_layers": s[4]})
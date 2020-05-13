""" Script to test the flask API
"""
import requests


# Test get_stream_list
response = requests.get("http://zeus.itleiria.pt:5000/get_stream_list")

# Test get_stream_list
response = requests.get("http://zeus.itleiria.pt:5000/select_stream?idx=0")


## Test original projection - frame info
response = requests.get("http://zeus.itleiria.pt:5000/get_frame_info")
response_body = response.json()
assert response_body["width"] == 3840
assert response_body["height"] == 1920

## Test get_frame
# Raw
response = requests.get("http://zeus.itleiria.pt:5000/get_frame_raw")
frame = response.content
#TODO: Add function to write frame
# With header
response = requests.get("http://zeus.itleiria.pt:5000/get_frame")
frame = response.content


## Test with cube-map projection
# get_frame_info
response = requests.get("http://zeus.itleiria.pt:5000/get_frame_info?projection=CMP")
response_body = response.json()
assert response_body["width"] == 3324
assert response_body["height"] == 2216
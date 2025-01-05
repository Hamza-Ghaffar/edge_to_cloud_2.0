import requests
import json
import time
from random import randrange
 
cam_counts = {
        "cam1": 0,
        "cam2": 0,
        "cam3": 0,
        "cam4": 0,
        "cam5": 0
        }
url = "http://127.0.0.1:8000/pushDetections2"
for i in range(50):
    cam_counts["cam1"] = randrange(100)
    cam_counts["cam2"] = randrange(100)
    cam_counts["cam3"] = randrange(100)
    cam_counts["cam4"] = randrange(100)
    cam_counts["cam5"] = randrange(3000)
    
    #jsonDump = json.dumps(cam_counts)  'do not need to dump the dictionary to json just passing the values as dictionary'
   
    print(cam_counts)
    post_response = requests.post(url, json = cam_counts, timeout=30.0, verify=False)
    print(post_response)
    time.sleep(1)
# {"image" :
#  ""}

import json
import redisearch as s
objects = ["key","passport","wallet","car","bag","watch","book","satchel","laptop","camera","mobile_phone"]

with open("/Users/kriti.pandey/cache-mere/src/event_generating/data/camera_desc.json") as f:
    cam_data = json.load(f)

tag_data = {}
i = 0
import random as r
for item in cam_data:

    for key, value in item.items():
        tags = []
        tags.append(objects[r.randint(0,10)])
        tags.append(objects[r.randint(0,10)])
        tags.append(objects[r.randint(0,10)])
        tags.append(objects[r.randint(0,10)])

        tag_data["tags"] = tags
        tag_data[key] = value
        tag_data["image"] = "b64str"
        print(tag_data)
        # with open("/Users/kriti.pandey/cache-mere/src/event_generating/data/camera_events.json", "w") as w:
        #     json.dump(tag_data, w)

r = s.TagField
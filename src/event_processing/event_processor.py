from src import config

import redis
import psycopg2

from datetime import datetime

import random as r

from redisearch import Client, TextField, NumericField, Query, TagField



# def listToString(s):  
    
#     # initialize an empty string 
#     str1 = ""  
    
#     # traverse in the string   
#     for ele in s:  
#         str1 += ele   
    
#     # return string   
#     return str1 

class EventProcessor():
    def __init__(self):
        self.r = redis.from_url(config.EVENT_BROKER_URL)
        self.client = Client('CCTV_DATA')
        try:
            self.client.create_index([TextField('CCTV_ID'), TagField('TAGS')])
        except Exception as error :
            print ("Error while creatign index", error)

        # self.client.create_index([TextField('title', weight=5.0), TextField('body')])

    
    def get_objects_in_image(self, image):
        # TODO: call RedisAI module
        objects = ["key","passport","wallet","car","bag","watch","book","satchel","laptop","camera","mobile_phone"]
        tags = []
        tags.append(objects[r.randint(0,10)])
        tags.append(objects[r.randint(0,10)])
        tags.append(objects[r.randint(0,10)])
        tags.append(objects[r.randint(0,10)])
        
        return tags


    def process(self, msg):
        print("Going to process message and and store it", msg)
        # print(float(msg["LON"]), float(msg["LAT"]), msg["CCTV_ID"])
        # print(type(float(msg["LON"])), type(float(msg["LAT"])), msg["CCTV_ID"])
        try:
            self.r.geoadd("CCTV_LOCATION", float(msg["LON"]), float(msg["LAT"]), msg["CCTV_ID"])
            msg["TAGS"] = self.get_objects_in_image(msg.get("IMAGE", ""))
            # print("Going to store this in search", msg)

            doc_unique_key = msg["CCTV_ID"] + "_" + msg["TS"]


            self.client.add_document(doc_unique_key, CCTV_ID = doc_unique_key, TAGS = ",".join(msg["TAGS"]))



            
        except Exception as error :
            print ("Error while adding ccty data", error)

        # 1. FIND/Create the key of the list using COUNTRY:PINCODE:"ATTRIBUTE"
        # 2. LPUSH the timestamp of the event to the list
        # 3. Compare the rightmost element's ts with the current ts
        #    if > # mins  pop the rightmost element. Repeat step 3.
        # 4. Compare the lenghth of list with threshcount. If greater, raise an alert
        # for key, val in msg.items():
        #     if key not in ["TS", "LAT", "LON", "COUNTRY", "PINCODE"] and val==1:
        #         list_key = msg["COUNTRY"] + ":" + msg["PINCODE"] + ":" + key
        #         print("list_key->", list_key)
        #         self.r.lpush(list_key, msg["TS"])
        #         current_ts = datetime.fromisoformat(msg["TS"])
        #         last_ts = self.r.lindex(list_key, -1)
        #         last_ts = datetime.fromisoformat(last_ts.decode("utf-8"))
        #         print("comparing timestamp difference.", current_ts, last_ts)
        #         print("time delta", divmod((current_ts - last_ts).total_seconds(),60)[0])
        #         print("thresh minutes", self.epidemic_thresholds.get(key).get("minutes"))
        #         while divmod((current_ts - last_ts).total_seconds(),60)[0] > self.epidemic_thresholds.get(key).get("minutes"):
        #             self.r.rpop(list_key)
        #             last_ts = self.r.lindex(list_key, -1)
        #             last_ts = datetime.fromisoformat(last_ts.decode("utf-8"))

        #         list_length = self.r.llen(list_key)
        #         if list_length > self.epidemic_thresholds.get(key).get("count"):
        #             print("TODO: raise an alert. Its an epidemic. Save yourselves. Runn for the hill!")

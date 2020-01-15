from src import config

import redis

from datetime import datetime


class EventProcessor():
    def __init__(self):
        # self.epidemic_thresholds = config.EPIDEMIC_THRESHOLDS
        self.epidemic_thresholds = {
            "MALARIA": {
                "count": 2,
                "mins": 24*60
            },
            "VIOLENCE": {
                "count": 10,
                "mins": 30*24*60
            },
            "LITCHI": {
                "count": 700,
                "mins": 30*24*60
            }
        }
        self.r = redis.from_url(config.EVENT_BROKER_URL)

    def process(self, msg):
        # {
        # "TS":"2020-01-15T20:11:03.411155",
        # "LAT":17.385044,
        # "LON": 78.486671,
        # "COUNTRY": "India",
        # "PINCODE": "500084",
        # "MALARIA": 1,
        # "VIOLENCE": 0,
        # "LITCHI": 0
        # }
        print("TODO: going to process message and and store it", msg)
        for key, val in msg.items():
            if key not in ["TS", "LAT", "LON", "COUNTRY", "PINCODE"] and val==1:
                list_key = msg["COUNTRY"] + "_" + msg["PINCODE"] + "_" + key
                self.r.lpush(list_key, msg["TS"])
                current_ts = datetime.fromisoformat(msg["TS"])
                print("list_key->", list_key)
                last_ts = self.r.lindex(list_key, -1)
                print("last_ts->", last_ts)
                last_ts = datetime.fromisoformat(last_ts.decode("utf-8"))
                print("compare timestamp difference. Assuming for now that its less than threshold", current_ts, last_ts)
                print("time delta", divmod((current_ts - last_ts).total_seconds(),60)[0])
                print("thresh mins", self.epidemic_thresholds.get(key).get("mins"))
                while divmod((current_ts - last_ts).total_seconds(),60)[0] > self.epidemic_thresholds.get(key).get("mins"):
                    self.r.rpop(list_key)
                    last_ts = self.r.lindex(list_key, -1)
                    last_ts = datetime.fromisoformat(last_ts.decode("utf-8"))

                list_length = self.r.llen(list_key)
                if list_length + 1 > self.epidemic_thresholds.get(key).get("count"):
                    print("TODO: raise an alert")
                else:
                    print("Don't raise an alert. Move on. Chalte bano bhai")

                # TODO:
                # 1. FIND/Create the key of the list using COUNTRY:PINCODE:"ATTRIBUTE"
                # 2. LPUSH the timestamp of the event to the list
                # 3. Compare the rightmost element's ts with the current ts
                #   3a. if > # mins  pop the rightmost element. Repeat step 3.
                #   3b. else compare the lenghth of list with threshcount. If greater, raise an alert

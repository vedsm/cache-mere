from src import config

import redis
import psycopg2

from datetime import datetime

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
        # self.epidemic_thresholds = config.EPIDEMIC_THRESHOLDS
        self.connect_to_data_lake()
        self.epidemic_thresholds = {
            "MALARIA": {
                "count": 2,
                "minutes": 24*60
            },
            "TYPHOID": {
                "count": 2,
                "minutes": 24*60
            },
            "DENGUE": {
                "count": 2,
                "minutes": 24*60
            },
            "NIPAH": {
                "count": 2,
                "minutes": 24*60
            },
            "CHOLERA": {
                "count": 2,
                "minutes": 24*60
            },
            "SARS": {
                "count": 2,
                "minutes": 24*60
            },
            "MENINGOCOCCAL": {
                "count": 2,
                "minutes": 24*60
            },
            "VIOLENCE": {
                "count": 10,
                "minutes": 30*24*60
            },
            "LITCHI": {
                "count": 700,
                "minutes": 30*24*60
            }
        }
        self.r = redis.from_url(config.EVENT_BROKER_URL)

    def process(self, msg):
        print("Going to process message and and store it", msg)
        self.save_to_data_lake(msg)
        # 1. FIND/Create the key of the list using COUNTRY:PINCODE:"ATTRIBUTE"
        # 2. LPUSH the timestamp of the event to the list
        # 3. Compare the rightmost element's ts with the current ts
        #    if > # mins  pop the rightmost element. Repeat step 3.
        # 4. Compare the lenghth of list with threshcount. If greater, raise an alert
        for key, val in msg.items():
            if key not in ["TS", "LAT", "LON", "COUNTRY", "PINCODE"] and val==1:
                list_key = msg["COUNTRY"] + ":" + msg["PINCODE"] + ":" + key
                print("list_key->", list_key)
                self.r.lpush(list_key, msg["TS"])
                current_ts = datetime.fromisoformat(msg["TS"])
                last_ts = self.r.lindex(list_key, -1)
                last_ts = datetime.fromisoformat(last_ts.decode("utf-8"))
                print("comparing timestamp difference.", current_ts, last_ts)
                print("time delta", divmod((current_ts - last_ts).total_seconds(),60)[0])
                print("thresh minutes", self.epidemic_thresholds.get(key).get("minutes"))
                while divmod((current_ts - last_ts).total_seconds(),60)[0] > self.epidemic_thresholds.get(key).get("minutes"):
                    self.r.rpop(list_key)
                    last_ts = self.r.lindex(list_key, -1)
                    last_ts = datetime.fromisoformat(last_ts.decode("utf-8"))

                list_length = self.r.llen(list_key)
                if list_length > self.epidemic_thresholds.get(key).get("count"):
                    print("TODO: raise an alert. Its an epidemic. Save yourselves. Runn for the hill!")

    def connect_to_data_lake(self):
        # self.data_lake_connection = psycopg2.connect("postgresql://ai_coe_user:immigrant_song123@localhost/ai_coe")
        connection = psycopg2.connect(user = "ai_coe_user",
                                  password = "immigrant_song123",
                                  host = "localhost",
                                  port = "5432",
                                  database = "ai_coe")
        try:
            cursor = connection.cursor()
            
            # create_table_query = '''CREATE TABLE mobile
            #     (ID INT PRIMARY KEY     NOT NULL,
            #     MODEL           TEXT    NOT NULL,
            #     PRICE         REAL); '''
            create_table_query = '''CREATE TABLE event_table
            (
                "ID" serial,
                "TS" timestamp with time zone,
                "LAT" double precision,
                "LON" double precision,
                "COUNTRY" text,
                "PINCODE" text,
                "MALARIA" integer DEFAULT 0,
                "TYPHOID" integer DEFAULT 0,
                "DENGUE" integer DEFAULT 0,
                "NIPAH" integer DEFAULT 0,
                "CHOLERA" integer DEFAULT 0,
                "SARS" integer DEFAULT 0,
                "MENINGOCOCCAL" integer DEFAULT 0,
                "VIOLENCE" integer DEFAULT 0,
                "LITCHI" integer DEFAULT 0
            ); '''
            
            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

    def save_to_data_lake(self, msg):
        try:
            connection = psycopg2.connect(user = "ai_coe_user",
                                  password = "immigrant_song123",
                                  host = "localhost",
                                  port = "5432",
                                  database = "ai_coe")
            string_keys = ""
            string_values = ""
            for key,val in msg.items():
                string_keys += " \"" + key + "\", "
                if isinstance(val, str): 
                    string_values += " '" + val + "', "
                else:
                    string_values += str(val) + ", "
            string_keys = string_keys.rstrip(", ")
            string_values = string_values.rstrip(", ")
            print("keys annd vals", string_keys, string_values)
            insert_query = "INSERT INTO event_table("+ string_keys +") VALUES("+ string_values +");"
            print("insert_query", insert_query)
            # create a new cursor
            cursor = connection.cursor()
            # execute the INSERT statement
            cursor.execute(insert_query)
            # commit the changes to the database
            connection.commit()
            # close communication with the database
        except (Exception, psycopg2.DatabaseError) as error:
            print("unable to save_to_data_lake", error)
        finally:
            if connection is not None:
                cursor.close()
                connection.close()


from src import config

from src.event_broker.event_broker_subscriber import EventBrokerSubscriber
from src.event_processing.event_processor import EventProcessor
import json


if __name__ == "__main__":
    print("Starting event reading")
    event_processor = EventProcessor()
    event_broker_subscriber = EventBrokerSubscriber()
    while True:
        msg = event_broker_subscriber.get_message()
        if msg:
            print(f"new message: {msg}")
            # print(f"new message: {msg['data']}")
            # if msg['type'] == "message":
            #     event_processor.process(json.loads(msg['data']))
            # print("msg[0]", msg[0])
            # print("msg[0][1]", msg[0][1])
            # print("msg[0][1][0]", msg[0][1][0])
            # print("msg[0][1][0][1]", msg[0][1][0][1])
            # print("type msg[0][1][0][1]", type(msg[0][1][0][1]))
            # msg = msg[0][1][0][1]
            decoded_msg = {}
            for key, val in msg[0][1][0][1].items():
                # print("key val", key, val)
                # print(type(key))
                # print("key val .decode(utf-8) ", key.decode("utf-8") , val.decode("utf-8") )
                decoded_msg[key.decode("utf-8")] = val.decode("utf-8")
                
            event_processor.process(decoded_msg)

from src import config

from src.event_broker.event_broker_subscriber import EventBrokerSubscriber
from src.event_processing.event_processor import EventProcessor
import json


if __name__ == "__main__":
    print("Starting event processing")
    event_processor = EventProcessor()
    event_broker_subscriber = EventBrokerSubscriber()
    while True:
        msg = event_broker_subscriber.get_message()
        if msg:
            print(f"new message: {msg}")
            # print(f"new message: {msg['data']}")
            if msg['type'] == "message":
                event_processor.process(json.loads(msg['data']))

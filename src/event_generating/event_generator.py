from src import config

import json
import requests
# from src.event_receiving.event_publisher import EventPublisher

if __name__ == "__main__":
    print("Starting to generate events. TODO; ingest more type of events")
    # event_publisher = EventPublisher()

    with open('./src/event_generating/data/disease_events.json') as f:
        events_data = json.load(f)
    # print(events_data)

    for msg in events_data:
        print(msg)
        # event_publisher.publish(msg)
        payload = {"msg": msg}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", config.EVENT_RECEIVER_URL, headers = headers, json = payload)
        print("response of sending events", response)

# TODO: read through the json
# 0. read the json file as dict
# 1. sort the values based on TS
# 2. for every 7th element , generate 20, 40, 60, 80... event at evebry 0.5 day/ 12 hours
# 3. Save the file

import json


def read_json(fileloc):
    with open(fileloc) as f:
        return json.load(f)

def save_json(fileloc, data):
    with open(fileloc, 'w') as fp:
        json.dump(data, fp)



if __name__ == "__main__":
    print("Going to prepare data")
    # event_publisher = EventPublisher()

    events_data = read_json('./src/event_generating/data/disease_events.json')
    # print sorted(lis, key = lambda i: i['age']) 
    # print sorted(lis, key = lambda i: (i['age'], i['name'])) 
    events_data = sorted(events_data, key = lambda i: i['TS']) 
    save_json('./src/event_generating/data/disease_events-sorted.json', events_data)

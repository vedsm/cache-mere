from src.event_broker.event_broker_publisher import EventBrokerPublisher
import json

class EventPublisher():
    def __init__(self):
        self.event_broker_publisher = EventBrokerPublisher()

    def publish(self, msg):
        print("going to publish message", msg)
        return self.event_broker_publisher.publish(json.dumps(msg))

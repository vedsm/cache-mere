from src.event_broker_factory.event_broker_subscriber_factory import EventBrokerSubscriberFactory
from src import config


class EventBrokerSubscriber():
    def __init__(self):
        self.event_broker_type = config.EVENT_BROKER_TYPE
        self.event_broker_url = config.EVENT_BROKER_URL
        self.event_broker_topic = config.EVENT_BROKER_TOPIC
        self.event_broker = EventBrokerSubscriberFactory(self.event_broker_type)
        self.event_broker.connect(self.event_broker_url)
        self.event_broker.subscribe(self.event_broker_topic)
    
    def get_message(self):
        msg = self.event_broker.get_message()
        return msg

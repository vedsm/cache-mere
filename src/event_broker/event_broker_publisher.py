from src.event_broker_factory.event_broker_publisher_factory import EventBrokerPublisherFactory
from src import config


class EventBrokerPublisher():
    def __init__(self):
        self.event_broker_type = config.EVENT_BROKER_TYPE
        self.event_broker_url = config.EVENT_BROKER_URL
        self.event_broker_topic = config.EVENT_BROKER_TOPIC
        self.event_broker = EventBrokerPublisherFactory(self.event_broker_type)
        self.event_broker.connect(self.event_broker_url)

    def publish(self, msg):
        self.event_broker.publish(self.event_broker_topic, msg)

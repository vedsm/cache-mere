from .redis_event_broker_publisher import RedisEventBrokerPublisher

def EventBrokerPublisherFactory(event_broker_type):
    if event_broker_type == "REDIS":
        return RedisEventBrokerPublisher()
    else:
        print("This event_broker_type is not supported", event_broker_type)

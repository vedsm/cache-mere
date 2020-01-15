from .redis_event_broker_subscriber_adapter import RedisEventBrokerSubscriber

def EventBrokerSubscriberFactory(event_broker_type):
    if event_broker_type == "REDIS":
        return RedisEventBrokerSubscriber()
    else:
        print("This event_broker_type is not supported", event_broker_type)

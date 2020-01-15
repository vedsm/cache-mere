import redis

class RedisEventBrokerSubscriber():
    def __init__(self):
        print("RedisEventBrokerSubscriber initiated!!")
    
    def connect(self, url):
        self.r = redis.from_url(url)
        # self.r = redis.Redis(host='localhost', port=6379, db=0)

    def subscribe(self, topic):
        print("Going to subscribe to redis topic", topic)
        self.sub = self.r.pubsub()
        self.sub.subscribe(topic)
    
    def get_message(self):
        # print("Reading a message from redis")
        msg = self.sub.get_message()
        # print("message read from redis", msg)
        return msg


import redis
import json

class RedisEventBrokerPublisher():
    def __init__(self):
        print("RedisEventBrokerPublisher initiated!!")
    
    def connect(self, url):
        self.r = redis.from_url(url)
        # self.r = redis.Redis(host='localhost', port=6379, db=0)

    # def publish(self, topic, msg):
    #     print("Going to publish msg to redis topic", topic, msg)

    def publish(self, stream, msg):
        print("Going to publish msg to redis stream", stream, msg)
        return self.r.xadd(stream, msg)

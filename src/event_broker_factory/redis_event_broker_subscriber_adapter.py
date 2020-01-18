import redis

class RedisEventBrokerSubscriber():
    def __init__(self):
        print("RedisEventBrokerSubscriber initiated!!")
    
    def connect(self, url):
        self.r = redis.from_url(url)
        # self.r = redis.Redis(host='localhost', port=6379, db=0)

    # def subscribe(self, topic):
    #     print("Going to subscribe to redis topic", topic)
    #     self.sub = self.r.pubsub()
    #     self.sub.subscribe(topic)

    # def get_message(self):
    #     # print("Reading a message from redis")
    #     msg = self.sub.get_message()
    #     # print("message read from redis", msg)
    #     return msg

    def subscribe(self, stream, consumer_group, consumer):
        print("Going to subscribe to redis stream", stream, consumer_group, consumer)
        self.stream = stream
        self.consumer_group = consumer_group
        self.consumer = consumer
        #TODO: use redis streams
        try:
            self.r.xgroup_create(self.stream, self.consumer_group, "$", True)
        except Exception as error:
            print("unable to create consumer group", error)
        # finally:
        #     print("Do something finally")
    
    def get_message(self):
        # print("Reading a message from redis")
        msg = self.r.xreadgroup(self.consumer_group, self.consumer, {self.stream: ">"}, 1)
        # print("message read from redis", msg)
        return msg


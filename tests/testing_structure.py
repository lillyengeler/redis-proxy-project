import os
import redis

REDIS_ADDRESS = host=os.getenv("REDIS_ADDRESS", 'redis-service')
REDIS_PORT = os.getenv("REDIS_PORT")
PROXY_ADDRESS = os.getenv('PROXY_ADDRESS','0.0.0.0')
PROXY_PORT = os.getenv('PROXY_PORT',5000)

# class TestStruct:
#     def __init__(self):
#         self.redis_instance = redis.Redis(REDIS_ADDRESS, REDIS_PORT)
#         self.base_url = 'http://' + str(PROXY_ADDRESS) + ':' + str(PROXY_PORT)

    # def addToRedis(self, key, value):
    #     self.redis_instance.set(key, value)
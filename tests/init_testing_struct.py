import os
import requests
from redis import Redis

# Default configurations can be set with environment variables
REDIS_ADDRESS = os.environ.get('REDIS_ADDRESS', 'redis-service')
PROXY_ADDRESS = os.environ.get('PROXY_ADDRESS',
                                 'web-app-service')
PROXY_PORT = os.environ.get('PROXY_PORT', 5000)


class InitTestStruct:

    def __init__(self, proxy_address=PROXY_ADDRESS, proxy_port=PROXY_PORT):
        self.redisInstance = Redis(REDIS_ADDRESS, 6379, None)
        self.proxy_url = 'http://' + proxy_address + ':' + proxy_port + '/'

    def clear_redis(self):
        """
        Clear all key-values pairs from Redis backing instance
        """
        self.redisInstance.flushall()

    def populate_redis(self, d):
        """
        Populate Redis backing instance from the given dictionary
        Parameters:
            d dict: a dictionary of key-value pairs
        """
        for k, v in d.items():
            self.redisInstance.set(k, v)

    def setVal(self, key, value):
        """
        Set single key value to Redis instance
        """
        self.redisInstance.set(key,value)

    def getVal(self,key):
        """
        Get single value from Redis Instance
        """
        return self.redisInstance.get(key)

    def make_get_request(self, key):
        """
        Make an HTTP GET request to the proxy instance
        """
        # newURL = self.proxy_url + key
        newURL = self.proxy_url + 'submit/' + key
        res = requests.get(url=newURL)
        return res

    def return_head_request(self):
        newURL2 = self.proxy_url + 'test/returnHead'
        res = requests.get(url=newURL2)
        return res

    def return_lru_request(self):
        newURL3 = self.proxy_url + 'test/returnTail'
        res = requests.get(url=newURL3)
        return res
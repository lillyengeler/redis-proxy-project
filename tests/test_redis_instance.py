"""
Testing that the proxy connects to a running Redis instance
"""
import os
from dotenv import load_dotenv, dotenv_values
import redis
# from testing_structure import TestStruct

REDIS_ADDRESS = os.getenv("REDIS_ADDRESS")
REDIS_PORT = os.getenv("REDIS_PORT")
PROXY_ADDRESS = os.getenv('PROXY_ADDRESS','0.0.0.0')
PROXY_PORT = os.getenv('PROXY_PORT',5000)


def redis_instance_case(key,value):
    # redisInst = TestStruct()
    # addy = os.getenv("REDIS_ADDRESS")
    # port = os.getenv("REDIS_PORT")

    redisInstance = redis.Redis(host="redis-service", port=5000, db=0)

    redisInstance.set(key,value)
    getVal = redisInstance.get(key)

    return getVal

def test_redis_instance_case():
    assert redis_instance_case('name','lilly') == 'lilly'


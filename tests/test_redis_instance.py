"""
Testing that the proxy connects to a running Redis instance
"""
from init_testing_struct import InitTestStruct


def redis_instance_case(key,value):
    redisInstance = InitTestStruct()
    redisInstance.clear_redis() 

    redisInstance.setVal(key,value)
    returnedVal = redisInstance.getVal(key)

    return str(returnedVal.decode("utf-8"))

def test_redis_instance_case():
    assert redis_instance_case('question','answer') == 'answer'


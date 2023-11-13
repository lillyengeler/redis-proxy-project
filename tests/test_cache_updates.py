"""
Test update/add node functionality 

Verify that when a node is added/updated to the cache, it becomes the most recently used -> 
assumes capacity = 3 and ttl = 60

"""

from init_testing_struct import InitTestStruct

def test_cache_updates_case():
    proxyInstance = InitTestStruct()
    proxyInstance.clear_redis() 

    # add 4 values to redis
    proxyInstance.populate_redis({"t1":"r1", "t2":"r2", "t3":"r3", "t4":"r4"})

    # add values to cache
    proxyInstance.make_get_request('t1')
    proxyInstance.make_get_request('t2')
    proxyInstance.make_get_request('t3')

    # head should now be the key 't3'
    result1 = proxyInstance.return_head_request()
    # look at t2 again:
    proxyInstance.make_get_request('t2')
    # now head should be the key 't2' : tests updateHead
    result2 = proxyInstance.return_head_request()
    # look at t4:
    proxyInstance.make_get_request('t4')
    # now head should be the key 't4' : tests addNewToHead
    result3 = proxyInstance.return_head_request()

    assert result1.text == 't3'
    assert result2.text == 't2'
    assert result3.text == 't4'
    
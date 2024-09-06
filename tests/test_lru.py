"""
Test LRU cache functionality 

Verify that a node not accessed for the longest amount of time will be at the back of the list -> 
assumes capacity = 3 and ttl = 60

"""

from init_testing_struct import InitTestStruct

def test_lru_case():
    proxyInstance = InitTestStruct()
    # proxyInstance.clear_redis() 

    # add 4 values to redis
    proxyInstance.populate_redis({"t1":"r1", "t2":"r2", "t3":"r3", "t4":"r4"})

    # add values to cache
    proxyInstance.make_get_request('t1')
    proxyInstance.make_get_request('t2')
    proxyInstance.make_get_request('t3')

    # LRU should now be the key 't1'
    result1 = proxyInstance.return_lru_request()
    # look at t2 again:
    proxyInstance.make_get_request('t4')
    # now t1 should be deleted from the list and lru is now 't2'
    result2 = proxyInstance.return_lru_request()
    # look at t4:
    proxyInstance.make_get_request('t1')
    proxyInstance.make_get_request('t3')
    # now lru should be the key 't4' 
    result3 = proxyInstance.return_lru_request()

    assert result1.text == 't1'
    assert result2.text == 't2'
    assert result3.text == 't4'
    

# web service using Flask 
from flask import Flask
import redis
import time
from localCache import * 

app = Flask(__name__)
redisClient = redis.Redis(host='redis-service', port=6379, db=0) # redis connected through docker-compose

redisClient.set('name','lillian')
redisClient.set('you','rock')
redisClient.set('color', 'pink')

# set capacity -> CHANGE LATER
capacity = 3

# set TTL (in seconds) -> CHANGE LATER 
maxTimeAllowed = 60

cache = localCache(capacity,maxTimeAllowed) # initialize empty dictionary and doubly linked list object


@app.route('/')
def home():
    # return "at home page"  
    return "home page"


@app.route('/printCache')
def printCache():
    # return "at home page"  
    print("PRINTING CACHE: ", flush=True)
    cache.printCache()
    return "printing local cache to console"


@app.route("/key=<key>") 
def search_key(key):
    # check local cache for key:
    inCache = cache.searchCache(key)
    # -> if in cache: 
    if inCache:
        # check if key has expired
        currNode = cache.listMap[key]
        currTime = time.time()
        print("curr key's time in cache: ", flush=True)
        print((currTime - currNode.timeCreated), flush=True)
        print("currTime: ", currTime, flush=True)
        # delete key from local cache if expired
        if (currTime - currNode.timeCreated) >= cache.timeLimit:
            print("key has expired", flush=True)
            print("currTime: ", currTime, flush=True)
            print("time node was created: ", currNode.timeCreated, flush=True)
            print("currTime - timeCreated = ", (currTime - currNode.timeCreated), flush=True)

            cache.delExpiredNode(key)
            # check Redis for key. Return None if not found
            keyValue = (redisClient.get(key))
            if keyValue == None:
                print("key not found in local cache or redis", flush=True)
                return "no key found"
            # add back to head of cache and return
            else:
                print("key found in redis, adding to cache", flush=True)
                # check cache size: delete LRU if full
                if len(cache.listMap) >= cache.capacity:
                    # delete LRU from TAIL of cache AND the listMap
                    cache.deleteLRU()
                cache.addNewToHead(key, keyValue)
                return keyValue

        # move key to head of list and return value
        return cache.updateNode(key)

    # -> not in cache: 
    else:
        # check Redis for key. Return None if not found
        keyValue = (redisClient.get(key))
        if keyValue == None:
            print("key not found in local cache or redis", flush=True)
            return "no key found"
        
        else:
            print("key found in redis, adding to cache", flush=True)
            # check cache size: delete LRU if full
            if len(cache.listMap) >= cache.capacity:
                # delete LRU from TAIL of cache AND the listMap
                cache.deleteLRU()

            # now can add the key to the HEAD of the cache
            cache.addNewToHead(key, keyValue)

            return keyValue

if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000, debug=True)



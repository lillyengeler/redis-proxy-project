# application entrypoint

# configure the redis cache 
# cache = Cache(app, config={
#     'CACHE_TYPE': 'redis',
#     'CACHE_KEY_PREFIX': 'server1',
#     'CACHE_REDIS_HOST': 'localhost',
#     'CACHE_REDIS_PORT': '6379',
#     'CACHE_REDIS_URL': 'redis://localhost:6379'
# })

# route == path (maps what user types in url to a python function)

# @app.route('/set')
# def set():
#     key = request.args.get('key')
#     value = request.args.get('value')
#     cache.set(key,value)
#     return "Cache has been set"

# @app.route('/get')
# def get():
#     key = request.args.get('key')

# web service using Flask (micro web framework)
from flask import Flask
import redis
# from flask import Flask, request, render_template
# from flask_caching import Cache


app = Flask(__name__)
redisClient = redis.Redis(host='redis-service', port=6379, db=0) # redis connected through docker-compose

redisClient.set('name','lillian')
redisClient.set('you','rock')

localCache = {} # initialize empty dictionary

@app.route('/')
def home():
    # return "at home page"  
    return "home page"

@app.route('/printCache')
def printCache():
    # return "at home page"  
    print("PRINTING CACHE: ", flush=True)
    for key in localCache:
        print(key, ": ", str(localCache[key]), flush=True)
    return "printing local cache to console"


@app.route("/<key>") 
def search_key(key):
    # (1.) check local cache to see if it has the key
    if localCache.get(key) != None:
        print("found the key in the local cache", flush=True)
        return localCache[key]
    # (2.) local cache doesn't have the key: see if it's in redis db
    else:
        print("key NOT in local cache: searching redis", flush=True)
        keyValue = (redisClient.get(key))
        # if the key isn't in the redis db just return no key found
        if keyValue == None:
            print("key not found in local cache or redis", flush=True)
            return "no key found"
        # if the key is in redis, add to local cache and then return value
        else:
            print("key found in redis, adding to cache", flush=True)
            localCache[key] = keyValue
            return keyValue


# @app.route("/<key>") 
# def search_key(key):
#     keyValue = (redisClient.get(key))

#     if keyValue == None:
#         return "no key found"
#     else:
#         return keyValue


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000, debug=True)



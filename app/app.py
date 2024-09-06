
# web service using Flask 
from flask import Flask, render_template, request, redirect, url_for, jsonify
import redis
import os
from dotenv import load_dotenv, dotenv_values
import time
import threading
from localCache import * 
from config import app

#app = Flask(__name__)
redisClient = redis.Redis(host=os.getenv("REDIS_ADDRESS"), port=os.getenv("REDIS_PORT"), db=0) # redis connected through docker-compose

capacity = int(os.getenv("CACHE_CAPACITY", 3)) # access capacity: default = 3
maxTimeAllowed = float(os.getenv("CACHE_EXPIRY_TIME", 60)) # access cache expiry time (in seconds): default = 60

cache = localCache(capacity,maxTimeAllowed) # initialize empty dictionary and doubly linked list object
lock = threading.Lock() # initialize lock to protect cache during reads/writes

# home page
@app.route('/')
def home():
    # return "To request a value from Redis, type a forward slash followed by the requested key into the search bar"
    return render_template("home.html")


@app.route('/submit', methods=['POST', 'GET'])
def return_key():
    if request.method=='POST':
        res = request.form.get("key")
        print(res)

    if res:
        # Redirect to search_key if key exists
        return redirect(url_for('search_key', key=res))
    else:
        # Handle case where key is not found (you can render a template with an error message or handle differently)
        return "Error: Key not provided", 400

# main function - get the requested key/value
@app.route("/submit/<key>") 
def search_key(key):   
    with lock:
        # check local cache for key:
        inCache = cache.searchCache(key)
    # -> if in cache: 
    if inCache:
        # check if key has expired
        if cache.hasExpired(key):            
            with lock:
                # delete key from local cache 
                cache.delExpiredNode(key)
            # check Redis for key. Return None if not found
            keyValue = (redisClient.get(key))
            if keyValue == None:
                return "~ Key not found in Redis ~"
            # add back to head of cache and return
            else:
                with lock:
                    # check cache size: delete LRU if full
                    if len(cache.listMap) >= cache.capacity:
                        # delete LRU from TAIL of cache AND the listMap
                        cache.deleteLRU()
                    cache.addNewToHead(key, keyValue)
                    return str(keyValue.decode("utf-8"))

        # if not expired: move key to head of list and return value
        else:
            with lock:
                keyValue = cache.updateNode(key)
                return str(keyValue.decode("utf-8"))

    # -> not in cache: 
    else:
        # check Redis for key. Return None if not found
        keyValue = (redisClient.get(key))
        if keyValue == None:
            return "~ Key not found in Redis ~"
        
        else:
            with lock:
                # check cache size: delete LRU if full
                if len(cache.listMap) >= cache.capacity:
                    # delete LRU from TAIL of cache AND the listMap
                    cache.deleteLRU()

                # now can add the key to the HEAD of the cache
                cache.addNewToHead(key, keyValue)

                return str(keyValue.decode("utf-8"))
                    
# print MRU from cache for testing purposes
@app.route('/test/returnHead')
def returnHead():
    key = cache.returnHead()
    return key

# print LRU from cache for testing purposes
@app.route('/test/returnTail')
def returnTail():
    key = cache.returnTail()
    return key

# print cache as a list for testing purposes
@app.route('/test/printCache', methods=['GET','POST'])
def printCache():
    curreCache = cache.printCache()
    if not curreCache:
        return jsonify({'message': 'Cache is empty'}), 404

    return jsonify(curreCache)


if (__name__ == "__main__"):
    app.run(host=os.getenv('PROXY_ADDRESS','0.0.0.0'), port=os.getenv('PROXY_PORT',5000), debug=True)
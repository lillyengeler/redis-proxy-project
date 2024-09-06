""" 
local cache: dictionary with doubly linked list
"""
import time

# create a Node class for adding Node objects
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.timeCreated = time.time()
        self.prev = None
        self.next = None

class localCache(object):
    def __init__(self, capacity, timeLimit):
        # initalize Map that will point to list nodes
        self.listMap = {}

        # initialize an empty doubly linked list
        self.head = Node(0,0)
        self.tail = Node(0,0)

        self.head.next = self.tail
        self.head.prev = None
        self.tail.prev = self.head
        self.tail.next = None

        self.capacity = capacity
        self.timeLimit = timeLimit

    # deletes the least recently used node in the list -> found at the tail 
    def deleteLRU(self):
        # get least recently node (@ tail's prev)
        nodeToDelete = self.tail.prev

        # update ptrs: 
        newLRU = nodeToDelete.prev
        # lru node's->prev should now point to the tail
        newLRU.next = self.tail
        # tail.prev should now point to the new LRU
        self.tail.prev = newLRU

        # delete node from listMap by referencing the key
        del self.listMap[nodeToDelete.key]

        # now there are no direct references to the node:
        # so CPython automatically reclaims this memory

    # adds a new key/value pair to the head of the doubly linked list
    def addNewToHead(self, key, value):
        nodeToAdd = Node(key, value)

        nodeToAdd.next = self.head.next
        self.head.next.prev = nodeToAdd
        self.head.next = nodeToAdd
        nodeToAdd.prev = self.head

        # add the key and ref to node to the listMap
        self.listMap[key] = nodeToAdd

    # searches dictionary for key
    def searchCache(self, key):
        if key in self.listMap:
            return True
        else:
            return False

    # updates the priority of a node already present in the list to MRU -> moves it to the head of the list
    def updateNode(self, key):
        # take node out of list
        newMRU = self.listMap[key]
        tempPrev = newMRU.prev
        newMRU.prev.next = newMRU.next
        newMRU.next.prev = tempPrev

        # add node to head of list
        tempNext = self.head.next
        self.head.next.prev = newMRU
        self.head.next = newMRU
        newMRU.next = tempNext
        newMRU.prev = self.head

        return newMRU.value

    # checks if key is past the set time limit
    def hasExpired(self,key):
        currNode = self.listMap[key]
        currTime = time.time()

        if (currTime - currNode.timeCreated) >= self.timeLimit:
            return True
        return False

    # deletes the node that has expired based on the global expiry
    def delExpiredNode(self, key):
        # take node out of list
        toDelete  = self.listMap[key]
        tempPrev = toDelete.prev
        toDelete.prev.next = toDelete.next
        toDelete.next.prev = tempPrev

        # delete node from listMap by referencing the key
        del self.listMap[key]

    # prints keys and their values in the cache
    def printCache(self):
        currCache = {}
        temp = self.head
        if temp.next != None:
            temp = temp.next
            while temp != self.tail:
                currCache[str(temp.key)] = str(temp.value.decode())
                print(temp.key, temp.value, flush=True)
                temp = temp.next

        return currCache
    
    # used in tests
    def returnHead(self):
        if self.head.next == self.tail or self.head.next == None:
            return "list is empty"
        return self.head.next.key

    # used in tests
    def returnTail(self):
        if self.tail.prev == self.head or self.tail.prev == None:
            return "list is empty"
        return self.tail.prev.key




from collections import OrderedDict
import tqdm
import os
import pickle
import struct

class LRUCache:

    def __init__(self, max_capacity: float):
        self.cache = OrderedDict()
        self.max_capacity = max_capacity
        self.used_capacity = 0

    # check if a key is in the cache
    def isIn(self, key):
        if key in self.cache:
            return True
        else:
            return False

    # getting tuple with the size and value
    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    # put size and value of the file in the cache
    def put(self, key, size, value) -> None:
        print (self.used_capacity)
        if(size > self.max_capacity):
            return -1
        while key not in self.cache:
            if (self.used_capacity + size) > self.max_capacity:
                aux = self.cache.popitem(last = False)
                self.used_capacity -= aux[1][0]            
            else:
                self.cache[key] = (size,value)
                self.cache.move_to_end(key)
                self.used_capacity += size

    def cacheList(self):
        key_list = []
        for key in self.cache:
            key_list.append(key)
        return key_list
            

# RUNNER
# initializing our cache with the capacity of 2
max_size = 64*1048576
#print(max_size)
cache = LRUCache(max_size) 
direc = "."
requested_filename = "projeto.pdf"

if(os.path.isfile(direc+"/"+requested_filename)):
    
    filesize = int(os.path.getsize(requested_filename))
    #progress = tqdm.tqdm(range(filesize), f"Receiving {requested_filename}", unit="B", unit_scale=True, unit_divisor=1024)
    #print(filesize)

    with open(direc+"/"+requested_filename, "rb") as arq:
        data = arq.read()
        data = pickle.dumps(data)
        #cache.put(requested_filename, filesize, data)

#print(cache.cache)        


cache.put("prr", 10, "adasdfafasf")

cache.put("dadar", 10, "adasdfafasf")
#print(cache.cache)
#aux = cache.get("projeto.pdf")
print(cache.cache)
#print(aux[0])

print(cache.cacheList())

#This code was contributed by Sachin Negi

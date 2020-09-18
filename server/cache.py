from collections import OrderedDict
import tqdm
import os
import pickle

class LRUCache:

    # initialising capacity
    def __init__(self, max_capacity: float):
        self.cache = OrderedDict()
        self.max_capacity = max_capacity
        self.used_capacity = 0

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, size, value) -> None:
        print (self.used_capacity)
        if(size > self.max_capacity):
            return -1
        while key not in self.cache:
            if (self.used_capacity + size) > self.max_capacity:
                
                aux = self.cache.popitem(last = False)
                self.used_capacity -= aux[1][0]
                
            else:
                #msg = pickle.dumps((size,value))
                self.cache[key] = (size,value)
                self.cache.move_to_end(key)
                self.used_capacity += size
            


# RUNNER
# initializing our cache with the capacity of 2
max_size = 64*1048576
print(max_size)
cache = LRUCache(max_size) 
direc = "."
requested_filename = "osx.txt"
if(os.path.isfile(direc+"/"+requested_filename)):

    filesize = int(os.path.getsize(requested_filename))
    print(filesize)

    arq = open(direc+"/"+requested_filename, "rb")
    cache.put(requested_filename, filesize, arq)
            


#cache.put("prr", 10, "adasdfafasf")
print(cache.cache)
#print(cache.get("prr"))
#cache.put("pr4", 10, "adaasfaafasf")
#print(cache.cache)
#cache.get("prr")
#cache.put("p2r", 40, "adasdfafasf")
#print(cache.cache)




#This code was contributed by Sachin Negi

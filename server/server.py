import socket
import sys
from collections import OrderedDict
import pickle
import time
import tqdm
import os
from io import BytesIO

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

    # return a list with cached keys
    def cacheList(self):
        key_list = []
        for key in self.cache:
            key_list.append(key)
        return key_list

def send_file(client_socket, address, requested_filename):
    # print client ip and file who is requested
    print(f"[+] Client {address} is requesting file {requested_filename}.")

    if(cache.isIn(requested_filename)):
        print(f"[+] Cache hit. File {requested_filename} sent to the client.")

        # get value for the requested file
        value = cache.get(requested_filename)

        # the filesize is the first element of the tuple
        filesize = value[0]

        # send the bool and filesize
        client_socket.send(f"{1}{SEPARATOR}{filesize}".encode())

        # the bytes of the archive is the second element
        bin_file = pickle.loads(value[1])

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {requested_filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with BytesIO(bin_file) as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                client_socket.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

    else:
        if(os.path.isfile(direc+"/"+requested_filename)):
            filesize = int(os.path.getsize(direc+"/"+requested_filename))

            print(f"[+] Cache missed. File {requested_filename} sent to the client.")
            
            #putting file in the cache
            with open(direc+"/"+requested_filename, "rb") as arq:
                data = arq.read()
                data = pickle.dumps(data)
                cache.put(requested_filename, filesize, data)

            # send the bool and filesize
            client_socket.send(f"{1}{SEPARATOR}{filesize}".encode())

            # get value for the requested file
            value = cache.get(requested_filename)
            
            # the bytes of the archive is the second element
            bin_file = pickle.loads(value[1])
    
            # start sending the file
            progress = tqdm.tqdm(range(filesize), f"Sending {requested_filename}", unit="B", unit_scale=True, unit_divisor=1024)

            with BytesIO(bin_file) as f:
                for _ in progress:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in 
                    # busy networks
                    client_socket.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read)) 
        else:
            print(f"[+] File {requested_filename} does not exist.")
            # send the bool and filesize
            client_socket.send(f"{0}{SEPARATOR}{0}".encode())

    # close the client socket
    client_socket.close()



# arguments
port = int(sys.argv[1])
direc = sys.argv[2]

# device's IP address
host = "localhost"

# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
s = socket.socket()

# bind the socket to our local address and start to listen
s.bind((host, port))
s.listen(5)

print(f"[*] Listening as {host}:{port}")

# set max size and create cache
max_size = 64*1048576
cache = LRUCache(max_size) 

# main loop
while True:

    print(f"[*] Waiting connection")
    client_socket, address = s.accept()

    requested_item = client_socket.recv(BUFFER_SIZE).decode()

    if (requested_item == "cache_list"):
        print(f"[+] Client {address} is requesting the cached files.")
        #client_socket.send(f"{cache.cacheList()}".encode())
        data = pickle.dumps(cache.cacheList())
        client_socket.sendall(data)
    else:
        send_file(client_socket, address, requested_item)
       
# close the server socket
s.close()
    





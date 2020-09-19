import socket
import sys
from collections import OrderedDict
import pickle
import time
import tqdm
import os
from io import BytesIO

class LRUCache:

    # initialising capacity
    def __init__(self, max_capacity: float):
        self.cache = OrderedDict()
        self.max_capacity = max_capacity
        self.used_capacity = 0

    def isIn(self, key):
        if key in self.cache:
            return True
        else:
            return False

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

#arguments
port = int(sys.argv[1])
direc = sys.argv[2]

# device's IP address
host = "localhost"

# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
s = socket.socket()

# bind the socket to our local address
s.bind((host, port))

s.listen(5)

print(f"[*] Listening as {host}:{port}")

# set max size and create cache
max_size = 64*1048576
cache = LRUCache(max_size) 

while True:

    print(f"[*] Waiting connection")
    client_socket, address = s.accept()

    requested_filename = client_socket.recv(BUFFER_SIZE).decode()

    # if below code is executed, that means the sender is connected
    print(f"[+] Client {address} is requesting file {requested_filename}.")

    #def send_file(requested_filename, host, port):

    if(cache.isIn(requested_filename)):
        print(f"[+] Cache hit. File {requested_filename} sent to the client.")
        #print(cache.get(requested_filename))

        filesize = cache.get(requested_filename)[0]

        # send the bool and filesize
        client_socket.send(f"{1}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {requested_filename}", unit="B", unit_scale=True, unit_divisor=1024)

        temp_file = cache.get(requested_filename)
        temp_file = pickle.loads(temp_file[1])
        
        with BytesIO(temp_file) as f:
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
            
            #putting file in the cache memory
            with open(direc+"/"+requested_filename, "rb") as arq:
                data = arq.read()
                data = pickle.dumps(data)
                cache.put(requested_filename, filesize, data)

            # send the bool and filesize
            client_socket.send(f"{1}{SEPARATOR}{filesize}".encode())

            # start sending the file
            progress = tqdm.tqdm(range(filesize), f"Sending {requested_filename}", unit="B", unit_scale=True, unit_divisor=1024)
            #with open(direc+"/"+requested_filename, "rb") as f:

            temp_file = cache.get(requested_filename)
            temp_file = pickle.loads(temp_file[1])
      

            with BytesIO(temp_file) as f:
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
    
# close the server socket
s.close()
    





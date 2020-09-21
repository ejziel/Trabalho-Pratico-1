import socket
import sys
from collections import OrderedDict
import pickle
import time
import tqdm
import os
from io import BytesIO
import threading

MAX_SIZE = 64*1048576

class RWLock:
    #construtor
    def __init__(self):
        self.readers = 0
        self.mutex = threading.Semaphore(1) #Semáforo de leitura
        self.lock = threading.Semaphore(1)  #Semáforo de escrita
 
    def read_acquire(self):
        self.mutex.acquire() #bloqueia para leitura
        self.readers += 1 #soma a quantidade de leitores
        if self.readers == 1:
            self.lock.acquire() #Se você é o primeiro leitor, bloqueie o recurso dos escritores.
                                # Recurso permanece reservado para leitores subseqüentes
        self.mutex.release() # desbloqueia
 
    def read_release(self):
        self.mutex.acquire() #bloqueia para leitura
        self.readers -= 1
        if self.readers == 0:
            self.lock.release() #Se você for o último leitor, poderá desbloquear o recurso. 
                                # Isso torna disponível para escritores.
        self.mutex.release() #desbloqueia
 
    def write_acquire(self):
        self.lock.acquire() #bloqueia o semaforo de escrita
 
    def write_release(self):
        self.lock.release() #desbloqueia

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
    print(f"[+] Client {address} is requesting file {requested_filename}.\n")
    lock.read_acquire()

    time.sleep(10)
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
                client_socket.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

    else:

        if(os.path.isfile(direc+"/"+requested_filename)):
            filesize = int(os.path.getsize(direc+"/"+requested_filename))
            print(f"[+] Cache missed. File {requested_filename} sent to the client.")
            
            if(filesize <= MAX_SIZE):

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
                        client_socket.sendall(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read)) 
            else:
                # if the file is bigger than max size of the cache
                # send the bool and filesize
                client_socket.send(f"{1}{SEPARATOR}{filesize}".encode())

                # start sending the file
                progress = tqdm.tqdm(range(filesize), f"Sending {requested_filename}", unit="B", unit_scale=True, unit_divisor=1024)

                with open(direc+"/"+requested_filename, "rb") as f:
                    for _ in progress:
                        # read the bytes from the file
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            # file transmitting is done
                            break
                        client_socket.sendall(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))

        else:
            print(f"[+] File {requested_filename} does not exist.")
            # send the bool and filesize
            client_socket.send(f"{0}{SEPARATOR}{0}".encode())

    # close the client socket
    client_socket.close()
    lock.read_release()

def send_list(client_socket, address):
    print(f"[+] Client {address} is requesting the cached files.\n")
    lock.read_acquire()

    #print(threading.current_thread().ident, "Reading:")
    time.sleep(10)
    data = pickle.dumps(cache.cacheList())
    client_socket.sendall(data)
    #time.sleep(0.5)
    client_socket.close()
    lock.read_release()
    


# arguments
port = int(sys.argv[1])
direc = sys.argv[2]

# device's IP address
host = "localhost"

# receive 4096 bytes each time
#BUFFER_SIZE = 4096
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

# create the server socket
s = socket.socket()

# bind the socket to our local address and start to listen
s.bind((host, port))
s.listen(5)

print(f"[*] Listening as {host}:{port}")

# create cache
cache = LRUCache(MAX_SIZE) #VERIFICAR CACHE

# create locker
lock = RWLock()

# main loop
while True:

    print(f"[*] Waiting connection.\n")
    client_socket, address = s.accept()

    requested_item = client_socket.recv(BUFFER_SIZE).decode()

    if (requested_item == "cache_list"):  
        #print("Main    : creating thread")
        x = threading.Thread(target=send_list, args=(client_socket, address))
        x.start()
        #print("Main    : running thread")
        #send_list(client_socket, address)
    else:
        #print("Main    : creating thread")
        x = threading.Thread(target=send_file, args=(client_socket, address, requested_item))
        x.start()
        #print("Main    : running thread")
        #send_file(client_socket, address, requested_item) #VERIFICAR CACHE


# close the server socket
s.close()
    





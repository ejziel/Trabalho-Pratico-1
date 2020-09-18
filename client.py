import socket
import sys
import pickle
import time
import os
import tqdm

#arguments

filename = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])
direc = sys.argv[4]

SEPARATOR = "<SEPARATOR>"

BUFFER_SIZE = 1024 * 4

def request_file(filename, host, port, direc):
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename 
    s.send(f"{filename}".encode())

    received = s.recv(BUFFER_SIZE).decode()
    aux, filesize = received.split(SEPARATOR)

    if (int(aux)):
        # convert to integer
        filesize = int(filesize)
        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(direc+"/"+filename, "wb") as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)
                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
    else:
        print(f"[+] File {filename} does not exist in the server")
    
     # close the socket
    s.close()

   
request_file(filename, host, port, direc)
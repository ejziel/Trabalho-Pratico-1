import socket
import sys
import pickle
import time
import tqdm
import os

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
# accept connection if there is any
while True:

    print(f"[*] Waiting connection")
    client_socket, address = s.accept()

    requested_filename = client_socket.recv(BUFFER_SIZE).decode()

    # if below code is executed, that means the sender is connected
    print(f"[+] Client {address} is requesting file {requested_filename}.")

    #def send_file(requested_filename, host, port):

    if(os.path.isfile(requested_filename)):
        filesize = int(os.path.getsize(requested_filename))

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
    





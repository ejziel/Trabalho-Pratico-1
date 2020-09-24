# Practical work 1 - client/server file transfer via sockets

Name : Ejziel Santos <br>
Email : ejziels@gmail.com <br>
Affiliation : Federal University of Recôncavo da Bahia (UFRB) <br>

## Project Description : <br>

(A) A multi-threaded server which interacts with any standard Clients. The server and client communicate using a TCP/IP socket. <br>
(B) A single-threaded client that communicates with the server asking for a file, and downloads it. <br>

### Specifications - Server

The server being multi-threaded, handles multiple requests concurrently. The main thread ( server ), listens to a specified port. Upon receiving a request, the server sets up a TCP connection to the requesting client and serves the request in a separate thread. <br>
The server execution cycle after receiving a request is described as follows: <br>
1. If the server receives a message with the key "cache_list" from the client, it will return a list of the cached files. 
2. When the client requests a file from the server, it prints "Client {address} is requesting file {requested_filename}.", and starts searching for the requested file in the cache memory.

     - If the file is cached, the server sends the file to the client and prints the message "Cache hit. File {requested_filename} sent to the client." 

     - If the file is not in cache, the server will check if it is in the directory.

         - If the file size is larger than 64 MB, the file is sent to the client and prints the message "Cache missed. File {requested_filename} sent to the client."
         - If the file size is less than or equal to 64 MB, the file is cached and then sent to the client. The caching process uses the LRU (Least recently used) cache replacement policy, and works as follows:

             (a) **if used cache storage + file size <= 64MB**: Caches the file, sends it to the client and prints the message "Cache missed. File {requested_filename} sent to the client."
             
             (b) **if used cache storage + file size > 64MB**: Remove the least recently requested file and perform step (a) again until the condition is satisfied.
     - If the file does not exist in the server's directory, print the message "File {requested_filename} does not exist."

In all cases of access to cache memory, the multithreaded locking process is carried out to ensure mutual exclusion.

• If running the server program using command line, the syntax should be : <br>
```
% python server.py port_to_listen_on file_directory
e.g.
% python server.py 9089 /home/ejziel/projeto1
```
<p>(a) port_to_listen_on: The port on which the server will listen for connections <br>
(b) file_directory: The directory where the server will fetch the requested files. <br>
  
### Specifications - Client

The client should be able to initiate a connection to the server via a socket, and request a file, or a list of cached files to the server. Upon receipt of the response message from the server, the client extracts and displays the message status and then save the file, otherwise it displays a corresponding error message .<br>

• The client program can be executed using command line, with the following syntax: <br>
```
% python client.py server_host server_port file_name directory
e.g.
% python client.py localhost 9089 projeto.pdf /home/ejziel/projeto1/client
```
<p>(a) server_host: The IP address or name of the server, e.g., 127.0.0.1 or localhost for the server running on the local machine. <br>
(b) server_port: The port on which the server is listening to connections from clients. <br>
(c) file_name: The name of the requested file. <br>
(d) directory: The directory to save the requested files. <br>

• To request a list of cached files, the reserved word "***list***" is used as an argument instead of the file name, with the following syntax: <br>

```
e.g.
% python client.py localhost 9089 list
```
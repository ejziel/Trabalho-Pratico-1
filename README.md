# Practical work 1 - client/server file transfer via sockets

Name : Ejziel Santos <br>
Email : ejziels@gmail.com <br>
Affiliation : Federal University of Recôncavo da Bahia (UFRB) <br>

## Project Description : <br>

(A) A multi-threaded server which interacts with any standard Clients. The server and client communicate using a TCP/IP socket. <br>
(B) A single-threaded client that communicates with the server asking for a file, and downloads it. <br>
(C) The essential parameters of the connection are displayed both on the client and on the server. <br>

### Specifications - Server

The server being multi-threaded, handles multiple requests concurrently. The main thread ( server ), listens to a specified port. Upon receiving a request, the server sets up a TCP connection to the requesting client and serves the request in a separate thread. After sending the response back to the client, it closes the connection. <br>
• If running the server program using command line, the syntax should be : <br>
```
% python server.py port_to_listen_on file_directory
e.g.
% python server.py 9089 /home/ejziel/projeto1
```
<p>(a) port_to_listen_on: The port on which the server will listen for connections <br>
(b) file_directory: The directory where the server will fetch the requested files. <br>
  
### Specifications - Client

The client should be able to initiate a connection to the server, via a socket and request any page on the server. Upon receipt of the response message from the server, the client extracts and displays/logs the message status and then retrieves the page content from the corresponding message body.<br>
• The client program can be executed using command line, with the following syntax, <br>
```
% python client.py server_host server_port file_name directory
e.g.
% python client.py localhost 9089 projeto.pdf .
```
<p>(a) server_host: The IP address or name of the server, e.g., 127.0.0.1 or localhost for the server running on the local machine. <br>
(b) server_port: The port on which the server is listening to connections from clients. <br>
(c) file_name: The name of the requested file. <br>
(d) directory: The directory to save the requested files. <br>

### Specifications - Connection Parameters
You should be able to extract the following information from the connection objects,<br>
(a) Calculate and Display RTT for the client request. <br>
(b) Print the relevant server details on client side. The examples could be Host Name of the server, socket family, socket type, protocol, timeout and get peer name. <br>
(c) Print the relevant client details on server side. The examples could be Host Name of the client, socket family, socket type, protocol, timeout and get peer name. <br>

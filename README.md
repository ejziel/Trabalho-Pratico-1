# Practical Work 1 - Client/Server file transfer via Sockets

Name : Ejziel Santos <br>
Email : ejziels@gmail.com <br>
Affiliation : Federal University of Recôncavo da Bahia (UFRB) <br>

## Project Description : <br>

(A) A multi-threaded server which interacts with any standard Clients. The server and client communicate using a TCP/IP socket. <br>
(B) A single-threaded client that communicates with the server asking for a file, and downloads it. <br>
(C) The essential parameters of the connection are displayed both on the client and on the server. <br>

### Specifications - Server

The server being multi-threaded, handles multiple requests concurrently. The main thread ( server ), listens to a specified port like the standard port for HTTP (8080). Upon receiving a HTTP request, the server sets up a TCP connection to the requesting client and serves the request in a separate thread using a new port. After sending the response back to the client, it closes the connection. The server is assumed to work with HTTP GET messages. If the requested file exists at the server, it responds with a “HTTP/1.1 200 OK” together with the requested page to the client, otherwise it sends a corresponding error message, “HTTP/1.1 404 Not Found” or “HTTP/1.1 400 Bad Request”. <br>
• If running the server program using command line, the syntax should be : <br>
<p align="center"> server_code_name \<port_number>

### Specifications - Client

The client should be able to initiate a connection to the server, via a socket and request any page on the server. Upon receipt of the response message from the server, the client extracts and displays/logs the message status and then retrieves the page content from the corresponding message body.<br>
• The client program can be executed using command line, with the following syntax, <br>
<p align="center"> client_code \<server_IP address>\<port_no>\<requested_file_name> <br> 
<p>(a) Server_IPaddress: The IP address or name of the Web server, e.g., 127.0.0.1 or localhost for the server running on the local machine. <br>
(b) port_no: The port on which the server is listening to contnections from clients. If the port number is not entered, the default port 8080 should be used. <br>
(c) requested_file_name: The name of the requested file, which may include the path to the file. <br>

### Specifications - Connection Parameters
You should be able to extract the following information from the connection objects,<br>
(a) Calculate and Display RTT for the client request. <br>
(b) Print the relevant server details on client side. The examples could be Host Name of the server, socket family, socket type, protocol, timeout and get peer name. <br>
(c) Print the relevant client details on server side. The examples could be Host Name of the client, socket family, socket type, protocol, timeout and get peer name. <br>

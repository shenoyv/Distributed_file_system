import socket
import threadpool
import os
import file_server
# global threadpool for server
server_thread_pool = threadpool.ThreadPool(500)

port_number = 1024

ip_addr = socket.gethostbyname(socket.gethostname())

file_manager = file_server.FileSystemManager('FileSystemDir')

def create_server_socket():
    # create socket  and initialise to localhost:8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_addr = ('127.0.0.1', port_number)
    print("starting server on %s port %s" % sock_addr)
    # bind socket to server address and wait for incoming connections4
    sock.bind(sock_addr)
    sock.listen(1)




def kill_service(connection):
    # Kill service
    response = "Killing Service"
    connection.sendall("%s" % response.encode())
    connection.close()
    os._exit(0)


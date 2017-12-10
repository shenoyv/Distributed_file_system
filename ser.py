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

def ls(connection, client_id, seperate_data):
    response = ""
    if len(seperate_data) == 1:
        response = file_manager.list_directory_contents(client_id)
        connection.sendall(response.encode())
    elif len(seperate_data) == 2:
        response = file_manager.list_directory_contents(client_id, seperate_data[1])
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def cd(connection, seperate_data, client_id):
    if len(seperate_data) == 2:
        resp = file_manager.change_directory(seperate_data[1], client_id)
        response = ""
        if resp == 0:
            response = "changed directory to %s" % seperate_data[1]
        elif resp == 1:
            response = "directory %s doesn't exist" % seperate_data[1]
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)




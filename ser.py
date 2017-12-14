import socket
import threadpool
import os
import file_server
# global threadpool for server
server_thread = threadpool.ThreadPool(500)

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

    while True:

        connection, client_address = sock.accept()
        server_thread.add_task(
             start_client_interaction,
             connection,
             client_addr
         )

 def start_client_interaction(connection, client_addr):
        try:
            # A client id is generated, that is associated with this client
            client_id = file_manager.add_client(connection)
            while True:
                data = connection.recv(1024).decode()
                seperate_data = seperate_input_data(data)

                if data == "KILL_SERVICE":
                    kill_service(connection)
                elif seperate_data[0] == "ls":
                    ls(connection, client_id, seperate_data)
                elif seperate_data[0] == "cd":
                    cd(connection, seperate_data, client_id)
                elif seperate_data[0] == "up":
                    up(connection, seperate_data, client_id)
                elif seperate_data[0] == "read":
                    read(connection, seperate_data, client_id)
                elif seperate_data[0] == "write":
                    write(connection, seperate_data, client_id)
                elif seperate_data[0] == "delete":
                    delete(connection, split_data, client_id)
                elif seperate_data[0] == "lock":
                    break;
                elif seperate_data[0] == "release":
                    break;
                elif seperate_data[0] == "mkdir":
                    break;
                elif seperate_data[0] == "rmdir":
                    break;
                elif seperate_data[0] == "pwd":
                    break;
                elif seperate_data[0] == "exit":
                    break;
                else:
                    error_response(connection, 1)
        except:
            error_response(connection, 0)
            connection.close()




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
        if resp  == 0:
            response = "changed directory to %s" % seperate_data[1]
        elif resp == 1:
            response = "directory %s doesn't exist" % seperate_data[1]
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)
def up(connection, split_data, client_id):
    if len(split_data) == 1:
        file_manager.move_up_directory(client_id)
    else:
        error_response(connection, 1)

def read(connection, split_data, client_id):
    if len(split_data) == 2:
        response = file_manager.read_item(client_id, split_data[1])
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def write(connection, split_data, client_id):
    response = ""
    if len(split_data) == 2:
        res = file_manager.write_item(client_id, split_data[1], "")
        if res == 0:
            response = "write process is successfull"
        elif res == 1:
            response = "file locked"
        elif res == 2:
            response = "cannot write to a directory file"
        connection.sendall(response.encode())
    elif len(split_data) == 3:
        res = file_manager.write_item(client_id, split_data[1], split_data[2])
        if res == 0:
            response = "write process is successfull"
        elif res == 1:
            response = "file locked"
        elif res == 2:
            response = "cannot write to a directory file"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)


def exit(connection, split_data, client_id):
    if len(split_data) == 1:
        file_manager.disconnect_client(connection, client_id)
    else:
        error_response(connection, 1)

def error_response(connection, error_code):
    response = ""
    if error_code == 0:
        response = "server error"
    if error_code == 1:
        response = "unrecognised command"
    connection.sendall(response.encode())

def seperate_input_data(input_data):
    seperated_data = input_data.split('////')
    return seperated_data

if __name__ == '__main__':
    create_server_socket()

    server_thread.wait_completion()




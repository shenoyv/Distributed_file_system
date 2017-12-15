import socket
import threadpool
import os
import file_server
# global threadpool for server
server_thread = threadpool.ThreadPool(500)

port_number = 8018

ip_addr = socket.gethostbyname(socket.gethostname())

file_manager = file_server.FileSystemManager('files')

def create_server_socket():
    #create socket  and initialise to localhost:8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_addr = ('127.0.0.1', port_number)
    print("starting server on %s port %s" % sock_addr)
    #bind socket to server address and wait for incoming connections4
    sock.bind(sock_addr)
    sock.listen(1)

    while True:
        connection, client_addr = sock.accept()
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
                     delete(connection, seperate_data, client_id)
                elif seperate_data[0] == "lock":
                    lock(connection, seperate_data, client_id)
                elif seperate_data[0] == "release":
                    release(connection, seperate_data, client_id)
                elif seperate_data[0] == "mkdir":
                    mkdir(connection, seperate_data, client_id)
                elif seperate_data[0] == "rmdir":
                    rmdir(connection, seperate_data, client_id)
                elif seperate_data[0] == "pwd":
                    pwd(connection, seperate_data, client_id)
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
def delete(connection, split_data, client_id):
    if len(split_data) == 2:
        res = file_manager.delete_file(client_id, split_data[1])
        response = ""
        if res == 0:
            response = "delete successfull"
        elif res == 1:
            response = "file locked"
        elif res == 2:
            response = "use rmdir to delete a directory"
        elif res == 3:
            response = "file doesn't exist"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)
def lock(connection, split_data, client_id):
    if len(split_data) == 2:
        client = file_manager.get_active_client(client_id)
        res = file_manager.lock_item(client, split_data[1])
        response = ""
        if res == 0:
            response = "file locked"
        elif res == 1:
            response = "file already locked"
        elif res == 2:
            response = "file doesn't exist"
        elif res == 3:
            response = "locking directories is not supported"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def release(connection, split_data, client_id):
    if len(split_data) == 2:
        client = file_manager.get_active_client(client_id)
        res = file_manager.release_item(client, split_data[1])
        if res == 0:
            response = split_data[1] + " released"
        elif res == -1:
            response = "you do not hold the lock for %s" % split_data[1]
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def mkdir(connection, split_data, client_id):
    if len(split_data) == 2:
        response = ""
        res = file_manager.make_directory(client_id, split_data[1])
        if res == 0:
            response = "new directory %s created" % split_data[1]
        elif res == 1:
            response = "file of same name exists"
        elif res == 2:
            response = "directory of same name exists"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def rmdir(connection, split_data, client_id):
    if len(split_data) == 2:
        response = ""
        res = file_manager.remove_directory(client_id, split_data[1])
        if res == -1:
            response = "%s doesn't exist" % split_data[1]
        elif res == 0:
            response = "%s removed" % split_data[1]
        elif res == 1:
            response = "%s is a file" % split_data[1]
        elif res == 2:
            response = "directory has locked contents"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def pwd(connection, split_data, client_id):
    if len(split_data) == 1:
        response = file_manager.get_working_dir(client_id)
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





import socket
import threadpool
import time
import os
client_thread = threadpool.ThreadPool(5)
ip_addr = socket.gethostbyname(socket.gethostname())
port = 8018
cache_time = 2
cache_queue = []
response_var = ""
def connect():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_addr = (ip_addr, port)
    print("connecting to %s on port %s\n" % sock_addr)
    sock.connect(sock_addr)
    client_thread.add_task(
        server_res,
        sock
    )
    client_thread.add_task(
        cache_auto_update
    )

    while True:
        user_input = input()
        Input_mes = generate_message(user_input)
        cache_response = cache_interaction(sock, Input_mes)
        # if there is no cached response
        if cache_response == None:
            sock.send(Input_mes.encode())
            if Input_mes == "exit":
                os._exit(0)
        else:
            print(cache_response)

    sock.close()

def server_res(socket):
    global res_var
    while True:
        data = socket.recv(1024).decode()
        res_var = data
        if (data != None):
            # if reading cache item
            if(len(data.split("////")) == 2):
                data_seperate = data.split("//"
                                           "//")
                add_to_cache(data_seperate[0], data_seperate[1])
                print(data_seperate[1])
            else:
                print(data)

def generate_message(input):
    seperate_input = input.split(" ")
    if seperate_input[0] == "write":
        if len(seperate_input) != 2:
            print("command not found")
            return ""
        try:
            file = open(seperate_input[1])
            file_contents = file.read()
            return "%s////%s////%s" % (seperate_input[0], seperate_input[1], file_contents)
        except IOError:
            print("no such file found")
            return ""
    else:
        return '////'.join(seperate_input)



# searches the cache for an item
def cache_search(path):
    for item in cache_queue:
        if item[0] == path:
            return item[1]
    return None

# adds an item to the cache
def add_to_cache(path, contents):
    cache_queue.insert(0, (path, contents, 0))
    if len(cache_queue) > 5:
        cache_queue.pop()

# logs the contents of the cache
def cache_log():
    for item in cache_queue:
        print("%s\t%s\t%d" % (item))

def cache_interaction(connection, message):
        global res_var
        seperate_message = message.split("////")
        if len(seperate_message) == 2 and seperate_message[0] == "read":
            connection.send("pwd".encode())
            time.sleep(1)
            res_msg = res_var
            search_term = "%s%s" % (res_msg, seperate_message[1])
            ret_msg = cache_search(search_term)
            cache_log()
            print(search_term)
            return ret_msg
        return None

# function removes old items from cache
def cache_auto_update():
    global cache_queue
    while True:
        time.sleep(10)
        cache_queue_update = []
        for item in cache_queue:
            if item[2] < cache_time:
                new_cache_record = (item[0], item[1], item[2] + 1)
                cache_queue_update.append(new_cache_record)
        cache_queue = cache_queue_update

if __name__ == '__main__':
    # Main line for program
    # Create 20 tasks that send messages to the server
    connect()
    # wait for threads to complete before finishing program
    client_thread.wait_completion()




import socket
import threadpool
import time
import os
client_thread_pool = threadpool.ThreadPool(5)
ip_addr = socket.gethostbyname(socket.gethostname())
port = 8018
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_addr = (ip_addr, port)
print("connecting to %s on port %s\n" % sock_addr)
sock.connect(sock_addr)

        



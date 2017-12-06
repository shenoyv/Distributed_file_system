import socket
import threadpool
import time
import os

server_thread_pool = threadpool.ThreadPool(500)

port = 8018

ip_addr = socket.gethostbyname(socket.gethostname())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_addr = (ip_addr, port)
print("starting up on %s port %s" % sock_addr)
sock.bind(sock_addr)
sock.listen(1)
print(sock.accept())
while True:
    connection, client_addr = sock.accept()
    print(sock.accept())
    print("Connection from %s, %s\n" % connection, client_addr)

import sys
import select
import socket
import threading
import time
import random
class Client():
    command_list =["READ FILE","WRITE FILE","PWDIR","CHDIR","LS","QUIT"]

def __init__(self, add_rs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((host, port))
        #print(" connecting to %s:%s " %(host,port))
        self.sock.connect ((self.addr_s,8018))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while True:
           self.Input =raw_input(":")
           if any(x in self.message for x in self.command_list):
               pass
           else:
               print"command not found\n"
        s.sendall(self.Input)
        if self.message == "Quit":
            sys.exit()
        



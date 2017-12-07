import socket
import threadpool
import os


server_thread_pool = threadpool.ThreadPool(500)

port_number = 1024

 ip_addr\
     = socket.gethostbyname(socket.gethostname())

 file_system_manager = dfs_server_filesystem_model.FileSystemManager('FileSystemDir')

 def create_server_socket():


      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_address = ('127.0.0.1', port_number)
      print("starting up on %s port %s" % server_address)
     # bind socket to server address and wait for incoming connections4
      sock.bind(server_address)
      sock.listen(1)

     while True:

         connection, client_address = sock.accept()
        # print "Connection from %s, %s\n" % connection, client_address
         # Hand the client interaction off to a seperate thread
         server_thread_pool.add_task(
                start_client_interaction,
             connection,
          client_address
            )


  def start_client_interaction(connection, client_address):
      try:
         #A client id is generated, that is associated with this client
         client_id = file_system_manager.add_client(connection)
         while True:
             data = connection.recv(1024).decode()
             split_data = seperate_input_data(data)
             # Respond to the appropriate message
             if data == "KILL_SERVICE":
                 kill_service(connection)
             elif split_data[0] == "ls":
                 ls(connection, client_id, split_data)
             elif split_data[0] == "cd":
                 cd(connection, split_data, client_id)
             elif split_data[0] == "up":
                 up(connection, split_data, client_id)
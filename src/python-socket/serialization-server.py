from collections import OrderedDict
import pickle
import socket
import sys

import numpy as np
import lz4.frame

import data
import data_commu as commu

HOST = ''           # Socket is reachable by any address the machine happens to have
PORT = int(sys.argv[1])        # Port to listen on (non-privileged ports are > 1023)
test_size = int(sys.argv[2])
compression_flag = int(sys.argv[3])
num_loop = int(sys.argv[4])

# Data arrangement
data = data.generate_data(test_size)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen(5) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
    conn, addr = s.accept() #block and wait for an incoming connection
    print('Connected by {}'.format(addr))
    with conn: 
        #Reply to client: send a numpy array of 1000 characters
        commu.transmit_notcompressed(conn, data.data_pre)
        print("Successfully sent the small packet")
        #receive the ack from the client of receiving 1000 characters
        confirm = commu.receive(conn)
        if confirm != 1000:
	        sys.exit("Error: client do not receive all 1000 bytes data")
        for i in range(num_loop):
            #Reply to client: send a numpy array of size_of_data character
            if compression_flag == 0:
                commu.transmit_notcompressed(conn,data)
            else:
                commu.transmit_compressed(conn,data)
            print("Successfully sent all the data")
            #receive the ack from the client of receving test_size characters
            confirm = commu.receive(conn)
            if confirm != test_size:
                sys.exit(f"Error: client do not receive all {test_size} bytes data")
        #Send back a request for closing
        commu.transmit_notcompressed(conn, 0)
        

import socket
import sys
import pickle
import numpy as np
from collections import OrderedDict

HOST = ''           # Socket is reachable by any address the machine happens to have
PORT = int(sys.argv[1])        # Port to listen on (non-privileged ports are > 1023)
test_size = int(sys.argv[2])

#Initialization of data
data_pre = np.chararray(1000)
data_pre[:] = '0'
data = np.chararray(test_size)
data[:] = '1'

def transmit(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(obj)

def receive(sock):
    unpickler = pickle.Unpickler(sock.makefile(mode='rb'))
    return unpickler.load()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen(5) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
    conn, addr = s.accept() #block and wait for an incoming connection
    print('Connected by {}'.format(addr))
    with conn: 
        #Reply to client: send a numpy array of 1000 characters
        transmit(conn, data_pre)
        print("Successfully sent the small packet")
        #Receive the ack from the client of receiving 1000 characters
        confirm = receive(conn)
        if confirm != 1000:
            sys.exit("Error: client do not receive all 1000 bytes data")
        for i in range(3):
            #Reply to client: send a numpy array of size_of_data characters
            transmit(conn,data)
            print("Successfully sent all the data")
            #Receive the ack from the client of receving test_size characters
            confirm = receive(conn)
            if confirm != test_size:
                sys.exit("Error: client do not receive all {test_size} bytes data")
        #Send back a request for closing
        transmit(conn, 0)
        

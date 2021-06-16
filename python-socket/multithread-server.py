import socket
import sys
import pickle
import numpy as np
from collections import OrderedDict
import threading

HOST = ''           # Socket is reachable by any address the machine happens to have
PORT = int(sys.argv[1])        # Port to listen on (non-privileged ports are > 1023)
test_size = int(sys.argv[2])

# Data arrange
data_pre = np.chararray(1000)
data_pre[:] = '0'
#data = np.chararray(test_size)
#data[:] = '1'
data = OrderedDict({x: x*2 for x in range(test_size)})

def transmit(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(obj)

def receive(sock):
    unpickler = pickle.Unpickler(sock.makefile(mode='rb'))
    return unpickler.load()

def threaded(name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by socket no. {}, address {}'.format(name, addr))
        with conn:
            transmit(conn, data)
            print("Packet {num} successfully sent the formal data packets")
            confirm = receive(conn)
            if confirm != test_size:
                sys.exit('Error: client do not receive all {} bytes data'.format(test_size))
            

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen(1) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
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

        # Formal test
        # Create threads
            t1 = threading.Thread(target=threaded, args=(0,))
            t2 = threading.Thread(target=threaded, args=(1,))
            t3 = threading.Thread(target=threaded, args=(2,))

        #Start threads
            t1.start()
            t2.start()
            t3.start()

        # Wait until all threads finish their jobs
            t1.join()
            t2.join()
            t3.join()

        # Send back a request for closing
        transmit(conn, 0)
        

import socket
import sys
import pickle
import time
import lz4.frame
from timeit import default_timer as timer

#HOST = '127.0.0.1'  # local host
HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = int(sys.argv[1])        # The port used by the server
target_size = int(sys.argv[2])
compression_flag = int(sys.argv[3])
num_loop = int(sys.argv[4])

def transmit(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(obj)

def receive(sock):
    unpickler = pickle.Unpickler(sock.makefile(mode='rb'))
    return unpickler.load()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while s.connect_ex((HOST,PORT)) != 0:
        time.sleep(2)
    print("Connected")
    
    #Receive a small packet from the server
    data = receive(s)
    print("Small packet received: %d bytes" %(len(data)))
    #Send out an ack to request the next transmission
    transmit(s, len(data))
    start = timer()
    for i in range(num_loop):
        #Receive formal data from the server
        data = receive(s)
        if compression_flag == 1:
            data=pickle.loads(lz4.frame.decompress(data))
        print("Large packet received: %d bytes" %(len(data)))
        #Send ack to server
        transmit(s, len(data))
    receive(s)
    end = timer()
    print("The elapsed time is %f" %(end - start))
    print(end-start)

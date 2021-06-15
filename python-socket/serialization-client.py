import socket
import sys
import pickle
from timeit import default_timer as timer

#HOST = '127.0.0.1'  # local host
HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = int(sys.argv[1])        # The port used by the server
target_size = int(sys.argv[2])

def transmit(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(obj)

def receive(sock):
    unpickler = pickle.Unpickler(sock.makefile(mode='rb'))
    return unpickler.load()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected")
    
    #Receive a small packet from the server
    data = receive(s)
    print("Small packet received: %d bytes" %(len(data)))
    #Send out an ack to request the next transmission
    transmit(s, len(data))
    start = timer()
    for i in range(3):
        #Receive formal data from the server
        data = receive(s)
        print("Large packet received: %d bytes" %(len(data)))
        #Send ack to server
        transmit(s, len(data))
    receive(s)
    end = timer()
    print("The elapsed time is %f" %(end - start))

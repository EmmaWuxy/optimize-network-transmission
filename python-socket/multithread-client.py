import sys
import socket
from timeit import default_timer as timer
from _thread import *
import threading
import pickle

#HOST = '127.0.0.1'  # local host
HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = int(sys.argv[1])    # The port used by the server
test_size = int(sys.argv[2])

def transmit(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(obj)

def receive(sock):
    unpickler = pickle.Unpickler(sock.makefile(mode='rb'))
    return unpickler.load()

def threaded(name, p):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, p))
        print(f"Thread {name} connected")
        data = receive(s)
        size = len(data)
        print(f"Thread {name} successfully receive {size} bytes")
        transmit(s, size)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected")

    # Receive a small packet from the server
    data = receive(s)
    print("Small packet received, in bytes:", len(data))
    #transmit(s, len(data))

    # Receive formal data from the server
    start = timer()

    # Create threads0
    t1 = threading.Thread(target=threaded,args=(1,PORT+1))
    t2 = threading.Thread(target=threaded,args=(2,PORT+2))
    t3 = threading.Thread(target=threaded,args=(3,PORT+3))

    # Start threads
    t1.start()
    t2.start()
    t3.start()

    # Wait untill threads finish their job
    t1.join()
    t2.join()
    t3.join()

    # Receive server's request for closing
    receive(s)
    end = timer()
    print("The elapsed time is %f" %(end - start))
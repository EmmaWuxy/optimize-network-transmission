import sys
import socket
import time
from timeit import default_timer as timer
from _thread import *
import threading
import pickle
from collections import OrderedDict
import lz4.frame

#HOST = '127.0.0.1'  # local host
HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = int(sys.argv[1])    # The port used by the server
test_size = int(sys.argv[2])
compression_flag = int(sys.argv[3])
num_thread = int(sys.argv[4])

threads = OrderedDict()

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
        if compression_flag == 1:
            data=pickle.loads(lz4.frame.decompress(data))
        size = len(data)
        print(f"Thread {name} successfully receive {size} bytes")
        transmit(s, size)

# Create threads
for i in range(1, num_thread+1):
    threads[i] = threading.Thread(target=threaded, args=(i, PORT+i))    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while s.connect_ex((HOST, PORT)) != 0:
        time.sleep(2)
    print("Connected")

    # Receive a small packet from the server
    data = receive(s)
    print("Small packet received, in bytes:", len(data))
    #transmit(s, len(data))

    # Receive formal data from the server
    start = timer()

    # Start threads
    for name, thread in threads:
        thread.start()
        
    # Wait until all threads finish their jobs
    for name, thread in threads:
        thread.join()

    # Receive server's request for closing
    receive(s)
    end = timer()
    print(f"The elapsed time is {end-start} seconds")
    print(end-start)

from collections import OrderedDict
import lz4.frame
import socket
import sys
import pickle
import time
import threading
from timeit import default_timer as timer

import data_commu as commu
from parameter import HOST

PORT = int(sys.argv[1])        # The port used by the server
compression_flag = int(sys.argv[2])

threads = OrderedDict()

def threaded(name, p):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,p))
        print(f"Thread {name} connected")

        #Receive column content
        data = commu.receive(s)
        if compression_flag == 1:
            data=pickle.loads(lz4.frame.decompress(data))
        print(f"Content received")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while s.connect_ex((HOST,PORT)) != 0:
        time.sleep(2)
    print("Connected")
    
    #Receive total row number from server
    thread_num = commu.receive(s)
    print(f"Total threads going to be received: {thread_num}")

    #Create threads
    for i in range(1, thread_num+1):
        threads[i] = threading.Thread(target=threaded, args=(i, PORT+i))

    start = timer()

    for name, thread in threads.items():
        thread.start()
    
    for name, thread in threads.items():
        thread.join()

    end = timer()

    print("The elapsed time is %f" %(end - start))
    print(end-start)

    #Send request for closing to server
    commu.transmit_notcompressed(s, -1)
    
    
    

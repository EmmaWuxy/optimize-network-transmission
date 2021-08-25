import socket
import sys
import pickle
import time
import lz4.frame
from timeit import default_timer as timer

import data_commu as commu
from parameter import HOST

PORT = int(sys.argv[1])        # The port used by the server
target_size = int(sys.argv[2])
compression_flag = int(sys.argv[3])
num_loop = int(sys.argv[4])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while s.connect_ex((HOST,PORT)) != 0:
        time.sleep(2)
    print("Connected")
    
    #Receive a small packet from the server
    data = commu.receive(s)
    print("Small packet received: %d bytes" %(len(data)))
    #Send out an ack to request the next transmission
    commu.transmit_notcompressed(s, len(data))

    start = timer()
    for i in range(num_loop):
        #Receive formal data from the server
        data = commu.receive(s)
        if compression_flag == 1:
            data=pickle.loads(lz4.frame.decompress(data))
        print("Large packet received: %d bytes" %(len(data)))
        #Send ack to server
        commu.transmit_notcompressed(s, len(data))
    commu.receive(s)
    end = timer()
    
    print("The elapsed time is %f" %(end - start))
    print(end-start)

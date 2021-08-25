import socket
import sys
import pickle
import time
import lz4.frame
from timeit import default_timer as timer

import data_commu as commu
from parameter import HOST

PORT = int(sys.argv[1])        # The port used by the server
compression_flag = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while s.connect_ex((HOST,PORT)) != 0:
        time.sleep(2)
    print("Connected")
    
    #Receive total column number from server
    col_num = commu.receive(s)
    print(f"Total columnn list received: {col_num}")

    start = timer()
    for col in range(col_num):
        #Request column content from the server
        commu.transmit_notcompressed(s, col)

        #Receive column content
        data = commu.receive(s)
        if compression_flag == 1:
            data=pickle.loads(lz4.frame.decompress(data))
        print(f"Column content received")

    #Send request for closing to server
    end = timer()

    print("The elapsed time is %f" %(end - start))
    print(end-start)

    commu.transmit_notcompressed(s, -1)
    
    
    

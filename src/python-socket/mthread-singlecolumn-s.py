from collections import OrderedDict
import pandas as pd
import pickle
import threading
import socket
import sys

import data_commu as commu

HOST = ''                 # Socket is reachable by any address the machine happens to have
PORT = int(sys.argv[1])   # Port to listen on (non-privileged ports are > 1023)
file_name = sys.argv[2]   # csv file name as a string
compression_flag = int(sys.argv[3])
thread_num = int(sys.argv[4])
col = int(sys.argv[5])    # Starts from 0

data = pd.read_table(filepath_or_buffer="/scratch/jdsilv2/data/tpch/sf01/" + file_name, sep='|')
row_num = len(data)
print(f"The column contains {row_num} rows.")

col_num = len(list(data.columns))
print(f"The file contains {col_num} columns.")

threads = OrderedDict()

#Calculate the offset
off_set = round(row_num/thread_num)

def threaded(name, p, part):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, p))
        s.listen(5)
        conn, addr = s.accept()
        print('Connected by socket no.{}, address {}'.format(name, addr))
        with conn:
            #receive the part number to be retrieved from the column
            #part = commu.receive(conn)
            #Reply to client: send back the part of the column, part counts starting from 1
            if part == thread_num:
                print(data.iloc[(part-1)*off_set,col])
                if compression_flag == 0:
                    commu.transmit_notcompressed(conn, data.iloc[(part-1)*off_set:,col])
                else:
                    commu.transmit_compressed(conn, data.iloc[(part-1)*off_set:,col])
            else:
                if compression_flag == 0:
                    commu.transmit_notcompressed(conn, data.iloc[(part-1)*off_set : part*off_set, col])
                else:
                    commu.transmit_compressed(conn, data.iloc[(part-1)*off_set : part*off_set, col])
            print(f"Thread {name} successfully sent the content of column {col} part {part}")

#Create threads
for i in range(1, thread_num+1):
    threads[i] = threading.Thread(target=threaded, args=(i, PORT+i, i))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen(5) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
    conn, addr = s.accept() #block and wait for an incoming connection
    print('Connected by {}'.format(addr))
    with conn: 
        #Reply to client: send the thread number to the client
        commu.transmit_notcompressed(conn, thread_num)
        print("Successfully sent the thread number")

        # Start threads
        for name, thread in threads.items():
            thread.start()

        #Wait until all threads finish their jobs
        for name, thread in threads.items():
            thread.join()

        if commu.receive(conn) != -1:
            sys.exit("Error: data transmission did not complete.")

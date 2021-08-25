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
compression_flag = int(sys.argv[3])	#1 for lz4 compression, 0 for no compression 
thread_num = int(sys.argv[4])	# Number of threads to slice the last column into, creating one thread for each slice

data = pd.read_table(filepath_or_buffer="/scratch/jdsilv2/data/tpch/sf01/" + file_name, sep='|')
col_num = len(list(data.columns))-1 # read_table is counting the column after the '|' as the last column, but the last column in testing tables are empty columns, we hence don't take the empty column into account
print(f"The file contains {col_num} columns.")
row_num = len(data)
print(f"The column contains {row_num} rows.")

threads = OrderedDict()

def threaded(name, p, col, content):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, p))
        s.listen(5)
        conn, addr = s.accept()
        print('Connected by socket no.{}, address {}'.format(name, addr))
        with conn:
            #receive the column name to be retrieved
            #col = commu.receive(conn)
            #Reply to client: send back the column content
            if compression_flag == 0:
                commu.transmit_notcompressed(conn, content)
            else:
                commu.transmit_compressed(conn, content)
            print(f"Thread {name} successfully sent the content of column {col}")

#Calculate the offset
off_set = round(row_num/thread_num)

#Create threads
for i in range(1, col_num+thread_num):
    if i == col_num+thread_num-1: #Last thread to send
         threads[i] = threading.Thread(target=threaded, args=(i, PORT+i, col_num-1, data.iloc[(i-col_num)*off_set:, col_num-1]))
    if i >= col_num:
        threads[i] = threading.Thread(target=threaded, args=(i, PORT+i, col_num-1, data.iloc[(i-col_num)*off_set:(i-col_num+1)*off_set, col_num-1]))
    else:
        threads[i] = threading.Thread(target=threaded, args=(i, PORT+i, i-1, data.iloc[:, i-1]))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen(5) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
    conn, addr = s.accept() #block and wait for an incoming connection
    print('Connected by {}'.format(addr))
    with conn: 
        #Reply to client: send the thread number to the client
        commu.transmit_notcompressed(conn, col_num+thread_num-1)
        print("Successfully sent the thread number")

        # Start threads
        for name, thread in threads.items():
            thread.start()

        #Wait until all threads finish their jobs
        for name, thread in threads.items():
            thread.join()

        if commu.receive(conn) != -1:
            sys.exit("Error: data transmission did not complete.")
import pandas as pd
import pickle
import socket
import sys

import data_commu as commu

HOST = ''                 # Socket is reachable by any address the machine happens to have
PORT = int(sys.argv[1])   # Port to listen on (non-privileged ports are > 1023)
file_name = sys.argv[2]   # csv file name as a string
compression_flag = int(sys.argv[3])

data = pd.read_table(filepath_or_buffer="/scratch/jdsilv2/data/tpch/sf01/" + file_name, sep='|')
col_num = len(list(data.columns))
print(f"The file contains {col_num} columns.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen(5) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
    conn, addr = s.accept() #block and wait for an incoming connection
    print('Connected by {}'.format(addr))
    with conn: 
        #Reply to client: send the colume number to the client
        commu.transmit_notcompressed(conn, col_num)
        print("Successfully sent the column number")

        while True:
            col = commu.receive(conn) #receive the column name to be retrieved from the client
            if col == -1:
                break
            #Reply to client: send back the column content
            if compression_flag == 0:
                commu.transmit_notcompressed(conn, data.iloc[:,col])
            else:
                commu.transmit_compressed(conn, data.iloc[:,col])
            print(f"Successfully sent the content of column {col}")

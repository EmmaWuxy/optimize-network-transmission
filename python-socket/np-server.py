import socket
import numpy as np

#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
HOST = ''           # Socket is reachable by any address the machine happens to have
PORT = 60000        # Port to listen on (non-privileged ports are > 1023)
size_of_data = 10000

#Initialization of data
data_pre = np.chararray(1000)
data_pre[:] = '0'
data = np.chararray(size_of_data)
data[:] = '1'

#Socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
s.listen(5) #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
conn, addr = s.accept() #block and wait for an incoming connection
print('Connected by', addr)


#Reply to client: send  a numpy array of 1000 characters
conn.sendall(data_pre.tobytes())
print("Successfully sent the small packet")

#Reply to client: send a numpy array of size_of_data characters
conn.sendall(data.tobytes())
print("Successfully sent all the data\n")

#Socket close
conn.close()
s.close()
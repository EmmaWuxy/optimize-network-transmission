
import socket
from timeit import default_timer as timer

HOST = '127.0.0.1'  # local host
#HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = 60000        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connected\n")

#Receive a small packet from the server
data = s.recv(4096)
print("Small packet received\n")

#Receive formal data from the server
start = timer()

while True:
    data = s.recv(4096)
    if not data:
        break
print("All data received\n")

end = timer()
print("The elapsed time in seconds:", end - start)

s.close()
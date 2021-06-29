import socket
import sys
from timeit import default_timer as timer

#HOST = '127.0.0.1'  # local host
HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = 60000        # The port used by the server
target_size = int(sys.argv[1])

size_count = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connected")

#Receive a small packet from the server
data = s.recv(4096)
print("Small packet received: %d bytes" %(len(data)))

#Receive formal data from the server
start = timer()

while True:
    data = s.recv(4096)
    size_count += len(data)
    if not data:
        break

if size_count != target_size:
    print("Receive %d bytes data" %(size_count))
    sys.exit("Error: do not receive all data")
print("All data received: %d bytes" % (size_count))

end = timer()
print("The elapsed time is %f" %(end - start))

s.close()

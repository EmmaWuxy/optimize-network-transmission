
import socket
from timeit import default_timer as timer
from _thread import *
import threading

#HOST = '127.0.0.1'  # local host
HOST = '132.206.51.95' # IP of mimi
#HOST = '10.0.0.20' # IP of Emma
PORT = 60000        # The port used by the server
size = 0            # Accumulate bytes received

def threaded(s, lock):
    while True:
        data = s.recv(4096)
        global size
        size += len(data)
        if not data:
            break


def Main():
    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected\n")

    #Receive a small packet from the server
    data = s.recv(4096)
    print("Small packet received, in bytes:", len(data))

    #Receive formal data from the server
    start = timer()
    lock = threading.Lock()

    #Create a lock

    #Create threads
    t1 = threading.Thread(target=threaded, args=(s,))
    t2 = threading.Thread(target=threaded, args=(s,))
    t3 = threading.Thread(target=threaded, args=(s,))

    #Start threads
    t1.start()
    t2.start()
    t3.start()

    #Wait untill threads finish their job
    t1.join()
    t2.join()
    t3.join()

    print("All data received, in bytes:", size)

    end = timer()
    print("The elapsed time in seconds:", end - start)

    s.close()
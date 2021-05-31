from timeit import default_timer as timer
import time

 #Receive formal data from the server
start = timer()

time.sleep(2.4)

end = timer()
print("The elapsed time inseconds: ", end - start)
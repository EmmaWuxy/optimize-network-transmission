from timeit import default_timer as timer
import time
import numpy as np
import sys

 #Receive formal data from the server
data_pre = np.chararray(1000)
data_pre[:] = '0'

print("size in bytes: ", sys.getsizeof(data_pre.tobytes()))

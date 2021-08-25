import numpy as np
data_pre = np.chararray(1000)
data_pre[:] = '0'

def generate_data(test_size):
    prng=np.random.RandomState(9999)
    return np.random.randint(0, 100, test_size, dtype='int64')
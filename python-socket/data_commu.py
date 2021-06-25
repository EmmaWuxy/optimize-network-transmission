import pickle
import lz4.frame
def transmit_notcompressed(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(obj)

def transmit_compressed(sock, obj):
    pickler = pickle.Pickler(sock.makefile(mode='wb'))
    pickler.dump(lz4.frame.compress(pickle.dumps(obj)))

def receive(sock):
    unpickler = pickle.Unpickler(sock.makefile(mode='rb'))
    return unpickler.load()
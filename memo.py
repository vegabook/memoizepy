from __future__ import print_function

import numpy as np
import mmh3                     # fast hashing library
import msgpack                  # fast serializer 
import msgpack_numpy as m       # extends msgpack to Numpy: pip install msgpack-numpy
from datetime import datetime   # timing
from rx import Observable

m.patch()                       # patch msgpack to be able to do ndarrays

def serialize(x):
    return msgpack.packb(x)


def hash(x):
    return str(mmh3.hash128(serialize(x)))


store_dict = {}


def memoize(func):

    def wrapper(*args, **kwargs):
        func_name = str(func).split()[1] # name only, not address
        signature = (func_name, args, kwargs) 
        sig_hash = hash(signature)
        if sig_hash in store_dict:
            return store_dict[sig_hash]
        else:
            func_val = func(*args, **kwargs)
            store_dict[sig_hash] = func_val
            return func_val

    return wrapper


@memoize
def longrun_eig(mtrx):
    """ takes a matrix, returns eigenvalue sum """
    eigs = np.linalg.eig(mtrx)[0]
    return sum(eigs)

@memoize
def primes_between(a, b):
    primes = []
    for num in range(a, b):
        if all(num % i != 0 for i in range(2, num)):
            primes.append(num)
    return(primes)


adim = 500
arrays = [np.random.rand(adim * adim).reshape(adim, adim) for x in range(5)]
print("longrun_eig not memoized:")
now_time = datetime.utcnow()
Observable.from_(arrays).map(longrun_eig).subscribe(print)
print("time taken {}".format(datetime.utcnow() - now_time))
print()
print("longrun_eig memoized:")
now_time = datetime.utcnow()
Observable.from_(arrays).map(longrun_eig).subscribe(print)
print("time taken {}".format(datetime.utcnow() - now_time))

print()
test_ranges = [(100, 200), (200, 1000), (1000, 5000), (5000, 15000)]
print("primes_between not memoized:")
now_time = datetime.utcnow()
Observable.from_(test_ranges).map(lambda x: primes_between(*x)).map(len).subscribe(print)
print("time taken {}".format(datetime.utcnow() - now_time))
print()
print("primes_between memoized:")
now_time = datetime.utcnow()
Observable.from_(test_ranges).map(lambda x: primes_between(*x)).map(len).subscribe(print)
print("time taken {}".format(datetime.utcnow() - now_time))

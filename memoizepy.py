from __future__ import print_function

import numpy as np
import mmh3                     # fast hashing library
import msgpack                  # fast serializer 
import msgpack_numpy as m       # extends msgpack to Numpy: pip install msgpack-numpy
from datetime import datetime   # timing
from rx import Observable
from concurrent.futures import ProcessPoolExecutor
from functools import wraps
import redis
import random

m.patch()                       # patch msgpack to be able to do ndarrays
r = redis.Redis()

def serialize(x):
    return msgpack.packb(x)


def hash(x):
    return str(mmh3.hash128(serialize(x)))


def store(hash, data):
    r.set(hash, data)


def get(hash):
    return r.get(hash)


def memoize(func):
    """ decorator which remembers funcname, arguments, and return values
        and returns saved values when available """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = str(func).split()[1] # name only, not address
        signature = (func_name, args, kwargs) 
        sig_hash = hash(signature)
        stored_res = get(sig_hash)
        if stored_res: 
            return stored_res
        else:
            func_val = func(*args, **kwargs)
            store(sig_hash, func_val)
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
    return(len(primes))

def testspeed(num_processes = 6, eigruns = 6):
    adim = 500
    num_processes = 6
    arrays = [np.random.rand(adim * adim).reshape(adim, adim) for _ in range(eigruns)]
    print("longrun_eig not memoized:")
    now_time = datetime.utcnow()
    with ProcessPoolExecutor(num_processes) as executor:
        Observable.from_(arrays) \
            .flat_map(lambda s: executor.submit(longrun_eig, s)) \
            .subscribe(print)
    print("time taken {}".format(datetime.utcnow() - now_time))
    print()
    print("longrun_eig memoized:")
    now_time = datetime.utcnow()
    Observable.from_(arrays) \
        .map(longrun_eig) \
        .subscribe(print)
    print("time taken {}".format(datetime.utcnow() - now_time))
    print()
    test_ranges = [(random.randint(1, 5000), random.randint(5001, 15000)) for _ in range(eigruns)]
    print("primes_between not memoized:")
    now_time = datetime.utcnow()
    with ProcessPoolExecutor(num_processes) as executor:
        Observable.from_(test_ranges) \
            .flat_map(lambda x: executor.submit(primes_between, *x)) \
            .subscribe(print)
    print("time taken {}".format(datetime.utcnow() - now_time))
    print()
    print("primes_between memoized:")
    now_time = datetime.utcnow()
    Observable.from_(test_ranges) \
        .map(lambda x: primes_between(*x)) \
        .subscribe(print)
    print("time taken {}".format(datetime.utcnow() - now_time))

if __name__ == "__main__":
    testspeed()

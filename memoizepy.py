from __future__ import print_function

import mmh3                     # fast hashing library
import msgpack                  # fast serializer 
import msgpack_numpy as m       # extends msgpack to Numpy: pip install msgpack-numpy
from functools import wraps
import redis

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



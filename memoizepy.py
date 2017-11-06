from __future__ import print_function

# Memoizer for python pure functions using Redis
# Usage: decorate function to memoize using @memoize
# Multiprocessing capable
# relies on Redis on localhost. Change appropriately
# For other data stores, change store and get functions appropriately

import mmh3                     # fast hashing library
from functools import wraps     # multiprocessing pool-safe decorators
import redis
try: 
    import cPickle as pickle
except ImportError: 
    import pickle

r = redis.Redis(host = "localhost", port = 6379)


def hash(x):
    return mmh3.hash128(pickle.dumps(x))


def store(hash, data):
    return r.set(hash, pickle.dumps(data))


def get(hash):
    pickled = r.get(hash)
    if pickled is None:
        return None
    else: 
        return pickle.loads(pickled)


def memoize(func):
    """ decorator which remembers funcname, arguments, and return values
        and returns saved values when available """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = str(func).split()[1] # name only, not address
        signature = (func_name, args, kwargs) 
        sig_hash = hash(signature)
        stored_res = get(sig_hash)
        if stored_res is not None:       # np and pd safe
            return stored_res
        else:
            func_val = func(*args, **kwargs)
            store(sig_hash, func_val)
            return func_val

    return wrapper



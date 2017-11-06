## memoizepy

Use to memoize a function using Redis. 

This is useful when you may rerun a long-running function many times. It will cache the value the first time, and return the cached value on subsequent runs with the same arguments and the same function names. 

It uses a 128-bit hash of function name, and function arguments. 

Note named args in a different order are considered different runs so will not cache-map to one another. 

Relies on Redis on default port and localhost. This can be changed if desired by updating the get and store functions. 

This code is multiprocessing pool aware as the decorated function is pickleable thanks to functools. 

Works on Numpy and Pandas.

Works on 2.7 and 3.x. Be careful to ensure a fast pickle is installed, that's cPickle. Usually 3.x std lib pickle is fast by default.

## usage:
```
from memoizepy import memoize
import numpy as np

@memoize
def some_fun_to_memoize(x, y, z):
    return x + y + z

```

There are some long-running really numerically intensive decorated functions in memoizetest.py for your perusal, namely longrun_eig and primes_between. 

run from command line python memoizepy.py for a speed test

if you wish to use something other than redis, change the store and get functions appropriately

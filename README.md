## memoizepy

use to memoize a function using Redis. 
Relies on Redis on default port and localhost. 
Works on Numpy and Pandas.

## usage:
```
from memoizepy import memoize
@memoize
def some_fun_to_memoize(x, y, z):
    return sum(x, y, z)
```

run from command line python memoizepy.py for a speed test

if you wish to use something other than redis, change the store and get functions appropriately

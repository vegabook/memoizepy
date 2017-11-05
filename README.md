## memoizepy

use to memoize a function using Redis. 
Experimental for now. 
Relies on Redis on default port and localhost
## usage:
```
from memoizepy import memoize
@memoize
def some_fun_to_memoize(x, y, z):
    return sum(x, y, z)
```

run from command line python memoizepy.py for a speed test

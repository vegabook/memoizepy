# memoizepy

use to memoize a function using Redis. 
Experimental for now. 
Relies on Redis on default port and localhost
# usage:
```
import memoizepy
@memoize
def sum_fun_to_memoize(x, y, z):
    sum(x, y, z)
```

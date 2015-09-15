JavaScript Backend Regression Tests - set
-----------------------------
the following tests compiled, and run in nodejs without any errors
* [issubset.py](set/issubset.py)

input:
------
```python
from runtime import *
"""get/set remote attributes"""

def main():
	x = set([1,2,3])
	y = set([1,2,3,4])

	assert( x.issubset(y)==True )
	assert( y.issubset(x)==False )

	
main()
```
output:
------
```javascript


var main =  function main()
{
	var y,x;
	x = set([1, 2, 3]);
	y = set([1, 2, 3, 4]);
	if (!(x.issubset(y) === true)) {throw new Error("assertion failed"); }
	if (!(y.issubset(x) === false)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
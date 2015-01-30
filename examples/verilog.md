Verilog Backend
---------------

```rusthon
#backend:verilog

def mymodule1(q,r):
	reg(a,b)

	with initial:
		a = 0
		b = 0
		with delay(10):
			a = 1
			b = 1

def mymodule2(q,r):
	reg( a,b,i, bits=(3,0) )
	wire( q,r,  bits=(3,0) )

	with always:
		a = b & r
		for i in range(20):
			output = i
			delay(10)
```
Verilog Backend
---------------
old-style (pre-2001 verilog)

```rusthon
#backend:verilog

bit1(0)  ## one bit number - becomes `1'd0`
bit4(16) ## `4'd16`
'1011'   ## if string then value is binary `4'b1011`

foo=40  ## constant `parameter foo = 40`

def mymodule1(q,r):
	reg(a,b)
	print('hello world')

	with initial:
		a = 0
		b = 0
		with delay(10):
			a = 1
			b = 1

def mymodule2(q,r):
	reg( a,b,i, bits=4, index=0 )  ## `reg [3:0] a,b,i;`
	wire( q,r,  bits=4 )           ## `wire [3:0] q,r;`

	with always:
		a = b & r
		#for i in range(20):
		#	output = i
		#	delay(10)

	with always.comb:
		a = b

	with always.ff(something, clock=negative_edge):
		## async assignment (synced every clock edge)
		a <- b  ## becomes: `a <= 15`

	r.assign( a & b )  ## `assign r = a & b`  (continuous assignment always updated)


#new-style (post-2001 verilog)

def mymoduleX( q:2, r:[2:1] ) -> wire(res1, res2, bits=8):
	reg(a,b)


```
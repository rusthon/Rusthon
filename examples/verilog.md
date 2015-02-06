SystemVerilog
-------
```verilog

typedef enum logic [2:0] {
	RED, GREEN, BLUE
} colortype;

//initial begin
//	colortype color = RED;
//	$display("hello world:", color.name());
//end
```

SystemVerilog Backend
---------------
old-style (pre-2001 verilog)

```rusthon
#backend:verilog


#foo=40  ## constant `parameter foo = 40`

@module
def mymodule1(q,r):
	reg(a,b)
	reg(onebit, bits=1)
	reg(fourbits, bits=4)

	with initial:
		a = 0
		b = 0
		with delay(10):
			a = 1
			b = 1
			onebit   = bit1(0)     ## one bit number - becomes `1'd0`
			fourbits = bit4(16)    ## `4'd16`
			fourbits = '1011'      ## if string of ones and zeros, then value is binary `4'b1011`

@module
def mymodule2(q,r):
	reg( a,b,i, bits=4, index=0 )  ## `reg [3:0] a,b,i;`
	wire( q,r )           ## `wire q,r;`
	reg( something )

	with always:
		a = b & r
		for i in range(20):
			print(i)
			delay(10)

	with always.comb:
		a = b

	#with always.ff(something, clock=negative_edge):
	#	## async assignment (synced every clock edge)
	#	#a <- b  ## becomes: `a <= 15`
	#	a = b  ## becomes: `a <= 15`

	r.assign( a & b )  ## `assign r = a & b`  (continuous assignment always updated)

	with initial:
		a = 0
		b = 1


#new-style (post-2001 verilog)

@module
def mymoduleX( q:2, r:[4:1] ) -> wire(res1, res2, bits=8):
	logic(a,b, bits=32)

@module
def mymod( clock, a:4, b:4 ) -> wire(res1, bits=8):
	res1.assign( (a,b) )

## below segfaults iverilog ##
#reg( A, bits=4 )
#reg( B, bits=4 )
#reg( clk )
#reg( R, bits=8 )
#mod = mymod( clock=clk, a=A, b=B, res1=R )

```
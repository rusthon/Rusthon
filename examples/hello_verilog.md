System Verilog
--------------
Below is some hand written verilog, "hello world" is printed first, because there is no delay.

```verilog

module mymodule();

	initial begin
		$display("hello world");
	end

endmodule

```

Rusthon System Verilog Backend
---------------------------
Below the function `mymodule2` is translated to a verilog "module" like above.
The special `with initial:` marks things that run first, before the simulation starts.
The call `delay(10)` pauses this module for 10 clock ticks, and then prints "hello from rusthon".

```rusthon
#backend:verilog

def mymodule2():
	with initial:
		delay(10)
		print('hello from rusthon')

```
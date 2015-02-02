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
Below `with module():` is translated to a verilog "module" like above.
All the statements inside the body are put inside an `initial begin` block in Verilog.
The call `delay(10)` pauses this module for 10 clock ticks, and then prints "hello from rusthon".

```rusthon
#backend:verilog

with module():
	delay(10)
	print('hello from rusthon')

```
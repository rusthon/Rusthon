
```rusthon
#backend:verilog

with module():
	delay(10)
	print('hello from rusthon')

	reg(a,b, bits=4)
	reg(c, bits=8)
	@always
	def myfunc():
		c = (a,b)

	def main():
		myfunc()
```
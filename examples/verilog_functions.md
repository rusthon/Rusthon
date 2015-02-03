
```rusthon
#backend:verilog

with module():
	reg(a,b, bits=4)
	reg(c, bits=8)

	delay(10)
	print('testing function types...')


	@always
	def myfunc():
		print('calling myfunc')
		c = (a,b)

	def main():
		delay(1)
		myfunc()
```
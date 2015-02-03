
```rusthon
#backend:verilog

with module():
	reg(a,b, bits=4)
	reg(iput, oput, bits=4)
	reg(c, bits=8)

	delay(10)
	print('testing function types...')


	@always
	def myfunc():
		print('calling myfunc')
		c = (a,b)

	@task
	def mytask( myinput:4 ) -> reg(myoutput, bits=4):
		#print('calling mytask')  ## printing now allowed in a task
		myoutput = myinput

	def main():
		delay(1)
		myfunc()
		iput = 4
		delay(1)
		mytask(iput, oput)
		delay(10)
		print(oput)
```
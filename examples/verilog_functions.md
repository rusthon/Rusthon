Tasks vs Functions
------------------
A function must finish in a single time unit, a task can take any amount of time.
Functions can not call tasks, tasks can call functions and other tasks.
A function takes input and returns a value, a task takes multiple inputs and outputs.
A function can be used in an expression, a task can only be used as a statement.
It is not safe to have multiple instances of the same task running at the same time,
because they share the same local storage (arguments and local variables).

```rusthon
#backend:verilog

with module():
	reg(a,b, bits=4)
	reg(iput, oput, bits=4)
	reg(c, bits=8)
	myint = 0
	myfloat = 0.0

	delay(10)
	print('testing function types...')

	def myadd(x:int, y:int) -> int:
		#return x+y  ## TODO
		myadd = x+y

	@always
	def myfunc():
		print('calling myfunc')
		c = (a,b)

	@task
	def mytask( myinput:4 ) -> reg(myoutput, bits=4):
		#print('calling mytask')  ## printing now allowed in a task
		myoutput <- myinput  ## prints `x` uninitalized
		#myoutput = myinput

	@always
	def main():
		delay(1)
		myfunc()
		iput = 4
		delay(1)
		mytask(iput, oput)
		delay(10)
		print(oput)

		print('for loop...')
		for i in range(4):
			print(i)
			delay(10)
			myfunc()

		print(oput)
		print('----------------')
		myint = myadd( 100, 150 )
		print(myint)



```
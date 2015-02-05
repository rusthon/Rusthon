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
	## infer register type
	myint = 0       ## becomes `reg integer myint;`
	myfloat = 0.0   ## becomes `reg real myfloat;`
	X = 10
	Y = 20

	## gets moved into `initial begin`
	delay(10)
	print('testing function types...')

	def myadd(x:int, y:int) -> int:
		print('calling myadd')
		print('x:', x)
		print('y:', y)
		x = x+2
		#myadd = x+y
		return x+y

	@always
	def myfunc():
		print('calling myfunc')
		c = (a,b)

	@task
	def mytask( myinput:4 ) -> reg(myoutput, bits=4):
		print('calling mytask')
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
		delay(10, myint=myadd( 100, 150 ) )  ## delayed assignment
		print(myint)
		print(X)
		print(Y)
		myint = myadd( x=X, y=Y )
		delay(1)
		print('printing myint')
		print(myint)



```
SystemVerilog allows you to spawn multiple tasks at once, but will share the same state, this can cause problems.  The newer task will over-write the input/output and local variables of the current task, the current task is not stopped.

A possible workaround is to generate `inmytask` and wait on that signal to become zero, and then call the task, but what if multiple loops are blocking and waiting to call the same task?

A better possible workaround is to generate multiple version of the same task, and then each spawn launches a different one, that way local variables and inputs remain valid for each instance.  This might use a new syntax like: `@task( instances=64 )`.

```rusthon
#backend:verilog

with module():
	inmytask = 0
	myglobal = 0
	reg(a,b, bits=8)


	@task
	def mytask( iput:8 ) -> reg(oput, bits=8):
		if inmytask:
			print('task already running!')
		inmytask = 1
		print('enter task')
		oput <- iput
		delay(1000)
		myglobal = iput
		print('exit task')
		inmytask = 0

	@always
	def myloop():
		for i in range(5):
			mytask(a,b)
			print(myglobal)

	def main():
		a = 1
		mytask(a,b)
		print(b)
		print(myglobal)
		a = 2
		mytask(a,b)
		print(b)
		print(myglobal)


```

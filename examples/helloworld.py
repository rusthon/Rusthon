'''
Helloworld Example

If this file is compiled without any extra arguments, it will be transpiled using the C++ backend, 
compiled with GCC, and then binary will be executed.
./rusthon.py ./examples/helloworld.py

To transpile with another backend use one of these command line options:
	--javascript
	--rust
	--go

JavaScript Example:
	This will transpile and test it using NodeJS
	./rusthon.py ./examples/helloworld.py --javascript

	This will transpile and save helloworld.js into mytar.tar file
	./rusthon.py ./examples/helloworld.py --javascript /tmp/mytar.tar


Note that using python files (.py) is not the preferred input method,
and instead you should use markdown files (.md) as the container format.
https://github.com/rusthon/Rusthon/wiki/Literate-Programming

Why are python files not preferred?
Because in regular python files are modules, and provide a namespace for what
they contain.  This is not the case here, where all files are merged into a
single unit of translation.

'''

def say_hi():
	print( 'hello world')

def main():
	say_hi()

main()
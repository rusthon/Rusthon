Introduction
------------
Gython is a transpiler written in Python that converts a python like language into Go.

[Syntax Documentation](https://github.com/PythonJS/PythonJS/blob/master/doc/go_syntax.md)


Getting Started
===============


gython.py
--------------------------------------
Install Python2.7 and git clone this repo, in the toplevel is the build script `gython.py`.  
Running gython.py from the command line and passing it one or more python scripts outputs
the Go translation to stdout.

Usage::

	gython.py file.py

Example::

	git clone https://github.com/gython/Gython.git
	cd Gython
	./gython.py myscript.py > myscript.go



Supported Features
================

####Language Overview
	
	go static types
	go channel syntax
	classes
	multiple inheritance
	list comprehensions
	yield (generator functions)  TODO
	regular and lambda functions  TODO nested functions
	function calls with keywords and defaults

####Language Keywords

	global, nonlocal
	while, for, continue, break
	if, elif, else
	try, except, raise
	def, lambda
	new, class
	from, import, as
	pass, assert
	and, or, is, in, not
	return, yield


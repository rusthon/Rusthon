Introduction
------------
PythonJS is a transpiler written in Python that converts a python like language into fast
JavaScript.  It also includes experimental backends that translate to: Dart, Lua, CoffeeScript, and Go.

[Syntax Documentation](https://github.com/PythonJS/PythonJS/blob/master/doc/syntax.md)


Go backend
----------
The Go backend uses a fully typed subset of Python, mixed with extra syntax inspired by Golang to output Go programs that can be compiled to native executeables, or translated to JavaScript using GopherJS.

[Syntax Documentation](https://github.com/PythonJS/PythonJS/blob/master/doc/go_syntax.md)


Getting Started
===============
PythonJS can be run with regular Python, or fully self-hosted within
NodeJS using Empythoned. 

To get started, you have two options:
1. install NodeJS, python-js package, and write a build script.
2. or install Python2 and use translator.py from this repo directly.


1. Installing NodeJS Package
-------------
You can quickly get started with the stable version of PythonJS by installing the NodeJS package,
and writing a build script in javascript to compile your python scripts to javascript.
(Python2.7 is not required)

```
npm install python-js
```

NodeJS Quick Example
--------------

```
var pythonjs = require('python-js');
var pycode = "a = []; a.append('hello'); a.append('world'); print(a)";
var jscode = pythonjs.translator.to_javascript( pycode );
eval( pythonjs.runtime.javascript + jscode );

```


Example Projects
----------------
The example projects below, require the NodeJS python-js package.

[https://github.com/PythonJS/pythonjs-demo-server-nodejs](https://github.com/PythonJS/pythonjs-demo-server-nodejs)

[https://github.com/PythonJS/pypubjs](https://github.com/PythonJS/pypubjs)



2. translator.py
--------------------------------------
If you want to run the latest version of the translator, you will need to install
Python2.7 and git clone this repo.  (the NodeJS package above is not required)
Then, to translate your python script, directly run the `translator.py` script in the "pythonjs" directory.  You can give it a list of python files to translate at once.  
It will output the translation to stdout.  The default output type is JavaScript.  
An html file can also be used as input, python code inside a script tag: `<script type="text/python">`
will be converted into JavaScript.

Usage::

	translator.py [--help|--go|--dart|--coffee|--lua|--no-wrapper|--analyzer] file.py

Examples::

	cd pythonjs
	./translator.py myscript.py > myscript.js
	./translator.py myapp.html > app.html

The option `--no-wrapper` will output the raw JavaScript, by default the output is wrapped as a requirejs module.

The option `--analyzer` requires the Dart SDK is installed to your home directory: `~/dart-sdk`,
if this option is used then your script is also translated using the dart backend and fed to
`dartanalyzer` which will perform static analysis of your code.  Dartanalyzer is able to catch many types of errors, like: missing functions, invalid names, calling a function with the wrong argument types.  The quality of the analysis will depend on how much type information can be
inferred from your code, combined with the variables you have manually typed.  If dartanalyzer detects an error in your code, translation will abort, and debugging information is printed.



Speed
---------------
PythonJS gives you the option to optimize your program for speed with a new syntax for static typing, in some cases this results in code that is 20X faster.
A variable can be statically typed as: int, float, long, str, list, or dict.  
The translator then uses this type information to speed up runtime checks and method calls.
In the example below `x` and `y` are typed as `int`.
```
def f(x,y):
	int x
	int y
	return x+y

```

The `int` type is accurate up to 53bits, if you need true 64bit integer math you can use the `long` type.  Note using `long` requires the Long.js library.

You can further optimize your code with `pythonjs.configure` or special with statements that mark sections of the code as less dynamic.

N-Body benchmark

![nbody](http://2.bp.blogspot.com/-pylzspKRu6M/UqbAv3qIGTI/AAAAAAAAAkE/NnsAM5DZ_8M/s400/nbody.png)

[More benchmarks: Richards, n-body, Pystone, Fannkuch](http://pythonjs.blogspot.com/2014/06/pythonjs-faster-than-cpython-part2.html)


GPU Translation
---------------
A Python typed subset can be translated to a GLSL fragment shader to speed up math on large arrays.
[GPU Documentation](https://github.com/PythonJS/PythonJS/blob/master/doc/gpu.md)



Supported Features
================

####Language Overview
	
	classes
	multiple inheritance
	operator overloading
	function and class decorators
	getter/setter function decorators
	list comprehensions
	yield (generator functions)
	regular and lambda functions
	function calls with *args and **kwargs

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

####HTML DOM: for item in iterable
	NodeList
	FileList
	ClientRectList
	DOMSettableTokenList
	DOMStringList
	DataTransferItemList
	HTMLCollection
	HTMLAllCollection
	SVGElementInstanceList
	SVGNumberList
	SVGTransformList


####Operator Overloading

	__getattr__
	__getattribute__
	__getitem__
	__setitem__
	__call__
	__iter__
	__add__
	__mul__

####builtins

	dir
	type
	hasattr
	getattr
	setattr
	issubclass
	isinstance
	dict
	list
	tuple
	int
	float
	str
	round
	range
	sum
	len
	map
	filter
	min
	max
	abs
	ord
	chr
	open  (nodejs only)

####List

	list.append
	list.extend
	list.remove
	list.insert
	list.index
	list.count
	list.pop
	list.__len__
	list.__contains__
	list.__getitem__
	list.__setitem__
	list.__iter__
	list.__getslice__

####Set

	set.bisect
	set.difference
	set.intersection
	set.issubset

####String

	str.split
	str.splitlines
	str.strip
	str.startswith
	str.endswith
	str.join
	str.upper
	str.lower
	str.index
	str.find
	str.isdigit
	str.format
	str.__iter__
	str.__getitem__
	str.__len__
	str.__getslice__

####Dict

	dict.copy
	dict.clear
	dict.has_key
	dict.update
	dict.items
	dict.keys
	dict.get
	dict.set
	dict.pop
	dict.values
	dict.__contains__
	dict.__iter__
	dict.__len__
	dict.__getitem__
	dict.__setitem__

####Libraries

	time.time
	time.sleep
	math.sin
	math.cos
	math.sqrt
	array.array
	os.path.dirname
	bisect.bisect
	random.random
	threading.start_new_thread

#####Libraries (nodejs only)
	tempfile.gettempdir
	sys.stdin
	sys.stdout
	sys.stderr
	sys.argv
	sys.exit
	subprocess.Popen
	subprocess.call
	os.path.*

------------------------------

Regression Tests
================

The best way to see what features are currently supported with each of the backends
is to run the automated regression tests in PythonJS/regtests.  To test all the backends
you need to install NodeJS, CoffeeScript, and Dart2JS.  You should download the Dart SDK,
and make sure that the executeable `dart2js` is in `~/dart-sdk/bin/`

####Run Regression Tests

	cd PythonJS/regtests
	./run.py


Community
---------

[https://groups.google.com/forum/#!forum/pythonjs](https://groups.google.com/forum/#!forum/pythonjs)

irc freenode::

	#pythonjs


pythonjs.configure
------------------
The special function call `pythonjs.configure` can be inserted anywhere in your code to turn off an on dynamic
features of the language.

If the option `direct_keys` is True then dictionary key lookups are done directly (faster),
objects can not be used as keys, only strings and numbers can then be used as dictionary keys.

The option `direct_operator` controls operator overloading for a given operator: '+', '*'.
If '+' is declared a direct operator then `__add__` overload methods are not called,
the operands are always assumed to be compatible with javascript addition.

The option `runtime_exceptions` if False disables extra runtime checking of expressions and assignments,
note this is always False in javascript mode.

```
pythonjs.configure(
	javascript=True/False,          ## default False
	runtime_exceptions=True/False,  ## default True
	direct_keys=True/False,         ## default False
	direct_operator=string          ## default 'None'
)
```

Gotchas
---------
0. in a dictionary number keys will be converted to strings.
In the example below the key `100` and `"100"` are the same key.
```
a = {"100": 'X'}
a[ 100 ] = 'Y'
```

1. The calling context of `this` must be taken into account when using fast javascript mode, code that comes after: `pythonjs.configure(javascript=True)` or is inside a `with javascript:` block.  When in javascript mode, passing a method as a callback, or setting it as an attribute on another object, requires you call `f.bind(self)` to ensure that `self` within the method points to the class instance.  This is not required when using classes defined normal mode, because the `this` calling context is automatically managed.
Note: you can use the special `->` syntax in place of the attribute operator `.` to call `bind` automatically.

```
class A:
	def method(self):
		print(self)

a = A()

with javascript:
	class B:
		def method(self):
			print(self)

	b = B()
	a.b_method1 = b.method
	a.b_method2 = b.method.bind(b)
	a.b_method3 = b->method

	a.method()     ## OK: prints a
	a.b_method1()  ## FAILS: prints a, should have printed b
	a.b_method2()  ## OK: prints b
	a.b_method3()  ## OK: prints b

	b.a_method = a.method
	b.a_method()   ## OK: prints a

```

2. When using direct operators, builtins are also affected.  List + list will no longer return a new array of items from both lists.  String * N will no longer return the string multipled by the number.

```
a = [1,2] + [3,4]  ## OK: a is [1,2,3,4]
pythonjs.configure(direct_operator="+")
b = [1,2] + [3,4]  ## FAILS

c = "HI" * 2  ## OK: c is "HIHI"
pythonjs.configure(direct_operator="*")
d = "HI" * 2  ## FAILS

```

3. The syntax `from mymodule import *` allows you to import another python script from the same folder,
but both mymodule and the parent will share the same namespace, mymodule can use global variables defined in the parent.

4. Using tuples as keys in a dict is allowed, the tuple may contain other tuples, objects, and a mix of numbers or strings.
Note that tuples in PythonJS are actually JavaScript arrays, so if you modify the contents of the tuple, it would no
longer be the same key in a dict.
```
a = (1,2,3)
b = ("1","2","3")
D = { a: 'hello', b: 'world' }
D[ a ] == 'hello'  ## OK
D[ b ] == 'world'  ## OK
```

5. AttributeError and KeyError are only raised in javascript mode when inside a block that catches those errors.
In the default python mode these errors will always be thrown, and halt the program.
```
pythonjs.configure(javascript=True)
a = {}
# this will not throw any error
b = a['xxx']
# this works as expected, "b" will be set to "my-default"
b = a['xxx'] except KeyError: 'my-default'
```

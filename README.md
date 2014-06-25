Introduction
------------
PythonJS is a transpiler written in Python that converts Python into fast
JavaScript.  It can be run with regular Python, or fully self-hosted within
NodeJS using Empythoned.  PythonJS has been designed with speed and easy
integration with existing JavaScript code in mind.


Using translator.py Without Installing
--------------------------------------
To simply convert your python script into javascript, git clone this repo, and
use translator.py located in the "pythonjs" directory.  You can give it a list
of python files to translate at once.  It will output the translation to
stdout.  The default output type is JavaScript.

Usage::

	translator.py [--dart|--coffee|--lua] file.py

Example::

	cd PythonJS/pythonjs
	./translator.py myscript.py > myscript.js



Installing
-------------
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

JavaScript API
----------
```
var pythonjs, output;
pythonjs = require('python-js');
output = pythonjs.translator.to_javascript( input );
output = pythonjs.translator.to_javascript_module( input );
output = pythonjs.translator.to_dart( input );
output = pythonjs.translator.to_coffee( input );
output = pythonjs.translator.to_lua( input );

pythonjs.runtime.javascript // runtime required by translator output

```

Example Projects
----------------
[https://github.com/PythonJS/pythonjs-demo-server-nodejs](https://github.com/PythonJS/pythonjs-demo-server-nodejs)

[https://github.com/PythonJS/pypubjs](https://github.com/PythonJS/pypubjs)


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

####Language
	
	classes
	multiple inheritance
	operator overloading
	function and class decorators
	getter/setter function decorators
	list comprehensions
	yield (generator functions)
	regular and lambda functions
	function calls with *args and **kwargs

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


![bitdeli](https://d2weczhvl823v0.cloudfront.net/PythonJS/pythonjs/trend.png)

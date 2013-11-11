PythonJS
############

.. image:: http://4.bp.blogspot.com/-oiwojUmueiM/UmjixTGKNYI/AAAAAAAAAfE/Tp4uNMx3iEE/s320/pythonjs-v9.png

:dependency: Python 2.7
:documentaiton: `PythonJS <https://pythonscript.readthedocs.org/en/latest/>`_

Introduction
======

PythonJS is a Python to Javascript translator written in Python, created by Amirouche Boubekki and Brett Hartshorn. It converts a subset of Python into a subset of Javascript.  It features: list comprehensions, classes, multiple inheritance, first-class functions, operator overloading, function and class decorators, HTML DOM, and easily integrates with JavaScript and external JavaScript libraries.


Getting Started - Stable Release
---------------

First::

   sudo pip install PythonJS

Write some Python, and then run::

   pythonjs < myapp.py > myapp.js

Then copy myapp.js and the runtime pythonscript.js into your project.

Demos
=====

- `sudo python <http://amirouche.github.io/sudo-python/>`_

See also
========

- `Type Inference <http://en.wikipedia.org/wiki/Type_inference>`_
- `The Missing Python AST Docs <http://greentreesnakes.readthedocs.org/en/latest/>`_

---------------

Getting Started - Main Development Branch
---------------

Get Source Code::

	git clone https://github.com/PythonJS/PythonJS.git

Install Tornado for Python3::

	wget https://pypi.python.org/packages/source/t/tornado/tornado-3.1.1.tar.gz
	tar xvf tornado-3.1.1.tar.gz
	cd tornado-3.1.1
	python3 setup.py build
	sudo python3 setup.py install

Run Test Server::

	cd PythonJS/tests
	./server.py

Then open a web browser and go to: http://localhost:8080


Test Server (server.py)
========

The test server dynamically compiles Python into JavaScript, this greatly speeds up the testing and development process.  Any html file you place in the PythonJS/tests directory will become available as a new web-page.  When this web-page is requested the server will parse the html and check all the <script> tags for external or embedded Python, and dynamically convert it to JavaScript.

External Python Scripts::

	<head>
	<script src="bindings/three.py"></script>
	</head>

The server knows that the above script needs to be dynamically compiled to JavaScript because the script is located in the "bindings" directory and the file name ends with ".py"

Embedded Python Scripts::

	<body>
	<script type="text/python">
	from three import *
	v1 = Vector3( x=1, y=2, z=3 )
	v2 = Vector3( x=4, y=5, z=6 )
	v3 = v1 + v2
	</script>
	</body>

The server knows that above is an embedded Python script because the script tag has its type attribute set to "text/python".  The server will compile and replace the Python code with JavaScript, change the type attribute to be "text/javascript", and serve the page to the client.

The syntax "from three import *" tells the compiler to load static type information about the previously compiled binding "three.py" into the compilers namespace, this is required because three.py uses operator overloading to wrap the THREE.js API.  PythonJS programs are explicitly and implicitly statically typed to allow for operator overloading and optimizations.

---------------

Directly Calling JavaScript Functions
---------------

HTML DOM Example::

	<html><head>
	<script src="pythonscript.js"></script>

	<script type="text/python">

	count = 0

	def mycallback():
		global count
		print( con.getAttribute('id') )
		btn = document.getElementById('mybutton')
		btn.firstChild.nodeValue = 'COUNTER:'+count
		count += 1

	a = 'hello'
	b = 'world'

	def test():
		con = document.createElement( 'div' )
		con.setAttribute('id', 'mydiv')
		document.body.appendChild(con)
		txt = document.createTextNode( a+b )
		con.appendChild(txt)

		window.setInterval( mycallback, 1000 )

	</script>

	</head><body>

	<button id="mybutton" onclick="test()">click me</button>

	</body>
	</html>

Numbers and strings can be passed directly to JavaScript functions.  Simple callbacks that do not take any arguments can also be passed as an argument to a JavaScript function, like window.setInterval.  PythonJS allows you to call any JavaScript function directly by wrapping it at runtime.  Attributes of JavaScript objects are also returned directly, like document.body.  This allows you to use the HTML DOM API just as you would in normal JavaScript.

---------------

Inline JavaScript
---------------

There are times that JavaScript needs to be directly inlined into PythonJS code, this is done with the special 'JS([str])' function that takes a string literal as its only argument.  The compiler will insert the string directly into the final output JavaScript.

JS Example::

	JS("var arr = new Array()")
	JS("var ob = new Object()")
	JS("ob['key'] = 'value'")
	if JS("Object.prototype.toString.call( arr ) === '[object Array]'"):
		JS("arr.push('hello world')")
		JS("arr.push( ob )")

In the example above we create a new JavaScript Array.  The if statement is still Python syntax, but its condition is allowed to be inlined JavaScript.  As the compiler becomes smarter and the PythonJS low-level API develops, there will be less need to write inline JavaScript in the above style.  Lets take a look at two alternative ways this can be rewritten.

1. JSArray, JSObject, and instanceof::

	arr = JSArray()
	ob = JSObject()
	if instanceof(arr, Array):
		arr.push('hello world')
		arr.push( ob )

The special function JSArray will create a new JavaScript Array object, and JSObject creates a new JavaScript Object.  The 'instanceof' function will be translated into using the 'instanceof' JavaScript operator.  At the end, arr.push is called without wrapping it in JS(), this is allowed because from PythonJS, we can directly call JavaScript functions by dynamically wrapping it at runtime.

This code is more clear than before, but the downside is that the calls to arr.push will be slower because it gets wrapped at runtime.  To have fast and clear code we need to use the final method below, 'with javascript'

2. with javascript::

	with javascript:
		arr = []
		ob = {}
		if instanceof(arr, Array):
			arr.push('hello world')
			arr.push( ob )

The "with javascript:" statement can be used to mark a block of code as being direct JavaScript.  The compiler will basically wrap each line it can in JS() calls.  The calls to arr.push will be fast because there is no longer any runtime wrapping.  Instead of using JSArray and JSObject you just use the literal notation to create them.

---------------

Calling PythonJS Functions from JavaScript
------------------------------

PythonJS functions can be used as callbacks in Javascript code, there are no special calling conventions that you need to worry about.  Simply define a function in PythonJS and call it from JavaScript.  Note that if your PythonJS function uses keyword arguments, you can use them as a normal positional arguments.

Example::

	# PythonJS
	def my_pyfunction( a,b,c, optional='some default'):
		print a,b,c, optional

	// javascript
	my_pyfunction( 1,2,3, 'my kwarg' );


---------------

Calling PythonJS Methods from JavaScript
------------------------------

Calling PythonJS methods is also simple, you just need to create an instance of the class in PythonJS and then pass the method to a JavaScript function, or assign it to a new variable that the JavaScript code will use.  PythonJS takes care of wrapping the method for you so that "self" is bound to the method, and is callable from JavaScript.

Example::

	// javascript
	function js_call_method( method_callback ) {
		method_callback( 1,2,3 )
	}

	# PythonJS
	class A:
		def my_method(self, a,b,c):
			print self, a,b,c
			self.a = a
			self.b = b
			self.c = c

	a = A()
	js_call_method( a.my_method )


---------------

Passing PythonJS Instances to JavaScript
------------------------------

If you are doing something complex like deep integration with an external JavaScript library, the above technique of passing each method callback to JavaScript might become inefficient.  If you want to pass the PythonJS instance itself and have its methods callable from JavaScript, you can do this now simply by passing the instance.  This only works for normal methods, not with property getter/setters.

Example::

	// javascript
	function js_function( pyob ) {
		pyob.foo( 1,2,3 )
		pyob.bar( 4,5,6 )
	}

	# PythonJS
	class A:
		def foo(self, a,b,c):
			print a+b+c
		def bar(self, a,b,c):
			print a*b*c

	a = A()
	js_function( a )


---------------

Define JavaScript Prototypes from PythonJS
------------------------------

If you are going beyond simple integration with an external JavaScript library, and perhaps want to change the way it works on a deeper level, you can modify JavaScript prototypes from PythonJS using some special syntax.

Example::

	with javascript:

		@String.prototype.upper
		def func():
			return this.toUpperCase()

		@String.prototype.lower
		def func():
			return this.toLowerCase()

		@String.prototype.index
		def func(a):
			return this.indexOf(a)

The above example shows how we modify the String type in JavaScript to act more like a Python string type.  The functions must be defined inside a "with javascript:" block, and the decorator format is: `[class name].prototype.[function name]`


---------------

Making PythonJS Wrappers for JavaScript Libraries
------------------------------

The above techniques provide all the tools you will need to interact with JavaScript code, and easily write wrapper code in PythonJS.  The last tool you will need, is a standard way of creating JavaScript objects, storing a reference to the instance, and later passing the instance to wrapped JavaScript function.  In JavaScript objects are created with the `new` keyword, in PythonJS you can use the `new()` function instead.  To store an instance created by `new()`, you should assign it to `self` like this: `self[...] = new( SomeJavaScriptClass() )`.  

If you have never seen `...` syntax in Python it is the rarely used Ellipsis syntax, we have hijacked it in PythonJS as a special case to assign something to a hidden attribute.  The builtin types: tuple, list, dict, etc, are wrappers that internally use JavaScript Arrays or Objects, to get to these internal objects you use the Ellipsis syntax.  The following example shows how the THREE.js binding wraps the Vector3 object and combines operator overloading.

Example::

	class Vector3:
		def __init__(self, x=0, y=0, z=0, object=None ):
			if object:
				self[...] = object
			else:
				with javascript:
					self[...] = new(THREE.Vector3(x,y,z))

		@property
		def x(self):
			with javascript: return self[...].x
		@x.setter
		def x(self, value):
			with javascript: self[...].x = value

		@property
		def y(self):
			with javascript: return self[...].y
		@y.setter
		def y(self, value):
			with javascript: self[...].y = value

		@property
		def z(self):
			with javascript: return self[...].z
		@z.setter
		def z(self, value):
			with javascript: self[...].z = value

		def set(self, x,y,z):
			self[...].set(x,y,z)

		def add(self, other):
			assert isinstance(other, Vector3)
			self.set( self.x+other.x, self.y+other.y, self.z+other.z )
			return self

		def addScalar(self, s):
			self.set( self.x+s, self.y+s, self.z+s )
			return self

		def __add__(self, other):
			if instanceof(other, Object):
				assert isinstance(other, Vector3)
				return Vector3( self.x+other.x, self.y+other.y, self.z+other.z )
			else:
				return Vector3( self.x+other, self.y+other, self.z+other )

		def __iadd__(self, other):
			if instanceof(other, Object):
				self.add( other )
			else:
				self.addScalar( other )


---------------

Optimized Function Calls
------------------------------

By default PythonJS functions have runtime call checking that ensures you have called the function with the required number of arguments, and also checks to see if you had called the function from JavaScript - and if so adapt the arguments.  This adds some overhead each time the function is called, and will generally be about 15 times slower than normal Python.  When performance is a concern you can decorate functions that need to be fast with @fastdef, or use the `with fastdef:` with statement.  Note that functions that do not have arguments are always fast.  Using fastdef will make each call to your function 100 times faster, so if you call the same function many times in a loop, it is a good idea to decorate it with @fastdef.

Example::

	@fastdef
	def f1( a, b, c ):
		return a+b+c

	with fastdef:
		def f2( a,b,c, x=1,y=2,z=3):
			return a+b+c+x+y+z

If you need to call a fastdef function from JavaScript you will need to call it with arguments packed into an array as the first argument, and keyword args packed into an Object as the second argument.

Example::

	// javascript
	f2( [1,2,3], {x:100, y:200, z:300} );

If you need fast function that is callable from javascript without packing its arguments like above, you can use the @javascript decorator, or nest the function inside a `with javascript:` statement.

Example::

	@javascript
	def f( a,b,c, x=1, y=2, z=3 ):
		return a+b+c+x+y+z

	// javascript
	f( 1,2,3, 100, 200, 300 );




.. image:: https://d2weczhvl823v0.cloudfront.net/PythonJS/pythonjs/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free


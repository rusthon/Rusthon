PythonJS
############

.. image:: http://3.bp.blogspot.com/-wd0nt-5J3Kg/Ul9RP_zmH5I/AAAAAAAAAd8/LjFdw0riJ0U/s320/pythonjs-v11.png

:dependency: Python 2.7
:documentaiton: `PythonJS <https://pythonscript.readthedocs.org/en/latest/>`_
:try: `apppyjs <http://apppyjs.appspot.com/>`_

Introduction
======

PythonJS is a Python to Javascript translator written in Python, created by Amirouche Boubekki and Brett Hartshorn. It converts a subset of Python into a subset of Javascript.  It features: list comprehensions, classes, multiple inheritance, first-class functions, operator overloading, decorators, HTML DOM, and easily integrates with JavaScript and external JavaScript libraries.


Getting Started - Stable Release
---------------

First::

   sudo pip install pythonscripttranslator

Write some Python, and then run::

   pythonscript < myapp.py > myapp.js

Then copy myapp.js and the runtime pythonscript.js into your project.

Demos
=====

- `sudo python <http://amirouche.github.io/sudo-python/>`_

See also
========

- `Type Inference <http://en.wikipedia.org/wiki/Type_inference>`_
- `The Missing Python AST Docs <http://greentreesnakes.readthedocs.org/en/latest/>`_

---------------

Getting Started - Experimental Development Branch
---------------

Get Source Code::

	git clone -b develop https://github.com/PythonScript-/PythonJS.git

Install Tornado for Python3::

	wget https://pypi.python.org/packages/source/t/tornado/tornado-3.1.1.tar.gz
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


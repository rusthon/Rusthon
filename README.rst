PythonScript
############

:dependency: Python 2.7
:documentaiton: `PythonScript <https://pythonscript.readthedocs.org/en/latest/>`_
:try: `apppyjs <http://apppyjs.appspot.com/>`_

Introduction
======

PythonScript is a Python to Javascript translator written in Python, created by Amirouche Boubekki and Brett Hartshorn. It converts a subset of Python into a subset of Javascript.  It features: classes, multiple inheritance, first-class functions, operator overloading, decorators, HTML DOM, and easily integrates with JavaScript and external JavaScript libraries.


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

	git clone https://github.com/hartsantler/PythonScript.git
	cd PythonScript
	git branch develop

Install Tornado for Python3::

	wget https://pypi.python.org/packages/source/t/tornado/tornado-3.1.1.tar.gz
	cd tornado-3.1.1
	python3 setup.py build
	sudo python3 setup.py install

Run Test Server::

	cd PythonScript/tests
	./server.py

Then open a web browser and go to: http://localhost:8080


Test Server (server.py)
========

The test server dynamically compiles PythonScript into JavaScript, this greatly speeds up the testing and development process.  Any html file you place in the PythonScript/tests directory will become available as a new web-page.  When this web-page is requested the server will parse the html and check all the <script> tags for external or embedded PythonScript, and dynamically convert it to JavaScript.

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

The syntax "from three import *" tells the compiler to load static type information about the previously compiled binding "three.py" into the compilers namespace, this is required because three.py uses operator overloading to wrap the THREE.js API.  PythonScript programs are explicitly and implicitly statically typed to allow for operator overloading and optimizations.

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

Numbers and strings can be passed directly to JavaScript functions.  Simple callbacks that do not take any arguments can also be passed as an argument to a JavaScript function, like window.setInterval.  PythonScript allows you to call any JavaScript function directly by wrapping it at runtime.  Attributes of JavaScript objects are also returned directly, like document.body.  This allows you to use the HTML DOM API just as you would in normal JavaScript.


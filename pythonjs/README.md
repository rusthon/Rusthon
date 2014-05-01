PythonJS
======

PythonJS is a multi-language Python translator.  The translator is written in Python and runs inside NodeJS using a hacked and stripped down version of Empythoned.  Empythoned is the standard C-Python interpreter compiled to JavaScript using Emscripten.

PythonJS can be used from the command line or as a library within your own NodeJS program.  By default the translator will output JavaScript.  You can also use the experimental backends for: Dart, Coffee, Lua and Vis.js.  The Vis.js backend turns your code into a graph so you can inspect it visually in a web-browser using the vis.js library.

####Command Line

	python-js INPUT OUTPUT [--dart, --coffee, --lua, --visjs]


####NodeJS Module

	var pythonjs = require('python-js');

	var code = pythonjs.translator.to_javascript( my_python_code ) // output javascript
	eval( code )  // runs the javascript output server side within nodejs

	// experimental backends
	var code = pythonjs.translator.to_dart( my_python_code )       // output dart
	var code = pythonjs.translator.to_coffee( my_python_code )     // output coffeescript
	var code = pythonjs.translator.to_lua( my_python_code )        // output lua
	var code = pythonjs.translator.to_visjs( my_python_code )      // output a graph for vis.js

	// the runtime required on the client side by the javascript and coffee backends
	var header = pythonjs.runtime.javascript

The PythonJS module exports an object named `translator` that contains functions to translate your python code using one of the backends.

When translating code for the Dart or Lua backends the required runtime header is inserted at the top of the output.  Note that for the Javascript and Coffee backends, the runtime header is not included in the output - so if code is going to be run on the client side in a web browser, then you will need to manually include `pythonjs.js` script in the HTML page.

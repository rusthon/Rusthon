PythonScript
############



Kesako
======

A Python to Javascript translator in Python. It converts a subset of Python to a subset of Javascript, making available enough Javascript in Python to do many things useful among which (at least I think) a full Python interpreter.

Getting started
---------------

::
   sudo pip install pythonscript
   pythonscript < python.py > jspython.js


What is supported
-----------------

- Functions with positional arguments only
- Class without inheritance
- ``for i in range(foo.bar)``
- ``JS('javascript code')`` will output ``javascript_code`` in the generated code, useful for accessing javascript objects, you can a still assign the result to whatever you want
- Any Python variable name will be output as is in the code which means ``Spam`` will be ``Spam`` in javascript. Similarly an ``egg`` variable in javascript will be ``egg`` in Python but there is still a bug in ``pythonpythonjs.py`` preventing to access directly javascript objects from Python.


How is it possible
==================

The actual implementation looks like::

  [PythonScript] -> ast -> [PythonScriptToPythonJs] -> ast -> [PythonJSToJS] -> javascript


So the last step before the actual Javascript file is a restricted version of Python which can be translated one to one to a subset of Javascript. PythonScript is actually another subset of Python bigger than PythonJS that takes advantage of a runtime library written in PythonJS called ``pythonpythonjs.py`` which is also converted to javascript by the PythonJSToJS machinery.


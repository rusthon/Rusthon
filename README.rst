PythonScript
############

:dependency: Python 2.7

Kesako
======

A Python to Javascript translator in Python. It converts a subset of Python to a subset of Javascript, making available enough Javascript in Python to do many things useful among which (at least I think) a full Python interpreter.

Getting started
---------------

First::

   sudo pip install pythonscripttranslator

Write some Python then::

   pythonscript < app.py > app.py.js

Then copy python.js from github to your project added both files as scripts of your page and voilà!


What is supported
-----------------

- print are translated to ``console.log``
- Functions & methods
- Class with multiple inheritance but not compatible with CPython
- ``for i in range(foo.bar)``
- Any Python variable name will be output as is in the code which means ``Spam`` will be ``Spam`` in javascript. Similarly an ``egg`` variable in javascript will be ``egg`` in Python but there is still a bug (or security in Javascript engines) preventing from doings for instance ``document.createElement("div")`` directly in Python, it seems to works with some pure javascript objects. Keep in mind that you'd rather use ``JS`` if you look for speed.
- ``JS('javascript code')`` will output ``javascript_code`` in the generated code, useful for accessing javascript objects that you cannot access directly, you can a still assign the result to whatever you want.
- ``for i in j`` is translated as ``(for(i=0, i<j, i++)``
- ``JSObject(foo="bar")`` is converted to ``{"foo": "bar" }``

Known bugs
----------

- no support for ``list``
- no support of ``super``

How is it possible
==================

The actual implementation looks like::

  [PythonScript] -> ast -> [PythonScriptToPythonJs] -> ast -> [PythonJSToJS] -> javascript


So the last step before the actual Javascript file is a restricted version of Python which can be translated one to one to a subset of Javascript. PythonScript is actually another subset of Python bigger than PythonJS that takes advantage of a runtime library written in PythonJS called ``pythonpythonjs.py`` which is also converted to javascript by the PythonJSToJS machinery.

``pythonpythonjs.py`` is converted to Javascript using ``pythonjs`` command.

TODO
====

Demos: infojs, chartjs, timelinejs

Changelog
=========

- 0.3 - 31/03/13

  - support of python(positional, arguments, key=word, *args, **kwargs), it doesn't work in callbacks

- 0.2

  - positional arguments
  - inheritance with custom mro

- 0.1

See also
========

- PyPy
- http://greentreesnakes.readthedocs.org/en/latest/

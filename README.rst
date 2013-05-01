PythonScript
############

:dependency: Python 2.7

Kesaco
======

A Python to Javascript translator in Python. It converts a subset of Python to a subset of Javascript, making available enough Javascript in Python to do many things useful among which (at least I think) a full Python interpreter.

Getting started
---------------

First::

   sudo pip install pythonscripttranslator

Write some Python then::

   pythonscript < app.py > app.py.js

Then copy pythonscript.js from github to your project added both files as scripts of your page and voilà!


What is supported
-----------------

- print are translated to ``console.log``
- Functions & methods
- Class with multiple inheritance but not compatible with CPython
- minimal list/dict/str
- minimal for/while/try/except/raise
- Any Python variable name will be output as is in the code which means ``Spam`` will be ``Spam`` in javascript. Similarly an ``egg`` variable in javascript will be ``egg`` in Python but there is still a bug (or security in Javascript engines) preventing from doings for instance ``document.createElement("div")`` directly in Python, it seems to works with some pure javascript objects. Keep in mind that you'd rather use ``JS`` if you look for speed.
- ``JS('javascript code')`` will output ``javascript_code`` in the generated code, useful for accessing javascript objects that you cannot access directly, you can a still assign the result to whatever you want.
- ``JSObject(foo="bar")`` is converted to ``{"foo": "bar" }``
- ``var(spam, egg)`` is translated to ``var spam, egg;`` each time you create a variable that is not global (in a method or function) you need to *var* it or expect bugs.

How is it possible
==================

The actual implementation looks like::

  [PythonScript] -> ast -> [PythonScriptToPythonJs] -> ast -> [PythonJSToJS] -> javascript


So the last step before the actual Javascript file is a restricted version of Python which can be translated one to one to a subset of Javascript. PythonScript is actually another subset of Python bigger than PythonJS that takes advantage of a runtime library written in PythonJS called ``pythonpythonjs.py`` which is also converted to javascript by the PythonJSToJS machinery.

``pythonpythonjs.py`` is converted to Javascript using ``pythonjs`` command.

Demos
=====

- `sudo python <http://amirouche.github.io/sudo-python/>`_


Changelog
=========

0.5 - 13/05/01 - Lazy labor
---------------------------

- improvements in jquery bindings
- add minimal support for exceptions
- better support for loops
- introduce a builtins.py file
- renamed the compiled python runtime file to pythonscript.js
- booleans
- minimal list/dict/str but not fully compatible with CPython
- ``get_attribute`` support now inhertance but still not as CPython
- new special function ``var(spam, egg)`` that is translated to ``var spam, egg;``
- new ``range`` that is compatible with for loop
- several fixes in the compilation
- `sudo python <http://amirouche.github.io/sudo-python/>`_

0.4 - tldr
----------

- lazy for loop implementation (only used in pythonjs now)
- while loops
- fixing some callbacks in jquery bindings with ``adapt_arguments``

0.3 - 13/03/31
--------------

- support of python(positional, arguments, key=word, *args, **kwargs), it doesn't work in callbacks

0.2 - acid lemon
----------------

- positional arguments
- inheritance with custom mro


0.1 - happy hacking
-------------------

See also
========

- PyPy
- http://greentreesnakes.readthedocs.org/en/latest/

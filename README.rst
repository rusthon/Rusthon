PythonScript
############

:dependency: Python 2.7

Kesaco
======

A Python to Javascript translator in Python. It converts a subset of Python to a subset of Javascript, making availabele enough Javascript in Python to do many things useful among which (at least I think) a full Python interpreter. **Right now pythonscript command is a compiler.

Getting started
---------------

First::

   sudo pip install pythonscripttranslator

Write some Python then::

   pythonscript < app.py > app.py.js

Then copy pythonscript.js from github to your project added both files as scripts of your page and voilà!

Demos
=====

- `sudo python <http://amirouche.github.io/sudo-python/>`_


Changelog
=========

0.6.1 - 13/05/12 - Open up
--------------------------

- added ``getattr`` and ``setattr``

0.6 - 13/05/09 - Dispatch
-------------------------

- added data descriptors
- added metaclasses functions and ``type`` as a class contructor
- args and kwargs in called are respectively list and dictionary instead of javascript objects

0.5 - 13/04/01 - Lazy labor
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

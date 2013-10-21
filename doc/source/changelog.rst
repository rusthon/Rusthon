Changelog
#########

0.8 - I need a hero
-------------------

A lot of changes and fixes among which

- Changed the name from PythonScript to PythonJS
- Changed license to BSD 2-clause
- Support of Closure Compiler
- ``__getitem__`` and ``__setitem__`` support
- Operator creation and overloading
- three.js bindings
- Tornado server that compiles code
- Javascript functions are callable from Python, which makes creating bindings almost not usefull except if you need further integration with the language (like operator overloading)
- No need to var anything, it's automatic. ``global`` has the same semantic as in Python
- You can use ``with javascript:`` to inline the block the generated javascript code

Don't forget to checkout the ``tests`` directory, there, you might find some jewels ;)

0.7.3 - Tricky
--------------

- Fixed ``pythnonjs`` and ``python_to_pythonjs`` commands to be runnable.

0.7.2 - Urban species
---------------------

- fixed ``pythonscript`` which was broken by last release

0.7.1 - Morcheeba
-----------------

- rework the way script are executed to be possible to call them from Python easly

0.7 - 13/05/12 - Electric Guest
-------------------------------

- move weblib to its own repository
- add support for ``is``
- added ``isinstance`` and ``issubclass``
- rework the translation for python to pythonjs
- improved generated code
- full support of exception (typed and named)
- added a set of reference transaltion ``tests/python-to-js/``


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

Sometime ago I started a quest to find the best solution to do Python in the browser. My
`first idea <https://bitbucket.org/amirouche/nomad-old>`_ was to create a browser in Python thinking
that it would be easy to embedded Python in a Python browser but it's actually there is no trivial way
to sandbox Python. Building a HTML renderer is not trivial too. Then I started to dig what existed and
discovered that most of the implementation were using javascript to bridge the gap between Python's
object oriented semantic and Javascript's one, whatever the mode: compiled or interpreted. Not happy
with what was available I started `an implementation <https://bitbucket.org/amirouche/subscript>`_
following the same route, I think I tried it twice. First time I started with Google Closure then
using requirejs and Classy. The good news is I know javascript better the bad news was none really
worked. Then Brython came, I started again to think about the problem. Do I really need to write it in
Javascript ? I've ditched PyPy before because RPython targets typed languages so it wasn't good for
Javascript, but the method still holds, after reading again
:download:`one of the best ressource regarding PyPy <https://github.com/amirouche/notes/raw/master/source/_static/pygirl-bruni-2009.pdf>`
I've started a new implementation that called `PythonScript <http://apppyjs.appspot.com/>`_. It's
intersting enough because the core is fully written in Python and it quite easier to write than the
other solutions, I've put less the first release took me less than 25 hours.

Right now is rough around the edge. Abstract syntax tree API aka. ``ast`` module beauty as no other, but it works enough.

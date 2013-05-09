How to write Python in PythonScript
===================================

How to use PythonScript ?
-------------------------

Install PythonScriptTranslator::

  pip install PythonScriptTranslator

And download the latest version on the master branch of `pythonscript.js <https://raw.github.com/amirouche/PythonScript/master/pythonscript.js>`_.

Prepare a app.html file that can look like the following:

.. code-block:: html

   <script src="pythonscript.js" type="text/javascript" charset="utf-8"></script>
   <script src="app.py.js" type="text/javascript" charset="utf-8"></script>

That is all, ``app.py.js`` is the result of the compilation of a ``app.py`` with the following command::

  pythonscript < app.py > app.py.js


.. note:: The following tests can be done in the `online editor <http://apppyjs.appspot.com/>`_.

.. note:: Or you can use the mini `Django project <https://github.com/amirouche/PythonScript/tree/master/demo-django>`_.

.. note:: Whatever route you go you will need `firebug <https://addons.mozilla.org/fr/firefox/addon/firebug/>`_.

Getting feedback
----------------

The old ``print`` statement will be converted to Javascript ``console.log`` which are printed in browser consoles like firebug.

Dealing with variables
----------------------

This is very important! Just like in Javascript you **must** «declare» the variables using the ``var`` function. For instance ``var(spam)``. It can take several arguments ``var(spam, egg, bottle)``. This is because PythonScript use the underlying Javascript variable scope and in Javascript a variable is by default global. The partical consequence is that you **must** declare every usage of a variable *except* if you want to use a global (which seldom happens). Typical code in PythonScript looks like:

.. code-block::

   var(spam, egg, bottle)
   spam = 1
   egg = 2
   bottle = spam + egg


How to work with functions
--------------------------

A function is defined just like in Python:

.. code-block:: python

   def my_function(foo, bar, baz, spam='spam', *args, **kwargs):
       print foo, bar, baz, args, kwargs

   my_function(1,2,3,4,5,spam=6,egg=7)

The above code will print in a browser console the following::

  1 2 3 Object { __class__={...}, __dict__={...}} Object { __class__={...}, __dict__={...}}

A bit cryptic but basically foo, bar, baz are respectively 1, 2, 3 and last two arguments, Javascript objects (but actually PythonScript objects) need more inspection.

Let's define a function that is more verbose:

.. code-block:: python

   def my_function(foo, bar, baz, spam='spam', *args, **kwargs):
       print 'foo', foo
       print 'bar', bar
       print 'baz', baz
       print 'args'
       for arg in args:
           print arg
       print 'kwargs'
       for key in kwargs.keys():
           print kwargs[key]

   my_function(1,2,3,4,5,spam=6,egg=7)

It will print in the browser console the following::

  foo

  1

  bar

  2

  baz

  3

  args

  4

  5

  kwargs

  spam 6

  egg 7

What we expected.

Also, as in Python, functions are objects so you can use them as such.

**Becarful**, ``*args`` and ``**kwargs`` are supported in definition but not in calling, this means that the following:

.. code-block:: python

   args = list()
   kwargs = dict()
   my_function(*args, **kwargs)

Will **not** work.


How to work with classes?
-------------------------

Once functions are done, classes are just a piece of cake, except there is yet no ``__get_attribute__`` or ``__getattr__`` hook it similar to CPython. Data descriptors works the same way. And metaclass is explained in the following paragraph.

.. warning:: You don't have to inherit ``object`` actually there is no ``object`` object in PythonScript yet.


How to use ``__metaclass__`` property?
--------------------------------------

``__metaclass__`` property is used to hook one function into the class creation processus. It's similar to how it's done in Python except it's doesn't support out-of-the-box classes that inherit from type... Whatever here is an example:

.. code-block:: python

   def telekin(self):
       print self.name, 'is telekinesing'


   def higher_level_power(class_name, parents, attrs):
       attrs.telekin = telekin
       return type(class_name, parents, attrs)


   class Person:

       __metaclass__ = higher_level_power

       def __init__(self, name):
           self.name = name

       def walk(self):
           print self.name, 'is walking'


   aria = Person('aria')
   aria.walk()
   aria.telekin()


.. warning:: Right now you need to repeat the ``__metaclass__`` attribute for every class that should be modified ie. the ``__metaclass__`` attribute is not inherited

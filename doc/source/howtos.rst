How to write Python in PythonScript
===================================

How to use PythonScript ?
-------------------------

Install PythonScriptTranslator:

.. code-block:: sh

  pip install PythonJS

And download the latest version on the master branch of `pythonjs.js <https://raw.github.com/PythonJS/PythonJS/master/pythonjs.js>`_.

Prepare a ``app.html`` file that can look like the following:

.. code-block:: html

   <script src="pythonjs.js" type="text/javascript" charset="utf-8"></script>
   <script src="app.py.js" type="text/javascript" charset="utf-8"></script>

That is all, ``app.py.js`` is the result of the compilation of a ``app.py`` with the following command:

.. code-block:: sh

  pythonjs < app.py > app.py.js


Getting feedback
----------------

The old ``print`` statement will be converted to Javascript ``console.log`` which are printed in browser consoles like firebug.


How to work with functions
--------------------------

A function is defined just like in Python:

.. code-block:: python

   def my_function(foo, bar, baz, spam='spam', *args, **kwargs):
       print foo, bar, baz, args, kwargs

   my_function(1,2,3,4,5,spam=6,egg=7)

The above code will print in a browser console the following:

.. code-block:: javascript

  1 2 3 Object { __class__={...}, __dict__={...}} Object { __class__={...}, __dict__={...}}

A bit cryptic but basically foo, bar, baz are respectively 1, 2, 3 and last two arguments, Javascript objects (but actually PythonJS objects) need more inspection.

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

It will print in the browser console the following:

.. code-block:: javascript

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

.. versionchanged:: 0.7
   Added support for ``*`` and ``**`` in calling, pratically it means that given ``args`` a ``list`` and ``kwargs`` a ``dict`` you can use the following call ``function(*args, **kwargs)``.

How to work with classes?
-------------------------

Once functions are done, classes are just a piece of cake, except there is yet no ``__get_attribute__`` but there is a ``__getattr__``. Data descriptors works the same way. And metaclass is explained in the following paragraph.

.. warning:: You don't have to inherit ``object`` actually there is no ``object`` object in PythonJS.


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

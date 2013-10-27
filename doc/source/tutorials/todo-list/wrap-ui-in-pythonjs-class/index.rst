Wrap UI in a PythonJS class
###########################


In the previous article (click the link on top of the page), we showed how to build a simple list using PythonJS and jQuery. This method perfectly works, but it doesn't scale well. As soon as your objects becomes complex, you need to store data somewhere. It happens that jQuery provides a `jQuery.data <http://api.jquery.com/data/>`_ method just for that. The thing is that it doesn't scale, and as soon you need to have methods on the UI element, you need somehow a way to map it to an object... So anyway you end up with what we will start with from the start: *a PythonJS object tree parallel to the HTML elements tree*. Of course HTML elements don't have to map one to one the PythonJS objects.

In this article we will see:

- What the above paragraph means in pratice
- Add a button to be able to set object to done
- Create several todo list on the same page

Initial code
============

``ìndex.html``
--------------

We will start with an index page almost identical to the result of the previous article:

.. literalinclude:: index_.html

Review the changes.

``app.py``
----------

We will start ``app.py`` from scratch!

Wrapping the todo list
======================

.. literalinclude:: todo-list.py

That is all!

You only need to add... the following to the end of ``app.py``:

.. code-block:: python

   NORMAL_TODOS = TodoList("#todo-normal")

Changing tasks status
=====================

Update ``TodoItem`` class with the following code:

.. literalinclude:: todo-item.py

You will have a new button on todo items that allows to change their status.

Several todo lists
==================

To have several to do list you just need to duplicate the html code and replace the id by something revelant. And instantiate a TodoList with the correct parameter.

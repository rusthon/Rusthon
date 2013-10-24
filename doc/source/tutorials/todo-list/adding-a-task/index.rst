Adding a task
#############

In what follows we will setup an application that allows the user to create a list of tasks.

Getting started
===============

First install PythonJS for Python 2.7 in a virtualenv if you want::

  pip install PythonJS

Then setup a directory to hold all the files::

  mkdir todo-list
  cd todo-list
  touch index.html
  touch app.css
  touch app.py
  wget http://code.jquery.com/jquery-2.0.3.min.js -O jquery.js
  wget https://raw.github.com/PythonJS/PythonJS/master/pythonjs.js

Now open the ``index.html`` file and add the following minimal code to the page:

.. literalinclude:: minimal.html

Open ``app.py`` and add the following code::

  print 'Héllo World'

Compile ``app.py`` with the following command::

  pythonjs < app.py > app.js

Open ``index.html`` in your favorite browser and open the console from developper tools or 
firebug, ``Héllo World`` must appear in the console, reload if necessary.


Setting up the view
===================

Copy past the following code to the top of the ``index.html`` file:

.. literalinclude:: view.html

Check in the browser that it's correctly rendered.

Adding a task
=============

In the following we will use jQuery and the ability to call javascript code directly inside Python code. There is no mistery to be able to do frontend development you need to know `jQuery API <http://api.jquery.com/>`_ or the DOM API.

The first way to use the ``jQuery`` object is to select objects, for instance the following::

  a = jQuery("#tasks")

.. warning:: always use double quotes to create string literals

Will retrieve all elements which have an ``id`` equal to ``tasks``. Check out the `selector reference <http://www.w3.org/TR/CSS2/selector.html>`_ if you don't know css selectors. In this case ``a`` will contain the ``ul`` element from the page.

Selectors can be very complex or midly complex, like the following::

  input = jQuery("input[type='text']")

The above will select the ``input`` html element that has the attribute ``type`` equal to ``text``. We also need to bind the click event on the submit button::

  submit = jQuery("input[type='submit']")

When the ``submit`` is clicked is express as follow::

  submit.click(on_add)

Which means: Execute ``on_add`` when submit is cliked. We define ``on_add`` as follow::

  def on_add():
      input = jQuery("input[type='text']")
      task = input.val()  # fetch the value of the input
      if task:
          # if it's not empty add it to the list
	  tasks = jQuery('#tasks')
	  tasks.append("<li>" + task + "</li>")
	  # empty the input field
	  input.val('')

``submit.click(on_add)`` must appear after ``on_add`` definition of course. If everything looks right, compile ``app.py`` with the usual command::

  pythonjs < app.py > app.js

Reload the browser page and try to add a task. It must appear after the other tasks that are already present. The next step is to remove those tasks from the html file so that the page loads with an empty list of tasks. Do it, reload the page, and try to add a task.

Solutions
=========

``index.html``
--------------

.. literalinclude:: index_.html


``app.py``
----------

.. literalinclude:: app.py

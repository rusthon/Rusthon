How to use Pythonjs with Django
###################################

Pythonjs is compatible with Django and more precisly with Django compressor which takes great advantage of its support of preprocessors

So what you need is Django and django-compressor:

.. code-block:: sh

   pip install PythonJS django django_compressor

Following `django compressor documentation <http://django-compressor.readthedocs.org/en/latest/quickstart/#installation>`_
you need to add ``compressor`` to the list of installed apps:

.. code-block:: python

   INSTALLED_APPS = (
        # other apps
        "compressor",
   )

In case you use Django’s staticfiles contrib app (or its standalone counterpart django-staticfiles) you have to add Django Compressor’s file finder to the ``STATICFILES_FINDERS`` setting, for example with ``django.contrib.staticfiles``:

.. code-block:: python

   STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
   )

Once this is done configure ``COMPRESS_PRECOMPILERS`` like it is explained `the documentation <http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_PRECOMPILERS>`_ with ``pythonjs`` command. You will end up with something similar to the following:

.. code-block:: python

   COMPRESS_PRECOMPILERS = ( ('text/pythonjs', 'pythonjs < {infile} > {outfile}'), )

Then you can include pythonjs files in the templates using a snippet similar to the following:

.. code-block:: html

   {% compress %}<script type="text/pythonjs" charset="utf-8" src="/static/py/app.py" />{% endcompress %}

Or you can try the demo `django project <https://github.com/Pythonjs/PythonJS/tree/master/django-demo>`_.

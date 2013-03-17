from setuptools import setup


setup(
    name='PythonScript',
    version='0.1',
    description='Python compiler for the browser',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='',
    zip_safe=False,
    packages=['pythonscript'],
    entry_points="""
    [console_scripts]
    pythonscript=pythonscript.main:main
    pythonjs=pythonscript.pythonjs:main
    """
)

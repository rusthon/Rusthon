from setuptools import setup


setup(
    name='PythonScriptTranslator',
    version='0.3',
    description='Python compiler for the browser',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/amirouche/PythonScript',
    zip_safe=False,
    packages=['pythonscript'],
    entry_points="""
    [console_scripts]
    pythonscript=pythonscript.main:main
    pythonjs=pythonscript.pythonjs:main
    """
)

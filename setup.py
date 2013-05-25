from setuptools import setup


setup(
    name='PythonScriptTranslator',
    version='0.7.2',
    description='Python translator for the browser',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/amirouche/PythonScript',
    zip_safe=False,
    packages=['pythonscript'],
    entry_points="""
    [console_scripts]
    pythonjs=pythonscript.pythonjs:main
    pythonscript=pythonscript.main:command
    python_to_pythonjs=pythonscript.python_to_pythonjs:command
    """,
    install_script='bin/pythonscript',
)

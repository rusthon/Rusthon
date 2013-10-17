from setuptools import setup


setup(
    name='PythonJS',
    version='0.8.1',
    description='Python translator for the browser',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/PythonScript-/PythonJS.git',
    zip_safe=False,
    packages=['pythonscript'],
    entry_points="""
    [console_scripts]
    pythonjs=pythonscript.pythonjs:main
    pythonscript=pythonscript.pythonscript:command
    python_to_pythonjs=pythonscript.python_to_pythonjs:command
    """,
    install_script='bin/pythonscript',
)

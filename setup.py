from setuptools import setup


setup(
    name='PythonJS',
    version='0.8.2',
    description='Python translator for the browser',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/PythonJS/PythonJS.git',
    zip_safe=False,
    packages=['pythonjs'],
    entry_points="""
    [console_scripts]
    rpythonjs=pythonjs.pythonjs:main
    pythonjs=pythonjs.pythonscript:command
    python_to_rpythonjs=pythonjs.python_to_pythonjs:command
    """,
    install_script='bin/pythonjs',
)

all: jquery pythonscript

jquery:
	./pythonscript/main.py < bindings/jquery.py > bindings/jquery.py.js

builtins:
	./pythonscript/main.py < builtins.py > builtins.py.js

python:
	./pythonscript/pythonjs.py < pythonscript/pythonpythonjs.py > python.js

pythonscript: python builtins
	cat python.js builtins.py.js > pythonscript.js

clean:
	rm python.js builtins.py.js pythonscript.js bindings/*py.js

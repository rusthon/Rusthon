CMD=pythonscript/pythonscript.py

all: jquery pythonscript

jquery:
	$(CMD) < bindings/jquery.py > bindings/jquery.py.js

builtins:
	$(CMD) < runtime/builtins.py > builtins.py.js

python:
	./pythonscript/pythonjs.py < runtime/pythonpythonjs.py > python.js

pythonscript: python builtins
	cat python.js builtins.py.js > pythonscript.js

clean:
	rm python.js builtins.py.js pythonscript.js bindings/*py.js

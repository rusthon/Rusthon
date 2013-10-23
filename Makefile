CMD=pythonjs/pythonscript.py

all: pythonjs

builtins:
	$(CMD) < runtime/builtins.py > builtins.py.js

python:
	./pythonjs/pythonjs.py < runtime/pythonpythonjs.py > python.js

pythonjs: python builtins
	cat python.js builtins.py.js > pythonjs.js

clean:
	rm python.js builtins.py.js pythonscript.js bindings/*py.js

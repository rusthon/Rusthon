all: python.js


python.js:
	./pythonjs.py < pythonpythonjs.py > ../python.js

clean:
	rm ../python.js || echo "no python.js"

test:
	cat test.py
	./main.py < test.py > test.py.js
	cat test.py.js

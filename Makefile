all: build_pythonscript build_bindings

build_pythonscript:
	cd pythonscript && make

build_bindings:
	cd bindings && make

clean:
	(cd bindings && make clean)
	(cd pythonscript && make clean)

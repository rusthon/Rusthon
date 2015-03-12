Rusthon
-------

* @link:python2.7
* @include:Python.h
```rusthon
#backend:c++

with pointers:
	def unbox( pyob:PyObject ) -> int:
		a = PyInt_AS_INT(pyob)
		return a

def main():
	Py_Initialize()
	PyRun_SimpleString("result = 1+2")
	mod = PyImport_AddModule("__main__")
	dict = PyModule_GetDict(mod)
	result = PyDict_GetItemString(dict, "result")
	x = unbox( result )
	print x
	Py_Finalize()

```
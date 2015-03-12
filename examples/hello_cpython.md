Embed CPython
-------
The syntax below `* @link:` allows you to list external pre-built libraries to link to.
The syntax `* @include:` allows you to list directories for GCC to find external header files,
and include them in the final build using `import myheader.h`.

note requires: static library `libpython.a`


* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import Python.h

with pointers:
	def unbox( pyob:PyObject ) -> int:
		a = PyInt_AS_LONG(pyob)
		return a as int

def main():
	Py_Initialize()
	PyRun_SimpleString(cstr("result = 1+2"))
	mod = PyImport_AddModule(cstr("__main__"))
	mdict = PyModule_GetDict(mod)
	result = PyDict_GetItemString(mdict, cstr("result"))
	x = unbox( result )
	print x
	Py_Finalize()

```
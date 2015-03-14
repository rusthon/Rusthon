Cpython C-API
--------

```python

CPYTHON_HEAD = '''
#include <Python.h>

PyThreadState* __cpython_initalize__(void) {
	Py_Initialize();
	PyEval_InitThreads();
	PyRun_SimpleString(__python_main_script__);
	return PyEval_SaveThread();
}
void __cpython_finalize__(PyThreadState* state) {
	PyEval_RestoreThread( state );
	Py_Finalize();
}
PyObject* __cpython_get__(const char* name) {
	auto mod = PyImport_AddModule("__main__");
	auto dict = PyModule_GetDict(mod);
	return PyDict_GetItemString(dict, name);
}
PyObject* __cpython_call__(const char* name) {
	auto empty_tuple = Py_BuildValue("()");
	return PyObject_Call(__cpython_get__(name), empty_tuple, NULL);
}

'''

def gen_cpython_header():
	return CPYTHON_HEAD

```
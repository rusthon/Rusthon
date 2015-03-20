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
	auto mod  = PyImport_AddModule("__main__");
	auto dict = PyModule_GetDict(mod);
	auto ptr  = PyDict_GetItemString(dict, name);
	if (ptr==nullptr) {
		std::cout << "checking __builtins__" << std::endl;
		std::cout << name << std::endl;
		auto bmod  = PyImport_AddModule("__builtins__");
		auto bdict = PyModule_GetDict(bmod);
		auto bptr  = PyDict_GetItemString(bdict, name);
		if (bptr==nullptr) {
			std::cout << "ERROR" << std::endl;
		} else {
			return bptr;
		}

	} else {
		return ptr;
	}
}
PyObject* __cpython_call__(const char* name) {
	auto empty_tuple = Py_BuildValue("()");
	return PyObject_Call(__cpython_get__(name), empty_tuple, NULL);
}

'''

def gen_cpython_header():
	return CPYTHON_HEAD


class CPythonGenerator:
	def gen_cpython_helpers(self):
		header = []
		if 'hasattr' in self._called_functions:
			header.append('bool hasattr(PyObject* o, std::string s) { return PyObject_HasAttrString(o,s.c_str());} ')
		if 'getattr' in self._called_functions:
			header.append('PyObject* getattr(PyObject* o, std::string s) { return PyObject_GetAttrString(o,s.c_str());} ')
		if 'setattr' in self._called_functions:
			header.append('void setattr(PyObject* o, std::string s, PyObject* v) { PyObject_SetAttrString(o,s.c_str(),v);} ')
		if 'str' in self._called_functions:
			header.append('std::string str(PyObject* o) { return std::string( PyString_AS_STRING(PyObject_Str(o)) );} ')
		if 'ispyinstance' in self._called_functions:
			header.append('bool ispyinstance(PyObject* o, std::string s) {')
			##header.append(' return PyObject_IsInstance(o, __cpython_get__(s.c_str()));} ')  ## TODO fix
			header.append('  if ( std::string(PyString_AS_STRING(PyObject_GetAttrString((PyObject*)o->ob_type, "__name__")))==s ) { return true; }')
			header.append('  else { return false; }')
			header.append('} ')
		if 'pytype' in self._called_functions:
			header.append('std::string pytype(PyObject* o) { return std::string(PyString_AS_STRING(PyObject_GetAttrString((PyObject*)o->ob_type, "__name__")));} ')

		return '\n'.join(header)

```
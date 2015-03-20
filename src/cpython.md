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

CPYTHON_ISPYINSTANCE = '''
bool ispyinstance(PyObject* pyob, std::string classname) {
	// TODO: PyObject_IsInstance(pyob, pyobclass)
	// the problem with directly using `ob_type` and reading `__name__` is object instances are "instance",
	// and not the name of the class.  For now we simply just check the class name without any namespace `o.__class__.__name__`
	//auto name = std::string(PyString_AS_STRING(PyObject_GetAttrString((PyObject*)pyob->ob_type, "__name__")));
	//if ( name==std::string("instance")) {
	//	auto classob = PyObject_GetAttrString(pyob, "__class__");
	//	name = std::string(PyString_AS_STRING(PyObject_GetAttrString((PyObject*)classob->ob_type, "__name__")));
	//}
	auto name = std::string(PyString_AS_STRING(PyObject_GetAttrString(PyObject_GetAttrString(pyob,"__class__"), "__name__")));
	if ( name==classname ) { return true; }
	else { return false; }
}
'''

CPYTHON_PYTYPE = '''
std::string pytype(PyObject* pyob) { 
	return std::string(PyString_AS_STRING(PyObject_GetAttrString(PyObject_GetAttrString(pyob,"__class__"), "__name__")));
}
'''

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
			header.append( CPYTHON_ISPYINSTANCE )
		if 'pytype' in self._called_functions:
			header.append( CPYTHON_PYTYPE )

		return '\n'.join(header)

```
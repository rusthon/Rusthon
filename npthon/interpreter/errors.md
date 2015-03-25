errors.c
-----------


@errors.c
```c
```

Error handling

```c
#include "Python.h"
#ifndef __STDC__
#ifndef MS_WINDOWS
extern char *strerror(int);
#endif
#endif
#ifdef MS_WINDOWS
#include "windows.h"
#include "winbase.h"
#endif
#include <ctype.h>
#ifdef __cplusplus
extern "C" {
#endif
void
PyErr_Restore(PyObject *type, PyObject *value, PyObject *traceback)
{
    PyThreadState *tstate = PyThreadState_GET();
    PyObject *oldtype, *oldvalue, *oldtraceback;
    if (traceback != NULL && !PyTraceBack_Check(traceback)) {
```

XXX Should never happen -- fatal error instead?

```c
```

Well, it could be None.

```c
        Py_DECREF(traceback);
        traceback = NULL;
    }
```

>invocation through Py_XDECREF

```c
    oldtype = tstate->curexc_type;
    oldvalue = tstate->curexc_value;
    oldtraceback = tstate->curexc_traceback;
    tstate->curexc_type = type;
    tstate->curexc_value = value;
    tstate->curexc_traceback = traceback;
    Py_XDECREF(oldtype);
    Py_XDECREF(oldvalue);
    Py_XDECREF(oldtraceback);
}
void
PyErr_SetObject(PyObject *exception, PyObject *value)
{
    Py_XINCREF(exception);
    Py_XINCREF(value);
    PyErr_Restore(exception, value, (PyObject *)NULL);
}
void
PyErr_SetNone(PyObject *exception)
{
    PyErr_SetObject(exception, (PyObject *)NULL);
}
void
PyErr_SetString(PyObject *exception, const char *string)
{
    PyObject *value = PyString_FromString(string);
    PyErr_SetObject(exception, value);
    Py_XDECREF(value);
}
PyObject *
PyErr_Occurred(void)
{
    PyThreadState *tstate = PyThreadState_GET();
    return tstate->curexc_type;
}
int
PyErr_GivenExceptionMatches(PyObject *err, PyObject *exc)
{
    if (err == NULL || exc == NULL) {
```

maybe caused by "import exceptions" that failed early on

```c
        return 0;
    }
    if (PyTuple_Check(exc)) {
        Py_ssize_t i, n;
        n = PyTuple_Size(exc);
        for (i = 0; i < n; i++) {
```

Test recursively

```c
             if (PyErr_GivenExceptionMatches(
                 err, PyTuple_GET_ITEM(exc, i)))
             {
                 return 1;
             }
        }
        return 0;
    }
```

err might be an instance, so check its class.

```c
    if (PyExceptionInstance_Check(err))
        err = PyExceptionInstance_Class(err);
    if (PyExceptionClass_Check(err) && PyExceptionClass_Check(exc)) {
        int res = 0, reclimit;
        PyObject *exception, *value, *tb;
        PyErr_Fetch(&exception, &value, &tb);
```

common case PyObject_IsSubclass will not raise a recursion
error we have to ignore anyway.  Don't do it when the limit
>is already insanely high, to avoid overflow

```c
        reclimit = Py_GetRecursionLimit();
        if (reclimit < (1 << 30))
            Py_SetRecursionLimit(reclimit + 5);
        res = PyObject_IsSubclass(err, exc);
        Py_SetRecursionLimit(reclimit);
```

This function must not fail, so print the error here

```c
        if (res == -1) {
            PyErr_WriteUnraisable(err);
            res = 0;
        }
        PyErr_Restore(exception, value, tb);
        return res;
    }
    return err == exc;
}
int
PyErr_ExceptionMatches(PyObject *exc)
{
    return PyErr_GivenExceptionMatches(PyErr_Occurred(), exc);
}
```

eval_code2(), do_raise(), and PyErr_Print()

```c
void
PyErr_NormalizeException(PyObject **exc, PyObject **val, PyObject **tb)
{
    PyObject *type = *exc;
    PyObject *value = *val;
    PyObject *inclass = NULL;
    PyObject *initial_tb = NULL;
    PyThreadState *tstate = NULL;
    if (type == NULL) {
```

There was no exception, so nothing to do.

```c
        return;
    }
```

set to NULL.

```c
    if (!value) {
        value = Py_None;
        Py_INCREF(value);
    }
    if (PyExceptionInstance_Check(value))
        inclass = PyExceptionInstance_Class(value);
```

value will be an instance.

```c
    if (PyExceptionClass_Check(type)) {
```

whose class is (or is derived from) type, then use the
value as an argument to instantiation of the type
class.

```c
        if (!inclass || !PyObject_IsSubclass(inclass, type)) {
            PyObject *args, *res;
            if (value == Py_None)
                args = PyTuple_New(0);
            else if (PyTuple_Check(value)) {
                Py_INCREF(value);
                args = value;
            }
            else
                args = PyTuple_Pack(1, value);
            if (args == NULL)
                goto finally;
            res = PyEval_CallObject(type, args);
            Py_DECREF(args);
            if (res == NULL)
                goto finally;
            Py_DECREF(value);
            value = res;
        }
```

class of the type, believe the instance

```c
        else if (inclass != type) {
            Py_DECREF(type);
            type = inclass;
            Py_INCREF(type);
        }
    }
    *exc = type;
    *val = value;
    return;
finally:
    Py_DECREF(type);
    Py_DECREF(value);
```

exception had a traceback, use the old traceback for the
new exception.  It's better than nothing.

```c
    initial_tb = *tb;
    PyErr_Fetch(exc, val, tb);
    if (initial_tb != NULL) {
        if (*tb == NULL)
            *tb = initial_tb;
        else
            Py_DECREF(initial_tb);
    }
```

normalize recursively

```c
    tstate = PyThreadState_GET();
    if (++tstate->recursion_depth > Py_GetRecursionLimit()) {
        --tstate->recursion_depth;
```

throw away the old exception...

```c
        Py_DECREF(*exc);
        Py_DECREF(*val);
```

... and use the recursion error instead

```c
        *exc = PyExc_RuntimeError;
        *val = PyExc_RecursionErrorInst;
        Py_INCREF(*exc);
        Py_INCREF(*val);
```

just keeping the old traceback

```c
        return;
    }
    PyErr_NormalizeException(exc, val, tb);
    --tstate->recursion_depth;
}
void
PyErr_Fetch(PyObject **p_type, PyObject **p_value, PyObject **p_traceback)
{
    PyThreadState *tstate = PyThreadState_GET();
    *p_type = tstate->curexc_type;
    *p_value = tstate->curexc_value;
    *p_traceback = tstate->curexc_traceback;
    tstate->curexc_type = NULL;
    tstate->curexc_value = NULL;
    tstate->curexc_traceback = NULL;
}
void
PyErr_Clear(void)
{
    PyErr_Restore(NULL, NULL, NULL);
}
```

Convenience functions to set a type error exception and return 0

```c
int
PyErr_BadArgument(void)
{
    PyErr_SetString(PyExc_TypeError,
                    "bad argument type for built-in operation");
    return 0;
}
PyObject *
PyErr_NoMemory(void)
{
    if (PyErr_ExceptionMatches(PyExc_MemoryError))
```

already current

```c
        return NULL;
```

raise the pre-allocated instance if it still exists

```c
    if (PyExc_MemoryErrorInst)
        PyErr_SetObject(PyExc_MemoryError, PyExc_MemoryErrorInst);
    else
```

hee, we have to instantiate this class

```c
        PyErr_SetNone(PyExc_MemoryError);
    return NULL;
}
PyObject *
PyErr_SetFromErrnoWithFilenameObject(PyObject *exc, PyObject *filenameObject)
{
    PyObject *v;
    char *s;
    int i = errno;
#ifdef PLAN9
    char errbuf[ERRMAX];
#endif
#ifdef MS_WINDOWS
    char *s_buf = NULL;
    char s_small_buf[28]; /* Room for "Windows Error 0xFFFFFFFF" */
#endif
#ifdef EINTR
    if (i == EINTR && PyErr_CheckSignals())
        return NULL;
#endif
#ifdef PLAN9
    rerrstr(errbuf, sizeof errbuf);
    s = errbuf;
#else
    if (i == 0)
        s = "Error"; /* Sometimes errno didn't get set */
    else
#ifndef MS_WINDOWS
        s = strerror(i);
#else
    {
```

errno error.  So if the error is in the MSVC error
table, we use it, otherwise we assume it really _is_
a Win32 error code

```c
        if (i > 0 && i < _sys_nerr) {
            s = _sys_errlist[i];
        }
        else {
            int len = FormatMessage(
                FORMAT_MESSAGE_ALLOCATE_BUFFER |
                FORMAT_MESSAGE_FROM_SYSTEM |
                FORMAT_MESSAGE_IGNORE_INSERTS,
                NULL,                   /* no message source */
                i,
                MAKELANGID(LANG_NEUTRAL,
                           SUBLANG_DEFAULT),
```

Default language

```c
                (LPTSTR) &s_buf,
                0,                      /* size not used */
                NULL);                  /* no args */
            if (len==0) {
```

>situations

```c
                sprintf(s_small_buf, "Windows Error 0x%X", i);
                s = s_small_buf;
                s_buf = NULL;
            } else {
                s = s_buf;
```

remove trailing cr/lf and dots

```c
                while (len > 0 && (s[len-1] <= ' ' || s[len-1] == '.'))
                    s[--len] = '\0';
            }
        }
    }
#endif /* Unix/Windows */
#endif /* PLAN 9*/
    if (filenameObject != NULL)
        v = Py_BuildValue("(isO)", i, s, filenameObject);
    else
        v = Py_BuildValue("(is)", i, s);
    if (v != NULL) {
        PyErr_SetObject(exc, v);
        Py_DECREF(v);
    }
#ifdef MS_WINDOWS
    LocalFree(s_buf);
#endif
    return NULL;
}
PyObject *
PyErr_SetFromErrnoWithFilename(PyObject *exc, const char *filename)
{
    PyObject *name = filename ? PyString_FromString(filename) : NULL;
    PyObject *result = PyErr_SetFromErrnoWithFilenameObject(exc, name);
    Py_XDECREF(name);
    return result;
}
#ifdef MS_WINDOWS
PyObject *
PyErr_SetFromErrnoWithUnicodeFilename(PyObject *exc, const Py_UNICODE *filename)
{
    PyObject *name = filename ?
                     PyUnicode_FromUnicode(filename, wcslen(filename)) :
             NULL;
    PyObject *result = PyErr_SetFromErrnoWithFilenameObject(exc, name);
    Py_XDECREF(name);
    return result;
}
#endif /* MS_WINDOWS */
PyObject *
PyErr_SetFromErrno(PyObject *exc)
{
    return PyErr_SetFromErrnoWithFilenameObject(exc, NULL);
}
#ifdef MS_WINDOWS
```

Windows specific error code handling

```c
PyObject *PyErr_SetExcFromWindowsErrWithFilenameObject(
    PyObject *exc,
    int ierr,
    PyObject *filenameObject)
{
    int len;
    char *s;
    char *s_buf = NULL; /* Free via LocalFree */
    char s_small_buf[28]; /* Room for "Windows Error 0xFFFFFFFF" */
    PyObject *v;
    DWORD err = (DWORD)ierr;
    if (err==0) err = GetLastError();
    len = FormatMessage(
```

Error API error

```c
        FORMAT_MESSAGE_ALLOCATE_BUFFER |
        FORMAT_MESSAGE_FROM_SYSTEM |
        FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL,           /* no message source */
        err,
        MAKELANGID(LANG_NEUTRAL,
        SUBLANG_DEFAULT), /* Default language */
        (LPTSTR) &s_buf,
        0,              /* size not used */
        NULL);          /* no args */
    if (len==0) {
```

Only seen this in out of mem situations

```c
        sprintf(s_small_buf, "Windows Error 0x%X", err);
        s = s_small_buf;
        s_buf = NULL;
    } else {
        s = s_buf;
```

remove trailing cr/lf and dots

```c
        while (len > 0 && (s[len-1] <= ' ' || s[len-1] == '.'))
            s[--len] = '\0';
    }
    if (filenameObject != NULL)
        v = Py_BuildValue("(isO)", err, s, filenameObject);
    else
        v = Py_BuildValue("(is)", err, s);
    if (v != NULL) {
        PyErr_SetObject(exc, v);
        Py_DECREF(v);
    }
    LocalFree(s_buf);
    return NULL;
}
PyObject *PyErr_SetExcFromWindowsErrWithFilename(
    PyObject *exc,
    int ierr,
    const char *filename)
{
    PyObject *name = filename ? PyString_FromString(filename) : NULL;
    PyObject *ret = PyErr_SetExcFromWindowsErrWithFilenameObject(exc,
                                                                 ierr,
                                                                 name);
    Py_XDECREF(name);
    return ret;
}
PyObject *PyErr_SetExcFromWindowsErrWithUnicodeFilename(
    PyObject *exc,
    int ierr,
    const Py_UNICODE *filename)
{
    PyObject *name = filename ?
                     PyUnicode_FromUnicode(filename, wcslen(filename)) :
             NULL;
    PyObject *ret = PyErr_SetExcFromWindowsErrWithFilenameObject(exc,
                                                                 ierr,
                                                                 name);
    Py_XDECREF(name);
    return ret;
}
PyObject *PyErr_SetExcFromWindowsErr(PyObject *exc, int ierr)
{
    return PyErr_SetExcFromWindowsErrWithFilename(exc, ierr, NULL);
}
PyObject *PyErr_SetFromWindowsErr(int ierr)
{
    return PyErr_SetExcFromWindowsErrWithFilename(PyExc_WindowsError,
                                                  ierr, NULL);
}
PyObject *PyErr_SetFromWindowsErrWithFilename(
    int ierr,
    const char *filename)
{
    PyObject *name = filename ? PyString_FromString(filename) : NULL;
    PyObject *result = PyErr_SetExcFromWindowsErrWithFilenameObject(
                                                  PyExc_WindowsError,
                                                  ierr, name);
    Py_XDECREF(name);
    return result;
}
PyObject *PyErr_SetFromWindowsErrWithUnicodeFilename(
    int ierr,
    const Py_UNICODE *filename)
{
    PyObject *name = filename ?
                     PyUnicode_FromUnicode(filename, wcslen(filename)) :
             NULL;
    PyObject *result = PyErr_SetExcFromWindowsErrWithFilenameObject(
                                                  PyExc_WindowsError,
                                                  ierr, name);
    Py_XDECREF(name);
    return result;
}
#endif /* MS_WINDOWS */
void
_PyErr_BadInternalCall(char *filename, int lineno)
{
    PyErr_Format(PyExc_SystemError,
                 "%s:%d: bad argument to internal function",
                 filename, lineno);
}
```

>export the entry point for existing object code:

```c
#undef PyErr_BadInternalCall
void
PyErr_BadInternalCall(void)
{
    PyErr_Format(PyExc_SystemError,
                 "bad argument to internal function");
}
#define PyErr_BadInternalCall() _PyErr_BadInternalCall(__FILE__, __LINE__)
PyObject *
PyErr_Format(PyObject *exception, const char *format, ...)
{
    va_list vargs;
    PyObject* string;
#ifdef HAVE_STDARG_PROTOTYPES
    va_start(vargs, format);
#else
    va_start(vargs);
#endif
    string = PyString_FromFormatV(format, vargs);
    PyErr_SetObject(exception, string);
    Py_XDECREF(string);
    va_end(vargs);
    return NULL;
}
PyObject *
PyErr_NewException(char *name, PyObject *base, PyObject *dict)
{
    char *dot;
    PyObject *modulename = NULL;
    PyObject *classname = NULL;
    PyObject *mydict = NULL;
    PyObject *bases = NULL;
    PyObject *result = NULL;
    dot = strrchr(name, '.');
    if (dot == NULL) {
        PyErr_SetString(PyExc_SystemError,
            "PyErr_NewException: name must be module.class");
        return NULL;
    }
    if (base == NULL)
        base = PyExc_Exception;
    if (dict == NULL) {
        dict = mydict = PyDict_New();
        if (dict == NULL)
            goto failure;
    }
    if (PyDict_GetItemString(dict, "__module__") == NULL) {
        modulename = PyString_FromStringAndSize(name,
                                             (Py_ssize_t)(dot-name));
        if (modulename == NULL)
            goto failure;
        if (PyDict_SetItemString(dict, "__module__", modulename) != 0)
            goto failure;
    }
    if (PyTuple_Check(base)) {
        bases = base;
```

INCREF as we create a new ref in the else branch

```c
        Py_INCREF(bases);
    } else {
        bases = PyTuple_Pack(1, base);
        if (bases == NULL)
            goto failure;
    }
```

Create a real new-style class.

```c
    result = PyObject_CallFunction((PyObject *)&PyType_Type, "sOO",
                                   dot+1, bases, dict);
  failure:
    Py_XDECREF(bases);
    Py_XDECREF(mydict);
    Py_XDECREF(classname);
    Py_XDECREF(modulename);
    return result;
}
```

Create an exception with docstring

```c
PyObject *
PyErr_NewExceptionWithDoc(char *name, char *doc, PyObject *base, PyObject *dict)
{
    int result;
    PyObject *ret = NULL;
    PyObject *mydict = NULL; /* points to the dict only if we create it */
    PyObject *docobj;
    if (dict == NULL) {
        dict = mydict = PyDict_New();
        if (dict == NULL) {
            return NULL;
        }
    }
    if (doc != NULL) {
        docobj = PyString_FromString(doc);
        if (docobj == NULL)
            goto failure;
        result = PyDict_SetItemString(dict, "__doc__", docobj);
        Py_DECREF(docobj);
        if (result < 0)
            goto failure;
    }
    ret = PyErr_NewException(name, base, dict);
  failure:
    Py_XDECREF(mydict);
    return ret;
}
```

>to handle it.  Examples: exception in __del__ or during GC.

```c
void
PyErr_WriteUnraisable(PyObject *obj)
{
    PyObject *f, *t, *v, *tb;
    PyErr_Fetch(&t, &v, &tb);
    f = PySys_GetObject("stderr");
    if (f != NULL) {
        PyFile_WriteString("Exception ", f);
        if (t) {
            PyObject* moduleName;
            char* className;
            assert(PyExceptionClass_Check(t));
            className = PyExceptionClass_Name(t);
            if (className != NULL) {
                char *dot = strrchr(className, '.');
                if (dot != NULL)
                    className = dot+1;
            }
            moduleName = PyObject_GetAttrString(t, "__module__");
            if (moduleName == NULL)
                PyFile_WriteString("<unknown>", f);
            else {
                char* modstr = PyString_AsString(moduleName);
                if (modstr &&
                    strcmp(modstr, "exceptions") != 0)
                {
                    PyFile_WriteString(modstr, f);
                    PyFile_WriteString(".", f);
                }
            }
            if (className == NULL)
                PyFile_WriteString("<unknown>", f);
            else
                PyFile_WriteString(className, f);
            if (v && v != Py_None) {
                PyFile_WriteString(": ", f);
                PyFile_WriteObject(v, f, 0);
            }
            Py_XDECREF(moduleName);
        }
        PyFile_WriteString(" in ", f);
        PyFile_WriteObject(obj, f, 0);
        PyFile_WriteString(" ignored\n", f);
        PyErr_Clear(); /* Just in case */
    }
    Py_XDECREF(t);
    Py_XDECREF(v);
    Py_XDECREF(tb);
}
extern PyObject *PyModule_GetWarningsModule(void);
```

If the exception is not a SyntaxError, also sets additional attributes
>to make printing of exceptions believe it is a syntax error.

```c
void
PyErr_SyntaxLocation(const char *filename, int lineno)
{
    PyObject *exc, *v, *tb, *tmp;
```

add attributes for the line number and filename for the error

```c
    PyErr_Fetch(&exc, &v, &tb);
    PyErr_NormalizeException(&exc, &v, &tb);
```

>* be, though.

```c
    tmp = PyInt_FromLong(lineno);
    if (tmp == NULL)
        PyErr_Clear();
    else {
        if (PyObject_SetAttrString(v, "lineno", tmp))
            PyErr_Clear();
        Py_DECREF(tmp);
    }
    if (filename != NULL) {
        tmp = PyString_FromString(filename);
        if (tmp == NULL)
            PyErr_Clear();
        else {
            if (PyObject_SetAttrString(v, "filename", tmp))
                PyErr_Clear();
            Py_DECREF(tmp);
        }
        tmp = PyErr_ProgramText(filename, lineno);
        if (tmp) {
            if (PyObject_SetAttrString(v, "text", tmp))
                PyErr_Clear();
            Py_DECREF(tmp);
        }
    }
    if (PyObject_SetAttrString(v, "offset", Py_None)) {
        PyErr_Clear();
    }
    if (exc != PyExc_SyntaxError) {
        if (!PyObject_HasAttrString(v, "msg")) {
            tmp = PyObject_Str(v);
            if (tmp) {
                if (PyObject_SetAttrString(v, "msg", tmp))
                    PyErr_Clear();
                Py_DECREF(tmp);
            } else {
                PyErr_Clear();
            }
        }
        if (!PyObject_HasAttrString(v, "print_file_and_line")) {
            if (PyObject_SetAttrString(v, "print_file_and_line",
                                       Py_None))
                PyErr_Clear();
        }
    }
    PyErr_Restore(exc, v, tb);
}
```

the exception refers to.  If it fails, it will return NULL but will
not set an exception.
XXX The functionality of this function is quite similar to the
functionality in tb_displayline() in traceback.c.

```c
PyObject *
PyErr_ProgramText(const char *filename, int lineno)
{
    FILE *fp;
    int i;
    char linebuf[1000];
    if (filename == NULL || *filename == '\0' || lineno <= 0)
        return NULL;
    fp = fopen(filename, "r" PY_STDIOTEXTMODE);
    if (fp == NULL)
        return NULL;
    for (i = 0; i < lineno; i++) {
        char *pLastChar = &linebuf[sizeof(linebuf) - 2];
        do {
            *pLastChar = '\0';
            if (Py_UniversalNewlineFgets(linebuf, sizeof linebuf, fp, NULL) == NULL)
                break;
```

far as pLastChar, it must have found a newline
or hit the end of the file; if pLastChar is \n,
it obviously found a newline; else we haven't
>yet seen a newline, so must continue

```c
        } while (*pLastChar != '\0' && *pLastChar != '\n');
    }
    fclose(fp);
    if (i == lineno) {
        char *p = linebuf;
        while (*p == ' ' || *p == '\t' || *p == '\014')
            p++;
        return PyString_FromString(p);
    }
    return NULL;
}
#ifdef __cplusplus
}
#endif
```
___
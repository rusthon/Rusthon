Nim C API
---------

imported by [cpptranslator.md](cpptranslator.md)

This supports user code using `import nim` and `nim.main()`, see example here:
https://github.com/rusthon/Rusthon/blob/master/examples/hello_nim.md

TODO: test `GC_ref(result)` and `GC_unref`

```python

NIM_HEADER = '''
extern "C" {
	void PreMain();
	void NimMain();
}

'''

def gen_nim_header():
	return NIM_HEADER

```
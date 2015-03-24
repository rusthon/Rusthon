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


def hack_nim_code(code):
	'''
	this is required because nim outputs multiple c files that we merge into a single c file,
	some functions in stdlib_system.c are inlined into the main code here, and they must be removed.
	'''
	out = []
	skip_structs = ['TGenericSeq', 'NimStringDesc']
	skip_struct = False
	skip_inline = False

	for line in code.splitlines():
		if line.startswith('static N_INLINE('):
			#if 'nimFrame' in line or 'popFrame' in line or 'initStackBottomWith' in line: --deadCodeElim:on removes initStackBottomWith
			if 'nimFrame' in line or 'popFrame' in line:
				if line.strip().endswith(';'):
					continue
				elif line.strip().endswith('{'):
					skip_inline = True
				else:
					raise RuntimeError('error parsing nim c code')
			else:
				out.append(line)  ## TODO check these
		elif line.startswith('struct '):
			for s in skip_structs:
				if s in line:
					skip_struct = True
					break
			if skip_struct:
				continue
			else:
				out.append(line)
		elif skip_inline:
			if line=='}':
				skip_inline = False
			continue
		elif skip_struct:
			if line=='};':
				skip_struct = False
			continue
		else:
			out.append(line)

	return '\n'.join(out)


def gen_nim_wrappers(src, out):
	for line in src.splitlines():
		## check if line is a function that exports to C ##
		if line.startswith('proc ') and '{.' in line and '.}' in line and 'cdecl' in line and 'exportc' in line:
			funcname = line.split('proc ')[-1].strip().split('(')[0]
			restype  = line.split(':')[-1].split('{')[0].strip()
			if not restype or not restype.startswith('c'):
				raise RuntimeError('TODO: some other nim return type')
			if restype=='cstring':
				raise RuntimeError('TODO: nim function returns cstring')

			restype = restype[1:] ## strip `c` prefix
			args = line.split('(')[-1].split(')')[0]
			wargs = []
			for arg in args.split(','):
				name, type = arg.split(':')
				name = name.strip()
				type = type.strip()
				if not type=='cstring':  ## keep as cstring because we define that as `char*`
					type = type[1:] # strip the `c` prefix
				wargs.append( '%s:%s' %(name,type))

			wrap = [
				'	def %s(%s) ->%s:' %(funcname, ','.join(wargs), restype),
				'		pass'
			]
			out.extend(wrap)
			
```
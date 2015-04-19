C++ Translator
-------------

![toplevel](http://rusthon.github.io/Rusthon/images/RusthonC++.svg)


Imports
-------
* [@import jvm.md](jvm.md)
* [@import nim.md](nim.md)
* [@import cppheader.md](cppheader.md)
* [@import cpython.md](cpython.md)
* [@import nuitka.md](nuitka.md)



```python

NUITKA_HEAD = '''
//PyObject *get_nuitka_module() { return module___main__; }
//PyDictObject *get_nuitka_module_dict() { return moduledict___main__; }

'''

def gen_nuitka_header():
	return NUITKA_HEAD

```

TODO: make inline cpp-channel.h an option.


```python

class CppGenerator( RustGenerator, CPythonGenerator ):

	def is_container_type(self, T):
		## TODO better parsing
		if 'std::vector' in T or 'std::map' in T:
			return True
		elif self.usertypes and 'vector' in self.usertypes:
			if self.usertypes['vector']['template'].split('<')[0] in T:
				return True
		return False

	def visit_ImportFrom(self, node):
		# print node.module
		# print node.names[0].name
		# print node.level
		if node.module=='runtime':
			self._use_runtime = True

		return ''


	def visit_Import(self, node):
		includes = []

		for alias in node.names:
			name = alias.name.replace('__SLASH__', '/')
			if alias.asname:
				self._user_class_headers[ alias.asname ] = {
					'file':name,
					'source':[]
				}

			if name == 'jvm':
				self._has_jvm = True
			elif name == 'nim':
				self._has_nim = True
			elif name == 'nuitka':
				self._has_nuitka = True
			elif name == 'cpython':
				self._has_cpython = True
			elif name.endswith('.h'):
				includes.append('#include "%s"' %name)
			else:
				includes.append('#include <%s>' %name)

		return '\n'.join(includes)


	def visit_Module(self, node):
		header = [ CPP_HEADER ]
		lines = []

		for b in node.body:
			line = self.visit(b)

			if line is not None:
				for sub in line.splitlines():
					if sub==';':
						#raise SyntaxError('bad semicolon')
						pass
					else:
						lines.append( sub )
			else:
				if isinstance(b, ast.Import):
					header.append( self.visit(b) )
				else:
					raise SyntaxError(b)

		if self._has_channels:
			## https://github.com/ahorn/cpp-channel
			#header.append('#include <channel>')
			## instead of including, just directly inline cpp-channel source
			dirname = os.path.dirname(os.path.abspath(__file__))
			header.append(
				open( os.path.join(dirname, 'src/runtime/c++/cpp-channel.h') ).read()
			)

		if self._has_jvm:
			header.append( gen_jvm_header(self._java_classpaths) )

		if self._has_nim:
			header.append( gen_nim_header() )

		if self._has_nuitka:
			header.append( gen_nuitka_header() )

		if self._has_cpython:
			header.append( gen_cpython_header() )

		## forward declare all classes
		for classname in self._classes:
			header.append('class %s;' %classname)

		if len(self._kwargs_type_.keys()):
			impl = []
			header.append('class _KwArgs_;')  ## forward declare
			header.append('class _KwArgs_ {')
			header.append('	public:')

			for name in self._kwargs_type_:
				type = self._kwargs_type_[name]
				header.append( '  %s _%s_;' %(type,name))
				header.append( '  bool __use__%s;' %name)

			for name in self._kwargs_type_:
				type = self._kwargs_type_[name]
				header.append( '  _KwArgs_*  %s(%s %s);' %(name, type, name))

				impl.append( '  _KwArgs_*   _KwArgs_::%s(%s %s) {' %(name, type, name))
				impl.append( '		this->__use__%s = true;' %name)
				impl.append( '		this->_%s_ = %s;' %(name, name))
				impl.append( '		return this;')
				impl.append('};')
			header.append('};')
			header.extend( impl )

		if self._has_cpython:
			header.append( self.gen_cpython_helpers() )


		self.output_pak = pak = {'c_header':'', 'cpp_header':'', 'main':''}
		cheader = None
		cppheader = None
		if len(self._cheader):
			cheader = []
			cppheader = ['extern "C" {']
			for line in self._cheader:
				cheader.append(line)
				cppheader.append('\t'+line)
			cppheader.append('}')

		if cheader:
			pak['header.c'] = '\n'.join( cheader )
		if cppheader:
			pak['header.cpp'] = '\n'.join( cppheader )

		if not self._user_class_headers:
			if 'int main() {' in lines:
				main_index = lines.index('int main() {')
				for idef in self._cpp_class_impl:
					lines.insert(main_index,idef)
			else:
				## option to split this part into the cpp body TODO
				for idef in self._cpp_class_impl:
					lines.append(idef)

		if self._use_runtime:
			lines = header + list(self._imports) + lines
		else:
			lines = list(self._imports) + lines

		pak['main'] = '\n'.join( lines )
		return pak['main']

```

low level `new` for interfacing with external c++.
Also used for code that is blocked with `with pointers:`
to create a class without having to create a temp variable,
`f( new(MyClass(x,y)) )`, directly calls the constructor,
if MyClass is a Rusthon class then __init__ will be called.
TODO fix mixing with std::shared_ptr by keeping a weak_ptr
in each object that __init__ returns (also fixes the _ref_hacks)

```python

	def _visit_call_helper_new(self, node):
		if isinstance(node.args[0], ast.BinOp): # makes an array or map
			a = self.visit(node.args[0])
			if type(a) is not tuple:
				raise SyntaxError(self.format_error('TODO some extended type'))

			atype, avalue = a
			if atype.endswith('*'): atype = atype[:-1]
			else: pass  ## this should never happen
			return '(new %s %s)' %(atype, avalue)

		## Rusthon class ##
		elif isinstance(node.args[0], ast.Call) and isinstance(node.args[0].func, ast.Name) and node.args[0].func.id in self._classes:
			classname = node.args[0].func.id
			args = [self.visit(arg) for arg in node.args[0].args ]
			if self._classes[classname]._requires_init:
				return '(new %s)->__init__(%s)' %(classname, ','.join(args))
			elif args:  ## a rusthon class that subclasses from an external c++ class ##
				return '(new %s(%s))' %(classname, ','.join(args))
			else:
				return '(new %s)' %classname

		## external c++ class ##
		else:
			return '(new %s)' %self.visit(node.args[0])

```

Subclasses from `RustGenerator`, see here:
[rusttranslator.md](rusttranslator.md)
TODO: reverse, `RustGenerator` should subclass from `CppGenerator`.

note: polymorphic classes are not generated by default, virtual methods are not required,
casting works fine with `static_cast` and `std::static_pointer_cast`.

```python

	def __init__(self, source=None, requirejs=False, insert_runtime=False, cached_json_files=None):
		RustGenerator.__init__(self, source=source, requirejs=False, insert_runtime=False)
		self._cpp = True
		self._rust = False  ## can not be true at the same time self._cpp is true, conflicts in switch/match hack.
		self._shared_pointers = True
		self._noexcept = False
		self._polymorphic = False  ## by default do not use polymorphic classes (virtual methods)
		self._has_jvm = False
		self._jvm_classes = dict()
		self._has_nim = False
		self._has_nuitka = False
		self._has_cpython = False
		self._known_pyobjects  = dict()
		self._use_runtime = insert_runtime
		self.cached_json_files = cached_json_files or dict()
		self.usertypes = dict()
		self._user_class_headers = dict()

	def visit_Delete(self, node):
		targets = [self.visit(t) for t in node.targets]
		if len(targets)==0:
			raise RuntimeError('no delete targets')
		r = []
		if self.usertypes and 'weakref' in self.usertypes and 'reset' in self.usertypes['weakref']:
			for t in targets:
				r.append('%s.%s();' %(t, self.usertypes['weakref']['reset']))
		elif self.usertypes and 'shared' in self.usertypes and 'reset' in self.usertypes['shared']:
			for t in targets:
				r.append('%s.%s();' %(t, self.usertypes['shared']['reset']))
		elif self._shared_pointers:
			for t in targets:
				r.append('%s.reset();' %t)
		else:
			for t in targets:
				if t in self._known_arrays:
					r.append('delete[] %s;')
				else:
					r.append('delete %s;')

		return '\n'.join(r)

	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		if self.usertypes and 'string' in self.usertypes.keys():
			if self.usertypes['string'] is None:
				return '"%s"' % s
			else:
				return self.usertypes['string']['new'] % '"%s"' % s
		else:
			return 'std::string("%s")' % s

	def visit_Print(self, node):
		r = []
		for e in node.values:
			s = self.visit(e)
			if isinstance(e, ast.List) or isinstance(e, ast.Tuple):
				for sube in e.elts:
					r.append('std::cout << %s;' %self.visit(sube))
				if r:
					r[-1] += 'std::cout << std::endl;'
				else:
					r.append('std::cout << std::endl;')
			else:
				r.append('std::cout << %s << std::endl;' %s)
		return '\n'.join(r)
```

TODO
----
* test finally

```python

	def visit_TryExcept(self, node, finallybody=None):
		out = []

		out.append( 'try {' )
		self.push()
		for b in node.body:
			out.append( self.indent()+self.visit(b) )

		self.pull()
		out.append( self.indent() + '} catch (const std::exception& e) {' )
		self.push()
		for h in node.handlers:
			out.append(self.indent()+self.visit(h))
		self.pull()

		if finallybody:
			## wrap in another try that is silent, always throw e
			out.append('try {		// finally block')
			for b in finallybody:
				out.append(self.visit(b))

			out.append('} throw e;')

		out.append( '}' )

		out.append( self.indent() + 'catch (const std::overflow_error& e) { std::cout << "OVERFLOW ERROR" << std::endl; }' )
		out.append( self.indent() + 'catch (const std::runtime_error& e) { std::cout << "RUNTIME ERROR" << std::endl; }' )
		out.append( self.indent() + 'catch (...) { std::cout << "UNKNOWN ERROR" << std::endl; }' )

		return '\n'.join( out )
```


CPython C-API
-------------
user syntax `import cpython` and `->`

```python

	def gen_cpy_call(self, pyob, node):
		fname = self.visit(node.func)
		if not node.args and not node.keywords:
			return 'PyObject_Call(%s, Py_BuildValue("()"), NULL)' %pyob
		else:
			lambda_args = [
				'[&] {',
				'auto args = PyTuple_New(%s);' %len(node.args),
			]
			for i,arg in enumerate(node.args):
				if isinstance(arg, ast.Num):
					n = arg.n
					if str(n).isdigit():
						n = 'PyInt_FromLong(%s)' %n
						lambda_args.append('PyTuple_SetItem(args, %s, %s);' %(i, n))
					else:
						n = 'PyFloat_FromDouble(%s)' %n
						lambda_args.append('PyTuple_SetItem(args, %s, %s);' %(i, n))
				elif isinstance(arg, ast.Str):
					n = 'PyString_FromString("%s")' %arg.s
					lambda_args.append('PyTuple_SetItem(args, %s, %s);' %(i, n))
				else:
					lambda_args.append('PyTuple_SetItem(args, %s, %s);' %(i, self.visit(arg)))
			lambda_args.append('return args; }()')
			return 'PyObject_Call(%s, %s, NULL)' %(pyob, '\n'.join(lambda_args))

	def gen_cpy_get(self, pyob, name):
		return 'PyObject_GetAttrString(%s,"%s")' %(pyob, name)

```

Slice and List Comprehension `[:]`, `[]int(x for x in range(n))`
----------------------------------
negative slice is not fully supported, only `-1` literal works.

```python

	def _gen_slice(self, target=None, value=None, lower=None, upper=None, step=None, type=None):
		assert target
		assert value

		if type:
			slice = ['/* <slice> %s : %s : %s */' %(lower, upper, step)]

			if step:
				slice.append('std::vector<%s> _ref_%s;' %(type,target))
				if lower and not upper:
					slice.append( ''.join([
						'if(%s<0){'%step,
						'for(int _i_=%s->size()-%s-1;_i_>=0;_i_+=%s){' %(value,lower,step),
						' _ref_%s.push_back((*%s)[_i_]);' %(target, value),
						'}} else {',
						'for(int _i_=%s;_i_<%s->size();_i_+=%s){' %(lower,value,step),
						' _ref_%s.push_back((*%s)[_i_]);' %(target, value),
						'}}',
						])
					)
				elif upper:
					raise SyntaxError('TODO slice upper with step')
				else:
					slice.append( ''.join([
						'if(%s<0){'%step,
						'for(int _i_=%s->size()-1;_i_>=0;_i_+=%s){' %(value,step),
						' _ref_%s.push_back((*%s)[_i_]);}' %(target, value),
						'} else {',
						'for(int _i_=0;_i_<%s->size();_i_+=%s){' %(value,step),
						' _ref_%s.push_back((*%s)[_i_]);}' %(target, value),
						'}',
						])
					)
			else:
				slice.append('std::vector<%s> _ref_%s(' %(type,target))

				if lower:
					slice.append('%s->begin()+%s,' %(value, lower))
				else:
					slice.append('%s->begin(),' %value)
				if upper:
					if upper < 0:
						slice.append('%s->end() %s'%(value, upper))
					else:
						slice.append('%s->begin()+%s'%(value, upper))
				else:
					slice.append('%s->end()'%value)
				slice.append(');')

			vectype = 'std::vector<%s>' %type

			if not self._shared_pointers:
				slice.append('%s* %s = &_ref_%s);' %(vectype, target, target))
			elif self._unique_ptr:
				slice.append('std::unique_ptr<%s> %s = _make_unique<%s>(_ref_%s);' %(vectype, target, vectype, target))
			else:
				slice.append('std::shared_ptr<%s> %s = std::make_shared<%s>(_ref_%s);' %(vectype, target, vectype, target))
			return '\n'.join(slice)

		else:  ## SEGFAULTS - TODO FIXME
			## note: `auto` can not be used to make c++11 guess the type from a constructor that takes start and end iterators.
			#return 'auto _ref_%s( %s->begin()+START, %s->end()+END ); auto %s = &_ref_%s;' %(target, val, val, target, target)
			#return 'std::vector<int> _ref_%s( %s->begin(), %s->end() ); auto %s = &_ref_%s;' %(target, val, val, target, target)

			## this sefaults because _ref_ is on the stack and gets cleaned up, while the new smart pointer also has a reference
			## to it and also cleans it up.  TODO how to force _ref_ onto the heap instead?
			slice = [
				'auto _ref_%s = *%s' %(target,value), ## deference and copy vector
				'auto %s = %s' %(target, value), ## copy shared_ptr
				'%s.reset( &_ref_%s )' %(target, target)  ## segfaults
				#'auto _ptr_%s = &_ref_%s' %(target,target),
				#'%s.reset( _ptr_%s )' %(target,target)
			]
			if lower:
				N = lower
				slice.append('_ref_%s.erase(_ref_%s.begin(), _ref_%s.begin()+%s)' %(target, target, target, N))

			if upper:  ## BROKEN, TODO FIXME
				N = upper
				slice.append( '_ref_%s.erase(_ref_%s.begin()+_ref_%s.size()-%s+1, _ref_%s.end())'   %(target, target, target, N, target))


			#return 'auto _ref_%s= *%s;%s;auto %s = &_ref_%s;' %(target, val, slice, target, target)
			return ';\n'.join(slice) + ';'

```


Translate to C++
----------------

TODO save GCC PGO files.

```python

def translate_to_cpp(script, insert_runtime=True, cached_json_files=None):
	#raise SyntaxError(script)
	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, os.path.join('src', 'runtime'))
		runtime = open( os.path.join(dirname, 'cpp_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		e = ['%s:	%s'%(i+1, line) for i,line in enumerate(script.splitlines())]
		sys.stderr.write('\n'.join(e))
		raise err

	g = CppGenerator( source=script, insert_runtime=insert_runtime, cached_json_files=cached_json_files )
	g.visit(tree) # first pass gathers classes
	pass2 = g.visit(tree)
	g.reset()
	pass3 = g.visit(tree)
	#open('/tmp/pass3.cpp', 'wb').write( pass3 )
	return g.output_pak

```


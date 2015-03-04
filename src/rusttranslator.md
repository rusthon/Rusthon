Rust Translator
---------------
The rust generator subclasses from the go generator.
Note: most of the c++ translator lives here to.

```python

TRY_MACRO = '''
macro_rules! try_wrap_err(
      ($e:expr, $ret:expr) => (match $e {Ok(e) => e, Err(e) => return ($ret)(e)})
);
'''

def default_type( T ):
	return {'int':0, 'string':'"".to_string()'}[T]

class RustGenerator( CppRustBase ):


```
Try Except `try`, `except`
----------

TODO fix try/finally

```python

	def visit_TryFinally(self, node):
		assert len(node.body)==1
		return self.visit_TryExcept(node.body[0], finallybody=node.finalbody)

	def visit_TryExcept(self, node, finallybody=None):
		out = []
		out.append( self.indent() + 'let try_lambda = || ->IoResult<bool> {' )
		self.push()
		for b in node.body:
			out.append( self.indent()+self.visit(b) )
			#out.append( '%stry!(%s);' %( self.indent(), self.visit(b)[:-1] ) )

		out.append(self.indent()+'return Ok(true);')
		self.pull()
		out.append( self.indent() + '};' )
		self.push()
		#out.extend(
		#	list( map(self.visit, node.handlers) )
		#)
		self.pull()
		#out.append( '}' )
		out.append('try_wrap_err!( try_lambda(), |_|{()});')
		return '\n'.join( out )

```

Slice `[:]`
-----------------
http://doc.rust-lang.org/std/slice/
#![feature(slicing_syntax)]

```python

	def visit_Slice(self, node):

		lower = upper = step = None
		if node.lower:
			lower = self.visit(node.lower)
		if node.upper:
			upper = self.visit(node.upper)
		if node.step:
			step = self.visit(node.step)

		if lower and upper:
			return '%s..%s' %(lower,upper)
		elif upper:
			return '0..%s' %upper
		elif lower:
			return '%s..'%lower
		else:
			raise SyntaxError('TODO slice')



	def visit_Print(self, node):
		r = []
		for e in node.values:
			if isinstance(e, ast.List) or isinstance(e, ast.Tuple):
				fmt = '{}' * len(e.elts)
				args = [self.visit(elt) for elt in e.elts]
				r.append('println!("%s", %s);' %(fmt, ','.join(args)))
			else:
				r.append('println!("{}", %s);' %self.visit(e))
		return ''.join(r)


```

Module
-----------------
generate main rust module
TODO clean up go code.

```python


	def visit_Module(self, node):
		top_header = [
			'#![allow(unknown_features)]',
			'#![feature(slicing_syntax)]',
			'#![feature(asm)]',
			'#![allow(unused_parens)]',
			'#![allow(non_camel_case_types)]',
			'#![allow(dead_code)]',
			'#![allow(non_snake_case)]',
			'#![allow(unused_mut)]',  ## if the compiler knows its unused - then it still can optimize it...?
			'#![allow(unused_variables)]',
			'#![feature(macro_rules)]',
		]

		header = [
			'use std::collections::{HashMap};',
			'use std::io::{File, Open, ReadWrite, Read, IoResult};',
			'use std::num::Float;',
			'use std::num::Int;',
			'use std::rc::Rc;',
			'use std::cell::RefCell;',
			'use std::thread::Thread;',
		]
		lines = []

		for b in node.body:
			line = self.visit(b)

			if line:
				for sub in line.splitlines():
					if sub==';':
						#raise SyntaxError('bad semicolon')
						pass
					else:
						lines.append( sub )
			else:
				if isinstance(b, ast.Import) or isinstance(b, ast.ImportFrom):  ## these write later in header
					pass
				else:
					raise SyntaxError(b)

		if self._go:
			assert not self._cpp

			if len(self._kwargs_type_.keys())==0:
				lines.append('struct _kwargs_type_;')
			else:
				lines.append('struct _kwargs_type_ {')
				for name in self._kwargs_type_:
					type = self._kwargs_type_[name]
					lines.append( '  %s : %s,' %(name,type))
					lines.append( '  __use__%s : bool,' %name)
				lines.append('}')

		elif self._rust and len(self._kwargs_type_.keys()):
			raise RuntimeError('TODO kwargs for rust')


		for crate in self._crates:
			top_header.append('extern crate %s;' %crate)
			use_items = self._crates[crate]
			if use_items:
				header.append('use %s::{%s};' %(crate, ','.join(use_items)))

		if len(self._cheader):
			header.append('extern "C" {')
			for line in self._cheader:
				header.append(line)
				raise SyntaxError(line)
			header.append('}')

		header.append( TRY_MACRO )

		lines = top_header + header + list(self._imports) + lines
		return '\n'.join( lines )


```

For Loop
-----------------
hooks into bad magic hack, 2nd pass rustc compile.

```python


	def visit_For(self, node):
		if not hasattr(node.iter, 'uid'):
			## in the first rustc pass we assume regular references using `&X`,
			## for loops over an array of Strings requires the other type using just `X` or `ref X`
			node.iter.uid = self.uid()
			node.iter.is_ref = True
			self.unodes[ node.iter.uid ] = node.iter

		target = self.visit(node.target)
		lines = []

		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):

			if node.iter.func.id == 'range':
				if len(node.iter.args)==1:
					iter = self.visit(node.iter.args[0])
					if self._cpp:
						lines.append('for (int %s=0; %s<%s; %s++) {' %(target, target, iter, target))
					else:
						lines.append('for %s in range(0u, %s) {' %(target, iter))
				elif len(node.iter.args)==2:
					start = self.visit(node.iter.args[0])
					iter = self.visit(node.iter.args[1])
					if self._cpp:
						lines.append('for (int %s=%s; %s<%s; %s++) {' %(target, start, target, iter, target))

					else:
						lines.append('for %s in range(%s as uint, %s as uint) {' %(target, start, iter))
				else:
					raise SyntaxError('invalid for range loop')

			elif node.iter.func.id == 'enumerate':
				iter = self.visit(node.iter.args[0])
				idx = self.visit(node.target.elts[0])
				tar = self.visit(node.target.elts[1])
				if self._cpp:
					lines.append('int %s = -1;' %idx)
					lines.append('for (auto &%s: _ref_%s) {' %(tar, iter))  ## TODO remove _ref_
				else:
					lines.append('let mut %s = -1i;' %idx)
					if node.iter.is_ref:
						lines.append('for &%s in %s.iter() { //magic:%s' %(tar, iter, node.iter.uid))
					else:
						lines.append('for %s in %s.iter() { //magic:%s' %(tar, iter, node.iter.uid))

				lines.append('  %s += 1;' %idx)

			else: ## generator function
				gfunc = node.iter.func.id
				gargs = ','.join( [self.visit(e) for e in node.iter.args] )
				lines.append('__gen%s := __new__%s(%s)' %(gfunc,gfunc, gargs))
				lines.append('for __gen%s.__done__ != 1 {' %gfunc)
				lines.append('	%s := __gen%s.next()' %(self.visit(node.target), gfunc))

		elif isinstance(node.target, ast.List) or isinstance(node.target, ast.Tuple):
			iter = self.visit( node.iter )
			key = self.visit(node.target.elts[0])
			val = self.visit(node.target.elts[1])
			iname = iter.split('.')[0]
			if self._cpp:
				assert iname in self._known_maps  ## TODO always assume its a map? and _ref_?
				lines.append('for (auto &_pair_%s : *%s) {' %(key, iter))
				lines[-1] += '  auto %s = _pair_%s.first;' %(key, key)
				lines[-1] += '  auto %s = _pair_%s.second;' %(val, key)

			else:
				lines.append('for (%s,&%s) in %s.iter() {' %(key,val, iter))

		else:

			iter = self.visit( node.iter )
			arrname = iter.split('.')[0]
			if node.iter.is_ref:
				if self._cpp:
					if arrname in self._known_arrays:
						lines.append('for (auto &%s: (*%s)) {' %(target, iter))
					elif arrname in self._known_maps:
						lines.append('for (auto &_pair_%s: (*%s)) {' %(target, iter))
						lines.append('  auto %s = _pair_%s.second;')
					else:
						lines.append('for (auto &%s: *%s) {' %(target, iter))

				else:
					lines.append('for &%s in %s.borrow_mut().iter() { //magic:%s' %(target, iter, node.iter.uid))
			else:
				lines.append('for %s in %s.borrow_mut().iter() { //magic:%s' %(target, iter, node.iter.uid))

		self.push()
		for b in node.body:
			lines.append( self.indent()+self.visit(b) )
		self.pull()
		lines.append( self.indent()+'}' )  ## end of for loop
		return '\n'.join(lines)


```

asm
-----------------
tries to convert basic gcc asm syntax to llvm asm syntax,
TODO fix me

```python


	def _gccasm_to_llvmasm(self, asmcode):
		r = []
		for i,char in enumerate(asmcode):
			if i+1==len(asmcode): break
			next = asmcode[i+1]
			if next.isdigit() and char == '%':
				r.append( '$' )
			else:
				r.append( char )
		r.append('"')
		a = ''.join(r)
		return a.replace('%%', '%')


```

The hack below runs the code generated in the second pass into the Rust compiler to check for errors,
in some cases Rusthon may not always track the types inside an array, or other types, and so it
it starts off by generating some dumb code that works most of the time.  If it will not pass the
Rust compiler, stdout is parsed to check for errors and a magic ID that links to a ast Node.

TODO: do not hard code rustc to /usr/local/bin

```python


def translate_to_rust(script, insert_runtime=True):
	#raise SyntaxError(script)
	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'src/runtime')
		runtime = open( os.path.join(dirname, 'rust_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	g = RustGenerator( source=script )
	g.visit(tree) # first pass gathers classes
	pass2 = g.visit(tree)

	exe = os.path.expanduser('/usr/local/bin/rustc')
	if not os.path.isfile(exe):
		raise RuntimeError('rustc not found in /usr/local/bin')

	import subprocess
	pass2lines = pass2.splitlines()
	path = '/tmp/pass2.rs'
	open(path, 'wb').write( pass2 )
	p = subprocess.Popen([exe, path], cwd='/tmp', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	errors = p.stderr.read().splitlines()

	def magic():
		if len(errors):
			hiterr = False
			for line in errors:
				if 'error:' in line:
					hiterr = True
				elif hiterr:
					hiterr = False
					if '//magic:' in line:
						uid = int( line.split('//magic:')[-1] )
						g.unodes[ uid ].is_ref = False
					elif line.startswith('for '):  ## needs magic id
						raise SyntaxError('BAD MAGIC:'+line)
					else:
						raise SyntaxError(line)
	try:
		magic()
	except SyntaxError as err:
		errors = ['- - - rustc output - - -', ''] + errors
		msg = '\n'.join(errors + ['- - - rustc error:', err[0]])
		raise RuntimeError(msg)

	pass3 = g.visit(tree)
	open('/tmp/pass3.rs', 'wb').write( pass3 )
	return pass3


```

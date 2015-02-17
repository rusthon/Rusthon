#!/usr/bin/env python
# PythonJS to C++ Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import os, sys
import ast
import pythonjs_to_rust



class CppGenerator( pythonjs_to_rust.RustGenerator ):
	def _visit_call_helper_new(self, node):
		assert self._cpp
		assert not self._shared_pointers
		if isinstance(node.args[0], ast.BinOp):
			a = self.visit(node.args[0])
			if type(a) is not tuple:
				raise SyntaxError(a)
			atype, avalue = a
			if atype.endswith('*'): atype = atype[:-1]
			return 'new %s %s' %(atype, avalue)
		else:
			classname = node.args[0].func.id
			args = [self.visit(arg) for arg in node.args[0].args ]
			return '(new %s)->__init__(%s)' %(classname, ','.join(args))

	def __init__(self, source=None, requirejs=False, insert_runtime=False):
		pythonjs_to_rust.RustGenerator.__init__(self, source=source, requirejs=False, insert_runtime=False)
		self._cpp = True
		self._rust = False  ## can not be true at the same time self._cpp is true, conflicts in switch/match hack.
		self._shared_pointers = True
		self._noexcept = False
		self._polymorphic = False  ## by default do not use polymorphic classes (virtual methods)


	def visit_Delete(self, node):
		targets = [self.visit(t) for t in node.targets]
		if len(targets)==0:
			raise RuntimeError('no delete targets')
		r = []
		if self._shared_pointers:
			for t in targets:
				## shared_ptr.reset only releases if no there are no other references,
				## is there a way to force the delete on all shared pointers to something?
				#r.append('delete %s;' %t)  ## only works on pointers
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

	def visit_Import(self, node):
		r = [alias.name.replace('__SLASH__', '/') for alias in node.names]
		if r:
			for name in r:
				self._imports.add('import("%s");' %name)
		return ''

	def visit_Module(self, node):
		header = [
			'#include <cmath>',
			'#include <memory>',
			'#include <vector>',
			'#include <array>',
			'#include <iostream>',
			'#include <fstream>',
			'#include <string>',
			'#include <map>',
			'#include <algorithm>', ## c++11
			'#include <functional>', ## c++11
			#'#include <sstream>',  ## c++11
			'#include <thread>', ## c++11
			'#include <chrono>', ## c++11
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
				if isinstance(b, ast.Import):
					pass
				else:
					raise SyntaxError(b)

		if self._has_channels:
			## https://github.com/ahorn/cpp-channel
			#header.append('#include <channel>')
			## instead of including, just directly inline cpp-channel source
			dirname = os.path.dirname(os.path.abspath(__file__))
			header.append(
				open( os.path.join(dirname, 'runtime/c++/cpp-channel.h') ).read()
			)

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

		main_index = lines.index('int main() {')
		for idef in self._cpp_class_impl:
			lines.insert(main_index,idef)

		lines = header + list(self._imports) + lines
		pak['main'] = '\n'.join( lines )
		return pak['main']





def main(script, insert_runtime=True):
	#raise SyntaxError(script)
	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'cpp_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		e = ['%s:	%s'%(i+1, line) for i,line in enumerate(script.splitlines())]
		sys.stderr.write('\n'.join(e))
		raise err

	g = CppGenerator( source=script )
	g.visit(tree) # first pass gathers classes
	pass2 = g.visit(tree)
	g.reset()
	pass3 = g.visit(tree)
	#open('/tmp/pass3.cpp', 'wb').write( pass3 )
	return g.output_pak



def command():
	scripts = []
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			if arg.endswith('.py'):
				scripts.append( arg )

	if len(scripts):
		a = []
		for script in scripts:
			a.append( open(script, 'rb').read() )
		data = '\n'.join( a )
	else:
		data = sys.stdin.read()

	out = main( data )
	print( out )


if __name__ == '__main__':
	command()

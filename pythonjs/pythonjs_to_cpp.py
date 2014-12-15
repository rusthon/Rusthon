#!/usr/bin/env python
# PythonJS to C++ Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import os, sys
import ast
import pythonjs_to_rust



class CppGenerator( pythonjs_to_rust.RustGenerator ):

	def __init__(self, requirejs=False, insert_runtime=False):
		pythonjs_to_rust.RustGenerator.__init__(self, requirejs=False, insert_runtime=False)
		self._cpp = True

	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		return 'std::string("%s")' % s


	def visit_Print(self, node):
		r = []
		for e in node.values:
			s = self.visit(e)
			if isinstance(e, ast.List):
				r.append('std::cout << %s << std::endl;' %s[1:-1])
			else:
				r.append('std::cout << %s << std::endl;' %s)
		return ''.join(r)


	def visit_Import(self, node):
		r = [alias.name.replace('__SLASH__', '/') for alias in node.names]
		if r:
			for name in r:
				self._imports.add('import("%s");' %name)
		return ''

	def visit_Module(self, node):
		header = [
			'#include <memory>',
			'#include <iostream>',
			'#include <string>',
			'#include <map>',
			'#include <functional>', ## c++11
			#'#include <sstream>',  ## c++11
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

		if len(self._kwargs_type_.keys())==0:
			header.append('struct _kwargs_type_;')
		else:
			header.append('struct _kwargs_type_ {')
			for name in self._kwargs_type_:
				type = self._kwargs_type_[name]
				header.append( '  %s %s;' %(type,name))
				header.append( '  bool __use__%s;' %name)
			header.append('};')

		self.output_pak = pak = {'c_header':'', 'cpp_header':'', 'main':''}
		if len(self._cheader):
			cheader = []
			cppheader = ['extern "C" {']
			for line in self._cheader:
				cheader.append(line)
				cppheader.append('\t'+line)
			cppheader.append('}')

		pak['header.c'] = '\n'.join( cheader )
		pak['header.cpp'] = '\n'.join( cppheader )
		lines = header + list(self._imports) + lines
		pak['main'] = '\n'.join( lines )
		return pak['main']





def main(script, insert_runtime=True):

	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'cpp_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	g = CppGenerator()
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

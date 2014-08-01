#!/usr/bin/env python
# PythonJS to Go Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import sys
import ast
import pythonjs



class GoGenerator( pythonjs.JSGenerator ):

	def __init__(self, requirejs=False, insert_runtime=False):
		pythonjs.JSGenerator.__init__(self, requirejs=False, insert_runtime=False)
		#self._classes = dict()
		#self._class_props = dict()

	def visit_Print(self, node):
		r = [ 'fmt.Print(%s);' %self.visit(e) for e in node.values]
		return ''.join(r)


	def visit_Module(self, node):
		header = [
			'package main',
			'import "fmt"'
		]
		lines = []


		if self._insert_runtime:
			dirname = os.path.dirname(os.path.abspath(__file__))
			runtime = open( os.path.join(dirname, 'pythonjs.js') ).read()
			lines.append( runtime )  #.replace('\n', ';') )

		for b in node.body:
			line = self.visit(b)
			if line: lines.append( line )
			else:
				#raise b
				pass


		lines = header + lines
		return '\n'.join( lines )

	def visit_FunctionDef(self, node):
		args = self.visit(node.args)
		out = []
		out.append( self.indent() + 'func %s(%s) {\n' % (node.name, ', '.join(args)) )
		self.push()
		for b in node.body:
			v = self.visit(b)
			if v:
				out.append( self.indent() + v )

		self.pull()
		out.append( self.indent()+'}' )
		return '\n'.join(out)

	def _visit_call_helper_var(self, node):
		args = [ self.visit(a) for a in node.args ]
		#if args:
		#	out.append( 'var ' + ','.join(args) )
		if node.keywords:
			for key in node.keywords:
				args.append( key.arg )

		out = []
		for v in args:
			out.append( self.indent() + 'var ' + v + ' int')

		#return '\n'.join(out)
		return ''

	def visit_Assign(self, node):
		target = node.targets[0]
		if isinstance(target, ast.Tuple):
			raise NotImplementedError('target tuple assignment should have been transformed to flat assignment by python_to_pythonjs.py')
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			code = 'var %s = %s;' % (target, value)
			return code


def main(script):
	tree = ast.parse(script)
	return GoGenerator().visit(tree)


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

#!/usr/bin/env python
# PythonJS to Go Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import os, sys
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

	def visit_Expr(self, node):
		return self.visit(node.value)


	def visit_Module(self, node):
		header = [
			'package main',
			'import "fmt"'
		]
		lines = []

		for b in node.body:
			line = self.visit(b)
			if line:
				for sub in line.splitlines():
					if sub==';':
						raise SyntaxError(line)
					else:
						lines.append( sub )
			else:
				raise SyntaxError(line)


		lines = header + lines
		return '\n'.join( lines )

	def _visit_call_helper_go(self, node):
		name = self.visit(node.func)
		if name == '__go__':
			return 'go %s' %self.visit(node.args[0])
		elif name == '__gomake__':
			return 'make(%s)' %self.visit(node.args[0])
		else:
			return SyntaxError('invalid special go call')

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
			raise NotImplementedError('TODO')

		elif isinstance(node.value, ast.BinOp) and self.visit(node.value.op)=='<<' and isinstance(node.value.left, ast.Name) and node.value.left.id=='__go__send__':
			target = self.visit(target)
			value = self.visit(node.value.right)
			return 'var %s <- %s;' % (target, value)

		else:
			target = self.visit(target)
			value = self.visit(node.value)
			code = 'var %s = %s;' % (target, value)
			return code

	def visit_While(self, node):
		body = [ 'for %s {' %self.visit(node.test)]
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def _inline_code_helper(self, s):
		return s

def main(script, insert_runtime=True):
	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'go_builtins.py') ).read()
		script = runtime + '\n' + script

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

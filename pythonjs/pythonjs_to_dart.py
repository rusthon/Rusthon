#!/usr/bin/env python
# PythonJS to Dart Translator
# by Brett Hartshorn - copyright 2013
# License: "New BSD"
import os, sys
import ast
import pythonjs

class DartGenerator( pythonjs.JSGenerator ):
	def visit_ClassDef(self, node):
		out = []
		bases = []
		for base in node.bases:
			bases.append( self.visit(base) )
		if bases:
			out.append('class %s extends %s {'%(node.name, ','.join(bases)))

		else:
			out.append('class %s {' %node.name)
		self.push()
		for b in node.body:
			line = self.visit(b)
			if line.startswith('var '):
				out.append( self.indent()+line )
			else:
				out.append( line )
		self.pull()
		out.append('}')
		return '\n'.join(out)

	def _visit_for_prep_iter_helper(self, node, out):
		pass


	def visit_Expr(self, node):
		# XXX: this is UGLY
		s = self.visit(node.value)
		if not s.endswith(';'):
			s += ';'
		return s



	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		s = 'print(%s);' % ', '.join(args)
		return s


	def visit_Assign(self, node):
		assert len(node.targets) == 1
		target = node.targets[0]
		if isinstance(target, ast.Tuple):
			raise NotImplementedError
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			if self.indent():
				code = '%s = %s;' % (target, value)
			else:
				code = 'var %s = %s;' % (target, value)
			return code

	def visit_FunctionDef(self, node):

		args = self.visit(node.args)
		buffer = self.indent() + '%s(%s) {\n' % (node.name, ', '.join(args))
		self.push()
		body = list()
		for child in node.body:
			if isinstance(child, ast.Str):
				continue
			else:
				body.append( self.indent() + self.visit(child) )

		buffer += '\n'.join(body)
		self.pull()
		buffer += '\n%s}\n' %self.indent()
		return buffer




def main(script):
	tree = ast.parse(script)
	return DartGenerator().visit(tree)


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

	js = main( data )
	print( js )


if __name__ == '__main__':
	command()

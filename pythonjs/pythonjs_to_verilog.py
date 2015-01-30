#!/usr/bin/env python
# PythonJS to Verilog Translator
# by Brett Hartshorn - copyright 2015
# License: "New BSD"
import os, sys, itertools
import ast
import pythonjs


class VerilogGenerator( pythonjs.JSGenerator ):

	def __init__(self, source=None, requirejs=False, insert_runtime=False):
		assert source
		pythonjs.JSGenerator.__init__(self, source=source, requirejs=False, insert_runtime=False)
		self._verilog = True


	def visit_With(self, node):
		r = []

		if isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'initial':
			r.append('initial begin')
			for b in node.body:
				r.append(self.visit(b))
			r.append('end')
		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'always':
			r.append('initial begin')
			for b in node.body:
				r.append(self.visit(b))
			r.append('end')

		return '\n'.join(r)



def main(script, insert_runtime=True):
	#raise SyntaxError(script)

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	g = VerilogGenerator( source=script )
	g.visit(tree) # first pass gathers classes
	return g.visit(tree)



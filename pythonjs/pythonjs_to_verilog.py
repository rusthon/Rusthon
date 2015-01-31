#!/usr/bin/env python
# PythonJS to Verilog Translator
# by Brett Hartshorn - copyright 2015
# License: "New BSD"
import os, sys, itertools
import ast
import pythonjs
import typedpython


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
			r.append('always begin')
			for b in node.body:
				r.append(self.visit(b))
			r.append('end')
		elif isinstance( node.context_expr, ast.Call ) and isinstance(node.context_expr.func, ast.Attribute) and node.context_expr.func.attr == 'ff':
			r.append('always_ff begin')
			for b in node.body:
				r.append(self.visit(b))
			r.append('end')

		return '\n'.join(r)

	def visit_Str(self, node):
		bits = len(node.s)
		return "%s'b%s" %(bits, node.s)


	def visit_Assign(self, node):

		if isinstance(node.targets[0], ast.Tuple):
			raise SyntaxError('not allowed in verilog')
			#if len(node.targets) > 1: raise NotImplementedError('TODO')
			#elts = [self.visit(e) for e in node.targets[0].elts]
			#target = '(%s)' % ','.join(elts)
		else:
			target = self.visit( node.targets[0] )

		if isinstance(node.value, ast.BinOp) and self.visit(node.value.op)=='<<' and isinstance(node.value.left, ast.Name) and node.value.left.id=='__go__send__':
			value = self.visit(node.value.right)
			return '%s <= %s;' % (target, value)

		elif not self._function_stack:  ## global level
			value = self.visit(node.value)
			return 'parameter %s = %s' %(target, value)

		else:
			value = self.visit(node.value)
			return '%s = %s' %(target, value)

	def _visit_call_helper(self, node):
		fname = self.visit(node.func)
		if fname=='reg' or fname=='wire':
			bits = 1
			index = 0
			args = [arg.id for arg in node.args]
			for kw in node.keywords:
				if kw.arg=='bits':
					bits = kw.value.n
				elif kw.arg=='index':
					index = kw.value.n
			if fname=='reg':
				return 'reg [%s:%s] %s;' %(bits,index, ','.join(args))
			else:
				return 'wire [%s:%s] %s;' %(bits,index, ','.join(args))
		elif fname.startswith('bit') and fname[3:].isdigit():
			bits = int(fname[3:])
			return "%s'd%s" %(bits, node.args[0].n)
		elif fname.endswith('.assign'):
			wire = fname.split('.')[0]
			return 'assign %s = %s' %(wire, self.visit(node.args[0]))
		else:
			raise SyntaxError(fname)

def main(script, insert_runtime=True):
	#raise SyntaxError(script)
	script = typedpython.transform_source(script)
	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	g = VerilogGenerator( source=script )
	g.visit(tree) # first pass gathers classes
	return g.visit(tree)



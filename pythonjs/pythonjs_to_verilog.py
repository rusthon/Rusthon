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


	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		s = '$display(%s);' % ', '.join(args)
		return s


	def visit_With(self, node):
		r = []

		if isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'initial':
			r.append('initial begin')
			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))
			self.pull()
			r.append(self.indent()+'end')
		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'always':
			r.append('always begin')
			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))
			self.pull()
			r.append(self.indent()+'end')
		elif isinstance( node.context_expr, ast.Call ) and isinstance(node.context_expr.func, ast.Attribute) and node.context_expr.func.attr == 'ff':
			opts = []
			for arg in node.context_expr.args:
				opts.append('posedge '+self.visit(arg))
			for kw in node.context_expr.keywords:
				edge = self.visit(kw.value)
				if 'neg' in edge.lower():
					edge = 'negedge'
				else:
					edge = 'posedge'
				opts.append('%s %s' %(edge, kw.arg))
			r.append('always_ff @(%s) begin' %' or '.join(opts))
			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))
			self.pull()
			r.append(self.indent()+'end')
		elif isinstance( node.context_expr, ast.Call ) and isinstance(node.context_expr.func, ast.Name) and node.context_expr.func.id == 'delay':
			delay = node.context_expr.args[0].n
			r.append('// delay = %s' %delay)
			for b in node.body:
				## should skip some nodes like if/else
				r.append(self.indent()+'# %s  %s' %(delay,self.visit(b)))

		return '\n'.join(r)

	def visit_Str(self, node):
		isbin = True
		for char in node.s:
			if char not in ('0', '1'):
				isbin = False
				break
		if isbin:
			bits = len(node.s)
			return "%s'b%s" %(bits, node.s)
		else:
			return '"%s"' %node.s


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
			return 'parameter %s = %s;' %(target, value)

		else:
			value = self.visit(node.value)
			return '%s = %s;' %(target, value)

	def _visit_call_helper(self, node):
		fname = self.visit(node.func)
		if fname=='reg' or fname=='wire':
			bits = 1
			index = 0
			args = [arg.id for arg in node.args]
			for kw in node.keywords:
				if kw.arg=='bits':
					bits = kw.value.n-1
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
			return 'assign %s = %s;' %(wire, self.visit(node.args[0]))
		else:
			raise SyntaxError(fname)

	def _visit_function(self, node):
		is_main = node.name == 'main'
		is_annon = node.name == ''

		args_typedefs = {}
		for decor in node.decorator_list:
			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id=='typedef':
				for kw in decor.keywords:
					if isinstance(kw.value, ast.Num):
						args_typedefs[ kw.arg ] = '[%s:0]' %(kw.value.n-1)

		r = ['module %s(' %node.name]
		args = []
		for arg in node.args.args:
			aname = self.visit(arg)
			if aname in args_typedefs:
				args.append('input %s %s' %(args_typedefs[aname], aname))
			else:
				args.append('input '+aname)

		r.append(','.join(args) + ');')
		self.push()
		for b in node.body:
			r.append(self.indent()+self.visit(b))
		self.pull()
		r.append('endmodule')
		return '\n'.join(r)


def main(script, insert_runtime=True):
	script = typedpython.transform_source(script)
	#raise SyntaxError(script)
	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	g = VerilogGenerator( source=script )
	g.visit(tree) # first pass gathers classes
	return g.visit(tree)



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
		self._modules = []


	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		s = '$display(%s);' % ', '.join(args)
		return s

	def visit_Tuple(self, node):
		'''
		concatenates bits in verilog
		'''
		return '{%s}' %','.join(map(self.visit, node.elts))


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
		elif isinstance( node.context_expr, ast.Call ) and isinstance(node.context_expr.func, ast.Name) and node.context_expr.func.id == 'module':
			r.append('module _mod%s ();' %len(self._modules))
			self.push()
			initial = []
			functions = []
			for b in node.body:
				if isinstance(b, ast.FunctionDef):
					functions.append(b)
				else:
					initial.append(b)

			r.append(self.indent()+'initial begin')
			self.push()
			for b in initial:
				r.append(self.indent()+self.visit(b))
			self.pull()
			r.append(self.indent()+'end')

			for b in functions:
				r.append(self.visit(b))

			self.pull()
			r.append('endmodule')

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
			if isinstance(node.value, ast.Num):
				value = self.visit(node.value)
				return 'parameter %s = %s;' %(target, value)
			elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id in self._global_functions:
				r = ['%s %s(' %(node.value.func.id, target)]
				args = []
				for kw in node.value.keywords:
					args.append('.%s(%s)' %(kw.arg, self.visit(kw.value)))
				r.append('	'+', '.join(args))
				r.append(');')
				return '\n'.join(r)
		else:
			value = self.visit(node.value)
			return '%s = %s;' %(target, value)

	def _visit_call_helper(self, node):
		fname = self.visit(node.func)
		if fname in ('reg','wire','logic'):
			bits = None
			index = 0
			args = [arg.id for arg in node.args]
			for kw in node.keywords:
				if kw.arg=='bits':
					bits = kw.value.n-1
				elif kw.arg=='index':
					index = kw.value.n
			if bits is not None:
				return '%s [%s:%s] %s;' %(fname, bits,index, ','.join(args))
			else:
				return '%s %s;' %(fname, ','.join(args))

		elif fname.startswith('bit') and fname[3:].isdigit():
			bits = int(fname[3:])
			return "%s'd%s" %(bits, node.args[0].n)
		elif fname.endswith('.assign'):
			wire = fname.split('.')[0]
			return 'assign %s = %s;' %(wire, self.visit(node.args[0]))
		elif fname in self._global_functions:
			#raise RuntimeError('never should be reached - see visit_Assign')
			return '%s<<1;' %fname  ## triggers signal to always-function.
		elif fname == 'delay':
			return '#%s' %node.args[0].n
		else:
			raise SyntaxError(fname)

	def _visit_function(self, node):
		## is it clear that top level functions are actually modules?
		## it is bad for translation to hardware to have more than one module,
		## the new syntax `with module():` replaces the old style.
		#is_module = node.name in self._global_functions
		is_module = False  ## force to be false
		is_main = node.name == 'main'
		is_annon = node.name == ''
		always_type = 'always'
		outputs = []

		args_typedefs = {}
		for decor in node.decorator_list:
			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id=='typedef':
				for kw in decor.keywords:
					if isinstance(kw.value, ast.Num):
						args_typedefs[ kw.arg ] = '[%s:0]' %(kw.value.n-1)
					elif isinstance(kw.value, ast.Str):
						s = kw.value.s
						if s.startswith('[') and s.endswith(']') and ':' in s:
							bits,index = s[1:-1].split(':')
							s = '[%s:%s]' %(int(bits)-1, index)

						args_typedefs[ kw.arg ] = s

			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id=='returns':
				a = decor.args[0]
				if isinstance(a, ast.Call):
					outputs.append(self.visit(a))
				else:
					raise SyntaxError(a)

		if is_module:
			args = []
			for arg in node.args.args:
				aname = self.visit(arg)
				if aname in args_typedefs:
					args.append('input %s %s' %(args_typedefs[aname], aname))
				else:
					args.append('input '+aname)

			for out in outputs:
				if out.endswith(';'): out = out[:-1]  ## ugly
				args.append('output '+out)

			r = ['module %s( %s );' %(node.name, ', '.join(args))]
			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))
			self.pull()
			r.append('endmodule')
			return '\n'.join(r)

		else:
			r = [
				'reg bit %s;' %node.name,
				'%s @(%s) begin' %(always_type, node.name),
			]
			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))
			self.pull()
			r.append('end')
			return '\n'.join(r)

	def visit_For(self, node):
		'''
		note: loops in verilog requires: a delay, @, or wait(FALSE)

		'''
		start = 0
		end   = 0
		step  = 1
		target = node.target.id
		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id=='range':
			if len(node.iter.args)==1:
				end = self.visit(node.iter.args[0])
			elif len(node.iter.args)==2:
				start = self.visit(node.iter.args[0])
				end   = self.visit(node.iter.args[1])
			else:
				start = self.visit(node.iter.args[0])
				end   = self.visit(node.iter.args[1])
				step  = self.visit(node.iter.args[2])

			out = ['for (%s=%s; %s<%s; %s=%s+%s) begin' %(target, start, target, end, target,target,step)]
			self.push()
			for b in node.body:
				out.append(self.indent()+self.visit(b))
			self.pull()
			out.append(self.indent()+'end')
			return '\n'.join(out)
		else:
			raise SyntaxError("TODO other for loop types")



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



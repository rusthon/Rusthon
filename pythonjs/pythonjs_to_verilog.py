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
		self._tasks   = {}
		self._functions = {}
		self._always_functions = {}
		self._declares = set()


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
			declares  = []
			initial   = []
			initextra = []
			functions = []
			body      = []
			for b in node.body:
				if isinstance(b, ast.FunctionDef):
					functions.append(b)
				elif isinstance(b, ast.Expr):
					b = b.value
					if isinstance(b, ast.Call) and isinstance(b.func, ast.Name) and b.func.id in ('reg', 'wire', 'logic'):
						declares.append(b)
					elif isinstance(b, ast.Assign):
						raise SyntaxError('should not happen')
					else:
						initial.append(b)
				elif isinstance(b, ast.Assign):
					assert isinstance(b.targets[0], ast.Name)
					if isinstance(b.value, ast.Num):
						type = 'integer'
						if '.' in str(b.value.n): type = 'real'
						r.append('reg %s %s;' %(type, b.targets[0].id))
						initextra.append('%s = %s;' %(b.targets[0].id, self.visit(b.value)))

				else:  ## catches things like ast.Print, which is not an expression
					initial.append(b)

			for b in declares:
				r.append(self.indent()+self.visit(b))


			for b in functions:
				body.append(self.indent()+self.visit(b))

			body.append(self.indent()+'initial begin')
			self.push()
			for b in initial:
				body.append(self.indent()+self.visit(b))
			for b in initextra:
				body.append(self.indent()+b)

			self.pull()
			body.append(self.indent()+'end')

			for decl in self._declares:
				r.append(self.indent()+decl)

			r.extend(body)

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

		elif not self._function_stack and not self.indent():  ## global level
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
		elif fname in self._tasks:
			return '%s(%s);' %(fname, ','.join([arg.id for arg in node.args]))
		elif fname in self._functions:
			args = [self.visit(arg) for arg in node.args]
			for kw in node.keywords:
				# `error: malformed statement` given by iverilog
				args.append('.%s(%s)' %(kw.arg, self.visit(kw.value)))
			return '%s(%s);' %(fname, ', '.join(args))
		elif fname in self._always_functions:
			#raise RuntimeError('never should be reached - see visit_Assign')
			return '%s += 1;' %fname  ## triggers signal to always-function.
		elif fname == 'delay':
			delay = node.args[0].n
			if node.keywords:  ## delayed assignment
				kw = node.keywords[0]
				return '%s = #%s %s;' %(kw.arg, delay, self.visit(kw.value))
			else:
				return '#%s;' %delay
		else:
			raise SyntaxError(fname)

	def _visit_function(self, node):
		is_module = False
		is_task = False
		is_main = node.name == 'main'
		is_annon = node.name == ''
		always_type = None
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
				elif isinstance(a, ast.Name):
					if a.id=='int':
						outputs.append('integer')
					elif a.id=='float':
						outputs.append('real')
					else:
						outputs.append(a.id)


				else:
					raise SyntaxError(a)

			elif isinstance(decor, ast.Name) and decor.id=='task':
				is_task = True
				self._tasks[node.name] = node

			elif isinstance(decor, ast.Name) and decor.id=='always':
				always_type = decor.id

			elif isinstance(decor, ast.Name) and decor.id=='module':
				is_module = True


		if is_module or is_task:
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

			if is_module:
				r = ['module %s( %s );' %(node.name, ', '.join(args))]
				self.push()
				for b in node.body:
					r.append(self.indent()+self.visit(b))
				self.pull()
				r.append('endmodule')
				return '\n'.join(r)
			else:
				r = ['task %s;' %node.name]
				self.push()
				for arg in args:
					r.append(self.indent()+arg+';')

				for b in node.body:
					r.append(self.indent()+self.visit(b))
				self.pull()
				r.append('endtask')
				return '\n'.join(r)

		elif always_type:
			self._always_functions[node.name] = node
			r = [
				'reg integer %s;' %node.name,  ## should this be logic?
				'initial %s=0;' %node.name,    ## this should not trigger the func TODO fixme
			]
			if is_main:
				#r.append('%s @(posedge) begin' %always_type)
				r.append('%s begin' %always_type)
			else:
				r.append('%s @(%s) begin' %(always_type, node.name))

			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))

			if is_main:
				r.append('$finish;')
			self.pull()
			r.append('end')
			return '\n'.join(r)

		else:  ## normal verilog function
			assert len(outputs) < 2
			self._functions[ node.name ] = node
			if not outputs: outputs.append('void')
			r = ['function %s %s;' %(outputs[0], node.name)]
			for arg in node.args.args:
				aname = self.visit(arg)
				if aname in args_typedefs:
					r.append('input %s %s;' %(args_typedefs[aname], aname))
				else:
					r.append('input %s;'%aname)

			self.push()
			for b in node.body:
				r.append(self.indent()+self.visit(b))
			self.pull()


			r.append('endfunction')
			return '\n'.join(r)

			raise RuntimeError( self.format_error('invalid function type') )

	## not required in SystemVerilog 2005
	#def visit_Return(self, node):
	#	return '%s = %s' %(self._function_stack[-1].name, self.visit(node.value))

	def visit_For(self, node):
		'''
		notes:
			. the loop target must be declared as a register in the module header
			. loops in verilog requires: a delay, @, or wait(FALSE)

		'''
		start = 0
		end   = 0
		step  = 1
		target = node.target.id
		self._declares.add('reg integer %s;' %target)  ## insert into module header

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

			out = [
				#'for(%s = %s; %s <= %s; %s = %s + %s)' %(target, start, target, end, target,target,step),
				'for (%s=%s; %s<%s; %s++)' %(target, start, target, end, target),
				#'do @(posedge)',
			]
			self.push()
			out.append(self.indent()+'begin')

			self.push()
			for b in node.body:
				out.append(self.indent()+self.visit(b))
			#out.append(self.indent()+'i += %s;' %step)
			self.pull()
			out.append(self.indent()+'end')
			self.pull()
			#out.append(self.indent()+'while (%s < %s);' %(target, end))
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



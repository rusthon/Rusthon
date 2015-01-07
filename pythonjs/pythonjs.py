#!/usr/bin/env python
# PythonJS to JavaScript Translator
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"


import os, sys
from types import GeneratorType

import ast
from ast import Str
from ast import Name
from ast import Tuple
from ast import parse
from ast import Attribute
from ast import NodeVisitor

import typedpython
import ast_utils

class SwapLambda( RuntimeError ):
	def __init__(self, node):
		self.node = node
		RuntimeError.__init__(self)

class JSGenerator(ast_utils.NodeVisitorBase):
	def __init__(self, source, requirejs=True, insert_runtime=True, webworker=False, function_expressions=True, fast_javascript=False, fast_loops=False):
		assert source
		ast_utils.NodeVisitorBase.__init__(self, source)

		self._fast_js = fast_javascript
		self._fast_loops = fast_loops
		self._func_expressions = function_expressions
		self._indent = 0
		self._global_functions = {}
		self._function_stack = []
		self._requirejs = requirejs
		self._insert_runtime = insert_runtime
		self._webworker = webworker
		self._exports = set()
		self._inline_lambda = False
		self.catch_call = set()  ## subclasses can use this to catch special calls

		self.special_decorators = set(['__typedef__', '__glsl__', '__pyfunction__', 'expression'])
		self._glsl = False
		self._has_glsl = False
		self._typed_vars = dict()

		## the helper function below _mat4_to_vec4 is invalid because something can only be indexed
		## with a constant expression.  The GLSL compiler will throw this ERROR: 0:19: '[]' : Index expression must be constant"
		#self.glsl_runtime = 'vec4 _mat4_to_vec4( mat4 a, int col) { return vec4(a[col][0], a[col][1], a[col][2],a[col][3]); }'
		self.glsl_runtime = 'int _imod(int a, int b) { return int(mod(float(a),float(b))); }'

		self._lua  = False
		self._dart = False
		self._go   = False
		self._rust = False
		self._cpp = False
		self._cheader = []
		self._cppheader = []
		self._match_stack = []  # dicts of cases


	def reset(self):
		self._cheader = []
		self._cppheader = []
		self._match_stack = []


	def indent(self): return '\t' * self._indent
	def push(self): self._indent += 1
	def pull(self):
		if self._indent > 0: self._indent -= 1

	def visit_ClassDef(self, node):
		raise NotImplementedError(node)


	def visit_Global(self, node):
		return '/*globals: %s */' %','.join(node.names)

	def visit_Assign(self, node):
		# XXX: I'm not sure why it is a list since, mutiple targets are inside a tuple
		target = node.targets[0]
		if isinstance(target, Tuple):
			raise NotImplementedError('target tuple assignment should have been transformed to flat assignment by python_to_pythonjs.py')
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			## visit_BinOp checks for `numpy.float32` and changes the operands from `a*a` to `a[id]*a[id]`
			if self._glsl and value.startswith('numpy.'):
				self._typed_vars[ target ] = value
				return ''
			else:
				code = '%s = %s;' % (target, value)
				if self._requirejs and target not in self._exports and self._indent == 0 and '.' not in target:
					self._exports.add( target )
				return code

	def visit_AugAssign(self, node):
		## n++ and n-- are slightly faster than n+=1 and n-=1
		target = self.visit(node.target)
		op = self.visit(node.op)
		value = self.visit(node.value)
		if op=='+' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s ++;' %target
		if op=='-' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s --;' %target
		else:
			a = '%s %s= %s;' %(target, op, value)
		return a

	def visit_With(self, node):
		'''
		unified with-hacked syntax for all backends
		'''
		r = []
		is_select = False
		is_switch = False
		is_match  = False
		is_case   = False
		is_extern = False
		has_default = False

		if isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'gojs':
			#transform_gopherjs( node )
			self._with_gojs = True
			for b in node.body:
				a = self.visit(b)
				if a: r.append(a)
			self._with_gojs = False
			return '\n'.join(r)

		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == '__default__':
			has_default = True
			if self._rust and not self._cpp:
				r.append(self.indent()+'}, _ => {')
			else:
				r.append(self.indent()+'default:')

		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == '__select__':
			is_select = True
			self._match_stack.append( list() )
			self._in_select_hack = True

			if self._rust:
				r.append(self.indent()+'select! (')
			elif self._cpp:
				r.append(self.indent()+'cpp::select _select_;')  ## TODO nested, _select_N
			else:
				assert self._go
				r.append(self.indent()+'select {')

		elif isinstance( node.context_expr, ast.Call ):
			if not isinstance(node.context_expr.func, ast.Name):
				raise SyntaxError( self.visit(node.context_expr))

			if len(node.context_expr.args):
				a = self.visit(node.context_expr.args[0])
			else:
				assert len(node.context_expr.keywords)
				## need to catch if this is a new variable ##
				name = node.context_expr.keywords[0].arg
				if name not in self._known_vars:
					a = 'let %s = %s' %(name, self.visit(node.context_expr.keywords[0].value))
				else:
					a = '%s = %s' %(name, self.visit(node.context_expr.keywords[0].value))

			if node.context_expr.func.id == '__case__':
				is_case = True
				case_match = None
				select_hack = None
				if not len(node.context_expr.args):
					assert len(node.context_expr.keywords)==1
					kw = node.context_expr.keywords[0]
					if self._go:
						case_match = '%s := %s' %(kw.arg, self.visit(kw.value))
					elif self._cpp and hasattr(self, '_in_select_hack') and self._in_select_hack:
						select_hack = True
						case_match = '_select_.recv(%s, %s);' %(self.visit(kw.value), kw.arg)						
					else:
						case_match = '%s = %s' %(kw.arg, self.visit(kw.value))
				else:
					if isinstance(node.context_expr.args[0], ast.Compare):
						raise SyntaxError('"case x==n:" is not allowed in a case statement, use "case n:" instead.')
					case_match = self.visit(node.context_expr.args[0])

				if self._cpp and select_hack:
					r.append(self.indent()+case_match)
				elif self._rust and not self._cpp:
					if len(self._match_stack[-1])==0:
						r.append(self.indent()+'%s => {' %case_match)
					else:
						r.append(self.indent()+'}, %s => { ' %case_match )
				else:
					r.append(self.indent()+'case %s:' %case_match)

				self._match_stack[-1].append(case_match)


			elif node.context_expr.func.id == '__switch__':
				is_switch = True
				self._match_stack.append( list() )

				if self._rust and not self._cpp:
					r.append(self.indent()+'match (%s) {' %self.visit(node.context_expr.args[0]))
					is_match = True
				else:
					r.append(self.indent()+'switch (%s) {' %self.visit(node.context_expr.args[0]))


			elif node.context_expr.func.id == 'extern':
				r.append('extern "C" {')  ## TODO other abi's
				is_extern = True

			else:
				raise SyntaxError( 'invalid use of with')
		else:
			raise SyntaxError( 'invalid use of with')


		for b in node.body:
			a = self.visit(b)
			if a: r.append(self.indent()+a)

		if is_case and not self._rust:  ## always break after each case - do not fallthru to default: block
			r.append(self.indent()+'break;')
		###################################

		if is_extern:
			r.append(self.indent()+'}')

		elif is_select:
			if self._cpp:
				r.append(self.indent()+'_select_.wait();')
			elif self._rust:
				r.append(self.indent()+'})')  ## rust needs extra closing brace for the match-block
			else:
				r.append(self.indent()+'}')

		elif is_switch:
			if self._rust and not self._cpp:
				r.append(self.indent()+'}}')  ## rust needs extra closing brace for the match-block
			else:
				r.append(self.indent()+'}')

		return '\n'.join(r)


	def _new_module(self, name='main.js'):
		header = []
		if self._requirejs and not self._webworker:
			header.extend([
				'define( function(){',
				'__module__ = {}'
			])

		return {
			'name'   : name,
			'header' : header,
			'lines'  : []
		}

	def visit_Module(self, node):
		modules = []

		mod = self._new_module()
		modules.append( mod )
		lines = mod['lines']
		header = mod['header']


		if self._insert_runtime:
			dirname = os.path.dirname(os.path.abspath(__file__))
			runtime = open( os.path.join(dirname, 'pythonjs.js') ).read()
			lines.append( runtime )  #.replace('\n', ';') )

		for b in node.body:
			if isinstance(b, ast.Expr) and isinstance(b.value, ast.Call) and isinstance(b.value.func, ast.Name) and b.value.func.id == '__new_module__':
				mod = self._new_module( '%s.js' %b.value.args[0].id )
				modules.append( mod )
				lines = mod['lines']
				header = mod['header']

			else:
				line = self.visit(b)
				if line: lines.append( line )

		if self._requirejs and not self._webworker:
			for name in self._exports:
				if name.startswith('__'): continue
				lines.append( '__module__.%s = %s' %(name,name))

			lines.append( 'return __module__')
			lines.append('}) //end requirejs define')

		if self._has_glsl:
			header.append( 'var __shader_header__ = ["%s"]'%self.glsl_runtime )

		if len(modules) == 1:
			lines = header + lines
			## fixed by Foxboron
			return '\n'.join(l if isinstance(l,str) else l.encode("utf-8") for l in lines)
		else:
			d = {}
			for mod in modules:
				lines = mod['header'] + mod['lines']
				d[ mod['name'] ] = '\n'.join(l if isinstance(l,str) else l.encode("utf-8") for l in lines)
			return d

	def visit_Expr(self, node):
		# XXX: this is UGLY
		s = self.visit(node.value)
		if s.strip() and not s.endswith(';'):
			s += ';'
		if s==';': return ''
		else: return s


	def visit_In(self, node):
		return ' in '

	def visit_Tuple(self, node):
		if self._rust:
			return 'vec!(%s)' % ', '.join(map(self.visit, node.elts))
		else:
			return '[%s]' % ', '.join(map(self.visit, node.elts))

	def visit_List(self, node):
		a = []
		for elt in node.elts:
			b = self.visit(elt)
			if b is None: raise SyntaxError(elt)
			a.append( b )
		return '[%s]' % ', '.join(a)


	def visit_TryExcept(self, node):
		out = []
		out.append( self.indent() + 'try {' )
		self.push()
		out.extend(
			list( map(self.visit, node.body) )
		)
		self.pull()
		out.append( self.indent() + '} catch(__exception__) {' )
		self.push()
		out.extend(
			list( map(self.visit, node.handlers) )
		)
		self.pull()
		out.append( '}' )
		return '\n'.join( out )

	def visit_Raise(self, node):
		return 'throw new %s;' % self.visit(node.type)

	def visit_Yield(self, node):
		return 'yield %s' % self.visit(node.value)

	def visit_ImportFrom(self, node):
		# print node.module
		# print node.names[0].name
		# print node.level
		return ''

	def visit_ExceptHandler(self, node):
		out = ''
		if node.type:
			out = 'if (__exception__ == %s || __exception__ instanceof %s) {\n' % (self.visit(node.type), self.visit(node.type))
		if node.name:
			out += 'var %s = __exception__;\n' % self.visit(node.name)
		out += '\n'.join(map(self.visit, node.body)) + '\n'
		if node.type:
			out += '}\n'
		return out

	def visit_Lambda(self, node):
		args = [self.visit(a) for a in node.args.args]
		if args and args[0]=='__INLINE_FUNCTION__':
			self._inline_lambda = True
			#return '<LambdaError>'   ## skip node, the next function contains the real def
			raise SwapLambda( node )
		else:
			return '(function (%s) {return %s;})' %(','.join(args), self.visit(node.body))

	def function_has_getter_or_setter(self, node):
		options = {'getter':False, 'setter':False}
		for d in node.decorator_list:
			self._visit_decorator(d, options=options)
		return options['getter'] or options['setter']


	def _visit_decorator(self, decor, options=None, args_typedefs=None, chan_args_typedefs=None, generics=None, args_generics=None, func_pointers=None ):
		if options is None: options = dict()
		if args_typedefs is None: args_typedefs = dict()
		if chan_args_typedefs is None: chan_args_typedefs = dict()
		if generics is None: generics = set()
		if args_generics is None: args_generics = dict()
		if func_pointers is None: func_pointers = set()

		if isinstance(decor, ast.Name) and decor.id == 'property':
			## a function is marked as a getter with `@property`
			options['getter'] = True
		elif isinstance(decor, ast.Attribute) and isinstance(decor.value, ast.Name) and decor.attr == 'setter':
			## a function is marked as a setter with `@name.setter`
			options['setter'] = True

		elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef__':
			if len(decor.args) == 3:
				vname = self.visit(decor.args[0])
				vtype = self.visit(decor.args[1])
				vptr = decor.args[2].s
				args_typedefs[ vname ] = '%s %s' %(vptr, vtype)  ## space is required because it could have the `mut` keyword

			else:
				for key in decor.keywords:
					if isinstance( key.value, ast.Str):
						args_typedefs[ key.arg ] = key.value.s
					else:
						args_typedefs[ key.arg ] = self.visit(key.value)

					if args_typedefs[key.arg].startswith('func(') or args_typedefs[key.arg].startswith('lambda('):
						is_lambda_style = args_typedefs[key.arg].startswith('lambda(')
						func_pointers.add( key.arg )
						funcdef = args_typedefs[key.arg]
						## TODO - better parser
						hack = funcdef.replace(')', '(').split('(')
						lambda_args = hack[1].strip()
						lambda_return  = hack[3].strip()
						if self._cpp:
							if is_lambda_style:
								if lambda_return:  ## c++11
									args_typedefs[ key.arg ] = 'std::function<%s(%s)>  %s' %(lambda_return, lambda_args, key.arg)
								else:
									args_typedefs[ key.arg ] = 'std::function<void(%s)>  %s' %(lambda_args, key.arg)

							else:  ## old C style function pointers
								if lambda_return:
									args_typedefs[ key.arg ] = '%s(*%s)(%s)' %(lambda_args, key.arg, lambda_return)
								else:
									args_typedefs[ key.arg ] = 'void(*%s)(%s)' %(key.arg, lambda_args)

						else:
							if lambda_return:
								args_typedefs[ key.arg ] = '|%s|->%s' %(lambda_args, lambda_return)
							else:
								args_typedefs[ key.arg ] = '|%s|' %lambda_args

					## check for super classes - generics ##
					if args_typedefs[ key.arg ] in self._classes:
						raise SyntaxError('DEPRECATED')
						if node.name=='__init__':
							## generics type switch is not possible in __init__ because
							## it is used to generate the type struct, where types are static.
							## as a workaround generics passed to init always become `interface{}`
							args_typedefs[ key.arg ] = 'interface{}'
							#self._class_stack[-1]._struct_def[ key.arg ] = 'interface{}'
						else:
							classname = args_typedefs[ key.arg ]
							options['generic_base_class'] = classname
							generics.add( classname ) # switch v.(type) for each
							generics = generics.union( self._classes[classname]._subclasses )  ## TODO
							args_typedefs[ key.arg ] = 'interface{}'
							args_generics[ key.arg ] = classname

		elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef_chan__':
			for key in decor.keywords:
				chan_args_typedefs[ key.arg ] = self.visit(key.value)
		elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'returns':
			if decor.keywords:
				raise SyntaxError('invalid go return type')
			elif isinstance(decor.args[0], ast.Name):
				options['returns'] = decor.args[0].id
			else:
				options['returns'] = decor.args[0].s

			if options['returns'] == 'self':
				options['returns'] = '*' + self._class_stack[-1].name  ## go hacked generics
				options['returns_self'] = True
				self.method_returns_multiple_subclasses[ self._class_stack[-1].name ].add(node.name)



	def visit_FunctionDef(self, node):
		self._function_stack.append( node )
		node._local_vars = set()
		buffer = self._visit_function( node )

		if node == self._function_stack[0]:  ## could do something special here with global function
			#buffer += 'pythonjs.%s = %s' %(node.name, node.name)  ## this is no longer needed
			self._global_functions[ node.name ] = node

		self._function_stack.pop()
		return buffer

	def _visit_call_helper_var_glsl(self, node):
		lines = []
		for key in node.keywords:
			ptrs = key.value.id.count('POINTER')
			if ptrs:
				## TODO - preallocate array size - if nonliteral arrays are used later ##
				#name = key.arg
				#pid = '[`%s.length`]' %name
				#ptrs = pid * ptrs
				#lines.append( '%s %s' %(key.value.id.replace('POINTER',''), name+ptrs))

				## assume that this is a dynamic variable and will be typedef'ed by
				## __glsl_dynamic_typedef() is inserted just before the assignment.
				pass
			else:
				self._typed_vars[ key.arg ] = key.value.id
				lines.append( '%s %s' %(key.value.id, key.arg))

		return ';'.join(lines)


	def _visit_function(self, node):
		comments = []
		body = []
		is_main = node.name == 'main'
		is_annon = node.name == ''
		is_pyfunc    = False
		is_prototype = False
		protoname    = None
		func_expr    = False

		for decor in node.decorator_list:
			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'expression':
				assert len(decor.args)==1
				func_expr = True
				node.name = self.visit(decor.args[0])
			elif isinstance(decor, ast.Name) and decor.id == '__pyfunction__':
				is_pyfunc = True
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__prototype__':
				assert len(decor.args)==1
				is_prototype = True
				protoname = decor.args[0].id

		args = self.visit(node.args)

		if is_prototype:
			fdef = '%s.prototype.%s = function(%s)' % (protoname, node.name, ', '.join(args))

		elif len(self._function_stack) == 1:
			## this style will not make function global to the eval context in NodeJS ##
			#buffer = self.indent() + 'function %s(%s) {\n' % (node.name, ', '.join(args))

			## note if there is no var keyword and this function is at the global level,
			## then it should be callable from eval in NodeJS - this is not correct.
			## infact, var should always be used with function expressions.

			if self._func_expressions or func_expr:
				fdef = 'var %s = function(%s)' % (node.name, ', '.join(args))
			else:
				fdef = 'function %s(%s)' % (node.name, ', '.join(args))


			if self._requirejs and node.name not in self._exports:
				self._exports.add( node.name )

		else:

			if self._func_expressions or func_expr:
				fdef = 'var %s = function(%s)' % (node.name, ', '.join(args))
			else:
				fdef = 'function %s(%s)' % (node.name, ', '.join(args))

		body.append( fdef )

		body.append( self.indent() + '{' )
		self.push()
		next = None
		for i,child in enumerate(node.body):
			if isinstance(child, Str) or hasattr(child, 'SKIP'):
				continue
			elif isinstance(child, ast.Expr) and isinstance(child.value, ast.Str):
				comments.append('/* %s */' %child.value.s.strip() )
				continue

			#try:
			#	v = self.visit(child)
			#except SwapLambda as error:
			#	error.node.__class__ = ast.FunctionDef
			#	next = node.body[i+1]
			#	if not isinstance(next, ast.FunctionDef):
			#		raise SyntaxError('inline def is only allowed in javascript mode')
			#	error.node.__dict__ = next.__dict__
			#	error.node.name = ''
			#	v = self.visit(child)

			v = self.try_and_catch_swap_lambda(child, node.body)


			if v is None:
				msg = 'error in function: %s'%node.name
				msg += '\n%s' %child
				raise SyntaxError(msg)
			else:
				body.append( self.indent()+v)

		#buffer += '\n'.join(body)
		self.pull()
		#buffer += '\n%s}' %self.indent()

		body.append( self.indent() + '}' )

		buffer = '\n'.join( comments + body )

		#if self._inline_lambda:
		#	self._inline_lambda = False
		if is_annon:
			buffer = '__wrap_function__(' + buffer + ')'
		elif is_pyfunc:
			## TODO change .is_wrapper to .__pyfunc__
			buffer += ';%s.is_wrapper = true;' %node.name
		else:
			buffer += '\n'

		return self.indent() + buffer

	def try_and_catch_swap_lambda(self, child, body):
		try:
			return self.visit(child)
		except SwapLambda as e:

			next = None
			for i in range( body.index(child), len(body) ):
				n = body[ i ]
				if isinstance(n, ast.FunctionDef):
					if hasattr(n, 'SKIP'):
						continue
					else:
						next = n
						break
			assert next
			next.SKIP = True
			e.node.__class__ = ast.FunctionDef
			e.node.__dict__ = next.__dict__
			e.node.name = ''
			return self.try_and_catch_swap_lambda( child, body )



	def _visit_subscript_ellipsis(self, node):
		name = self.visit(node.value)
		return '%s["$wrapped"]' %name


	def visit_Subscript(self, node):
		if isinstance(node.slice, ast.Ellipsis):
			if self._glsl:
				#return '%s[_id_]' % self.visit(node.value)
				return '%s[matrix_index()]' % self.visit(node.value)
			else:
				return self._visit_subscript_ellipsis( node )
		else:
			return '%s[%s]' % (self.visit(node.value), self.visit(node.slice))

	def visit_Index(self, node):
		return self.visit(node.value)

	def visit_Slice(self, node):
		raise SyntaxError('list slice')  ## slicing not allowed here at js level

	def visit_arguments(self, node):
		out = []
		for name in [self.visit(arg) for arg in node.args]:
			out.append(name)
		return out

	def visit_Name(self, node):
		if node.id == 'None':
			return 'null'
		elif node.id == 'True':
			return 'true'
		elif node.id == 'False':
			return 'false'
		elif node.id == 'null':
			return 'null'
		return node.id

	def visit_Attribute(self, node):
		name = self.visit(node.value)
		attr = node.attr
		if self._glsl and name not in ('self', 'this'):
			if name not in self._typed_vars:
				return '`%s.%s`' % (name, attr)
			else:
				return '%s.%s' % (name, attr)
		return '%s.%s' % (name, attr)

	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		s = 'console.log(%s);' % ', '.join(args)
		return s

	def visit_keyword(self, node):
		if isinstance(node.arg, basestring):
			return node.arg, self.visit(node.value)
		return self.visit(node.arg), self.visit(node.value)

	def _visit_call_helper_instanceof(self, node):
		args = map(self.visit, node.args)
		if len(args) == 2:
			return '%s instanceof %s' %tuple(args)
		else:
			raise SyntaxError( args )

	def _visit_call_helper_new(self, node):
		args = map(self.visit, node.args)
		if len(args) == 1:
			return ' new %s' %args[0]
		else:
			raise SyntaxError( args )

	def _visit_call_special( self, node ):
		raise NotImplementedError('special call')

	def parse_go_style_arg( self, s ):
		if isinstance(s, ast.Str): s = s.s
		return s.split(']')[-1]

	def _visit_call_helper_go(self, node):
		go_types = 'bool string int float64'.split()

		name = self.visit(node.func)
		if name == '__go__':
			if self._cpp:
				## simple auto threads
				thread = '__thread%s__' %len(self._threads)
				self._threads.append(thread)
				closure_wrapper = '[&]{%s;}'%self.visit(node.args[0])
				return 'std::thread %s( %s );' %(thread, closure_wrapper)
			elif self._rust:
				return 'spawn(proc() {%s;} );' % self.visit(node.args[0])
			elif self._dart:
				return 'Isolate.spawn(%s);' %self.visit(node.args[0])
			else:
				return 'go %s' %self.visit(node.args[0])
		elif name == '__go_make__':
			if len(node.args)==2:
				return 'make(%s, %s)' %(self.visit(node.args[0]), self.visit(node.args[1]))
			elif len(node.args)==3:
				return 'make(%s, %s, %s)' %(self.visit(node.args[0]), self.visit(node.args[1]), self.visit(node.args[1]))
			else:
				raise SyntaxError('go make requires 2 or 3 arguments')
		elif name == '__go_make_chan__':
			## channel constructors
			if self._cpp:
				## cpp-channel API supports input/output
				return 'cpp::channel<%s>{}'%self.visit(node.args[0])
			elif self._rust:
				## rust returns a tuple input/output that needs to be destructured by the caller
				return 'channel::<%s>()' %self.visit(node.args[0])
			else:  ## Go
				return 'make(chan %s)' %self.visit(node.args[0])

		elif name == '__go__array__':
			if isinstance(node.args[0], ast.BinOp):# and node.args[0].op == '<<':  ## todo assert right is `typedef`
				a = self.visit(node.args[0].left)
				if a in go_types:
					if self._go:
						return '*[]%s' %a
					elif self._rust:
						return '&mut Vec<%s>' %a  ## TODO test this
					else:
						raise RuntimeError('todo')
				else:
					return '*[]*%s' %a  ## todo - self._catch_assignment_array_of_obs = true

			else:
				a = self.visit(node.args[0])
				if a in go_types:
					return '[]%s{}' %a
				else:
					return '[]*%s{}' %a
		elif name == '__go__addr__':
			return '&%s' %self.visit(node.args[0])
		else:
			raise SyntaxError(name)


	def visit_Call(self, node):
		name = self.visit(node.func)
		if name in typedpython.GO_SPECIAL_CALLS.values():
			return self._visit_call_helper_go( node )

		elif name in self.catch_call:
			return self._visit_call_special( node )

		elif self._glsl and isinstance(node.func, ast.Attribute):
			if isinstance(node.func.value, ast.Name) and node.func.value.id in self._typed_vars:
				args = ','.join( [self.visit(a) for a in node.args] )
				return '`__struct_name__`_%s(%s, %s)' %(node.func.attr, node.func.value.id, args)
			else:
				return '`%s`' %self._visit_call_helper(node)

		elif self._glsl and name == 'len':
			if isinstance(node.args[0], ast.Name):
				return '`%s.length`' %node.args[0].id
			elif isinstance(node.args[0], ast.Subscript):
				s = node.args[0]
				v = self.visit(s).replace('`', '')
				return '`%s.length`' %v

			elif isinstance(node.args[0], ast.Attribute):  ## assume struct array attribute
				s = node.args[0]
				v = self.visit(s).replace('`', '')
				return '`%s.length`' %v

		elif name == 'glsl_inline_assign_from_iterable':
			## the target must be declared without a typedef, because if declared first, it can not be redeclared,
			## in the if-assignment block, the typedef is not given because `Iter_n` already has been typed beforehand.
			sname = node.args[0].s
			target = node.args[1].s
			iter  = node.args[2].id
			self._typed_vars[ target ] = sname


			lines = [
				'`@var __length__ = %s.length;`' %iter,
				#'`@console.log("DEBUG iter: "+%s);`' %iter,
				#'`@console.log("DEBUG first item: "+%s[0]);`' %iter,
				#'`@var __struct_name__ = %s[0].__struct_name__;`' %iter,
				##same as above - slower ##'`@var __struct_name__ = glsljit.define_structure(%s[0]);`' %iter,
				#'`@console.log("DEBUG sname: "+__struct_name__);`',
				'`@var %s = %s[0];`' %(target, iter)  ## capture first item with target name so that for loops can get the length of member arrays
			]

			#lines.append('for (int _iter=0; _iter < `__length__`; _iter++) {' )

			## declare struct variable ##
			#lines.append( '%s %s;' %(sname, target))

			## at runtime loop over subarray, for each index inline into the shader's for-loop an if test,
			lines.append( '`@for (var __j=0; __j<__length__; __j++) {`')
			#lines.append(     '`@glsljit.push("if (OUTPUT_INDEX==" +__j+ ") { %s %s=%s_" +__j+ ";}");`' %(sname, target, iter))
			lines.append(     '`@glsljit.push("if (matrix_index()==" +__j+ ") { %s=%s_" +__j+ ";}");`' %(target, iter))
			lines.append( '`@}`')


			#lines.append( '}' )  ## end of for loop
			return '\n'.join(lines)

		elif name == 'glsl_inline_push_js_assign':
			# '@' triggers a new line of generated code
			n = node.args[0].s
			if isinstance(node.args[1], ast.Attribute):  ## special case bypass visit_Attribute
				v = '%s.%s' %(node.args[1].value.id, node.args[1].attr )
			else:
				v = self.visit(node.args[1])

			v = v.replace('`', '')  ## this is known this entire expression is an external call.

			## check if number is required because literal floats like `1.0` will get transformed to `1` by javascript toString
			orelse = 'typeof(%s)=="object" ? glsljit.object(%s, "%s") : glsljit.push("%s="+%s+";")' %(n, n,n, n,n)

			## if a constant number literal directly inline
			if v.isdigit() or (v.count('.')==1 and v.split('.')[0].isdigit() and v.split('.')[1].isdigit()):
				#if_number = ' if (typeof(%s)=="number") { glsljit.push("%s=%s;") } else {' %(n, n,v)
				#return '`@%s=%s; %s if (%s instanceof Array) {glsljit.array(%s, "%s")} else {%s}};`' %(n,v, if_number, n, n,n, orelse)
				return '`@%s=%s; glsljit.push("%s=%s;");`' %(n,v, n,v)
			else:
				return '`@%s=%s; if (%s instanceof Array) {glsljit.array(%s, "%s")} else { if (%s instanceof Int16Array) {glsljit.int16array(%s,"%s")} else {%s} };`' %(n,v, n, n,n,  n,n,n,  orelse)

		#elif name == 'glsl_inline':
		#	return '`%s`' %self.visit(node.args[0])
		#elif name == 'glsl_inline_array':
		#	raise NotImplementedError
		#	return '`__glsl_inline_array(%s, "%s")`' %(self.visit(node.args[0]), node.args[1].s)

		elif name == 'instanceof':  ## this gets used by "with javascript:" blocks to test if an instance is a JavaScript type
			return self._visit_call_helper_instanceof( node )

		elif name == 'new':
			return self._visit_call_helper_new( node )

		elif name == '__ternary_operator__':
			args = map(self.visit, node.args)
			if len(args) == 2:
				return '((%s) ? %s : %s)' %(args[0], args[0], args[1])
			elif len(args) == 3:
				return '((%s) ? %s : %s)' %(args[0], args[1], args[2])
			else:
				raise SyntaxError( args )

		elif name == 'numpy.array':
			return self._visit_call_helper_numpy_array(node)

		elif name == 'JSObject':
			return self._visit_call_helper_JSObject( node )

		elif name == 'var':
			if self._glsl:
				return self._visit_call_helper_var_glsl( node )
			else:
				return self._visit_call_helper_var( node )

		elif name == 'JSArray':
			return self._visit_call_helper_JSArray( node )

		elif name == 'inline' or name == 'JS':
			assert len(node.args)==1 and isinstance(node.args[0], ast.Str)
			return self._inline_code_helper( node.args[0].s )

		elif name == 'dart_import':
			if len(node.args) == 1:
				return 'import "%s";' %node.args[0].s
			elif len(node.args) == 2:
				return 'import "%s" as %s;' %(node.args[0].s, node.args[1].s)
			else:
				raise SyntaxError
		elif name == 'list':
			return self._visit_call_helper_list( node )

		elif name == '__get__' and len(node.args)==2 and isinstance(node.args[1], ast.Str) and node.args[1].s=='__call__':
			return self._visit_call_helper_get_call_special( node )

		#elif name in self._global_functions:
		#	return_id = self.inline_function( node )
		#	code = self.writer.getvalue()
		#	return '\n'.join([code, return_id])
		elif name.split('.')[-1] == '__go__receive__':
			raise SyntaxError('__go__receive__')

		else:
			return self._visit_call_helper(node)

	def _visit_call_helper(self, node):
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		fname = self.visit(node.func)
		if fname=='__DOLLAR__': fname = '$'
		return '%s(%s)' % (fname, args)

	def inline_helper_remap_names(self, remap):
		return "var %s;" %','.join(remap.values())

	def inline_helper_return_id(self, return_id):
		return "var __returns__%s = null;"%return_id

	def _visit_call_helper_numpy_array(self, node):
		if self._glsl:
			return self.visit(node.keywords[0].value)
		else:
			return self.visit(node.args[0])

	def _visit_call_helper_list(self, node):
		name = self.visit(node.func)
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		return '%s(%s)' % (name, args)

	def _visit_call_helper_get_call_special(self, node):
		name = self.visit(node.func)
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		return '%s(%s)' % (name, args)


	def _visit_call_helper_JSArray(self, node):
		if node.args:
			args = map(self.visit, node.args)
			out = ', '.join(args)
			#return '__create_array__(%s)' % out
			return '[%s]' % out

		else:
			return '[]'


	def _visit_call_helper_JSObject(self, node):
		if node.keywords:
			kwargs = map(self.visit, node.keywords)
			f = lambda x: '"%s": %s' % (x[0], x[1])
			out = ', '.join(map(f, kwargs))
			return '{%s}' % out
		else:
			return '{}'

	def _visit_call_helper_var(self, node):
		args = [ self.visit(a) for a in node.args ]
		if self._function_stack:
			fnode = self._function_stack[-1]
			rem = []
			for arg in args:
				if arg in fnode._local_vars:
					rem.append( arg )
				else:
					fnode._local_vars.add( arg )
			for arg in rem:
				args.remove( arg )
		out = []
		if args:
			out.append( 'var ' + ','.join(args) )
		if node.keywords:
			out.append( 'var ' + ','.join([key.arg for key in node.keywords]) )
		return ';'.join(out)

	def _inline_code_helper(self, s):
		## TODO, should newline be changed here?
		s = s.replace('\n', '\\n').replace('\0', '\\0')  ## AttributeError: 'BinOp' object has no attribute 's' - this is caused by bad quotes
		if s.strip().startswith('#'): s = '/*%s*/'%s

		if '__new__>>' in s:
			## hack that fixes inline `JS("new XXX")`,
			## TODO improve typedpython to be aware of quoted strings
			s = s.replace('__new__>>', ' new ')

		elif '"' in s or "'" in s:  ## can not trust direct-replace hacks
			pass
		else:
			if ' or ' in s:
				s = s.replace(' or ', ' || ')
			if ' not ' in s:
				s = s.replace(' not ', ' ! ')
			if ' and ' in s:
				s = s.replace(' and ', ' && ')
		return s

	def visit_While(self, node):
		body = [ 'while (%s)' %self.visit(node.test), self.indent()+'{']
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		#if '"' in s:
		#	return "'%s'" % s
		return '"%s"' % s

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)

		if op == '>>' and left == '__new__':

			## this can happen because python_to_pythonjs.py will catch when a new class instance is created
			## (when it knows that class name) and replace it with `new(MyClass())`; but this can cause a problem
			## if later the user changes that part of their code into a module, and loads it as a javascript module,
			## they may update their code to call `new MyClass`, and then later go back to the python library.
			## the following hack prevents `new new`
			if isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name) and node.right.func.id=='new':
				right = self.visit(node.right.args[0])

			return ' new %s' %right

		if left in self._typed_vars and self._typed_vars[left] == 'numpy.float32':
			left += '[_id_]'
		if right in self._typed_vars and self._typed_vars[right] == 'numpy.float32':
			right += '[_id_]'

		return '(%s %s %s)' % (left, op, right)

	def visit_Mult(self, node):
		return '*'

	def visit_Add(self, node):
		return '+'

	def visit_Sub(self, node):
		return '-'

	def visit_Div(self, node):
		return '/'

	def visit_Mod(self, node):
		return '%'

	def visit_Lt(self, node):
		return '<'

	def visit_Gt(self, node):
		return '>'

	def visit_GtE(self, node):
		return '>='

	def visit_LtE(self, node):
		return '<='

	def visit_LShift(self, node):
		return '<<'
	def visit_RShift(self, node):
		return '>>'
	def visit_BitXor(self, node):
		return '^'
	def visit_BitOr(self, node):
		return '|'
	def visit_BitAnd(self, node):
		return '&'

	def visit_Return(self, node):
		if isinstance(node.value, Tuple):
			return 'return [%s];' % ', '.join(map(self.visit, node.value.elts))
		if node.value:
			return 'return %s;' % self.visit(node.value)
		return 'return undefined;'

	def visit_Pass(self, node):
		return '/*pass*/'

	def visit_Eq(self, node):
		return '=='

	def visit_NotEq(self, node):
		return '!='

	def visit_Num(self, node):
		return str(node.n)

	def visit_Is(self, node):
		return '==='

	def visit_Compare(self, node):
		if self._glsl:
			return self.visit(node.left)
		elif isinstance(node.ops[0], ast.Eq):
			left = self.visit(node.left)
			right = self.visit(node.comparators[0])
			if self._lua:
				return '%s == %s' %(left, right)
			elif self._fast_js:
				return '(%s===%s)' %(left, right)
			else:
				return '(%s instanceof Array ? JSON.stringify(%s)==JSON.stringify(%s) : %s===%s)' %(left, left, right, left, right)
		elif isinstance(node.ops[0], ast.NotEq):
			left = self.visit(node.left)
			right = self.visit(node.comparators[0])
			if self._lua:
				return '%s ~= %s' %(left, right)
			elif self._fast_js:
				return '(%s!==%s)' %(left, right)
			else:
				return '(!(%s instanceof Array ? JSON.stringify(%s)==JSON.stringify(%s) : %s===%s))' %(left, left, right, left, right)

		else:
			comp = [ '(']
			comp.append( self.visit(node.left) )
			comp.append( ')' )

			for i in range( len(node.ops) ):
				comp.append( self.visit(node.ops[i]) )

				if isinstance(node.ops[i], ast.Eq):
					raise SyntaxError('TODO')

				elif isinstance(node.comparators[i], ast.BinOp):
					comp.append('(')
					comp.append( self.visit(node.comparators[i]) )
					comp.append(')')
				else:
					comp.append( self.visit(node.comparators[i]) )

			return ' '.join( comp )

	def visit_Not(self, node):
		return '!'

	def visit_IsNot(self, node):
		return '!=='

	def visit_UnaryOp(self, node):
		#return self.visit(node.op) + self.visit(node.operand)
		return '%s (%s)' %(self.visit(node.op),self.visit(node.operand))

	def visit_USub(self, node):
		return '-'
		
	def visit_And(self, node):
		return ' && '

	def visit_Or(self, node):
		return ' || '

	def visit_BoolOp(self, node):
		op = self.visit(node.op)
		return '('+ op.join( [self.visit(v) for v in node.values] ) +')'

	def visit_If(self, node):
		out = []
		test = self.visit(node.test)
		if test.startswith('(') and test.endswith(')'):
			out.append( 'if %s' %test )
		else:
			out.append( 'if (%s)' %test )
		out.append( self.indent() + '{' )

		self.push()

		for line in list(map(self.visit, node.body)):
			if line is None: continue
			out.append( self.indent() + line )

		orelse = []
		for line in list(map(self.visit, node.orelse)):
			orelse.append( self.indent() + line )

		self.pull()

		if orelse:
			out.append( self.indent() + '}')
			out.append( self.indent() + 'else')
			out.append( self.indent() + '{')
			out.extend( orelse )

		out.append( self.indent() + '}' )

		return '\n'.join( out )


	def visit_Dict(self, node):
		a = []
		for i in range( len(node.keys) ):
			k = self.visit( node.keys[ i ] )
			v = self.visit( node.values[i] )
			a.append( '%s:%s'%(k,v) )
		b = ', '.join( a )
		return '{ %s }' %b


	def _visit_for_prep_iter_helper(self, node, out, iter_name):
		## support "for key in JSObject" ##
		#out.append( self.indent() + 'if (! (iter instanceof Array) ) { iter = Object.keys(iter) }' )
		## new style - Object.keys only works for normal JS-objects, not ones created with `Object.create(null)`
		if not self._fast_loops:
			out.append(
				self.indent() + 'if (! (%s instanceof Array || typeof %s == "string" || __is_typed_array(%s) || __is_some_array(%s) )) { %s = __object_keys__(%s) }' %(iter_name, iter_name, iter_name, iter_name, iter_name, iter_name)
			)

	def _visit_for_glsl(self, node):
		target = self.visit(node.target)

		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id=='iter':  ## `for i in iter(n):`
			assert isinstance(node.iter.args[0], ast.Name)
			iter = node.iter.args[0].id
			self._typed_vars[target] = 'struct*'  ## this fixes attributes on structs

			lines = [
				'`@var __length__ = %s.length;`' %iter,
				#'`@console.log("DEBUG iter: "+%s);`' %iter,
				#'`@console.log("DEBUG first item: "+%s[0]);`' %iter,
				'`@var __struct_name__ = %s[0].__struct_name__;`' %iter,
				##same as above - slower ##'`@var __struct_name__ = glsljit.define_structure(%s[0]);`' %iter,
				#'`@console.log("DEBUG sname: "+__struct_name__);`',
				'`@var %s = %s[0];`' %(target, iter)  ## capture first item with target name so that for loops can get the length of member arrays
			]

			##TODO## lines.append('$')  ## optimizes webclgl parser

			lines.append('for (int _iter=0; _iter < `__length__`; _iter++) {' )

			## declare struct variable ##
			lines.append( '`__struct_name__` %s;' %target)

			## at runtime loop over subarray, for each index inline into the shader's for-loop an if test,
			lines.append( '`@for (var __j=0; __j<__length__; __j++) {`')
			lines.append(     '`@glsljit.push("if (_iter==" +__j+ ") { %s=%s_" +__j+ ";}");`' %(target, iter))
			lines.append( '`@}`')

			##TODO## lines.append('$')  ## optimizes webclgl parser


		elif isinstance(node.iter, ast.Call):  ## `for i in range(n):`
			iter = self.visit(node.iter.args[0])
			lines = ['for (int %s=0; %s < %s; %s++) {' %(target, target, iter, target)]
		elif isinstance(node.iter, ast.Name):  ## `for subarray in arrayofarrays:`
			## capture the length of the subarray into the current javascript scope
			## this is required to inline the lengths as constants into the GLSL for loops
			lines = ['`@var __length__ = %s[0].length;`' %node.iter.id]
			## start the GLSL for loop - `__length__` is set above ##
			lines.append('for (int _iter=0; _iter < `__length__`; _iter++) {' )

			## declare subarray with size ##
			lines.append( 'float %s[`__length__`];' %target)

			## at runtime loop over subarray, for each index inline into the shader's for-loop an if test,
			lines.append( '`@for (var __j=0; __j<__length__; __j++) {`')
			## below checks if the top-level iterator is the same index, and if so copy its contents into the local subarray,
			lines.append(     '`@glsljit.push("if (_iter==" +__j+ ") { for (int _J=0; _J<" +__length__+ "; _J++) {%s[_J] = %s_" +__j+ "[_J];} }");`' %(target, node.iter.id))
			lines.append( '`@}`')
			## this works because the function glsljit.array will unpack an array of arrays using the variable name with postfix "_n"
			## note the extra for loop `_J` is required because the local subarray can not be assigned to `A_n`

		else:
			raise SyntaxError(node.iter)

		for b in node.body:
			lines.append( self.visit(b) )
		lines.append( '}' )  ## end of for loop
		return '\n'.join(lines)


	_iter_id = 0
	def visit_For(self, node):
		'''
		for loops inside a `with javascript:` block will produce this faster for loop.

		note that the rules are python-style, even though we are inside a `with javascript:` block:
			. an Array is like a list, `for x in Array` gives you the value (not the index as you would get in pure javascript)
			. an Object is like a dict, `for v in Object` gives you the key (not the value as you would get in pure javascript)

		if your are trying to opitmize looping over a PythonJS list, you can do this:
			for v in mylist[...]:
				print v
		above works because [...] returns the internal Array of mylist

		'''
		if self._glsl:
			return self._visit_for_glsl( node )

		target = node.target.id
		iter = self.visit(node.iter) # iter is the python iterator

		out = []
		body = []

		self._iter_id += 1
		index = '__i%s' %self._iter_id
		if not self._fast_loops:
			iname = '__iter%s' %self._iter_id
			out.append( self.indent() + 'var %s = %s;' % (iname, iter) )
		else:
			iname = iter

		self._visit_for_prep_iter_helper(node, out, iname)

		if self._fast_loops:
			out.append( 'for (var %s=0; %s < %s.length; %s++)' % (index, index, iname, index) )
			out.append( self.indent() + '{' )

		else:
			out.append( self.indent() + 'for (var %s=0; %s < %s.length; %s++) {' % (index, index, iname, index) )
		self.push()

		body.append( self.indent() + 'var %s = %s[ %s ];' %(target, iname, index) )

		for line in list(map(self.visit, node.body)):
			body.append( self.indent() + line )

		self.pull()
		out.extend( body )
		out.append( self.indent() + '}' )

		return '\n'.join( out )

	def visit_Continue(self, node):
		return 'continue'

	def visit_Break(self, node):
		return 'break;'


def generate_minimal_runtime():
	from python_to_pythonjs import main as py2pyjs
	a = py2pyjs(
		open('runtime/builtins_core.py', 'rb').read(),
		module_path = 'runtime',
		fast_javascript = True
	)
	return main( a, requirejs=False, insert_runtime=False, function_expressions=True, fast_javascript=True )

def generate_runtime():
	from python_to_pythonjs import main as py2pyjs
	builtins = py2pyjs(
		open('runtime/builtins.py', 'rb').read(),
		module_path = 'runtime',
		fast_javascript = True
	)
	lines = [
		main( open('runtime/pythonpythonjs.py', 'rb').read(), requirejs=False, insert_runtime=False, function_expressions=True, fast_javascript=True ), ## lowlevel pythonjs
		main( builtins, requirejs=False, insert_runtime=False, function_expressions=True, fast_javascript=True )
	]
	return '\n'.join( lines )

def main(source, requirejs=True, insert_runtime=True, webworker=False, function_expressions=True, fast_javascript=False, fast_loops=False):
	head = []
	tail = []
	script = False
	osource = source
	if source.strip().startswith('<html'):
		lines = source.splitlines()
		for line in lines:
			if line.strip().startswith('<script') and 'type="text/python"' in line:
				head.append( '<script type="text/javascript">')
				script = list()
			elif line.strip() == '</script>':
				if type(script) is list:
					source = '\n'.join(script)
					script = True
					tail.append( '</script>')
				elif script is True:
					tail.append( '</script>')
				else:
					head.append( '</script>')

			elif isinstance( script, list ):
				script.append( line )

			elif script is True:
				tail.append( line )

			else:
				head.append( line )


	try:
		tree = ast.parse( source )
		#raise SyntaxError(source)
	except SyntaxError:
		import traceback
		err = traceback.format_exc()
		sys.stderr.write( err )
		sys.stderr.write( '\n--------------error in second stage translation--------------\n' )

		lineno = 0
		for line in err.splitlines():
			if "<unknown>" in line:
				lineno = int(line.split()[-1])


		lines = source.splitlines()
		if lineno > 10:
			for i in range(lineno-5, lineno+5):
				sys.stderr.write( 'line %s->'%i )
				sys.stderr.write( lines[i] )
				if i==lineno-1:
					sys.stderr.write('  <<SyntaxError>>')
				sys.stderr.write( '\n' )

		else:
			sys.stderr.write( lines[lineno] )
			sys.stderr.write( '\n' )

		if '--debug' in sys.argv:
			sys.stderr.write( osource )
			sys.stderr.write( '\n' )

		sys.exit(1)

	gen = JSGenerator(
		source = source,
		requirejs=requirejs, 
		insert_runtime=insert_runtime, 
		webworker=webworker, 
		function_expressions=function_expressions,
		fast_javascript = fast_javascript,
		fast_loops      = fast_loops
	)
	output = gen.visit(tree)

	if head and not isinstance(output, dict):
		head.append( output )
		head.extend( tail )
		output = '\n'.join( head )

	return output


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
	if '--runtime' in sys.argv:
		print('creating new runtime: pythonjs.js')
		open('pythonjs.js', 'wb').write( generate_runtime() )
	elif '--miniruntime' in sys.argv:
		print('creating new runtime: pythonjs-minimal.js')
		open('pythonjs-minimal.js', 'wb').write( generate_minimal_runtime() )

	else:
		command()

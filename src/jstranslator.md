Javascript Translator
---------------------

translates intermediate form into final javascript.
This is also subclassed by these other backends:
* [gotranslator.md](gotranslator.md)
* [rusttranslator.md](rusttranslator.md)
* [cpptranslator.md](cpptranslator.md)

notes:
* the implementation of `spawn` is in [generatorbase.md](generatorbase.md)
* the builtin webworker pool spawn manager is in [builtins_core.py](runtime/builtins_core.py)

```python
# PythonJS to JavaScript Translator
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

## note this should be cleared after a full round of translation,
## first the runtime is regenerated, and that is the first to populate
## the unicode name mapping.
UNICODE_NAME_MAP = {}

from types import GeneratorType
from ast import Str
from ast import Name
from ast import Tuple
from ast import Attribute
from ast import NodeVisitor

class SwapLambda( RuntimeError ):
	def __init__(self, node):
		self.node = node
		RuntimeError.__init__(self)

class JSGenerator(NodeVisitorBase, GeneratorBase):
	def __init__(self, source, requirejs=True, insert_runtime=True, webworker=False, function_expressions=True, fast_javascript=False, fast_loops=False, runtime_checks=True):
		assert source
		NodeVisitorBase.__init__(self, source)

		self._unicode_name_map = UNICODE_NAME_MAP

		self._iter_id = 0  ## used by for loops
		self._in_try = False
		self._runtime_type_checking = runtime_checks
		self.macros = {}
		self._sleeps = 0
		self._has_channels = False
		self._func_recv = 0
		self._with_oo = False
		self._fast_js = fast_javascript
		self._fast_loops = fast_loops
		self._func_expressions = function_expressions
		self._indent = 0
		self._global_functions = {}
		self._function_stack = []
		self._requirejs = requirejs
		self._insert_runtime = insert_runtime
		self._insert_nodejs_runtime = False
		self._insert_nodejs_tornado = False
		self._webworker = webworker
		self._exports = set()
		self._inline_lambda = False
		self.catch_call = set()  ## subclasses can use this to catch special calls

		self.special_decorators = set(['__typedef__', '__pyfunction__', 'expression'])

		self._typed_vars = dict()

		self._lua  = False
		self._dart = False
		self._go   = False
		self._rust = False
		self._cpp = False
		self._cheader = []
		self._cppheader = []
		self._cpp_class_impl = []
		self._match_stack = []       ## dicts of cases
		self._rename_hacks = {}      ## used by c++ backend, to support `if isinstance`
		self._globals = {}           ## name : type
		self._called_functions = {}  ## name : number of calls
```

reset
-----
`reset()` needs to be called for multipass backends, that are dumb and run translation twice to gather info in two passes.

```python

	def reset(self):
		self._cheader = []
		self._cppheader = []
		self._cpp_class_impl = []
		self._match_stack = []

```

Class
------
class is not implemented here for javascript, it gets translated ahead of time in 
[intermediateform.md](intermediateform.md)


```python

	def visit_ClassDef(self, node):
		raise NotImplementedError(node)


	def visit_Global(self, node):
		return '/*globals: %s */' %','.join(node.names)

	def visit_Assert(self, node):
		return 'if (!(%s)) {throw new Error("assertion failed"); }' %self.visit(node.test)


	def visit_Expr(self, node):
		## note: the javascript backend overloads this ##
		s = self.visit(node.value)
		if s is None:
			raise RuntimeError('GeneratorBase ExpressionError: %s' %node.value)
		if s.strip() and not s.endswith(';'):
			s += ';'

		if s==';' or not s:
			return ''
		else:
			if self._in_try or not self._runtime_type_checking:
				return s
			elif not len(self._function_stack) or s.startswith('var '):
				return s
			elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id=='inline':
				return s
			elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id=='sleep':
				assert self._stack[-1] is node
				if len(self._stack) < 3:
					raise SyntaxError('the builtin `sleep` can not be used at the global level outside of a function.')
				elif isinstance(self._stack[-2], ast.If):
					raise SyntaxError('the builtin `sleep` can only be used in the function body, and not under an `if` block.')
				elif isinstance(self._stack[-2], ast.For):
					raise SyntaxError('the builtin `sleep` can only be used in the function body, and not inside a `for` loop.')
				elif isinstance(self._stack[-2], ast.While):
					raise SyntaxError('the builtin `sleep` can only be used in the function body, and not inside a `for` or `while` loop.')
				elif not isinstance(self._stack[-2], ast.FunctionDef):
					raise SyntaxError('the builtin `sleep` can only be used in the function body, and not nested under any blocks.')
				return s
			else:
				## note `debugger` is a special statement in javascript that sets a break point if the js console debugger is open ##
				caller = self._function_stack[-1].name
				called = None
				if isinstance(node.value, ast.Call):
					called = self.visit(node.value.func)

				a = '/***/ try {\n'
				a += self.indent() + s + '\n'
				if called:
					a += self.indent() + '/***/ } catch (__err) { if (𝗗𝗲𝗯𝘂𝗴𝗴𝗲𝗿.onerror(__err, %s, %s)==true){debugger;}else{throw __err;} };' %(caller, called)
				else:
					a += self.indent() + '/***/ } catch (__err) { if (𝗗𝗲𝗯𝘂𝗴𝗴𝗲𝗿.onerror(__err, %s)==true){debugger;}else{throw __err;} };' %caller
				return a


	def visit_Assign(self, node):
		target = node.targets[0]
		if isinstance(target, Tuple):
			raise NotImplementedError('target tuple assignment should have been transformed to flat assignment by python_to_pythonjs.py')
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			if value.startswith('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.send('):
				if target=='this':  ## should assert that this is on the webworker side
					target = 'this.__uid__'
					value = value.replace('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.send(', 'self.postMessage(')
				code = value % target
			elif value.startswith('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.recv') or value.startswith('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.get') or value.startswith('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.call'):
				self._func_recv += 1
				self.push()
				code = value % target
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
		elif op=='-' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s --;' %target
		elif op=='+' and isinstance(node.value, ast.Num):
			a = '%s %s= %s;' %(target, op, value)  ## direct
		elif op == '+':
			## supports += syntax for arrays ##
			x = [
				'if (%s instanceof Array || 𝑰𝒔𝑻𝒚𝒑𝒆𝒅𝑨𝒓𝒓𝒂𝒚(%s)) { %s.extend(%s); }' %(target,target,target, value),
				'else { %s %s= %s; }'%(target, op, value)
			]
			a = '\n'.join(x)
		else:
			a = '%s %s= %s;' %(target, op, value)  ## direct


		return a

```

RequireJS
---------

generate a generic or requirejs module.

```python
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

```
Module
------
top level the module, this builds the output and returns the javascript string translation

```python

	def _check_for_unicode_decorator(self, node):
		if isinstance(node, ast.FunctionDef):
			for decor in node.decorator_list:
				if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'unicode':
					assert len(decor.args)==1
					self._unicode_name_map[ node.name ] = decor.args[0].s


	def visit_Module(self, node):
		modules = []

		mod = self._new_module()
		modules.append( mod )
		lines = mod['lines']
		header = mod['header']

		## first check for all the @unicode decorators,
		## also check for special imports like `from runtime import *`
		for b in node.body:
			self._check_for_unicode_decorator(b)

			if isinstance(b, ast.ImportFrom):
				line = self.visit(b)
				if line:
					raise RuntimeError('import-from specials do not return a string!')


		if self._insert_runtime:
			## always regenerate the runtime, in case the user wants to hack it ##
			runtime = generate_js_runtime(
				nodejs         = self._insert_nodejs_runtime,
				nodejs_tornado = self._insert_nodejs_tornado
			)
			lines.insert( 0, runtime )



		for b in node.body:
			if isinstance(b, ast.Expr) and isinstance(b.value, ast.Call) and isinstance(b.value.func, ast.Name) and b.value.func.id == '__new_module__':
				mod = self._new_module( '%s.js' %b.value.args[0].id )
				modules.append( mod )
				lines = mod['lines']
				header = mod['header']

			else:
				line = self.visit(b)
				if line: lines.append( line )

		if self._has_channels and not self._webworker:
			#lines.insert( 0, 'var __workerpool__ = new __WorkerPool__(__workersrc__, __workerimports__);')
			# moved to intermediateform.md
			pass


		if self._requirejs and not self._webworker:
			for name in self._exports:
				if name.startswith('__'): continue
				lines.append( '__module__.%s = %s' %(name,name))

			lines.append( 'return __module__')
			lines.append('}) //end requirejs define')


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

```
In
----
note a `in` test in javascript is very different from the way python normally works,
for example `0 in [1,2,3]` is true in javascript, while it is false in python,
this is because an `in` test on an array in javascript checks the indices, not the values,
while in python it works by testing if the value is in the array.
Depending on the options given in the first stage of translation [intermediateform.md](intermediateform.md),
`in` tests will be replaced with a function call to `__contains__` which implements the python style logic.
However, in some cases an `in` test is still generated at here in the final stage of translation.

```python

	def visit_In(self, node):
		return ' in '

```
Try/Except and Raise
--------------
TODO `finnally` for the javascript backend 

```python

	def visit_TryExcept(self, node):
		self._in_try = True
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
		self._in_try = False
		return '\n'.join( out )

	def visit_Raise(self, node):
		if self._rust:
			return 'panic!("%s");'  % self.visit(node.type)
		elif self._cpp:
			T = self.visit(node.type)
			if T == 'RuntimeError()': T = 'std::exception'
			return 'throw %s;' % T
		else:
			## TODO - when re-raising an error, it fails because it is an Error object
			## TODO - inject some code here to check the type at runtime.
			return 'throw new %s;' % self.visit(node.type)

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

```
Yield
------
note yield is new in javascript, and works slightly different from python, ie.
yielding is not cooperative, calling `some_function_that_also_yields()` inside
a function that is already using yield will not co-op yield.


```python

	def visit_Yield(self, node):
		return 'yield %s' % self.visit(node.value)

	def visit_Lambda(self, node):
		args = [self.visit(a) for a in node.args.args]
		if args and args[0]=='__INLINE_FUNCTION__':
			self._inline_lambda = True
			#return '<LambdaError>'   ## skip node, the next function contains the real def
			raise SwapLambda( node )
		else:
			return '(function (%s) {return %s;})' %(','.join(args), self.visit(node.body))


```

Function/Methods
----------------
note: `visit_Function` after doing some setup, calls `_visit_function` that subclasses overload.


```python

	def _visit_function(self, node):
		if node.name == '__DOLLAR__':
			node.name = '$'
		comments = []
		body = []
		is_main = node.name == 'main'
		is_annon = node.name == ''
		is_pyfunc    = False
		is_prototype = False
		is_debugger  = False
		is_redef     = False
		is_staticmeth= False
		is_getter    = False
		is_setter    = False
		is_unicode   = False
		bind_to      = None
		protoname    = None
		func_expr    = False  ## function expressions `var a = function()` are not hoisted
		func_expr_var = True  ## this should always be true, was this false before for hacking nodejs namespace?
		returns = None

		## decorator specials ##
		## note: only args_typedefs is used for now in the js backend ##
		options = {'getter':False, 'setter':False, 'returns':None, 'returns_self':False, 'generic_base_class':None, 'classmethod':False}
		args_typedefs = {}
		chan_args_typedefs = {}
		generics = set()
		args_generics = dict()
		func_pointers = set()
		arrays = dict()
		########################
		decorators = []
		for decor in node.decorator_list:

			##note: `_visit_decorator` is defined in generatorbase.md
			self._visit_decorator(
				decor,
				node=node,
				options=options,
				args_typedefs=args_typedefs,
				chan_args_typedefs=chan_args_typedefs,
				generics=generics,
				args_generics=args_generics,
				func_pointers=func_pointers,
				arrays = arrays,
			)

			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'expression':
				assert len(decor.args)==1
				func_expr = True
				func_expr_var = isinstance(decor.args[0], ast.Name)
				node.name = self.visit(decor.args[0])


			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'unicode':
				assert len(decor.args)==1
				is_unicode = True
				node.name = decor.args[0].s

			elif isinstance(decor, ast.Name) and decor.id == 'getter':
				is_getter = True

			elif isinstance(decor, ast.Name) and decor.id == 'setter':
				is_setter = True

			elif isinstance(decor, ast.Name) and decor.id == 'staticmethod':
				is_staticmeth = True

			elif isinstance(decor, ast.Name) and decor.id == 'debugger':
				is_debugger = True
			elif isinstance(decor, ast.Name) and decor.id == 'redef':
				is_redef = True

			elif isinstance(decor, ast.Name) and decor.id == '__pyfunction__':
				is_pyfunc = True

			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef__':
				pass

			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__prototype__':
				assert len(decor.args)==1
				is_prototype = True
				protoname = decor.args[0].id
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'returns':
				returns = decor.args[0].id
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'bind':
				assert len(decor.args)==1
				bind_to = self.visit(decor.args[0])

			else:
				decorators.append( self.visit(decor)+'(' )

		dechead = ''.join(decorators)
		dectail = ')' * len(decorators)
		args = self.visit(node.args)
		funcname = node.name


		#if len(self._function_stack) == 1:
		#	self._iter_id = 0

		if is_prototype:
			funcname = '%s_%s' %(protoname, node.name)
			if is_debugger:
				raise SyntaxError('@debugger is not allowed on methods: %s.%s' %(protoname, node.name))
			if bind_to:
				raise SyntaxError('@bind is not allowed on methods: %s.%s' %(protoname, node.name))

			if is_getter:
				assert len(args)==0
				funcname = '__getter__' + funcname
				fdef = '%s function %s(%s)' % (dechead, funcname, ', '.join(args))
			elif is_setter:
				funcname = '__setter__' + funcname
				fdef = '%s function %s(%s)' % (dechead, funcname, ', '.join(args))

			elif is_staticmeth:
				fdef = '%s.%s = %s function %s(%s)' % (protoname, node.name, dechead, funcname, ', '.join(args))
			else:
				fdef = '%s.prototype.%s = %s function %s(%s)' % (protoname, node.name, dechead, funcname, ', '.join(args))

		elif len(self._function_stack) == 1:
			## note: var should always be used with function expressions.

			if self._func_expressions or func_expr:
				if is_debugger:
					## first open devtools then wait two seconds and then run function  ##
					d = [
						'var %s = function debugger_entrypoint_%s() {' %(node.name, node.name),
						'	/***/ var __entryargs__ = arguments;',
						'	/***/ try {var __win = require("nw.gui").Window.get(); __win.showDevTools(); __win.focus(); __win.moveTo(10,0);} catch (__err) {};',
						'	setTimeout(function(){%s_wrapped(__entryargs__)}, 2000);' %node.name,
						'	function %s_wrapped(%s)' % (node.name, ', '.join(args)),  ## scope lifted ok here
					]
					fdef = '\n'.join(d)
					self.push()
				elif bind_to:
					fdef = '%s = %s function %s(%s)' % (bind_to,dechead, node.name,  ', '.join(args))
				else:
					fdef = 'var %s = %s function %s(%s)' % (node.name,dechead, node.name,  ', '.join(args))

			else:  ## scope lifted functions are not safe ##
				fdef = 'function %s(%s)' % (node.name, ', '.join(args))


			if self._requirejs and node.name not in self._exports:
				self._exports.add( node.name )

		else:
			if is_debugger:
				raise SyntaxError('the decorator `@debugger` is only used on top level functions in the global namespace')

			if self._func_expressions or func_expr:
				if bind_to:
					fdef = '%s = %s function %s(%s)' % (bind_to,dechead, node.name,  ', '.join(args))
				else:
					fdef = 'var %s = %s function %s(%s)' % (node.name,dechead, node.name,  ', '.join(args))

			else: ## scope lifted functions are not safe ##
				fdef = 'function %s(%s)' % (node.name, ', '.join(args))

		body.append( fdef )

		body.append( self.indent() + '{' )
		self.push()

		if self._runtime_type_checking or is_redef:
			## doing the recompile and eval inside the function itself allows it to pick
			## up any variables from the outer scope if it is a nested function.
			## note: the user calls `myfunc.redefine(src)` and then on next call it is recompiled.
			body.append(
				'/***/ if (%s.__recompile !== undefined) { eval("%s.__redef="+%s.__recompile); %s.__recompile=undefined; };' %(funcname, funcname, funcname, funcname)
			)
			body.append(
				'/***/ if (%s.__redef !== undefined) { return %s.__redef.apply(this,arguments); };' %(funcname, funcname)
			)

		next = None
		for i,child in enumerate(node.body):
			if isinstance(child, Str) or hasattr(child, 'SKIP'):  ## TODO check where the SKIP hack is coming from
				continue
			elif isinstance(child, ast.Expr) and isinstance(child.value, ast.Str):
				comments.append('/* %s */' %child.value.s.strip() )
				continue


			v = self.try_and_catch_swap_lambda(child, node.body)

			if v is None:
				msg = 'error in function: %s'%node.name
				msg += '\n%s' %child
				raise SyntaxError(msg)
			else:
				body.append( self.indent()+v)

		## todo fix when sleep comes before channel async _func_recv, should be a stack of ['}', '});']
		if self._sleeps:
			body.append( '}/*end-sleep*/' * self._sleeps)
			self._sleeps = 0

		if self._func_recv:
			while self._func_recv:  ## closes nested generated callbacks
				self.pull()
				body.append( self.indent() + '});/*end-async*/' )
				self._func_recv -= 1

		## end of function ##
		self.pull()
		body.append( self.indent() + '}/*end-function*/' )
		if is_debugger:
			self.pull()
			body.append( '}/*debugger*/' )

		if dectail:
			body.append(dectail + ';/*end-decorators*/')

		if is_getter:
			#gtemplate = 'Object.defineProperty(%s.prototype, "%s", {get:%s, enumerable:false, writable:false, configurable:false});'
			gtemplate = 'Object.defineProperty(%s.prototype, "%s", {get:%s, configurable:true});'
			body.append( gtemplate%(protoname,node.name, funcname))
		elif is_setter:
			## assume that there is a getter
			getterfunc = funcname.replace('__setter__', '__getter__')
			#stemplate = 'Object.defineProperty(%s.prototype, "%s", {get:%s, set:%s, enumerable:false, writable:false, configurable:true});'
			stemplate = 'Object.defineProperty(%s.prototype, "%s", {get:%s, set:%s, configurable:true});'
			body.append( stemplate%(protoname,node.name, getterfunc, funcname))

		## below is used for runtime type checking ##
		if returns:
			if is_prototype:
				body.append(
					'%s.prototype.%s.returns = "%s";' % (protoname, node.name, returns)
				)
			else:
				body.append( node.name + '.returns = "%s";' %returns )

		_func_typed_args = []
		for arg in node.args.args:
			if arg.id in args_typedefs:
				argtype = args_typedefs[arg.id]
				if argtype.startswith('__arg_map__'):
					argtype = argtype.split('"')[1]
				_func_typed_args.append( argtype )

		if _func_typed_args:
			targs = ','.join( ['"%s"'%t for t in _func_typed_args] )
			if is_prototype:
				body.append(
					'%s.prototype.%s.args = [%s];' % (protoname, node.name, targs)
				)
			else:
				body.append( node.name + '.args = [%s];' %targs )



		buffer = '\n'.join( comments + body )
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
		raise SyntaxError('ellipsis slice is deprecated in the javascript backend')
		return '%s["$wrapped"]' %name


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
		elif node.id == '__DOLLAR__':
			return '$'
		elif node.id == 'debugger':  ## keyword in javascript
			return '𝗗𝗲𝗯𝘂𝗴𝗴𝗲𝗿'
		elif node.id in self._unicode_name_map:
			return self._unicode_name_map[node.id]
		else:
			return node.id

	def visit_Attribute(self, node):
		name = self.visit(node.value)
		attr = node.attr
		return '%s.%s' % (name, attr)

	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		#s = 'console.log(%s);' % ', '.join(args)
		s = '𝑷𝒓𝒊𝒏𝒕(%s);' % ', '.join(args)
		return s

	def visit_keyword(self, node):
		if isinstance(node.arg, basestring):
			return node.arg, self.visit(node.value)
		return self.visit(node.arg), self.visit(node.value)

```

Call Helper
------------


```python

	def _visit_call_helper(self, node):
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''

		fname = self.visit(node.func)
		if fname=='__DOLLAR__': fname = '$'

		if fname in self.macros:
			macro = self.macros[fname]
			args = ','.join([self.visit(arg) for arg in node.args])
			if '"%s"' in macro:
				return macro % tuple([s.s for s in node.args])
			elif '%s' in macro:
				if macro.count('%s')==1:
					return macro % args
				else:
					return macro % tuple([self.visit(s) for s in node.args])
			else:
				return '%s(%s)' %(macro,args)
		elif fname == 'sleep':
			self._sleeps += 1
			return 'setTimeout(__sleep__%s.bind(this), %s*1000); function __sleep__%s(){' % (self._sleeps, args[0], self._sleeps)
		else:
			return '%s(%s)' % (fname, args)

	def inline_helper_remap_names(self, remap):
		return "var %s;" %','.join(remap.values())

	def inline_helper_return_id(self, return_id):
		return "var __returns__%s = null;"%return_id

	def _visit_call_helper_numpy_array(self, node):
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
		if 'this' in args:
			args.remove('this')
		out = []
		if args:
			out.append( 'var ' + ','.join(args) )
		if node.keywords:
			out.append( 'var ' + ','.join([key.arg for key in node.keywords]) )
			for key in node.keywords:
				## inside a webworker this is a type cast
				if self._webworker:
					out.append('%s.__proto__ = %s.prototype' %(key.arg, self.visit(key.value)))

				## outside of a webworker this is a type assertion
				elif self._runtime_type_checking:
					funcname = self._function_stack[-1].name

					if isinstance(key.value, ast.Call):
						if key.value.func.id == '__arg_array__':
							s = key.value.args[0].s
							dims = '[0]' * s.count('[')
							t = s.split(']')[-1]
							out.append('/***/ if (!(isinstance(%s,Array))) {throw new TypeError("invalid type - not an array")}' %key.arg)
							out.append('/***/ if (%s.length > 0 && !( isinstance(%s%s, %s) )) {throw new TypeError("invalid array type")}' %(key.arg, key.arg, dims, t))
						else:  ## typed hash map
							keytype   = key.value.args[0].s.split(']')[0].split('[')[1].strip()
							valuetype = key.value.args[0].s.split(']')[1].strip()
							out.append('/***/ if (%s.__keytype__ != "%s") {throw new TypeError("invalid dict key type")}' %(key.arg, keytype))
							out.append('/***/ if (%s.__valuetype__ != "%s") {throw new TypeError("invalid dict value type")}' %(key.arg, valuetype))

					elif isinstance(key.value, ast.Str) and key.value.s.startswith('func('):

						out.append('/***/ if (!(%s instanceof Function)) {throw new TypeError("`%s` is not a callback function: instead got type->"+typeof(%s))}' %(key.arg, key.arg, key.arg))
						targs = []
						head,tail = key.value.s.split(')(')
						head = head.split('func(')[-1]
						for j, targ in enumerate(head.split('|')):  ## NOTE TODO replace `|` with space
							out.append(
								'/***/ if (!(%s.args[%s]=="%s")) {throw new TypeError("callback `%s` requires argument `%s` as type `%s`")}' %(key.arg, j, targ,   key.value.s.replace('|',' '), j, targ)
							)

						returns = tail.replace(')','')
						if returns:
							out.append(
								'/***/ if (!(%s.returns=="%s")) {throw new TypeError("callback `%s` requires a return type of `%s`, instead got->" + typeof(%s.returns))}' %(key.arg, returns, key.arg, returns, key.arg)
							)

					else:
						val = self.visit(key.value)
						out.append('/***/ if ( !(isinstance(%s, %s))) {throw new TypeError("in function `%s`, argument `%s` must of type `%s`, instead got->"+typeof(%s))}' %(key.arg, val, funcname, key.arg,val, key.arg))

		return ';\n'.join(out)

```

Inline Code Helper
------------------

TODO clean this up

```python

	def _inline_code_helper(self, s):
		## TODO, should newline be changed here?
		s = s.replace('\n', '\\n').replace('\0', '\\0')  ## AttributeError: 'BinOp' object has no attribute 's' - this is caused by bad quotes
		if s.strip().startswith('#'): s = '/*%s*/'%s

		if '"' in s or "'" in s:  ## can not trust direct-replace hacks
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
		if hasattr(self, '_in_timeout') and self._in_timeout:
			body.append(
				self.indent() +  'if ( (new Date()).getTime() - __clk__ >= %s )  { break;}' % self._timeout
			)

		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		return '"%s"' % s

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)
		go_hacks = ('__go__array__', '__go__arrayfixed__', '__go__map__', '__go__func__', '__go__receive__', '__go__send__')

		if op == '>>' and left == '__new__':
			## this can happen because python_to_pythonjs.py will catch when a new class instance is created
			## (when it knows that class name) and replace it with `new(MyClass())`; but this can cause a problem
			## if later the user changes that part of their code into a module, and loads it as a javascript module,
			## they may update their code to call `new MyClass`, and then later go back to the python library.
			## the following hack prevents `new new`
			if isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name) and node.right.func.id=='new':
				right = self.visit(node.right.args[0])
			return ' new %s' %right


		elif op == '<<':

			if left == '__go__receive__':
				self._has_channels = True
				r = []
				if isinstance(node.right, ast.Name):
					r.append('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.recv( %s,'%right)
				elif isinstance(node.right, ast.Attribute):
					wid = node.right.value.id
					attr = node.right.attr
					r.append('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.get( %s, "%s", '%(wid, attr))
				elif isinstance(node.right, ast.Call):
					if isinstance(node.right.func, ast.Name):
						fname = node.right.func.id
						args  = [self.visit(a) for a in node.right.args]
						r.append('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.call( "%s", [%s], ' % (fname, ','.join(args)))

					else:
						wid = node.right.func.value.id
						attr = node.right.func.attr
						args  = [self.visit(a) for a in node.right.args]
						r.append('𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.callmeth( %s, "%s", [%s], '%(wid, attr, ','.join(args)))
				else:
					raise RuntimeError(node.right)

				r.append(' function (%s) {')  ## gets filled in later
				return ''.join(r)

			elif left == '__go__send__':
				self._has_channels = True
				r = [
					'𝑾𝒐𝒓𝒌𝒆𝒓𝑷𝒐𝒐𝒍.send({message:%s,'%right,
					'id:%s})'
				]
				return ''.join(r)

			elif isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id in go_hacks:
				if node.left.func.id == '__go__func__':
					raise SyntaxError('TODO - go.func')

				elif node.left.func.id == '__go__map__':  ## typed hash maps for javascript
					key_type = node.left.args[0].id
					value_type = node.left.args[1].id
					## right will take the form: `𝑫𝒊𝒄𝒕({  }, { copy:false })`
					## here was simply clip off the end and inject the type options
					clipped = right[:-2]
					if 'keytype:' not in clipped:
						clipped += ',keytype:"%s"'  % key_type 
					clipped += ',valuetype:"%s" })' % value_type
					return clipped
				else:
					if isinstance(node.right, ast.Name):
						raise SyntaxError(node.right.id)

					right = []
					for elt in node.right.elts:
						if isinstance(elt, ast.Num):
							right.append( str(elt.n)+'i' )
						else:
							right.append( self.visit(elt) )
					right = '(%s)' %','.join(right)

					if node.left.func.id == '__go__array__':
						T = self.visit(node.left.args[0])
						if T in go_types:
							#return '&mut vec!%s' %right
							return 'Rc::new(RefCell::new(vec!%s))' %right
						else:
							self._catch_assignment = {'class':T}  ## visit_Assign catches this
							return '&[]*%s%s' %(T, right)

					elif node.left.func.id == '__go__arrayfixed__':
						asize = self.visit(node.left.args[0])
						atype = self.visit(node.left.args[1])
						return ' new Array(%s) /*array of: %s*/' %(asize, atype)

		if self._with_oo:
			methodnames = {
				'+': 'add',
				'-': 'sub',
				'*': 'mul',
				'/': 'div',
				'%': 'mod'
			}
			return '(%s.__%s__(%s))' % (left, methodnames[op], right)
		else:
			return '(%s %s %s)' % (left, op, right)


	def visit_Return(self, node):
		if isinstance(node.value, Tuple):
			return 'return [%s];' % ', '.join(map(self.visit, node.value.elts))
		if node.value:
			return 'return %s;' % self.visit(node.value)
		return 'return undefined;'

	def visit_Pass(self, node):
		return '/*pass*/'

	def visit_Is(self, node):
		return '==='

	def visit_IsNot(self, node):
		return '!=='


	def visit_Compare(self, node):
		#if isinstance(node.ops[0], ast.Eq):
		#	left = self.visit(node.left)
		#	right = self.visit(node.comparators[0])
		#	if self._lua:
		#		return '%s == %s' %(left, right)
		#	elif self._fast_js:
		#		return '(%s===%s)' %(left, right)
		#	else:
		#		return '(%s instanceof Array ? JSON.stringify(%s)==JSON.stringify(%s) : %s===%s)' %(left, left, right, left, right)
		#elif isinstance(node.ops[0], ast.NotEq):
		#	left = self.visit(node.left)
		#	right = self.visit(node.comparators[0])
		#	if self._lua:
		#		return '%s ~= %s' %(left, right)
		#	elif self._fast_js:
		#		return '(%s!==%s)' %(left, right)
		#	else:
		#		return '(!(%s instanceof Array ? JSON.stringify(%s)==JSON.stringify(%s) : %s===%s))' %(left, left, right, left, right)
		#		
		#else:
		comp = []
		if isinstance( node.left, ast.BinOp ):
			comp.append( '('+self.visit(node.left)+')' )
		else:
			comp.append( self.visit(node.left) )

		for i in range( len(node.ops) ):
			op = None
			if isinstance(node.ops[i], ast.Eq):
				op = '==='
			elif isinstance(node.ops[i], ast.NotEq):
				op = '!=='
			else:
				op = self.visit(node.ops[i])

			comp.append( op )
			right = node.comparators[i]

			if op in ('===', '!==') and isinstance(right, ast.Name) and right.id=='undefined':
				## this fixes `if x is not undefined:`
				## the users expects above to work because this works: `if x.y is not undefined:`
				comp[0] = 'typeof(%s)' %comp[0]
				comp.append('"undefined"')

			elif isinstance(node.comparators[i], ast.BinOp):
				comp.append('(')
				comp.append( self.visit(node.comparators[i]) )
				comp.append(')')
			else:
				comp.append( self.visit(node.comparators[i]) )

		return ' '.join( comp )


	def visit_UnaryOp(self, node):
		#return self.visit(node.op) + self.visit(node.operand)
		return '%s (%s)' %(self.visit(node.op),self.visit(node.operand))


	def visit_BoolOp(self, node):
		op = self.visit(node.op)
		return '('+ op.join( [self.visit(v) for v in node.values] ) +')'

```
If Test
-------


```python

	def visit_If(self, node):
		out = []
		test = self.visit(node.test)
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

```
For Loop
--------
when fast_loops is off much of python `for in something` style of looping is lost.


```python

	def _visit_for_prep_iter_helper(self, node, out, iter_name):
		if not self._fast_loops:
			s = 'if (! (%s instanceof Array || typeof %s == "string" || 𝑰𝒔𝑻𝒚𝒑𝒆𝒅𝑨𝒓𝒓𝒂𝒚(%s) || 𝑰𝒔𝑨𝒓𝒓𝒂𝒚(%s) )) { %s = __object_keys__(%s) }' %(iter_name, iter_name, iter_name, iter_name, iter_name, iter_name)
			if len(out):
				out.append( self.indent() + s )
			else:
				out.append( s )

	def remap_to_subscript(self, number):  ## NOT USED FOR NOW
		## converts a regular number into a subscript number
		## too bad these subscripts are not in the valid unicode range.
		s = str(number)
		assert '.' not in s
		remap = {
			'0' : '₀',
			'1' : '₁',
			'2' : '₂',
			'3' : '₃',
			'4' : '₄',
			'5' : '₅',
			'6' : '₆',
			'7' : '₇',
			'8' : '₈',
			'9' : '₉',
		}

		r = ''
		for char in s:
			r += remap[ char ]
		return r


	def visit_For(self, node):

		target = node.target.id
		iter = self.visit(node.iter) # iter is the python iterator

		out = []
		body = []

		#index = '_i%s' % self._iter_id
		#index = '𝘪𝘯𝘥𝘦𝘹%s' %self._iter_id
		if self._iter_id == 0:
			index = '𝓷'
		else:
			#index = '𝓷%s' % self.remap_to_subscript(self._iter_id)
			index = '𝓷%s' % self._iter_id


		##if not self._fast_loops and not isinstance(node.iter, ast.Name):
		## note: above will fail with `for key in somedict:`, it can not
		## be simply assumed that if its a name, to use that name as the
		## iterator, because _visit_for_prep_iter_helper might break it,
		## by reassigning the original dict, to its keys (an array),
		## later code in the block will then fail when it expects a dict.
		if not self._fast_loops:
			if isinstance(node.iter, ast.Name):
				iname = '𝕚𝕥𝕖𝕣%s' %iter
			elif self._iter_id:
				iname = '𝕚𝕥𝕖𝕣%s' %self._iter_id
			else:
				iname = '𝕚𝕥𝕖𝕣'

			out.append( 'var %s = %s;' % (iname, iter) )
		else:
			iname = iter

		self._iter_id += 1

		## note this type of looping can break with _fast_loops on a dict,
		## because it reassigns the dict when looping over it
		## like this `for key in somedict:`, the only safe way
		## to loop with _fast_loops is `for key in somedict.keys():`
		if iter.startswith('𝑲𝒆𝒚𝒔'):
			## in theory we can optimize away using _visit_for_prep_iter_helper,
			## because we know almost for sure that the result of 𝑲𝒆𝒚𝒔
			## is going to be an array of keys; however, it could still be
			## a user defined class that is returning an object of something
			## other than an array.
			## the only safe way to omit _visit_for_prep_iter_helper is to check
			## if the user had statically typed the iterator variable as a dict.
			pass
		self._visit_for_prep_iter_helper(node, out, iname)

		if self._fast_loops:
			out.append( 'for (var %s = 0; %s < %s.length; %s++)' % (index, index, iname, index) )
			out.append( self.indent() + '{' )

		else:
			out.append( self.indent() + 'for (var %s = 0; %s < %s.length; %s++) {' % (index, index, iname, index) )
		self.push()

		if hasattr(self, '_in_timeout') and self._in_timeout:
			body.append(
				self.indent() + 'if ( (new Date()).getTime() - __clk__ >= %s )  { break; }' % self._timeout
			)


		body.append( self.indent() + 'var %s = %s[ %s ];' %(target, iname, index) )


		for line in list(map(self.visit, node.body)):
			body.append( self.indent() + line )

		self.pull()
		out.extend( body )
		out.append( self.indent() + '}' )

		self._iter_id -= 1

		return '\n'.join( out )

	def visit_Continue(self, node):
		return 'continue'

	def visit_Break(self, node):
		return 'break;'

```

Regenerate JS Runtime
---------------------

TODO: update and test generate new js runtimes

```python
def generate_minimal_js_runtime():
	from python_to_pythonjs import main as py2pyjs
	a = py2pyjs(
		open('src/runtime/builtins_core.py', 'rb').read(),
		module_path = 'runtime',
		fast_javascript = True
	)
	return main( a, requirejs=False, insert_runtime=False, function_expressions=True, fast_javascript=True )

def generate_js_runtime( nodejs=False, nodejs_tornado=False ):
	## note: RUSTHON_LIB_ROOT gets defined in the entry of rusthon.py
	r = [
		open(os.path.join(RUSTHON_LIB_ROOT,'src/runtime/pythonpythonjs.py'), 'rb').read(),
		python_to_pythonjs(
			open(os.path.join(RUSTHON_LIB_ROOT,'src/runtime/builtins_core.py'), 'rb').read(),
			fast_javascript = True,
			pure_javascript = False
		)

	]
	if nodejs:
		r.append(
			python_to_pythonjs(
				open(os.path.join(RUSTHON_LIB_ROOT,'src/runtime/builtins_nodejs.py'), 'rb').read(),
				fast_javascript = True,
				pure_javascript = False
			)
		)

	if nodejs_tornado:
		r.append(
			python_to_pythonjs(
				open(os.path.join(RUSTHON_LIB_ROOT,'src/runtime/nodejs_tornado.py'), 'rb').read(),
				fast_javascript = True,
				pure_javascript = False
			)
		)


	builtins = translate_to_javascript(
		'\n'.join(r),
		requirejs = False,
		insert_runtime = False,
		fast_javascript = True,
		fast_loops = True,
		runtime_checks = False
	)

	return builtins

```

Translate to Javascript
-----------------------
html files can also be translated, it is parsed and checked for `<script type="text/python">`

```python

def translate_to_javascript(source, requirejs=True, insert_runtime=True, webworker=False, function_expressions=True, fast_javascript=False, fast_loops=False, runtime_checks=True):
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
		fast_loops      = fast_loops,
		runtime_checks  = runtime_checks
	)
	output = gen.visit(tree)

	if head and not isinstance(output, dict):
		head.append( output )
		head.extend( tail )
		output = '\n'.join( head )

	return output


```
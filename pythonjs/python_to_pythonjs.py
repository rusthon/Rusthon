#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Python to PythonJS Translator
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

import os, sys, pickle, copy
from tempfile import gettempdir
from types import GeneratorType

import ast
from ast import Str
from ast import Call
from ast import Name
from ast import Tuple
from ast import Assign
from ast import keyword
from ast import Subscript
from ast import Attribute
from ast import FunctionDef
from ast import BinOp
from ast import Pass
from ast import Global
from ast import With

from ast import parse
from ast import NodeVisitor

if sys.version_info.major == 3:
	import io
	StringIO = io.StringIO
else:
	from cStringIO import StringIO as StringIO


import ministdlib

try:
	_log_file = open(gettempdir() + '/python_to_pythonjs.log', 'wb')
except:
	_log_file = None
def log(txt):
	if _log_file:
		_log_file.write( str(txt)+'\n' )
		_log_file.flush()


GLOBAL_VARIABLE_SCOPE = False              ## Python style
if '--global-variable-scope' in sys.argv:  ## JavaScript style
	GLOBAL_VARIABLE_SCOPE = True
	log('not using python style variable scope')


class Writer(object):

	def __init__(self):
		self.level = 0
		self.buffer = list()
		self.output = StringIO()
		self.with_javascript = False

	def is_at_global_level(self):
		return self.level == 0

	def push(self):
		self.level += 1

	def pull(self):
		self.level -= 1

	def append(self, code):
		self.buffer.append(code)

	def write(self, code):
		for content in self.buffer:
			self._write(content)
		self.buffer = list()
		self._write(code)

	def _write(self, code):
		indentation = self.level * 4 * ' '
		#if self.with_javascript and False: ## deprecated
		#	if not code.endswith(':'):  ## will this rule always catch: while, and if/else blocks?
		#		if not code.startswith('print '):
		#			if not code.startswith('var('):
		#				if not code == 'pass':
		#					if not code.startswith('JS('):
		#						if not code.startswith('@'):
		#							code = """JS('''%s''')"""%code
		s = '%s%s\n' % (indentation, code)
		#self.output.write(s.encode('utf-8'))
		self.output.write(s)

	def getvalue(self):
		s = self.output.getvalue()
		self.output = StringIO()
		return s

writer = Writer()



class Typedef(object):
	# http://docs.python.org/2/reference/datamodel.html#emulating-numeric-types
	_opmap = dict(
		__add__ = '+',
		__iadd__ = '+=',
		__sub__ = '-',
		__isub__ = '-=',
		__mul__ = '*',
		__imul__ = '*=',
		__div__ = '/',
		__idiv__ = '/=',
		__mod__ = '%',
		__imod__ = '%=',
		__lshift__ = '<<',
		__ilshift__ = '<<=',
		__rshift__ = '>>',
		__irshift__ = '>>=',
		__and__ = '&',
		__iand__ = '&=',
		__xor__ = '^',
		__ixor__ = '^=',
		__or__ = '|',
		__ior__ = '|=',
	)

	def __init__(self, **kwargs):
		for name in kwargs.keys():
			setattr( self, name, kwargs[name] )

		self.operators = dict()
		for name in self.methods:
			if name in self._opmap:
				op = self._opmap[ name ]
				self.operators[ op ] = self.get_pythonjs_function_name( name )

	def get_pythonjs_function_name(self, name):
		assert name in self.methods
		return '__%s_%s' %(self.name, name) ## class name

	def check_for_parent_with(self, method=None, property=None, operator=None, class_attribute=None):

		for parent_name in self.parents:
			if not self.compiler.is_known_class_name( parent_name ):
				continue

			typedef = self.compiler.get_typedef( class_name=parent_name )
			if method and method in typedef.methods:
				return typedef
			elif property and property in typedef.properties:
				return typedef
			elif operator and typedef.operators:
				return typedef
			elif class_attribute in typedef.class_attributes:
				return typedef
			elif typedef.parents:
				res = typedef.check_for_parent_with(
					method=method, 
					property=property, 
					operator=operator,
					class_attribute=class_attribute
				)
				if res:
					return res

class PythonToPythonJS(NodeVisitor):

	identifier = 0
	_func_typedefs = ()

	def __init__(self, source=None, module=None, module_path=None, dart=False, coffee=False, lua=False):
		super(PythonToPythonJS, self).__init__()

		self._with_ll = False   ## lowlevel
		self._with_lua = lua
		self._with_coffee = coffee
		self._with_dart = dart
		self._with_js = False

		self._source = source.splitlines()
		self._classes = dict()    ## class name : [method names]
		self._class_parents = dict()  ## class name : parents
		self._instance_attributes = dict()  ## class name : [attribute names]
		self._class_attributes = dict()
		self._catch_attributes = None
		self._names = set() ## not used?
		self._instances = dict()  ## instance name : class name
		self._decorator_properties = dict()
		self._decorator_class_props = dict()
		self._function_return_types = dict()
		self._return_type = None
		self._module = module
		self._module_path = module_path
		self._typedefs = dict()  ## class name : typedef  (not pickled)

		self._globals = dict()
		self._global_nodes = dict()
		self._with_static_type = None
		self._global_typed_lists = dict()  ## global name : set  (if len(set)==1 then we know it is a typed list)
		self._global_typed_dicts = dict()
		self._global_typed_tuples = dict()
		self._global_functions = dict()
		self._with_inline = False
		self._inline = []
		self._inline_ids = 0
		self._inline_breakout = False
		self._js_classes = dict()
		self._in_js_class = False

		self._cache_for_body_calls = False
		self._cache_while_body_calls = False
		self._comprehensions = []
		self._generator_functions = set()

		self._custom_operators = {}
		self._injector = []  ## advanced meta-programming hacks
		self._in_class = None
		self._with_fastdef = False
		self.setup_builtins()

		source = self.preprocess_custom_operators( source )
		tree = parse( source )
		self._generator_function_nodes = collect_generator_functions( tree )

		for node in tree.body:
			## skip module level doc strings ##
			if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
				pass
			else:
				self.visit(node)


	def preprocess_custom_operators(self, data):
		'''
		custom operators must be defined before they are used
		'''
		code = []
		for line in data.splitlines():
			if line.strip().startswith('@custom_operator'):
				l = line.replace('"', "'")
				a,b,c = l.split("'")
				op = b.decode('utf-8')
				self._custom_operators[ op ] = None
			else:
				for op in self._custom_operators:
					op = op.encode('utf-8')
					line = line.replace(op, '|"%s"|'%op)

			code.append( line )

		data = '\n'.join( code )
		return data

	def setup_builtins(self):
		self._classes['dict'] = set(['__getitem__', '__setitem__'])
		self._classes['list'] = set() #['__getitem__', '__setitem__'])
		self._classes['tuple'] = set() #['__getitem__', '__setitem__'])
		self._builtin_classes = set(['dict', 'list', 'tuple'])
		self._builtin_functions = {
			'ord':'%s.charCodeAt(0)', 
			'chr':'String.fromCharCode(%s)',
			'abs':'Math.abs(%s)',
			'cos':'Math.cos(%s)',
			'sin':'Math.sin(%s)',
			'sqrt':'Math.sqrt(%s)'
		}
		self._builtin_functions_dart = {
			'ord':'%s.codeUnitAt(0)', 
			'chr':'new( String.fromCharCodes([%s]) )',
		}

	def is_known_class_name(self, name):
		return name in self._classes

	def get_typedef(self, instance=None, class_name=None):
		assert instance or class_name
		if isinstance(instance, Name) and instance.id in self._instances:
			class_name = self._instances[ instance.id ]

		if class_name:
			#assert class_name in self._classes
			if class_name not in self._classes:
				log('ERROR: class name not in self._classes: %s'%class_name)
				log('self._classes: %s'%self._classes)
				raise RuntimeError('class name: %s - not found in self._classes - node:%s '%(class_name, instance))

			if class_name not in self._typedefs:
				self._typedefs[ class_name ] = Typedef(
					name = class_name,
					methods = self._classes[ class_name ],
					#properties = self._decorator_class_props[ class_name ],
					#attributes = self._instance_attributes[ class_name ],
					#class_attributes = self._class_attributes[ class_name ],
					#parents = self._class_parents[ class_name ],
					properties = self._decorator_class_props.get(  class_name, set()),
					attributes = self._instance_attributes.get(    class_name, set()),
					class_attributes = self._class_attributes.get( class_name, set()),
					parents = self._class_parents.get(             class_name, set()),

					compiler = self,
				)
			return self._typedefs[ class_name ]

	def save_module(self):
		if self._module and self._module_path:
			a = dict(
				classes = self._classes,
				instance_attributes = self._instance_attributes,
				class_attributes = self._class_attributes,
				decorator_class_props = self._decorator_class_props,
				function_return_types = self._function_return_types,
				class_parents = self._class_parents,
			)
			pickle.dump( a, open(os.path.join(self._module_path, self._module+'.module'), 'wb') )

	def _check_for_module(self, name):
		if self._module_path and name+'.module' in os.listdir(self._module_path):
			return True
		else:
			return False

	def _load_module(self, name):
		f = open( os.path.join(self._module_path, name+'.module'), 'rb' )
		a = pickle.load( f ); f.close()
		return a

	def visit_Import(self, node):
		for alias in node.names:
			writer.write( '## import: %s :: %s' %(alias.name, alias.asname) )
                        ## TODO namespaces: import x as y
			raise NotImplementedError('import, line %s' % node.lineno)

	def visit_ImportFrom(self, node):
		if self._with_dart:
			lib = ministdlib.DART
		elif self._with_lua:
			lib = ministdlib.LUA
		else:
			lib = ministdlib.JS


		if node.module in lib:
			imported = False
			for n in node.names:
				if n.name in lib[ node.module ]:
					if not imported:
						imported = True
						if ministdlib.REQUIRES in lib[node.module]:
							writer.write('import %s' %','.join(lib[node.module][ministdlib.REQUIRES]))

					writer.write( 'JS("%s")' %lib[node.module][n.name] )
					if n.name not in self._builtin_functions:
						self._builtin_functions[ n.name ] = n.name + '()'


		elif self._check_for_module( node.module ):
			if node.names[0].name == '*':
				a = self._load_module( node.module )
				self._classes.update( a['classes'] )
				self._class_attributes.update( a['class_attributes'] )
				self._instance_attributes.update( a['instance_attributes'] )
				self._decorator_class_props.update( a['decorator_class_props'] )
				self._function_return_types.update( a['function_return_types'] )
				self._class_parents.update( a['class_parents'] )
			else:
				raise SyntaxError('only "from module import *" is allowed')

			writer.write('## import from: %s :: %s' %(node.module, [ (a.name,a.asname) for a in node.names]))

		elif node.module.startswith('nodejs.'):
			## this import syntax is now used to import NodeJS bindings see: PythonJS/nodejs/bindings
			## the helper script (nodejs.py) checks for these import statements, and loads the binding,
			pass
		else:
			raise SyntaxError( 'invalid import - could not find cached module: %s' %node.module )

	def visit_Assert(self, node):
		## hijacking "assert isinstance(a,A)" as a type system ##
		if isinstance( node.test, Call ) and isinstance(node.test.func, Name) and node.test.func.id == 'isinstance':
			a,b = node.test.args
			if b.id in self._classes:
				self._instances[ a.id ] = b.id

	def visit_Dict(self, node):
		node.returns_type = 'dict'
		a = []
		for i in range( len(node.keys) ):
			k = self.visit( node.keys[ i ] )
			v = self.visit( node.values[i] )
			if self._with_js:
				a.append( '[%s,%s]'%(k,v) )
			elif self._with_dart or self._with_ll:
				a.append( '%s:%s'%(k,v) )
				#if isinstance(node.keys[i], ast.Str):
				#	a.append( '%s:%s'%(k,v) )
				#else:
				#	a.append( '"%s":%s'%(k,v) )
			else:
				a.append( 'JSObject(key=%s, value=%s)'%(k,v) )

		if self._with_js:
			b = ','.join( a )
			return '__jsdict( [%s] )' %b
		elif self._with_dart or self._with_ll:
			b = ','.join( a )
			return '{%s}' %b
		else:
			b = '[%s]' %', '.join(a)
			#return '__get__(dict, "__call__")([], JSObject(js_object=%s))' %b
			return '__get__(dict, "__call__")([%s], JSObject())' %b

	def visit_Tuple(self, node):
		node.returns_type = 'tuple'
		a = '[%s]' % ', '.join(map(self.visit, node.elts))
		if self._with_dart:
			return 'tuple(%s)' %a
		else:
			return a

	def visit_List(self, node):
		node.returns_type = 'list'
		a = '[%s]' % ', '.join(map(self.visit, node.elts))
		if self._with_ll:
			pass
		elif self._with_lua:
			a = '__get__(list, "__call__")({}, {pointer:%s, length:%s})'%(a, len(node.elts))
		return a

	def visit_GeneratorExp(self, node):
		return self.visit_ListComp(node)

	_comp_id = 0
	def visit_ListComp(self, node):
		node.returns_type = 'list'

		if len(self._comprehensions) == 0:
			comps = collect_comprehensions( node )
			for i,cnode in enumerate(comps):
				cname = '__comp__%s' % self._comp_id
				self._comp_id += 1
				cnode._comp_name = cname
				self._comprehensions.append( cnode )

		cname = node._comp_name
		if not self._with_dart:
			writer.write('var(%s)'%cname)

			length = len( node.generators )
			a = ['idx%s'%i for i in range(length)]
			writer.write('var( %s )' %','.join(a) )
			a = ['iter%s'%i for i in range(length)]
			writer.write('var( %s )' %','.join(a) )
			a = ['get%s'%i for i in range(length)]
			writer.write('var( %s )' %','.join(a) )

		writer.write('%s = JSArray()'%cname)

		generators = list( node.generators )
		generators.reverse()
		self._gen_comp( generators, node )

		self._comprehensions.remove( node )
		#return '__get__(list, "__call__")([], {pointer:%s})' %cname
		return cname


	def _gen_comp(self, generators, node):
		gen = generators.pop()
		#if len(gen.ifs): raise NotImplementedError  ## TODO
		id = len(generators) + self._comprehensions.index( node )
		assert isinstance(gen.target, Name)
		writer.write('idx%s = 0'%id)

		is_range = False
		if isinstance(gen.iter, ast.Call) and isinstance(gen.iter.func, ast.Name) and gen.iter.func.id in ('range', 'xrange'):
			is_range = True

			#writer.write('iter%s = __get__(len, "__call__")([%s], JSObject())' %(id, self.visit(gen.iter.args[0])) )
			writer.write('iter%s = %s' %(id, self.visit(gen.iter.args[0])) )
			writer.write('while idx%s < iter%s:' %(id,id) )
			writer.push()

			writer.write('var(%s)'%gen.target.id)
			writer.write('%s=idx%s' %(gen.target.id, id) )

		else:
			writer.write('iter%s = %s' %(id, self.visit(gen.iter)) )
			writer.write('get%s = __get__(iter%s, "__getitem__")'%(id,id) )


			writer.write('while idx%s < __get__(len, "__call__")([iter%s], JSObject()):' %(id,id) )  ## TODO optimize
			writer.push()

			writer.write('var(%s)'%gen.target.id)
			writer.write('%s=get%s( [idx%s], JSObject() )' %(gen.target.id, id,id) )

		if generators:
			self._gen_comp( generators, node )
		else:
			cname = node._comp_name #self._comprehensions[-1]
			if len(gen.ifs):
				test = []
				for compare in gen.ifs:
					test.append( self.visit(compare) )

				writer.write('if %s:' %' and '.join(test))

				writer.push()
				if self._with_dart:
					writer.write('%s.add( %s )' %(cname,self.visit(node.elt)) )
				elif self._with_lua:
					writer.write('table.insert(%s, %s )' %(cname,self.visit(node.elt)) )
				else:
					writer.write('%s.push( %s )' %(cname,self.visit(node.elt)) )
				writer.pull()
			else:

				if self._with_dart:
					writer.write('%s.add( %s )' %(cname,self.visit(node.elt)) )
				elif self._with_lua:
					writer.write('table.insert(%s, %s )' %(cname,self.visit(node.elt)) )
				else:
					writer.write('%s.push( %s )' %(cname,self.visit(node.elt)) )
		if self._with_lua:
			writer.write('idx%s = idx%s + 1' %(id,id) )
		else:
			writer.write('idx%s+=1' %id )
		writer.pull()

		if self._with_lua:  ## convert to list
			writer.write('%s = list.__call__({},{pointer:%s, length:idx%s})' %(cname, cname, id))



	def visit_In(self, node):
		return ' in '

	def visit_NotIn(self, node):
		#return ' not in '
		raise RuntimeError('"not in" is only allowed in if-test: see method - visit_Compare')

	def visit_AugAssign(self, node):
		target = self.visit( node.target )
		op = '%s=' %self.visit( node.op )

		typedef = self.get_typedef( node.target )

		if self._with_lua:
			if op == '+=':
				a = '__add__(%s,%s)' %(target, self.visit(node.value))
			elif op == '-=':
				a = '__sub__(%s,%s)' %(target, self.visit(node.value))
			elif op == '*=':
				a = '__mul__(%s,%s)' %(target, self.visit(node.value))
			elif op == '/=' or op == '//=':
				a = '__div__(%s,%s)' %(target, self.visit(node.value))
			elif op == '%=':
				a = '__mod__(%s,%s)' %(target, self.visit(node.value))
			elif op == '&=':
				a = '__and__(%s,%s)' %(target, self.visit(node.value))
			elif op == '|=':
				a = '__or__(%s,%s)' %(target, self.visit(node.value))
			elif op == '^=':
				a = '__xor__(%s,%s)' %(target, self.visit(node.value))
			elif op == '<<=':
				a = '__lshift__(%s,%s)' %(target, self.visit(node.value))
			elif op == '>>=':
				a = '__rshift__(%s,%s)' %(target, self.visit(node.value))
			else:
				raise NotImplementedError(op)

			writer.write('%s=%s' %(target,a))


		elif typedef and op in typedef.operators:
			func = typedef.operators[ op ]
			a = '%s( [%s, %s] )' %(func, target, self.visit(node.value))
			writer.write( a )
		elif op == '//=':
			if self._with_dart:
				a = '%s = (%s/%s).floor()' %(target, target, self.visit(node.value))
			else:
				a = '%s = Math.floor(%s/%s)' %(target, target, self.visit(node.value))
			writer.write(a)

		elif self._with_dart:
			if op == '+=':
				a = '%s.__iadd__(%s)' %(target, self.visit(node.value))
			elif op == '-=':
				a = '%s.__isub__(%s)' %(target, self.visit(node.value))
			elif op == '*=':
				a = '%s.__imul__(%s)' %(target, self.visit(node.value))
			elif op == '/=':
				a = '%s.__idiv__(%s)' %(target, self.visit(node.value))
			elif op == '%=':
				a = '%s.__imod__(%s)' %(target, self.visit(node.value))
			elif op == '&=':
				a = '%s.__iand__(%s)' %(target, self.visit(node.value))
			elif op == '|=':
				a = '%s.__ior__(%s)' %(target, self.visit(node.value))
			elif op == '^=':
				a = '%s.__ixor__(%s)' %(target, self.visit(node.value))
			elif op == '<<=':
				a = '%s.__ilshift__(%s)' %(target, self.visit(node.value))
			elif op == '>>=':
				a = '%s.__irshift__(%s)' %(target, self.visit(node.value))
			else:
				raise NotImplementedError

			b = '%s %s %s' %(target, op, self.visit(node.value))
			## dart2js is smart enough to optimize this if/else away ##
			writer.write('if instanceof(%s, Number) or instanceof(%s, String): %s' %(target,target,b) )
			writer.write('else: %s' %a)

		elif self._with_js:  ## no operator overloading in with-js mode
			a = '%s %s %s' %(target, op, self.visit(node.value))
			writer.write(a)

		elif isinstance(node.target, ast.Attribute):
			name = self.visit(node.target.value)
			attr = node.target.attr
			a = '%s.%s %s %s' %(name, attr, op, self.visit(node.value))
			writer.write(a)

		elif isinstance(node.target, ast.Subscript):
			name = self.visit(node.target.value)
			slice = self.visit(node.target.slice)
			#if self._with_js:
			#	a = '%s[ %s ] %s %s'
			#	writer.write(a %(name, slice, op, self.visit(node.value)))
			#else:
			op = self.visit(node.op)
			a = '__get__(%s, "__setitem__")( [%s, __get__(%s, "__getitem__")([%s], {}) %s (%s)], {} )'
			writer.write(a %(name, slice, name, slice, op, self.visit(node.value)))

		else:
			## TODO extra checks to make sure the operator type is valid in this context
			a = '%s %s %s' %(target, op, self.visit(node.value))
			writer.write(a)

	def visit_Yield(self, node):
		return 'yield %s' % self.visit(node.value)

	def _get_js_class_base_init(self, node ):
		for base in node.bases:
			if base.id == 'object':
				continue
			n = self._js_classes[ base.id ]
			if hasattr(n, '_cached_init'):
				return n._cached_init
			else:
				return self._get_js_class_base_init( n )  ## TODO fixme

	def _visit_dart_classdef(self, node):
		name = node.name
		log('Dart-ClassDef: %s'%name)
		self._js_classes[ name ] = node

		methods = {}
		method_list = []  ## getter/setters can have the same name
		props = set()
		for item in node.body:
			if isinstance(item, FunctionDef):
				methods[ item.name ] = item
				finfo = inspect_method( item )
				props.update( finfo['properties'] )

				if item.name != '__init__':
					method_list.append( item )

				#if item.name == '__init__': continue
				continue

				item.args.args = item.args.args[1:]  ## remove self
				for n in finfo['name_nodes']:
					if n.id == 'self':
						n.id = 'this'

		if props:
			writer.write('@properties(%s)'%','.join(props))
			for dec in node.decorator_list:
				writer.write('@%s'%self.visit(dec))

		bases = []
		for base in node.bases:
			bases.append( self.visit(base) )
		if bases:
			writer.write('class %s( %s ):'%(node.name, ','.join(bases)))

		else:
			writer.write('class %s:' %node.name)

		init = methods.get( '__init__', None)

		writer.push()
		## declare vars here
		#for attr in props:
		#	writer.write('JS("var %s")'%attr)
		## constructor
		if init:
			methods.pop( '__init__' )
			init.name = node.name
			self.visit(init)
		## methods
		for method in method_list:
			self.visit(method)

		if not init and not method_list:
			writer.write( 'pass' )

		writer.pull()

	def _visit_js_classdef(self, node):
		name = node.name
		log('JavaScript-ClassDef: %s'%name)
		self._js_classes[ name ] = node
		self._in_js_class = True

		methods = {}
		for item in node.body:
			if isinstance(item, FunctionDef):
				methods[ item.name ] = item
				item.args.args = item.args.args[1:]  ## remove self
				finfo = inspect_function( item )
				for n in finfo['name_nodes']:
					if n.id == 'self':
						n.id = 'this'

		#init = methods.pop('__init__')
		init = methods.get( '__init__', None)
		if init:
			args = [self.visit(arg) for arg in init.args.args]
			node._cached_init = init

		else:
			args = []
			init = self._get_js_class_base_init( node )
			if init:
				args = [self.visit(arg) for arg in init.args.args]
				node._cached_init = init

		writer.write('def %s(%s):' %(name,','.join(args)))
		writer.push()
		if init:
			#for b in init.body:
			#	line = self.visit(b)
			#	if line: writer.write( line )

			if hasattr(init, '_code'):  ## cached ##
				code = init._code
			elif args:
				code = '%s.__init__(this, %s)'%(name, ','.join(args))
				init._code = code
			else:
				code = '%s.__init__(this)'%name
				init._code = code

			writer.write(code)

		else:
			writer.write('pass')

		## `self.__class__` pointer ##
		writer.write('this.__class__ = %s' %name)

		## instance UID ##
		writer.write('this.__uid__ = "￼" + _PythonJS_UID')
		writer.write('_PythonJS_UID += 1')

		writer.pull()
		## class UID ##
		writer.write('%s.__uid__ = "￼" + _PythonJS_UID' %name)
		writer.write('_PythonJS_UID += 1')

		keys = methods.keys()
		keys.sort()
		for mname in keys:
			method = methods[mname]
			writer.write('@%s.prototype'%name)
			line = self.visit(method)
			if line: writer.write( line )
			#writer.write('%s.prototype.%s = %s'%(name,mname,mname))
			f = 'function () { return %s.prototype.%s.apply(arguments[0], Array.prototype.slice.call(arguments,1)) }' %(name, mname)
			writer.write('%s.%s = JS("%s")'%(name,mname,f))

		for base in node.bases:
			base = self.visit(base)
			if base == 'object': continue
			a = [
				'for (var n in %s.prototype) {'%base,
				'  if (!(n in %s.prototype)) {'%name,
				'    %s.prototype[n] = %s.prototype[n]'%(name,base),
				'  }',
				'}'
			]
			a = ''.join(a)
			writer.write( "JS('%s')" %a )

		self._in_js_class = False

	def visit_ClassDef(self, node):
		if self._with_dart:
			self._visit_dart_classdef(node)
			return
		elif self._with_js:
			self._visit_js_classdef(node)
			return

		name = node.name
		log('ClassDef: %s'%name)
		self._in_class = name
		self._classes[ name ] = list()  ## method names
		self._class_parents[ name ] = set()
		self._class_attributes[ name ] = set()
		self._catch_attributes = None
		self._decorator_properties = dict() ## property names :  {'get':func, 'set':func}
		self._decorator_class_props[ name ] = self._decorator_properties
		self._instances[ 'self' ] = name

		class_decorators = []
		self._injector = []
		for decorator in node.decorator_list:  ## class decorators
			if isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id == 'pythonjs':
				if decorator.attr == 'property_callbacks':
					self._injector.append('set')
				elif decorator.attr == 'init_callbacks':
					self._injector.append('init')
				else:
					raise SyntaxError( 'unsupported pythonjs class decorator' )

			else:
				#raise SyntaxError( 'unsupported class decorator' )
				class_decorators.append( decorator )

		## always catch attributes ##
		self._catch_attributes = set()
		self._instance_attributes[ name ] = self._catch_attributes

		if not self._with_coffee:
			writer.write('var(%s, __%s_attrs, __%s_parents)' % (name, name, name))
		writer.write('__%s_attrs = JSObject()' % name)
		writer.write('__%s_parents = JSArray()' % name)
		writer.write('__%s_properties = JSObject()' % name)

		for base in node.bases:
			base = self.visit(base)
			if base == 'object': continue
			self._class_parents[ name ].add( base )
			if self._with_lua:
				writer.write('table.insert( __%s_parents, %s)' % (name, base))
			else:
				writer.write('__%s_parents.push(%s)' % (name, base))

		for item in node.body:
			if isinstance(item, FunctionDef):
				log('  method: %s'%item.name)

				self._classes[ name ].append( item.name )
				item_name = item.name
				item.original_name = item.name
				item.name = '__%s_%s' % (name, item_name)

				self.visit(item)  # this will output the code for the function

				if item_name in self._decorator_properties:
					pass
				else:
					writer.write('__%s_attrs.%s = %s' % (name, item_name, item.name))

			elif isinstance(item, Assign) and isinstance(item.targets[0], Name):
				item_name = item.targets[0].id
				item.targets[0].id = '__%s_%s' % (name, item_name)
				self.visit(item)  # this will output the code for the assign
				writer.write('__%s_attrs.%s = %s' % (name, item_name, item.targets[0].id))
				self._class_attributes[ name ].add( item_name )  ## should this come before self.visit(item) ??
			elif isinstance(item, Pass):
				pass
			elif isinstance(item, ast.Expr) and isinstance(item.value, Str):  ## skip doc strings
				pass
			elif isinstance(item, ast.With) and isinstance( item.context_expr, Name ) and item.context_expr.id == 'javascript':
				self._with_js = True
				writer.with_javascript = True
				for sub in item.body:
					if isinstance(sub, Assign) and isinstance(sub.targets[0], Name):
						item_name = sub.targets[0].id
						sub.targets[0].id = '__%s_%s' % (name, item_name)
						self.visit(sub)  # this will output the code for the assign
						writer.write('__%s_attrs.%s = %s' % (name, item_name, sub.targets[0].id))
						self._class_attributes[ name ].add( item_name )  ## should this come before self.visit(item) ??
					else:
						raise NotImplementedError( sub )
				writer.with_javascript = False
				self._with_js = False

			else:
				raise NotImplementedError( item )

		for prop_name in self._decorator_properties:
			getter = self._decorator_properties[prop_name]['get']
			writer.write('__%s_properties["%s"] = JSObject()' %(name, prop_name))
			writer.write('__%s_properties["%s"]["get"] = %s' %(name, prop_name, getter))
			if self._decorator_properties[prop_name]['set']:
				setter = self._decorator_properties[prop_name]['set']
				writer.write('__%s_properties["%s"]["set"] = %s' %(name, prop_name, setter))

		self._catch_attributes = None
		self._decorator_properties = None
		self._instances.pop('self')
		self._in_class = False

		writer.write('%s = __create_class__("%s", __%s_parents, __%s_attrs, __%s_properties)' % (name, name, name, name, name))
		if 'init' in self._injector:
			writer.write('%s.init_callbacks = JSArray()' %name)
		self._injector = []

		for dec in class_decorators:
			writer.write('%s = __get__(%s,"__call__")( [%s], JSObject() )' % (name, self.visit(dec), name))

	def visit_And(self, node):
		return ' and '

	def visit_Or(self, node):
		return ' or '

	def visit_BoolOp(self, node):
		op = self.visit(node.op)
		return op.join( [self.visit(v) for v in node.values] )

	def visit_If(self, node):
		if self._with_lua:
			writer.write('if __test_if_true__(%s):' % self.visit(node.test))

		elif isinstance(node.test, ast.Dict):
			if self._with_js:
				writer.write('if Object.keys(%s).length:' % self.visit(node.test))
			else:
				writer.write('if %s.keys().length:' % self.visit(node.test))

		elif isinstance(node.test, ast.List):
			writer.write('if %s.length:' % self.visit(node.test))

		elif isinstance(node.test, ast.Name):
			writer.write('if __test_if_true__(%s):' % self.visit(node.test))
		else:
			writer.write('if %s:' % self.visit(node.test))
		writer.push()
		map(self.visit, node.body)
		writer.pull()
		if node.orelse:
			writer.write('else:')
			writer.push()
			map(self.visit, node.orelse)
			writer.pull()

	def visit_TryExcept(self, node):
		writer.write('try:')
		writer.push()
		map(self.visit, node.body)
		writer.pull()
		map(self.visit, node.handlers)

	def visit_Raise(self, node):
		#if self._with_js or self._with_dart:
		#	writer.write('throw Error')
		#else:
		writer.write('raise %s' % self.visit(node.type))

	def visit_ExceptHandler(self, node):
		if node.type and node.name:
			writer.write('except %s, %s:' % (self.visit(node.type), self.visit(node.name)))
		elif node.type and not node.name:
			writer.write('except %s:' % self.visit(node.type))
		else:
			writer.write('except:')
		writer.push()
		map(self.visit, node.body)
		writer.pull()

	def visit_Pass(self, node):
		writer.write('pass')

	def visit_Name(self, node):
		if self._with_js or self._with_dart:
			if node.id == 'True':
				return 'true'
			elif node.id == 'False':
				return 'false'
			elif node.id == 'None':
				if self._with_dart:
					return 'null'
				else:
					return 'undefined'

		return node.id

	def visit_Num(self, node):
		return str(node.n)

	def visit_Return(self, node):
		if node.value:
			if isinstance(node.value, Call) and isinstance(node.value.func, Name) and node.value.func.id in self._classes:
				self._return_type = node.value.func.id
			elif isinstance(node.value, Name) and node.value.id == 'self' and 'self' in self._instances:
				self._return_type = self._instances['self']

			if self._cached_property:
				writer.write('self["__dict__"]["%s"] = %s' %(self._cached_property, self.visit(node.value)) )
				writer.write('return self["__dict__"]["%s"]' %self._cached_property)
			else:
				if self._inline:
					writer.write('__returns__%s = %s' %(self._inline[-1], self.visit(node.value)) )
					if self._inline_breakout:
						writer.write('break')

				elif isinstance(node.value, ast.Tuple):
					writer.write( 'return %s;' % ','.join([self.visit(e) for e in node.value.elts]) )

				else:
					writer.write('return %s' % self.visit(node.value))

		else:
			if self._inline:
				if self._inline_breakout:
					writer.write('break')
			else:
				writer.write('return')  ## empty return

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)

		if op == '|':
			if isinstance(node.right, Str):
				self._custom_op_hack = (node.right.s, left)
				return ''
			elif hasattr(self, '_custom_op_hack') and isinstance(node.left, BinOp):
				op,left_operand = self._custom_op_hack
				right_operand = self.visit(node.right)
				#return '%s( %s, %s )' %(op, left_operand, right_operand)
				if op.decode('utf-8') in self._custom_operators:  ## swap name to python function
					op = self._custom_operators[ op.decode('utf-8') ]
				return '%s( [%s, %s], JSObject() )' %(op, left_operand, right_operand)

		elif op == '%' and isinstance(node.left, ast.Str):
			if self._with_js:
				return '__sprintf( %s, %s )' %(left, right)  ## assumes that right is a tuple, or list.
			else:
				return '__sprintf( %s, %s )' %(left, right)  ## assumes that right is a tuple, or list.

		elif op == '*' and isinstance(node.left, ast.List):
			if len(node.left.elts) == 1 and isinstance(node.left.elts[0], ast.Name) and node.left.elts[0].id == 'None' and not self._with_lua and not self._with_dart:
				return 'JS("new Array(%s)")' %self.visit(node.right)
			elif isinstance(node.right,ast.Num):
				n = node.right.n
			elif isinstance(node.right, Name):
				if node.right.id in self._global_nodes:
					n = self._global_nodes[ node.right.id ].n
				else:
					raise SyntaxError
			else:
				raise SyntaxError

			elts = [ self.visit(e) for e in node.left.elts ]
			expanded = []
			for i in range( n ): expanded.extend( elts )

			if self._with_lua:
				return 'list.__call__([], {pointer:[%s], length:%s})' %(','.join(expanded), n)
			else:
				return '[%s]' %','.join(expanded)

		elif op == '//':
			if self._with_dart:
				return '(%s/%s).floor()' %(left, right)				
			else:
				return 'Math.floor(%s/%s)' %(left, right)

		elif op == '**':
			return 'Math.pow(%s,%s)' %(left, right)

		elif op == '+' and not self._with_dart:
			return '__add_op(%s, %s)'%(left, right)

		elif isinstance(node.left, Name):
			typedef = self.get_typedef( node.left )
			if typedef and op in typedef.operators:
				func = typedef.operators[ op ]
				node.operator_overloading = func
				return '%s( [%s, %s], JSObject() )' %(func, left, right)


		return '(%s %s %s)' % (left, op, right)

	def visit_Eq(self, node):
		return '=='

	def visit_NotEq(self, node):
		return '!='

	def visit_Is(self, node):
		return 'is'

	def visit_Pow(self, node):
		return '**'

	def visit_Mult(self, node):
		return '*'

	def visit_Add(self, node):
		return '+'

	def visit_Sub(self, node):
		return '-'

	def visit_FloorDiv(self, node):
		return '//'
	def visit_Div(self, node):
		return '/'
	def visit_Mod(self, node):
		return '%'
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

	def visit_Lt(self, node):
		return '<'

	def visit_Gt(self, node):
		return '>'

	def visit_GtE(self, node):
		return '>='

	def visit_LtE(self, node):
		return '<='

	def visit_Compare(self, node):
		left = self.visit(node.left)
		comp = [ left ]
		for i in range( len(node.ops) ):
			if isinstance(node.ops[i], ast.In) or isinstance(node.ops[i], ast.NotIn):
				if comp[-1] == left:
					comp.pop()
				else:
					comp.append( ' and ' )

				if isinstance(node.ops[i], ast.NotIn):
					comp.append( ' not (')

				a = ( self.visit(node.comparators[i]), left )

				if self._with_dart:
					## indexOf works with lists and strings in Dart
					comp.append( '%s.contains(%s)' %(a[0], a[1]) )

				elif self._with_js:
					## this makes "if 'x' in Array" work like Python: "if 'x' in list" - TODO fix this for js-objects
					## note javascript rules are confusing: "1 in [1,2]" is true, this is because a "in test" in javascript tests for an index
					## TODO double check this code
					#comp.append( '%s in %s or' %(a[1], a[0]) )  ## this is ugly, will break with Arrays
					#comp.append( '( Object.hasOwnProperty.call(%s, "__contains__") and' %a[0])
					#comp.append( "%s['__contains__'](%s) )" %a )
					##comp.append( ' or (instanceof(%s,Object) and %s in %s) ')
					#comp.append( ' or Object.hasOwnProperty.call(%s, %s)' %(a[0],a[1]))
					## fixes 'o' in 'helloworld' in javascript mode ##
					#comp.append( ' or typeof(%s)=="string" and %s.__contains__(%s)' %(a[0],a[0],a[1]))
					comp.append( '__contains__(%s, %s)' %(a[0],a[1]))
				else:
					comp.append( "__get__(__get__(%s, '__contains__'), '__call__')([%s], JSObject())" %a )

				if isinstance(node.ops[i], ast.NotIn):
					comp.append( ' )')  ## it is not required to enclose NotIn

			else:
				comp.append( self.visit(node.ops[i]) )
				comp.append( self.visit(node.comparators[i]) )
		return ' '.join( comp )

	def visit_Not(self, node):
		return ' not '

	def visit_IsNot(self, node):
		return ' is not '

	def visit_UnaryOp(self, node):
		op = self.visit(node.op)
		if op is None: raise RuntimeError( node.op )
		operand = self.visit(node.operand)
		if operand is None: raise RuntimeError( node.operand )
		return op + operand

	def visit_USub(self, node):
		return '-'

	def visit_Attribute(self, node):
		node_value = self.visit(node.value)

		if self._with_js or self._with_dart or self._with_ll:
			return '%s.%s' %(node_value, node.attr)
		typedef = None
		if isinstance(node.value, Name):
			typedef = self.get_typedef( instance=node.value )
		elif hasattr(node.value, 'returns_type'):
			typedef = self.get_typedef( class_name=node.value.returns_type )

		if typedef:
			if node.attr in typedef.properties:
				getter = typedef.properties[ node.attr ]['get']
				if getter in self._function_return_types:
					node.returns_type = self._function_return_types[getter]
				return '%s( [%s], JSObject() )' %(getter, node_value)

			if '__getattribute__' in typedef.methods or typedef.check_for_parent_with( method='__getattribute__' ):
				return '__get__(%s, "%s")' % (node_value, node.attr)


			#elif node.attr in typedef.class_attributes and not typedef.check_for_parent_with( class_attribute=node.attr ) and node_value != 'self':
			#	## This optimization breaks when a subclass redefines a class attribute,
			#	## but we need it for inplace assignment operators, this is safe only when
			#	## other parent classes have not defined the same class attribute.
			#	## This is also not safe when node_value is "self".
			#	return "%s['__class__']['%s']" %(node_value, node.attr)

			elif node.attr in typedef.attributes:
				return "%s.%s" %(node_value, node.attr)

			#elif '__getattr__' in typedef.methods:
			#	func = typedef.get_pythonjs_function_name( '__getattr__' )
			#	return '%s([%s, "%s"], JSObject())' %(func, node_value, node.attr)

			elif typedef.check_for_parent_with( property=node.attr ):
				parent = typedef.check_for_parent_with( property=node.attr )
				getter = parent.properties[ node.attr ]['get']
				if getter in self._function_return_types:
					node.returns_type = self._function_return_types[getter]
				return '%s( [%s], JSObject() )' %(getter, node_value)

			#elif typedef.check_for_parent_with( class_attribute=node.attr ):
			#	#return '__get__(%s, "%s")' % (node_value, node.attr)  ## __get__ is broken with grandparent class attributes - TODO double check and fix this
			#	if node.attr in typedef.class_attributes:
			#		## this might not be always correct
			#		return "%s['__class__']['%s']" %(node_value, node.attr)
			#	else:
			#		parent = typedef.check_for_parent_with( class_attribute=node.attr )
			#		return "__%s_attrs['%s']" %(parent.name, node.attr)  ## TODO, get from class.__dict__

			#elif typedef.check_for_parent_with( method='__getattr__' ):
			#	parent = typedef.check_for_parent_with( method='__getattr__' )
			#	func = parent.get_pythonjs_function_name( '__getattr__' )
			#	return '%s([%s, "%s"], JSObject())' %(func, node_value, node.attr)

			else:
				return '__get__(%s, "%s")' % (node_value, node.attr)  ## TODO - this could be a builtin class like: list, dict, etc.
		else:
			return '__get__(%s, "%s")' % (node_value, node.attr)      ## TODO - double check this


	def visit_Index(self, node):
		return self.visit(node.value)

	def visit_Subscript(self, node):
		name = self.visit(node.value)

		if isinstance(node.slice, ast.Ellipsis):
			#return '%s["$wrapped"]' %name
			return '%s[...]' %name

		elif self._with_ll:
			return '%s[ %s ]' %(name, self.visit(node.slice))

		elif self._with_js or self._with_dart:
			if isinstance(node.slice, ast.Slice):  ## allow slice on Array
				if self._with_dart:
					## this is required because we need to support slices on String ##
					return '__getslice__(%s, %s)'%(name, self.visit(node.slice))
				else:
					return '%s.__getslice__(%s)'%(name, self.visit(node.slice))

			elif self._with_dart:
				return '%s[ %s ]' %(name, self.visit(node.slice))

			elif isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.Num):
				if node.slice.value.n < 0:
					return '%s[ %s.length+%s ]' %(name, name, self.visit(node.slice))
				else:
					return '%s[ %s ]' %(name, self.visit(node.slice))

			else:
				s = self.visit(node.slice)
				return '%s[ __ternary_operator__(%s.__uid__, %s) ]' %(name, s, s)

		elif isinstance(node.slice, ast.Slice):
			return '__get__(%s, "__getslice__")([%s], JSObject())' % (
				self.visit(node.value),
				self.visit(node.slice),
			)

		elif name in self._func_typedefs and self._func_typedefs[name] == 'list':
			#return '%s[...][%s]'%(name, self.visit(node.slice))
			return '%s[%s]'%(name, self.visit(node.slice))

		elif name in self._instances:  ## support x[y] operator overloading
			klass = self._instances[ name ]
			if '__getitem__' in self._classes[ klass ]:
				return '__%s___getitem__([%s, %s], JSObject())' % (klass, name, self.visit(node.slice))
			else:
				return '__get__(%s, "__getitem__")([%s], JSObject())' % (
					self.visit(node.value),
					self.visit(node.slice),
				)
		else:
			return '__get__(%s, "__getitem__")([%s], JSObject())' % (
				self.visit(node.value),
				self.visit(node.slice),
			)

	def visit_Slice(self, node):
		if self._with_dart:
			lower = upper = step = 'null'
		elif self._with_js:
			lower = upper = step = 'undefined'
		else:
			lower = upper = step = None
		if node.lower:
			lower = self.visit(node.lower)
		if node.upper:
			upper = self.visit(node.upper)
		if node.step:
			step = self.visit(node.step)
		return "%s, %s, %s" % (lower, upper, step)

	def visit_Assign(self, node):
		for target in node.targets:
			self._visit_assign_helper( node, target )
			node = ast.Expr( value=target )

	def _visit_assign_helper(self, node, target):
		if isinstance(target, Subscript):
			name = self.visit(target.value)  ## target.value may have "returns_type" after being visited

			if isinstance(target.slice, ast.Ellipsis):
				#code = '%s["$wrapped"] = %s' %(self.visit(target.value), self.visit(node.value))
				code = '%s[...] = %s' %(self.visit(target.value), self.visit(node.value))

			elif self._with_dart or self._with_ll:
				code = '%s[ %s ] = %s'
				code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))

			elif self._with_js:
				s = self.visit(target.slice.value)
				if isinstance(target.slice.value, ast.Num):
					code = '%s[ %s ] = %s' % (self.visit(target.value), s, self.visit(node.value))
				else:
					code = '%s[ __ternary_operator__(%s.__uid__, %s) ] = %s' % (self.visit(target.value), s, s, self.visit(node.value))

			elif name in self._func_typedefs and self._func_typedefs[name] == 'list':
				#code = '%s[...][%s] = %s'%(name, self.visit(target.slice.value), self.visit(node.value))
				code = '%s[%s] = %s'%(name, self.visit(target.slice.value), self.visit(node.value))

			else:
				code = "__get__(__get__(%s, '__setitem__'), '__call__')([%s, %s], JSObject())"
				code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))

			writer.write(code)

		elif isinstance(target, Attribute):
			target_value = self.visit(target.value)  ## target.value may have "returns_type" after being visited
			typedef = None
			if isinstance(target.value, Name):
				if target.value.id == 'self' and isinstance(self._catch_attributes, set):
					self._catch_attributes.add( target.attr )
				typedef = self.get_typedef( instance=target.value )
			elif hasattr(target.value, 'returns_type'):
				typedef = self.get_typedef( class_name=target.value.returns_type )

			if self._with_js or self._with_dart:
				writer.write( '%s.%s=%s' %(target_value, target.attr, self.visit(node.value)) )
			elif typedef and target.attr in typedef.properties and 'set' in typedef.properties[ target.attr ]:
				setter = typedef.properties[ target.attr ]['set']
				writer.write( '%s( [%s, %s], JSObject() )' %(setter, target_value, self.visit(node.value)) )
			elif typedef and target.attr in typedef.class_attributes:
				writer.write( '''%s['__class__']['%s'] = %s''' %(target_value, target.attr, self.visit(node.value)))
			elif typedef and target.attr in typedef.attributes:
				writer.write( '%s.%s = %s' %(target_value, target.attr, self.visit(node.value)))

			elif typedef and typedef.parents:
				parent_prop = typedef.check_for_parent_with( property=target.attr )
				parent_classattr = typedef.check_for_parent_with( class_attribute=target.attr )
				parent_setattr = typedef.check_for_parent_with( method='__setattr__' )
				if parent_prop and 'set' in parent_prop.properties[target.attr]:
					setter = parent_prop.properties[target.attr]['set']
					writer.write( '%s( [%s, %s], JSObject() )' %(setter, target_value, self.visit(node.value)) )

				elif parent_classattr:
					writer.write( "__%s_attrs.%s = %s" %(parent_classattr.name, target.attr, self.visit(node.value)) )

				elif parent_setattr:
					func = parent_setattr.get_pythonjs_function_name( '__setattr__' )
					writer.write( '%s([%s, "%s", %s], JSObject() )' %(func, target_value, target.attr, self.visit(node.value)) )

				elif '__setattr__' in typedef.methods:
					func = typedef.get_pythonjs_function_name( '__setattr__' )
					writer.write( '%s([%s, "%s", %s], JSObject() )' %(func, target_value, target.attr, self.visit(node.value)) )

				else:
					code = '__set__(%s, "%s", %s)' % (
						target_value,
						target.attr,
						self.visit(node.value)
					)
					writer.write(code)

			elif typedef and '__setattr__' in typedef.methods:
				func = typedef.get_pythonjs_function_name( '__setattr__' )
				log('__setattr__ in instance typedef.methods - func:%s target_value:%s target_attr:%s' %(func, target_value, target_attr))
				writer.write( '%s([%s, "%s", %s], JSObject() )' %(func, target_value, target.attr, self.visit(node.value)) )


			else:
				code = '__set__(%s, "%s", %s)' % (
					target_value,
					target.attr,
					self.visit(node.value)
				)
				writer.write(code)

		elif isinstance(target, Name):
			node_value = self.visit( node.value )  ## node.value may have extra attributes after being visited

			if writer.is_at_global_level():
				log('GLOBAL: %s : %s'%(target.id, node_value))
				self._globals[ target.id ] = None
				self._global_nodes[ target.id ] = node.value

			if isinstance(node.value, Call) and hasattr(node.value.func, 'id') and node.value.func.id in self._classes:
				self._instances[ target.id ] = node.value.func.id  ## keep track of instances
			elif isinstance(node.value, Call) and isinstance(node.value.func, Name) and node.value.func.id in self._function_return_types:
				self._instances[ target.id ] = self._function_return_types[ node.value.func.id ]
			elif isinstance(node.value, Call) and isinstance(node.value.func, Attribute) and isinstance(node.value.func.value, Name) and node.value.func.value.id in self._instances:
				typedef = self.get_typedef( node.value.func.value )
				method = node.value.func.attr
				if method in typedef.methods:
					func = typedef.get_pythonjs_function_name( method )
					if func in self._function_return_types:
						self._instances[ target.id ] = self._function_return_types[ func ]
					else:
						writer.write('## %s - unknown return type for: %s' % (typedef.name, func))
				else:
					writer.write('## %s - not a method: %s' %(typedef.name, method))

			elif isinstance(node.value, Name) and node_value in self._instances:  ## if this is a simple copy: "a = b" and "b" is known to be of some class
				self._instances[ target.id ] = self._instances[ node_value ]
			elif isinstance(node.value, BinOp) and hasattr(node.value, 'operator_overloading') and node.value.operator_overloading in self._function_return_types:
				self._instances[ target.id ] = self._function_return_types[ node.value.operator_overloading ]
			elif hasattr(node.value, 'returns_type'):
				self._instances[ target.id ] = node.value.returns_type
			elif target.id in self._instances:
				if target.id in self._globals:
					pass
				else:
					log('--forget: %s'%target.id)
					type = self._instances.pop( target.id )
					log('----%s'%type)

			if target.id in self._instances:
				type = self._instances[ target.id ]
				log('typed assignment: %s is-type %s' %(target.id,type))
				if writer.is_at_global_level():
					self._globals[ target.id ] = type
					log('known global:%s - %s'%(target.id,type))

					if self._with_static_type:
						if type == 'list':
							self._global_typed_lists[ target.id ] = set()
						elif type == 'tuple':
							self._global_typed_tuples[ target.id ] = set()
						elif type == 'dict':
							self._global_typed_dicts[ target.id ] = set()

					writer.write('%s = %s' % (self.visit(target), node_value))
				else:
					if target.id in self._globals and self._globals[target.id] is None:
						self._globals[target.id] = type
						self._instances[ target.id ] = type
						log('set global type: %s'%type)

					writer.write('%s = %s' % (self.visit(target), node_value))

			#elif self._with_dart and writer.is_at_global_level():
			#	writer.write('JS("var %s = %s")' % (self.visit(target), node_value))
			else:
				writer.write('%s = %s' % (self.visit(target), node_value))

		elif self._with_lua or self._with_dart:  ## Tuple - lua and dart supports destructured assignment
			elts = [self.visit(e) for e in target.elts]
			writer.write('%s = %s' % (','.join(elts), self.visit(node.value)))

		else:  # it's a Tuple
			id = self.identifier
			self.identifier += 1
			r = '__r_%s' % id
			writer.write('var(%s)' % r)
			writer.write('%s = %s' % (r, self.visit(node.value)))
			for i, target in enumerate(target.elts):
				if isinstance(target, Attribute):
					code = '__set__(%s, "%s", %s[%s])' % (
						self.visit(target.value),
						target.attr,
						r,
						i
					)
					writer.write(code)
				elif self._with_js or self._with_dart:
					writer.write("%s = %s[%s]" % (self.visit(target), r, i))
				else:
					writer.write("%s = __get__(__get__(%s, '__getitem__'), '__call__')([%s], __NULL_OBJECT__)" % (self.visit(target), r, i))

	def visit_Print(self, node):
		writer.write('print %s' % ', '.join(map(self.visit, node.values)))

	def visit_Str(self, node):
		s = node.s.replace('\\','\\\\').replace('\n', '\\n').replace('\0', '\\0')
		if self._with_js or self._with_dart:
			return '"%s"' %s
		else:
			if len(s) == 0:
				return '""'
			elif s.startswith('"') or s.endswith('"'):
				return "'''%s'''" %s
			else:
				return '"""%s"""' %s

	def visit_Expr(self, node):
		log('line: %s' %node.lineno )
		if node.lineno < len(self._source):
			src = self._source[ node.lineno ]
			log( src )

		line = self.visit(node.value)
		if line:
			writer.write(line)

	def inline_function(self, node):
		name = self.visit(node.func)
		log('--------------------------starting inline: %s---------------'%name)
		writer.write('################################inlined->%s'%name)
		fnode = self._global_functions[ name ]
		fnode = copy.deepcopy( fnode )
		log('inspecting:%s' %fnode)
		finfo = inspect_function( fnode )
		remap = {}
		for n in finfo['name_nodes']:
			if n.id not in finfo['locals']: continue

			if isinstance(n.id, Name):
				log(n.id.id)
				raise RuntimeError

			if n.id not in remap:
				new_name = n.id + '_%s'%self._inline_ids
				remap[ n.id ] = new_name
				self._inline_ids += 1

			n.id = remap[ n.id ]

		if remap:
			writer.write( "JS('var %s')" %','.join(remap.values()) )
			for n in remap:
				if n in finfo['typedefs']:
					self._func_typedefs[ remap[n] ] = finfo['typedefs'][n]

		offset = len(fnode.args.args) - len(fnode.args.defaults)
		for i,ad in enumerate(fnode.args.args):
			if i < len(node.args):
				ac = self.visit( node.args[i] )
			else:
				assert fnode.args.defaults
				dindex = i - offset
				ac = self.visit( fnode.args.defaults[dindex] )

			ad = remap[ self.visit(ad) ]
			writer.write( "%s = %s" %(ad, ac) )


		return_id = name + str(self._inline_ids)
		self._inline.append( return_id )

		writer.write("JS('var __returns__%s = null')"%return_id)
		#if len( finfo['return_nodes'] ) > 1:  ## TODO fix me
		if True:
			self._inline_breakout = True
			writer.write('while True:')
			writer.push()
			for b in fnode.body:
				self.visit(b)

			if not len( finfo['return_nodes'] ):
				writer.write('break')
			writer.pull()
			#self._inline_breakout = False
		else:
			for b in fnode.body:
				self.visit(b)

		if self._inline.pop() != return_id:
			raise RuntimeError

		for n in remap:
			gname = remap[n]
			for n in finfo['name_nodes']:
				if n.id == gname:
					n.id = n
		log('###########inlined %s###########'%name)
		return '__returns__%s' %return_id

	def visit_Call(self, node):
		if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'pythonjs' and node.func.attr == 'configure':
			for kw in node.keywords:
				if kw.arg == 'javascript':
					if kw.value.id == 'True':
						self._with_js = True
						writer.with_javascript = True
					elif kw.value.id == 'False':
						self._with_js = False
						writer.with_javascript = False
					else:
						raise SyntaxError

				elif kw.arg == 'dart':
					if kw.value.id == 'True':
						self._with_dart = True
					elif kw.value.id == 'False':
						self._with_dart = False
					else:
						raise SyntaxError

				elif kw.arg == 'coffee':
					if kw.value.id == 'True':
						self._with_coffee = True
					elif kw.value.id == 'False':
						self._with_coffee = False
					else:
						raise SyntaxError

				elif kw.arg == 'lua':
					if kw.value.id == 'True':
						self._with_lua = True
					elif kw.value.id == 'False':
						self._with_lua = False
					else:
						raise SyntaxError

				elif kw.arg == 'inline':
					if kw.value.id == 'True':
						self._with_inline = True
					elif kw.value.id == 'False':
						self._with_inline = False
					else:
						raise SyntaxError

				else:
					raise SyntaxError

		elif self._with_ll:
			name = self.visit(node.func)
			args = [self.visit(arg) for arg in node.args]
			if node.keywords:
				args.extend( [self.visit(x.value) for x in node.keywords] )
				return '%s(%s)' %( self.visit(node.func), ','.join(args) )

			else:
				return '%s(%s)' %( self.visit(node.func), ','.join(args) )

		elif self._with_js or self._with_dart:
			name = self.visit(node.func)
			args = list( map(self.visit, node.args) )

			if name in self._generator_functions:
				return ' new(%s(%s))' %(name, ','.join(args))

			elif self._with_dart and name in self._builtin_functions_dart:
				if args:
					return self._builtin_functions_dart[name] % ','.join(args)
				else:
					return self._builtin_functions_dart[name]

			elif name in self._builtin_functions and self._builtin_functions[name]:  ## inlined js
				if args:
					return self._builtin_functions[name] % ','.join(args)
				else:
					return self._builtin_functions[name]

			elif isinstance(node.func, Name) and node.func.id == 'new':
				assert len(args) == 1
				return 'new(%s)' %args[0]

			elif isinstance(node.func, ast.Attribute) and not self._with_dart:  ## special method calls
				anode = node.func
				if anode.attr == 'get':
					if args:
						return '__jsdict_get(%s, %s)' %(self.visit(anode.value), ','.join(args) )
					else:
						return '__jsdict_get(%s)' %self.visit(anode.value)

				elif anode.attr == 'set' and len(args)==2:
					return '__jsdict_set(%s, %s)' %(self.visit(anode.value), ','.join(args))

				elif anode.attr == 'keys' and not args:
					return '__jsdict_keys(%s)' %self.visit(anode.value)

				elif anode.attr == 'values' and not args:
					return '__jsdict_values(%s)' %self.visit(anode.value)

				elif anode.attr == 'items' and not args:
					return '__jsdict_items(%s)' %self.visit(anode.value)

				elif anode.attr == 'pop':
					if args:
						return '__jsdict_pop(%s, %s)' %(self.visit(anode.value), ','.join(args) )
					else:
						return '__jsdict_pop(%s)' %self.visit(anode.value)

				elif anode.attr == 'split' and not args:
					return '__split_method(%s)' %self.visit(anode.value)

				else:
					a = ','.join(args)
					if node.keywords:
						args.extend( [self.visit(x.value) for x in node.keywords] )
						return '%s(%s)' %( self.visit(node.func), ','.join(args) )

					else:
						return '%s(%s)' %( self.visit(node.func), ','.join(args) )


			elif isinstance(node.func, Name) and node.func.id in self._js_classes:
				a = ','.join(args)
				return 'new( %s(%s) )' %( self.visit(node.func), a )

			elif name in self._global_functions and self._with_inline:
				return self.inline_function( node )

			elif self._with_dart:  ## DART
				args
				if node.keywords:
					kwargs = ','.join( ['%s:%s'%(x.arg, self.visit(x.value)) for x in node.keywords] )
					if args:
						return '%s(%s, JS("%s"))' %( self.visit(node.func), ','.join(args), kwargs )
					else:
						return '%s( JS("%s"))' %( self.visit(node.func), kwargs )

				else:
					a = ','.join(args)
					return '%s(%s)' %( self.visit(node.func), a )

			else:  ## javascript mode
				if node.keywords:
					args.extend( [self.visit(x.value) for x in node.keywords] )
					return '%s(%s)' %( self.visit(node.func), ','.join(args) )

				else:
					return '%s(%s)' %( self.visit(node.func), ','.join(args) )


		elif isinstance(node.func, Name) and node.func.id in self._generator_functions:
			name = self.visit(node.func)
			args = list( map(self.visit, node.args) )
			if name in self._generator_functions:
				return 'JS("new %s(%s)")' %(name, ','.join(args))

		elif isinstance(node.func, Name) and node.func.id == 'new':
			tmp = self._with_js
			self._with_js = True
			args = list( map(self.visit, node.args) )
			self._with_js = tmp
			assert len(args) == 1
			return 'new(%s)' %args[0]

		elif isinstance(node.func, Name) and node.func.id in ('JS', 'toString', 'JSObject', 'JSArray', 'var', 'instanceof', 'typeof'):
			args = list( map(self.visit, node.args) ) ## map in py3 returns an iterator not a list
			if node.func.id == 'var':
				for k in node.keywords:
					self._instances[ k.arg ] = k.value.id
					args.append( k.arg )
			else:
				kwargs = map(lambda x: '%s=%s' % (x.arg, self.visit(x.value)), node.keywords)
				args.extend(kwargs)
			args = ', '.join(args)
			return '%s(%s)' % (node.func.id, args)
		else:

			## check if pushing to a global typed list ##
			if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id in self._global_typed_lists and node.func.attr == 'append':
				gtype = self._globals[ node.func.value.id ]
				if gtype == 'list' and node.func.attr == 'append':
					if isinstance(node.args[0], Name):
						if node.args[0].id in self._instances:
							gset = self._global_typed_lists[ node.func.value.id ]
							gset.add( self._instances[node.args[0].id])
							if len(gset) != 1:
								raise SyntaxError('global lists can only contain one type: instance "%s" is different' %node.args[0].id)
						else:
							raise SyntaxError('global lists can only contain one type: instance "%s" is unknown' %node.args[0].id)

			call_has_args_only = len(node.args) and not (len(node.keywords) or node.starargs or node.kwargs)
			call_has_args_kwargs_only = len(node.args) and len(node.keywords) and not (node.starargs or node.kwargs)
			call_has_args = len(node.args) or len(node.keywords) or node.starargs or node.kwargs
			name = self.visit(node.func)
			args = None
			kwargs = None

			if call_has_args_only:  ## lambda only supports simple args for now.
				args = ', '.join(map(self.visit, node.args))

			elif call_has_args_kwargs_only:
				args = ', '.join(map(self.visit, node.args))
				kwargs = ', '.join(map(lambda x: '%s:%s' % (x.arg, self.visit(x.value)), node.keywords))

			elif call_has_args:
				args = ', '.join(map(self.visit, node.args))
				kwargs = ', '.join(map(lambda x: '%s=%s' % (x.arg, self.visit(x.value)), node.keywords))
				args_name = '__args_%s' % self.identifier
				kwargs_name = '__kwargs_%s' % self.identifier

				writer.append('var(%s, %s)' % (args_name, kwargs_name))
				self.identifier += 1

				writer.append('%s = [%s]' % (args_name, args))

				if node.starargs:
					writer.append('%s.push.apply(%s, %s)' % (args_name, args_name, self.visit(node.starargs)))

				writer.append('%s = JSObject(%s)' % (kwargs_name, kwargs))

				if node.kwargs:
					kwargs = self.visit(node.kwargs)
					writer.write('var(__kwargs_temp)')
					writer.write('__kwargs_temp = %s[...]' %kwargs)
					#code = "JS('for (var name in %s) { %s[name] = %s[...][name]; }')" % (kwargs, kwargs_name, kwargs)
					#code = "for __name in %s: %s[__name] = %s[__name]" % (kwargs, kwargs_name, kwargs)
					code = "JS('for (var name in __kwargs_temp) { %s[name] = __kwargs_temp[name]; }')" %kwargs_name
					writer.append(code)

			#######################################

			## special method calls ##
			if isinstance(node.func, ast.Attribute) and node.func.attr in ('get', 'keys', 'values', 'pop', 'items', 'split') and not self._with_lua:
				anode = node.func
				if anode.attr == 'get':
					if args:
						return '__jsdict_get(%s, %s)' %(self.visit(anode.value), args )
					else:
						return '__jsdict_get(%s)' %self.visit(anode.value)

				elif anode.attr == 'keys' and not args:
					return '__jsdict_keys(%s)' %self.visit(anode.value)

				elif anode.attr == 'values' and not args:
					return '__jsdict_values(%s)' %self.visit(anode.value)

				elif anode.attr == 'items' and not args:
					return '__jsdict_items(%s)' %self.visit(anode.value)

				elif anode.attr == 'pop':
					if args:
						return '__jsdict_pop(%s, %s)' %(self.visit(anode.value), args )
					else:
						return '__jsdict_pop(%s)' %self.visit(anode.value)

				elif anode.attr == 'split' and not args:
					return '__split_method(%s)' %self.visit(anode.value)

				else:
					return '%s(%s)' %( self.visit(node.func), args )

			elif not self._with_lua and not self._with_dart and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id in self._func_typedefs:
				type = self._func_typedefs[ node.func.value.id ]
				if type == 'list' and node.func.attr == 'append':
					return '%s.push(%s)' %(node.func.value.id, self.visit(node.args[0]))
				else:
					raise RuntimeError

			elif hasattr(node,'constant') or name in self._builtin_functions:
				if args and kwargs:
					return '%s([%s], {%s})' %(args, kwargs)
				elif args:
					return '%s([%s], __NULL_OBJECT__)' %(name,args)
				elif kwargs:
					return '%s([], {%s})' %(name,kwargs)
				else:
					return '%s()' %name

			elif name in self._global_functions and self._with_inline:
				return self.inline_function( node )

			elif call_has_args_only:
				if name in self._global_functions:
					return '%s( [%s], __NULL_OBJECT__ )' %(name,args)
				else:
					return '__get__(%s, "__call__")([%s], __NULL_OBJECT__)' % (name, args)

			elif call_has_args_kwargs_only:
				if name in self._global_functions:
					return '%s( [%s], {%s} )' %(name,args, kwargs)
				else:
					return '__get__(%s, "__call__")([%s], {%s} )' % (name, args, kwargs)


			elif call_has_args:
				if name == 'dict':
					return '__get__(%s, "__call__")(%s, JSObject(pointer=%s))' % (name, args_name, kwargs_name)
				else:
					return '__get__(%s, "__call__")(%s, %s)' % (name, args_name, kwargs_name)

			elif name in self._classes:
				return '__get__(%s, "__call__")( )' %name

			elif name in self._builtin_classes:
				return '__get__(%s, "__call__")( )' %name

			elif name in self._global_functions:
				#return '__get__(%s, "__call__")( JSArray(), JSObject() )' %name  ## SLOW ##
				return '%s( )' %name  ## this is much FASTER ##

			else:
				## if the user is trying to create an instance of some class
				## and that class is define in an external binding,
				## and they forgot to put "from mylibrary import *" in their script (an easy mistake to make)
				## then this fails to call __call__ to initalize the instance,
				## or a factory function was used that was passed the class to make,
				## it will throw this confusing error:
				## Uncaught TypeError: Property 'SomeClass' of object [object Object] is not a function 
				## TODO - remove this optimization, or provide the user with a better error message.

				## So to be safe we still wrap with __get__ and "__call__"
				return '__get__(%s, "__call__")( )' %name

	def visit_Lambda(self, node):
		args = [self.visit(a) for a in node.args.args]
		#if self._with_js:  ## TODO is it better to return a normal lambda
		#	return """JS('(function (%s) {return %s})')""" %(','.join(args), self.visit(node.body))
		#else:
		return 'lambda %s: %s' %(','.join(args), self.visit(node.body))

	def visit_FunctionDef(self, node):
		log('-----------------')
		if node in self._generator_function_nodes:
			log('generator function: %s'%node.name)
			self._generator_functions.add( node.name )
			if '--native-yield' in sys.argv:
				raise NotImplementedError  ## TODO
			else:
				GeneratorFunctionTransformer( node, compiler=self )
				return
		log('function: %s'%node.name)

		property_decorator = None
		decorators = []
		with_js_decorators = []
		with_dart_decorators = []
		setter = False
		return_type = None
		fastdef = False
		javascript = False
		inline = False
		self._cached_property = None
		self._func_typedefs = {}

		if writer.is_at_global_level():
			self._global_functions[ node.name ] = node  ## save ast-node

		for decorator in reversed(node.decorator_list):
			log('@decorator: %s' %decorator)
			if isinstance(decorator, Name) and decorator.id == 'inline':
				inline = True
				self._with_inline = True

			elif self._with_dart:
				with_dart_decorators.append( self.visit(decorator) )

			elif self._with_js:  ## decorators are special in with-js mode
				with_js_decorators.append( self.visit( decorator ) )

			elif isinstance(decorator, Name) and decorator.id == 'fastdef':
				fastdef = True

			elif isinstance(decorator, Name) and decorator.id == 'javascript':
				javascript = True

			elif isinstance(decorator, Name) and decorator.id in ('property', 'cached_property'):
				property_decorator = decorator
				n = node.name + '__getprop__'
				self._decorator_properties[ node.original_name ] = dict( get=n, set=None )
				node.name = n
				if decorator.id == 'cached_property':  ## TODO DEPRECATE
					self._cached_property = node.original_name

			elif isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id in self._decorator_properties:
				if decorator.attr == 'setter':
					if self._decorator_properties[ decorator.value.id ]['set']:
						raise SyntaxError('user error - the same decorator.setter is used more than once!')
					n = node.name + '__setprop__'
					self._decorator_properties[ decorator.value.id ]['set'] = n
					node.name = n
					setter = True
					prop_name = node.original_name

				elif decorator.attr == 'deleter':
					raise NotImplementedError
				else:
					raise RuntimeError

			elif isinstance(decorator, Call) and decorator.func.id == 'custom_operator':
				assert len(decorator.args) == 1
				assert isinstance( decorator.args[0], Str )
				op = decorator.args[0].s.decode('utf-8')
				if op not in self._custom_operators:
					raise RuntimeError( op, self._custom_operators )
				self._custom_operators[ op ] = node.name

			elif isinstance(decorator, Call) and decorator.func.id == 'returns':
				assert len(decorator.args) == 1
				assert isinstance( decorator.args[0], Name)
				return_type = decorator.args[0].id

			elif isinstance(decorator, Call) and decorator.func.id == 'typedef':
				c = decorator
				assert len(c.args) == 0 and len(c.keywords)
				for kw in c.keywords:
					assert isinstance( kw.value, Name)
					self._instances[ kw.arg ] = kw.value.id
					self._func_typedefs[ kw.arg ] = kw.value.id
					log('@typedef - %s : %s'%(kw.arg, kw.value.id))

			else:
				decorators.append( decorator )

		if self._with_dart:
			## dart supports optional positional params [x=1, y=2], or optional named {x:1, y:2}
			## but not both at the same time.
			if node.args.kwarg:
				raise SyntaxError( 'dart functions can not take variable keyword arguments (**kwargs)' )

			for dec in with_dart_decorators: writer.write('@%s'%dec)

			args = []
			offset = len(node.args.args) - len(node.args.defaults)
			for i, arg in enumerate(node.args.args):
				a = arg.id
				dindex = i - offset
				if dindex >= 0 and node.args.defaults:
					default_value = self.visit( node.args.defaults[dindex] )
					args.append( '%s=%s' %(a, default_value) )
				else:
					args.append( a )

			if node.args.vararg:
				if node.args.defaults:
					raise SyntaxError( 'dart functions can not use variable arguments (*args) and have keyword arguments' )

				args.append('__variable_args__%s' %node.args.vararg)


			writer.write( 'def %s( %s ):' % (node.name, ','.join(args)) )


		elif self._with_js or javascript:# or self._with_coffee:
			if node.args.vararg:
				raise SyntaxError( 'pure javascript functions can not take variable arguments (*args)' )
			elif node.args.kwarg:
				raise SyntaxError( 'pure javascript functions can not take variable keyword arguments (**kwargs)' )

			args = [ a.id for a in node.args.args ]
			writer.write( 'def %s( %s ):' % (node.name, ','.join(args)) )

		else:
			writer.write('def %s(args, kwargs):' % node.name)
		writer.push()

		## the user will almost always want to use Python-style variable scope,
		## this is kept here as an option to be sure we are compatible with the
		## old-style code in runtime/pythonpythonjs.py and runtime/builtins.py
		if not GLOBAL_VARIABLE_SCOPE and not self._with_coffee:
			local_vars, global_vars = retrieve_vars(node.body)
			if local_vars-global_vars:
				vars = []
				args = [ a.id for a in node.args.args ]

				for v in local_vars-global_vars:
					if v in args: pass
					else: vars.append( v )

				a = ','.join( vars )
				writer.write('var(%s)' %a)

		#####################################################################
		if self._with_dart:
			pass

		elif self._with_js or javascript:
			if node.args.defaults:
				offset = len(node.args.args) - len(node.args.defaults)
				for i, arg in enumerate(node.args.args):
					dindex = i - offset
					if dindex >= 0:
						default_value = self.visit( node.args.defaults[dindex] )
						writer.write( '''JS("if (%s == undefined) %s = %s")'''%(arg.id, arg.id, default_value) )

		elif self._with_fastdef or fastdef:
			offset = len(node.args.args) - len(node.args.defaults)
			for i, arg in enumerate(node.args.args):
				dindex = i - offset
				if dindex >= 0 and node.args.defaults:
					default_value = self.visit( node.args.defaults[dindex] )
					writer.write('''JS("var %s = kwargs[ '%s' ]")''' % (arg.id, arg.id))
					writer.write( '''JS("if (%s == undefined) %s = %s")'''%(arg.id, arg.id, default_value) )

				else:
					writer.write("""JS("var %s = args[ %s ]")""" % (arg.id, i))

		elif self._with_lua:
			writer.write( 'var(%s)' %','.join([arg.id for arg in node.args.args]))
			offset = len(node.args.args) - len(node.args.defaults)
			for i,arg in enumerate(node.args.args):
				dindex = i - offset
				if dindex >= 0 and node.args.defaults:
					default_value = self.visit( node.args.defaults[dindex] )
					writer.write("%s = kwargs.%s or %s" % (arg.id, arg.id, default_value))
				else:
					writer.write( "%s = args[ %s ]" %(arg.id, i+1) )

		elif len(node.args.defaults) or len(node.args.args) or node.args.vararg or node.args.kwarg:
			# First check the arguments are well formed 
			# ie. that this function is not a callback of javascript code
			writer.write("""if (JS('args instanceof Array') and JS("{}.toString.call(kwargs) === '[object Object]'") and arguments.length == 2):""")
			# XXX: there is bug in the underlying translator preventing me to write the condition
			# in a more readble way... something to do with brakects...
			writer.push()
			writer.write('pass')  # do nothing if it's not called from javascript
			writer.pull()
			writer.write('else:')
			writer.push()
			# If it's the case, move use ``arguments`` to ``args`` 
			writer.write('args = Array.prototype.slice.call(arguments)')
			# This means you can't pass keyword argument from javascript but we already knew that
			writer.write('kwargs = JSObject()')
			writer.pull()
			# done with pythonjs function used as callback of Python code 

			# new pythonjs' python function arguments handling
			# create the structure representing the functions arguments
			# first create the defaultkwargs JSObject
			if not self._with_coffee:
				writer.write('var(__sig__, __args__)')

			L = len(node.args.defaults)
			kwargsdefault = map(lambda x: keyword(self.visit(x[0]), x[1]), zip(node.args.args[-L:], node.args.defaults))
			kwargsdefault = Call(
				Name('JSObject', None),
				[],
				kwargsdefault,
				None,
				None
			)
			args = Call(
				Name('JSArray', None),
				map(lambda x: Str(x.id), node.args.args),
				[],
				None,
				None
			)
			keywords = list([
				keyword(Name('kwargs', None), kwargsdefault),
				keyword(Name('args', None), args),
			])
			if node.args.vararg:
				keywords.append(keyword(Name('vararg', None), Str(node.args.vararg)))
			if node.args.kwarg:
				keywords.append(keyword(Name('varkwarg', None), Str(node.args.kwarg)))

			# create a JS Object to store the value of each parameter
			#signature = ', '.join(map(lambda x: '%s=%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
			#writer.write('__sig__ = JSObject(%s)' % signature)
			signature = ', '.join(map(lambda x: '%s:%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
			writer.write('__sig__ = {%s}' % signature)

			writer.write('__args__ = get_arguments(__sig__, args, kwargs)')
			# # then for each argument assign its value
			for arg in node.args.args:
				writer.write("""JS("var %s = __args__['%s']")""" % (arg.id, arg.id))
			if node.args.vararg:
				writer.write("""JS("var %s = __args__['%s']")""" % (node.args.vararg, node.args.vararg))
			if node.args.kwarg:
				writer.write("""JS('var %s = __args__["%s"]')""" % (node.args.kwarg, node.args.kwarg))
		else:
			log('(function has no arguments)')

		################# function body #################
		if self._cached_property:
			writer.write('if self["__dict__"]["%s"]: return self["__dict__"]["%s"]' %(self._cached_property, self._cached_property))


		self._return_type = None # tries to catch a return type in visit_Return

		map(self.visit, node.body)  ## write function body

		if self._return_type:       ## check if a return type was caught
			if return_type:
				assert return_type == self._return_type
			else:
				return_type = self._return_type
			self._function_return_types[ node.name ] = self._return_type
		self._return_type = None

		if setter and 'set' in self._injector:  ## inject extra code
			value_name = node.args.args[1].id
			inject = [
				'if self.property_callbacks["%s"]:' %prop_name,
				'self.property_callbacks["%s"](["%s", %s, self], JSObject())' %(prop_name, prop_name, value_name)
			]
			writer.write( ' '.join(inject) )

		elif self._injector and node.original_name == '__init__':
			if 'set' in self._injector:
				writer.write( 'self.property_callbacks = JSObject()' )
			if 'init' in self._injector:
				writer.write('if self.__class__.init_callbacks.length:')
				writer.push()
				writer.write('for callback in self.__class__.init_callbacks:')
				writer.push()
				writer.write('callback( [self], JSObject() )')
				writer.pull()
				writer.pull()

		writer.pull()

		if inline:
			self._with_inline = False

		if self._in_js_class:
			return


		types = []
		for x in zip(node.args.args[-len(node.args.defaults):], node.args.defaults):
			key = x[0]
			value = x[1]
			if isinstance(value, ast.Name):
				value = value.id
			else:
				value = type(value).__name__.lower()
			types.append( '%s : "%s"' %(self.visit(key), value) )


		if not self._with_dart and not self._with_lua:  ## Dart functions can not have extra attributes?
			## note, in javascript function.name is a non-standard readonly attribute,
			## the compiler creates anonymous functions with name set to an empty string.
			writer.write('%s.NAME = "%s"' %(node.name,node.name))

			writer.write( '%s.args_signature = [%s]' %(node.name, ','.join(['"%s"'%n.id for n in node.args.args])) )
			defaults = ['%s:%s'%(self.visit(x[0]), self.visit(x[1])) for x in zip(node.args.args[-len(node.args.defaults):], node.args.defaults) ]
			writer.write( '%s.kwargs_signature = {%s}' %(node.name, ','.join(defaults)) )
			if self._with_fastdef or fastdef:
				writer.write('%s.fastdef = True' %node.name)

			writer.write( '%s.types_signature = {%s}' %(node.name, ','.join(types)) )

			if return_type:
				writer.write('%s.return_type = "%s"'%(node.name, return_type))

			if not self._with_js and not javascript:
				writer.write('%s.pythonscript_function=True'%node.name)


		if self._with_js and with_js_decorators:
			for dec in with_js_decorators:
				if '.prototype.' in dec:
					## these with-js functions are assigned to a some objects prototype,
					## here we assume that they depend on the special "this" variable,
					## therefore this function can not be marked as f.pythonscript_function,
					## because we need __get__(f,'__call__') to dynamically bind "this"
					writer.write( '%s=%s'%(dec,node.name) )
				else:  ## TODO fix with-javascript decorators
					writer.write( '%s = __get__(%s,"__call__")( [%s], {} )' %(node.name, dec, node.name))



		# apply decorators
		for decorator in decorators:
			assert not self._with_js
			dec = self.visit(decorator)
			if dec == 'classmethod':
				writer.write( '%s.is_classmethod = True' %node.name)
			elif dec == 'staticmethod':
				writer.write( '%s.is_staticmethod = True' %node.name)
				writer.write( '%s.is_wrapper = True' %node.name)
			else:
				writer.write('%s = __get__(%s,"__call__")( [%s], JSObject() )' % (node.name, dec, node.name))

	#################### loops ###################
	## the old-style for loop that puts a while loop inside a try/except and catches StopIteration,
	## has a problem because at runtime if there is an error inside the loop, it will not show up in a strack trace,
	## the error is slient.  FAST_FOR is safer and faster, although it is not strictly Python because in standard
	## Python a list is allowed to grow or string while looping over it.  FAST_FOR only deals with a fixed size thing to loop over.
	FAST_FOR = True

	def visit_Continue(self, node):
		if self._with_js:
			writer.write('continue')
		else:
			writer.write('continue')
		return ''

	def visit_Break(self, node):
		writer.write('break')

	def visit_For(self, node):
		log('for loop:')
		if self._cache_for_body_calls:  ## TODO add option for this
			for n in node.body:
				calls = collect_calls(n)
				for c in calls:
					log('--call: %s' %c)
					log('------: %s' %c.func)
					if isinstance(c.func, ast.Name):  ## these are constant for sure
						i = self._call_ids
						writer.write( '''JS('var __call__%s = __get__(%s,"__call__")')''' %(i,self.visit(c.func)) )
						c.func.id = '__call__%s'%i
						c.constant = True
						self._call_ids += 1

		target = node.target
		enumtar = None
		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, Name) and node.iter.func.id == 'enumerate':
			iter = node.iter.args[0]
			if isinstance(target, ast.Tuple):
				enumtar = target.elts[0]
				target = target.elts[1]
		else:
			iter = node.iter

		if enumtar:
			writer.write('var(%s)'%enumtar.id)
			writer.write('%s = 0' %enumtar.id)

		vars = []
		multi_target = []

		if isinstance(target, ast.Tuple):
			vars.append( '__mtarget__')
			for elt in target.elts:
				if isinstance(elt, ast.Name):
					multi_target.append( elt.id )
					vars.append( elt.id )
				else:
					raise NotImplementedError('unknown iterator sub-target type: %s'%target)
		elif isinstance(target, ast.Name):
			vars.append( target.id )
		else:
			raise NotImplementedError('unknown iterator target type: %s'%target)


		if self._with_ll:
			writer.write('for %s in %s:' %(self.visit(target), self.visit(iter)))
			writer.push()
			map(self.visit, node.body)
			writer.pull()

		elif self._with_js or self._with_dart:
			if isinstance(iter, ast.Call) and isinstance(iter.func, Name) and iter.func.id in ('range','xrange'):
				iter_start = '0'
				if len(iter.args) == 2:
					iter_start = self.visit(iter.args[0])
					iter_end = self.visit(iter.args[1])
				else:
					iter_end = self.visit(iter.args[0])

				iter_name = target.id
				writer.write('var(%s)' %iter_name)
				writer.write('%s = %s' %(iter_name, iter_start))
				writer.write('while %s < %s:' %(iter_name, iter_end))
				writer.push()
				map(self.visit, node.body)
				writer.write('%s += 1' %iter_name )

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()

			elif isinstance(iter, ast.Call) and isinstance(iter.func, Name) and iter.func.id in self._generator_functions:
				iter_name = self.visit(target)
				writer.write('var(%s, __generator__)' %iter_name)
				writer.write('__generator__ = %s' %self.visit(iter))
				writer.write('while __generator__.__done__ != 1:')
				writer.push()
				writer.write('%s = __generator__.next()'%iter_name)
				map(self.visit, node.body)
				writer.pull()

			else:
				if multi_target:
					writer.write('var(%s)' % ','.join(vars))
					writer.write('for %s in %s:' %('__mtarget__',self.visit(iter)))
					writer.push()
					for i,elt in enumerate(multi_target):
						writer.write('%s = __mtarget__[%s]' %(elt,i))

				else:
					writer.write('for %s in %s:' %(self.visit(target),self.visit(iter)))
					writer.push()


				map(self.visit, node.body)

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()
		else:

			## TODO else remove node.target.id from self._instances
			if isinstance(iter, Name) and iter.id in self._global_typed_lists:
				self._instances[ target.id ] = list( self._global_typed_lists[ iter.id ] )[0]

			vars.append('__iterator__')  ## TODO - test nested for loops - this should be __iterator__N
			if not self._with_coffee:
				writer.write('var(%s)' % ','.join(vars))


			is_range = False
			is_generator = False
			iter_start = '0'
			iter_end = None
			if self.FAST_FOR and isinstance(iter, ast.Call) and isinstance(iter.func, Name) and iter.func.id in ('range','xrange'):
				is_range = True
				if len(iter.args) == 2:
					iter_start = self.visit(iter.args[0])
					iter_end = self.visit(iter.args[1])
				else:
					iter_end = self.visit(iter.args[0])

			elif isinstance(iter, ast.Call) and isinstance(iter.func, Name) and iter.func.id in self._generator_functions:
				is_generator = True
			else:
				writer.write('__iterator__ = __get__(__get__(%s, "__iter__"), "__call__")(JSArray(), JSObject())' % self.visit(iter))

			if is_generator:
				iter_name = self.visit(target)
				if not self._with_coffee:
					writer.write('var(%s, __generator__)' %iter_name)
				writer.write('__generator__ = %s' %self.visit(iter))
				writer.write('while __generator__.__done__ != 1:')
				writer.push()
				writer.write('%s = __generator__.next()'%iter_name)
				map(self.visit, node.body)
				writer.pull()


			elif is_range:
				iter_name = target.id
				if not self._with_coffee:
					writer.write('var(%s)' %iter_name)
				writer.write('%s = %s' %(iter_name, iter_start))
				writer.write('while %s < %s:' %(iter_name, iter_end))
				writer.push()
				map(self.visit, node.body)
				if self._with_lua:
					writer.write('%s = %s + 1' %(iter_name, iter_name) )
				else:
					writer.write('%s += 1' %iter_name )

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()
			else:
				if not self._with_coffee:
					writer.write('var(__next__)')
				writer.write('__next__ = __get__(__iterator__, "next_fast")')
				writer.write('while __iterator__.index < __iterator__.length:')

				writer.push()

				if multi_target:
					writer.write('__mtarget__ = __next__()')
					for i,elt in enumerate(multi_target):
						if self._with_lua:
							writer.write('%s = __mtarget__[...][%s]' %(elt,i+1))
						else:
							writer.write('%s = __mtarget__[%s]' %(elt,i))
				else:
					writer.write('%s = __next__()' % target.id)

				map(self.visit, node.body)

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()
	
			return ''

	_call_ids = 0
	def visit_While(self, node):
		log('while loop:')
		if self._cache_while_body_calls:  ## TODO add option for this
			for n in node.body:
				calls = collect_calls(n)
				for c in calls:
					log('--call: %s' %c)
					log('------: %s' %c.func)
					if isinstance(c.func, ast.Name):  ## these are constant for sure
						i = self._call_ids
						writer.write( '__call__%s = __get__(%s,"__call__")' %(i,self.visit(c.func)) )
						c.func.id = '__call__%s'%i
						c.constant = True
						self._call_ids += 1


		writer.write('while %s:' % self.visit(node.test))
		writer.push()
		map(self.visit, node.body)
		writer.pull()

	def visit_With(self, node):
		if isinstance( node.context_expr, Name ) and node.context_expr.id == 'lowlevel':
			self._with_ll = True
			map(self.visit, node.body)
			self._with_ll = False
		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'javascript':
			self._with_js = True
			writer.with_javascript = True
			map(self.visit, node.body)
			writer.with_javascript = False
			self._with_js = False
		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'python':
			if not self._with_js:
				raise SyntaxError('"with python:" is only used inside of a "with javascript:" block')
			self._with_js = False
			writer.with_javascript = False
			map(self.visit, node.body)
			writer.with_javascript = True
			self._with_js = True

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'fastdef':
			self._with_fastdef = True
			map(self.visit, node.body)
			self._with_fastdef = False

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'static':
			self._with_static_type = True
			map(self.visit, node.body)
			self._with_static_type = False

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'inline':
			self._with_inline = True
			map(self.visit, node.body)
			self._with_inline = False

		elif isinstance( node.context_expr, Name ) and node.optional_vars and isinstance(node.optional_vars, Name) and node.optional_vars.id == 'jsobject':
			#instance_name = node.context_expr.id
			#for n in node.body:
			#    if isinstance(n, ast.Expr) and isinstance(n.value, Name):
			#        attr_name = n.value.id
			#        writer.write('%s.%s = __get__(%s, "%s")'%(instance_name, attr_name, instance_name, attr_name))
			#    else:
			#        raise SyntaxError('invalid statement inside of "with x as jsobject:" block')
			raise SyntaxError('"with x as jsobject:" is DEPRECATED - methods on instances are now callable by default from JavaScript')

		else:
			raise SyntaxError('improper use of "with" statement')


class GeneratorFunctionTransformer( PythonToPythonJS ):
	'''
	Translates a simple generator function into a class with state-machine that can be iterated over by
	calling its next method.

	A `simple generator` is one with no more than three yield statements, and a single for loop:
		. the first yield comes before the for loop
		. the second yield is the one inside the loop
		. the third yield comes after the for loop

	'''
	def __init__(self, node, compiler=None):
		self._with_ll = False
		self._with_js = False
		self._with_dart = False
		self._with_coffee = False
		self._with_lua = False
		if compiler._with_dart:  ## TODO
			self._with_dart = True
		elif compiler._with_coffee:
			self._with_coffee = True
		elif compiler._with_lua:
			self._with_lua = True
		else:
			self._with_js = True

		self._builtin_functions = compiler._builtin_functions
		self._js_classes = compiler._js_classes
		self._global_functions = compiler._global_functions
		self._with_inline = False
		self._cache_for_body_calls = False
		self._source = compiler._source
		self._instances = dict()
		self._head_yield = False
		self.visit( node )

	def visit_Yield(self, node):
		if self._in_head:
			writer.write('this.__head_yield = %s'%self.visit(node.value))
			writer.write('this.__head_returned = 0')
			self._head_yield = True
		else:
			writer.write('__yield_return__ = %s'%self.visit(node.value))

	def visit_Name(self, node):
		return 'this.%s' %node.id

	def visit_FunctionDef(self, node):
		args = [a.id for a in node.args.args]
		writer.write('def %s(%s):' %(node.name, ','.join(args)))
		writer.push()
		for arg in args:
			writer.write('this.%s = %s'%(arg,arg))

		self._in_head = True
		loop_node = None
		tail_yield = []
		for b in node.body:
			if loop_node:
				tail_yield.append( b )

			elif isinstance(b, ast.For):
				iter_start = '0'
				iter = b.iter
				if isinstance(iter, ast.Call) and isinstance(iter.func, Name) and iter.func.id in ('range','xrange'):
					if len(iter.args) == 2:
						iter_start = self.visit(iter.args[0])
						iter_end = self.visit(iter.args[1])
					else:
						iter_end = self.visit(iter.args[0])
				else:
					iter_end = self.visit(iter)

				writer.write('this.__iter_start = %s'%iter_start)
				writer.write('this.__iter_index = %s'%iter_start)
				writer.write('this.__iter_end = %s'%iter_end)
				writer.write('this.__done__ = 0')
				loop_node = b
				self._in_head = False

			else:
				self.visit(b)

		writer.pull()

		writer.write('@%s.prototype'%node.name)
		writer.write('def next():')
		writer.push()

		if self._head_yield:
			writer.write('if this.__head_returned == 0:')
			writer.push()
			writer.write('this.__head_returned = 1')
			writer.write('return this.__head_yield')
			writer.pull()
			writer.write('elif this.__iter_index < this.__iter_end:')

		else:
			writer.write('if this.__iter_index < this.__iter_end:')

		writer.push()
		for b in loop_node.body:
			self.visit(b)

		if self._with_lua:
			writer.write('this.__iter_index = this.__iter_index + 1')
		else:
			writer.write('this.__iter_index += 1')

		if not tail_yield:
			writer.write('if this.__iter_index == this.__iter_end: this.__done__ = 1')

		writer.write('return __yield_return__')
		writer.pull()
		writer.write('else:')
		writer.push()
		writer.write('this.__done__ = 1')
		if tail_yield:
			for b in tail_yield:
				self.visit(b)
			writer.write('return __yield_return__')
		writer.pull()
		writer.pull()


class CollectCalls(NodeVisitor):
	_calls_ = []
	def visit_Call(self, node):
		self._calls_.append( node )

def collect_calls(node):
	CollectCalls._calls_ = calls = []
	CollectCalls().visit( node )
	return calls

class CollectNames(NodeVisitor):
	_names_ = []
	def visit_Name(self, node):
		self._names_.append( node )

def collect_names(node):
	CollectNames._names_ = names = []
	CollectNames().visit( node )
	return names

class CollectReturns(NodeVisitor):
	_returns_ = []
	def visit_Return(self, node):
		self._returns_.append( node )

def collect_returns(node):
	CollectReturns._returns_ = returns = []
	CollectReturns().visit( node )
	return returns

class CollectComprehensions(NodeVisitor):
	_comps_ = []
	def visit_GeneratorExp(self,node):
		self._comps_.append( node )		
		self.visit( node.elt )
		for gen in node.generators:
			self.visit( gen.iter )
			self.visit( gen.target )
	def visit_ListComp(self, node):
		self._comps_.append( node )
		self.visit( node.elt )
		for gen in node.generators:
			self.visit( gen.iter )
			self.visit( gen.target )

def collect_comprehensions(node):
	CollectComprehensions._comps_ = comps = []
	CollectComprehensions().visit( node )
	return comps

class CollectGenFuncs(NodeVisitor):
	_funcs = []
	_genfuncs = []
	def visit_FunctionDef(self, node):
		self._funcs.append( node )
		node._yields = []
		node._loops = []
		for b in node.body:
			self.visit(b)
		self._funcs.pop()

	def visit_Yield(self, node):
		func = self._funcs[-1]
		func._yields.append( node )
		if func not in self._genfuncs:
			self._genfuncs.append( func )

	def visit_For(self, node):
		if len(self._funcs):
			self._funcs[-1]._loops.append( node )
		for b in node.body:
			self.visit(b)

	def visit_While(self, node):
		if len(self._funcs):
			self._funcs[-1]._loops.append( node )
		for b in node.body:
			self.visit(b)


def collect_generator_functions(node):
	CollectGenFuncs._funcs = []
	CollectGenFuncs._genfuncs = gfuncs = []
	CollectGenFuncs().visit( node )
	return gfuncs

def retrieve_vars(body):
	local_vars = set()
	global_vars = set()
	for n in body:
		if isinstance(n, Assign) and isinstance(n.targets[0], Name):  ## assignment to local - TODO support `a=b=c`
			local_vars.add( n.targets[0].id )
		elif isinstance(n, Assign) and isinstance(n.targets[0], ast.Tuple):
			for c in n.targets[0].elts:
				local_vars.add( c.id )
		elif isinstance(n, Global):
			global_vars.update( n.names )
		elif hasattr(n, 'body') and not isinstance(n, FunctionDef):
			# do a recursive search inside new block except function def
			l, g = retrieve_vars(n.body)
			local_vars.update(l)
			global_vars.update(g)
			if hasattr(n, 'orelse'):
				l, g = retrieve_vars(n.orelse)
				local_vars.update(l)
				global_vars.update(g) 

	return local_vars, global_vars

def retrieve_properties(body):
	props = set()
	for n in body:
		if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Attribute) and isinstance(n.targets[0].value, ast.Name) and n.targets[0].value.id == 'self':
			props.add( n.targets[0].attr )
		elif hasattr(n, 'body') and not isinstance(n, FunctionDef):
			props.update( retrieve_properties(n.body) )
	return props
	
def inspect_function( node ):
	local_vars, global_vars = retrieve_vars(node.body)
	local_vars = local_vars - global_vars
	for arg in node.args.args:
		local_vars.add( arg.id )
	names = []
	returns = []
	for n in node.body:
		names.extend( collect_names(n) )
		returns.extend( collect_returns(n) )

	typedefs = {}
	for decorator in node.decorator_list:
		if isinstance(decorator, Call) and decorator.func.id == 'typedef':
			c = decorator
			assert len(c.args) == 0 and len(c.keywords)
			for kw in c.keywords:
				assert isinstance( kw.value, Name)
				typedefs[ kw.arg ] = kw.value.id

	info = {
		'locals':local_vars, 
		'globals':global_vars, 
		'name_nodes':names, 
		'return_nodes':returns,
		'typedefs': typedefs
	}
	return info

def inspect_method( node ):
	info = inspect_function( node )
	info['properties'] = retrieve_properties( node.body )
	return info

def main(script):
	PythonToPythonJS( source=script, dart='--dart' in sys.argv )
	return writer.getvalue()


def command():
	module = None
	module_path = gettempdir()
	scripts = []
	if len(sys.argv) > 1:
		argv = sys.argv[1:]
		for i,arg in enumerate(argv):
			if arg.endswith('.py'):
				scripts.append( arg )
				module = arg.split('.')[0]
			elif i > 0:
				if argv[i-1] == '--module':
					module = arg

	if len(scripts):
		a = []
		for script in scripts:
			a.append( open(script, 'rb').read() )
		data = '\n'.join( a )
	else:
		data = sys.stdin.read()


	compiler = PythonToPythonJS(
		source=data, 
		module=module, 
		module_path=module_path,
		dart='--dart' in sys.argv
	)
	compiler.save_module()
	output = writer.getvalue()
	print( output )  ## pipe to stdout


if __name__ == '__main__':
	command()

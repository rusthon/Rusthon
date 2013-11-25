#!/usr/bin/env python
# Python to PythonJS Translator
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

import os, sys, pickle, copy
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

try:
	_log_file = open('/tmp/python_to_pythonjs.log', 'wb')
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
		self.buffers = list()
		self.output = StringIO()
		self.with_javascript = False

	def is_at_global_level(self):
		return self.level == 0

	def push(self):
		self.level += 1

	def pull(self):
		self.level -= 1

	def append(self, code):
		self.buffers.append(code)

	def write(self, code):
		for buffer in self.buffers:
			self._write(buffer)
		self.buffers = list()
		self._write(code)

	def _write(self, code):
		indentation = self.level * 4 * ' '
		if self.with_javascript:
			if not code.endswith(':'):  ## will this rule always catch: while, and if/else blocks?
				if not code.startswith('print '):
					if not code.startswith('var('):
						if not code == 'pass':
							if not code.startswith('JS('):
								code = """JS('''%s''')"""%code
		s = '%s%s\n' % (indentation, code)
		#self.output.write(s.encode('utf-8'))
		self.output.write(s)

	def getvalue(self):
		s = self.output.getvalue()
		self.output = StringIO()
		return s

writer = Writer()

MINI_STDLIB = {
	'time': {
		'time': 'function time() { return new Date().getTime() / 1000.0; }',
		'clock': 'function clock() { return new Date().getTime() / 1000.0; }'
	},
	'random': {
		'random': 'var random = Math.random'
	}
}

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

	def __init__(self, module=None, module_path=None):
		super(PythonToPythonJS, self).__init__()
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
		self._with_js = False
		self._typedefs = dict()  ## class name : typedef  (not pickled)

		self._globals = dict()
		self._with_static_type = None
		self._global_typed_lists = dict()  ## global name : set  (if len(set)==1 then we know it is a typed list)
		self._global_typed_dicts = dict()
		self._global_typed_tuples = dict()
		self._global_functions = dict()
		self._with_inline = False
		self._inline = []
		self._inline_ids = 0
		self._js_classes = dict()
		self._in_js_class = False

		self._cache_for_body_calls = False
		self._cache_while_body_calls = False

		self._custom_operators = {}
		self._injector = []  ## advanced meta-programming hacks
		self._in_class = None
		self._with_fastdef = False
		self.setup_builtins()

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
		self._classes['list'] = set(['__getitem__', '__setitem__'])
		self._classes['tuple'] = set(['__getitem__', '__setitem__'])
		self._builtin_classes = set(['dict', 'list', 'tuple'])
		self._builtin_functions = {
			'ord':'%s.charCodeAt(0)', 
			'chr':'String.fromCharCode(%s)',
			'abs':'Math.abs(%s)'
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
			raise NotImplementedError  ## TODO namespaces: import x as y

	def visit_ImportFrom(self, node):
		if node.module in MINI_STDLIB:
			for n in node.names:
				if n.name in MINI_STDLIB[ node.module ]:
					writer.write( 'JS("%s")' %MINI_STDLIB[node.module][n.name] )
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
		#keys = [x.s for x in node.keys]
		#values = map(self.visit, node.values)
		#a = [ '%s=%s'%x for x in zip(keys, values) ]
		#b = 'JSObject(%s)' %', '.join(a)
		#return '__get__(dict, "__call__")([], JSObject(js_object=%s))' %b
		a = []
		for i in range( len(node.keys) ):
			k = self.visit( node.keys[ i ] )
			v = self.visit( node.values[i] )
			if self._with_js:
				a.append( '%s:%s'%(k,v) )
			else:
				a.append( 'JSObject(key=%s, value=%s)'%(k,v) )
		if self._with_js:
			b = ','.join( a )
			return '{ %s }' %b
		else:
			b = '[%s]' %', '.join(a)
			return '__get__(dict, "__call__")([], JSObject(js_object=%s))' %b

	def visit_Tuple(self, node):
		node.returns_type = 'tuple'
		a = '[%s]' % ', '.join(map(self.visit, node.elts))
		return '__get__(tuple, "__call__")([], {js_object:%s})' %a

	def visit_List(self, node):
		node.returns_type = 'list'
		a = '[%s]' % ', '.join(map(self.visit, node.elts))
		if self._with_js:
			return a
		else:
			return '__get__(list, "__call__")([], JSObject(js_object=%s))' %a

	def visit_ListComp(self, node):
		node.returns_type = 'list'
		writer.write('var(__comprehension__)')
		writer.write('__comprehension__ = JSArray()')

		length = len( node.generators )
		a = ['idx%s'%i for i in range(length)]
		writer.write('var( %s )' %','.join(a) )
		a = ['iter%s'%i for i in range(length)]
		writer.write('var( %s )' %','.join(a) )
		a = ['get%s'%i for i in range(length)]
		writer.write('var( %s )' %','.join(a) )

		generators = list( node.generators )
		self._gen_comp( generators, node )

		return '__get__(list, "__call__")([], JSObject(js_object=__comprehension__))'


	def _gen_comp(self, generators, node):
		gen = generators.pop()
		if len(gen.ifs): raise NotImplementedError  ## TODO
		id = len(generators)
		assert isinstance(gen.target, Name)
		writer.write('idx%s = 0'%id)
		writer.write('iter%s = %s' %(id, self.visit(gen.iter)) )
		writer.write('get%s = __get__(iter%s, "__getitem__")'%(id,id) )
		writer.write('while idx%s < __get__(len, "__call__")([iter%s], JSObject()):' %(id,id) )
		writer.push()

		writer.write('var(%s)'%gen.target.id)
		writer.write('%s=get%s( [idx%s], JSObject() )' %(gen.target.id, id,id) )

		if generators:
			self._gen_comp( generators, node )
		else:
			writer.write('__comprehension__.push( %s )' %self.visit(node.elt) )

		writer.write('idx%s+=1' %id )
		writer.pull()

	def visit_In(self, node):
		return ' in '

	def visit_NotIn(self, node):
		#return ' not in '
		raise RuntimeError('"not in" is only allowed in if-test: see method - visit_Compare')

	def visit_AugAssign(self, node):
		target = self.visit( node.target )
		op = '%s=' %self.visit( node.op )

		typedef = self.get_typedef( node.target )
		if typedef and op in typedef.operators:
			func = typedef.operators[ op ]
			a = '%s( [%s, %s] )' %(func, target, self.visit(node.value))
			writer.write( a )
		else:
			## TODO extra checks to make sure the operator type is valid in this context
			a = '%s %s %s' %(target, op, self.visit(node.value))
			writer.write(a)

	def visit_Yield(self, node):
		return 'yield %s' % self.visit(node.value)

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

		init = methods.pop('__init__')
		args = [self.visit(arg) for arg in init.args.args]

		writer.write('def %s(%s):' %(name,','.join(args)))
		writer.push()
		for b in init.body:
			line = self.visit(b)
			if line: writer.write( line )

		#for mname in methods:
		#	method = methods[mname]
		#	line = self.visit(method)
		#	if line: writer.write( line )
		#	writer.write('this.%s = %s'%(mname,mname))

		writer.pull()

		for mname in methods:
			method = methods[mname]
			line = self.visit(method)
			if line: writer.write( line )
			writer.write('%s.prototype.%s = %s'%(name,mname,mname))

		self._in_js_class = False

	def visit_ClassDef(self, node):
		if self._with_js:
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


		writer.write('var(%s, __%s_attrs, __%s_parents)' % (name, name, name))
		writer.write('__%s_attrs = JSObject()' % name)
		writer.write('__%s_parents = JSArray()' % name)
		writer.write('__%s_properties = JSObject()' % name)

		for base in node.bases:
			code = '__%s_parents.push(%s)' % (name, self.visit(base))
			writer.write(code)
			self._class_parents[ name ].add( self.visit(base) )

		for item in node.body:
			if isinstance(item, FunctionDef):
				log('  method: %s'%item.name)

				#if item.name == '__contains__':  ## this is required because we added Object.prototype.__contains__ - DEPRECATED!
				#    item.name = item.name.upper()

				self._classes[ name ].append( item.name )
				item_name = item.name
				item.original_name = item.name
				item.name = '__%s_%s' % (name, item_name)

				self.visit(item)  # this will output the code for the function

				if item_name in self._decorator_properties:
					pass
				else:
					writer.write('__%s_attrs["%s"] = %s' % (name, item_name, item.name))

			elif isinstance(item, Assign) and isinstance(item.targets[0], Name):
				item_name = item.targets[0].id
				item.targets[0].id = '__%s_%s' % (name, item_name)
				self.visit(item)  # this will output the code for the assign
				writer.write('__%s_attrs["%s"] = %s' % (name, item_name, item.targets[0].id))
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
						writer.write('__%s_attrs["%s"] = %s' % (name, item_name, sub.targets[0].id))
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

		writer.write('%s = create_class("%s", __%s_parents, __%s_attrs, __%s_properties)' % (name, name, name, name, name))
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
		if self._with_js:
			if node.id == 'True':
				return 'true'
			elif node.id == 'False':
				return 'false'
			elif node.id == 'None':
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
					writer.write('break')
				else:
					writer.write('return %s' % self.visit(node.value))

		else:
			if self._inline:
				writer.write('break')
				pass  ## TODO put inline inside a while loop that iterates once? and use `break` here to exit early?
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
			return '__sprintf( %s, %s[...] )' %(left, right)  ## assumes that right is a tuple, or list.

		elif op == '*' and isinstance(node.left, ast.List) and isinstance(node.right,ast.Num):
			elts = [ self.visit(e) for e in node.left.elts ]
			expanded = []
			for i in range( node.right.n ): expanded.extend( elts )
			return '__get__(list, "__call__")( [], {pointer:[%s]} )' %','.join(expanded)

		elif isinstance(node.left, Name):
			typedef = self.get_typedef( node.left )
			if typedef and op in typedef.operators:
				func = typedef.operators[ op ]
				node.operator_overloading = func
				return '%s( [%s, %s], JSObject() )' %(func, left, right)


		return '%s %s %s' % (left, op, right)

	def visit_Eq(self, node):
		return '=='

	def visit_NotEq(self, node):
		return '!='

	def visit_Is(self, node):
		return 'is'

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
				if self._with_js:
					## this makes "if 'x' in Array" work like Python: "if 'x' in list" - TODO fix this for js-objects
					## note javascript rules are confusing: "1 in [1,2]" is true, this is because a "in test" in javascript tests for an index
					## TODO double check this code
					comp.append( '%s in %s or' %(a[1], a[0]) )  ## this is ugly, will break with Arrays
					comp.append( 'Object.hasOwnProperty.call(%s, "__contains__") and' %a[0])
					comp.append( "%s['__contains__'](%s)" %a )
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

		if self._with_js:
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


			elif node.attr in typedef.class_attributes and not typedef.check_for_parent_with( class_attribute=node.attr ) and node_value != 'self':
				## This optimization breaks when a subclass redefines a class attribute,
				## but we need it for inplace assignment operators, this is safe only when
				## other parent classes have not defined the same class attribute.
				## This is also not safe when node_value is "self".
				return "%s['__class__']['%s']" %(node_value, node.attr)

			elif node.attr in typedef.attributes:
				return "%s.%s" %(node_value, node.attr)

			elif '__getattr__' in typedef.methods:
				func = typedef.get_pythonjs_function_name( '__getattr__' )
				return '%s([%s, "%s"], JSObject())' %(func, node_value, node.attr)

			elif typedef.check_for_parent_with( property=node.attr ):
				parent = typedef.check_for_parent_with( property=node.attr )
				getter = parent.properties[ node.attr ]['get']
				if getter in self._function_return_types:
					node.returns_type = self._function_return_types[getter]
				return '%s( [%s], JSObject() )' %(getter, node_value)

			elif typedef.check_for_parent_with( class_attribute=node.attr ):
				#return '__get__(%s, "%s")' % (node_value, node.attr)  ## __get__ is broken with grandparent class attributes - TODO double check and fix this
				if node.attr in typedef.class_attributes:
					## this might not be always correct
					return "%s['__class__']['%s']" %(node_value, node.attr)
				else:
					parent = typedef.check_for_parent_with( class_attribute=node.attr )
					return "__%s_attrs['%s']" %(parent.name, node.attr)  ## TODO, get from class.__dict__

			elif typedef.check_for_parent_with( method='__getattr__' ):
				parent = typedef.check_for_parent_with( method='__getattr__' )
				func = parent.get_pythonjs_function_name( '__getattr__' )
				return '%s([%s, "%s"], JSObject())' %(func, node_value, node.attr)

			else:
				return '__get__(%s, "%s")' % (node_value, node.attr)  ## TODO - this could be a builtin class like: list, dict, etc.
		else:
			return '__get__(%s, "%s")' % (node_value, node.attr)      ## TODO - double check this


	def visit_Index(self, node):
		return self.visit(node.value)

	def visit_Subscript(self, node):
		name = self.visit(node.value)

		if isinstance(node.slice, ast.Ellipsis):
			return '%s["$wrapped"]' %name

		elif self._with_js:
			if isinstance(node.slice, ast.Slice):
				raise SyntaxError
			return '%s[ %s ]' %(name, self.visit(node.slice))

		elif isinstance(node.slice, ast.Slice):
			return '__get__(%s, "__getslice__")([%s], JSObject())' % (
				self.visit(node.value),
				self.visit(node.slice),
			)

		elif name in self._func_typedefs and self._func_typedefs[name] == 'list':
			return '%s[...][%s]'%(name, self.visit(node.slice))

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
		lower = upper = step = None
		if node.lower:
			lower = self.visit(node.lower)
		if node.upper:
			upper = self.visit(node.upper)
		if node.step:
			step = self.visit(node.step)
		return "%s, %s, %s" % (lower, upper, step)

	def visit_Assign(self, node):
		# XXX: support only one target for subscripts
		target = node.targets[0]
		if isinstance(target, Subscript):
			name = self.visit(target.value)  ## target.value may have "returns_type" after being visited

			if isinstance(target.slice, ast.Ellipsis):
				code = '%s["$wrapped"] = %s' %(self.visit(target.value), self.visit(node.value))

			elif self._with_js:
				code = '%s[ %s ] = %s'
				code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))

			elif name in self._func_typedefs and self._func_typedefs[name] == 'list':
				code = '%s[...][%s] = %s'%(name, self.visit(target.slice.value), self.visit(node.value))

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

			if self._with_js:
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

				elif parent_classattr:  ## TODO fix get/set class attributes
					writer.write( "__%s_attrs['%s'] = %s" %(parent_classattr.name, target.attr, self.visit(node.value)) )

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

					writer.write('%s = %s' % (target.id, node_value))
				else:
					if target.id in self._globals and self._globals[target.id] is None:
						self._globals[target.id] = type
						self._instances[ target.id ] = type
						log('set global type: %s'%type)

					writer.write('%s = %s' % (target.id, node_value))
			else:
				writer.write('%s = %s' % (target.id, node_value))

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
				else:
					writer.write("%s = __get__(__get__(%s, '__getitem__'), '__call__')([%s], __NULL_OBJECT__)" % (target.id, r, i))

	def visit_Print(self, node):
		writer.write('print %s' % ', '.join(map(self.visit, node.values)))

	def visit_Str(self, node):
		s = node.s.replace('\n', '\\n').replace('\0', '\\0')
		if self._with_js:
			return '"%s"' %s
		else:
			if len(s) == 0:
				return '""'
			elif s.startswith('"') or s.endswith('"'):
				return "'''%s'''" %s
			else:
				return '"""%s"""' %s

	def visit_Expr(self, node):
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

		for i,a in enumerate(node.args):
			b = self.visit( fnode.args.args[i] )
			b = remap[ b ]
			writer.write( "%s = %s" %(b, self.visit(a)) )

		self._inline.append( name )

		writer.write("JS('var __returns__%s = null')"%name)
		writer.write('while True:')
		writer.push()
		for b in fnode.body:
			self.visit(b)
		if len( finfo['return_nodes'] ) == 0:
			writer.write('break')
		writer.pull()

		if self._inline.pop() != name:
			raise RuntimeError

		for n in remap:
			gname = remap[n]
			for n in finfo['name_nodes']:
				if n.id == gname:
					n.id = n
		log('###########inlined %s###########'%name)
		return '__returns__%s' %name

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

				elif kw.arg == 'inline':
					if kw.value.id == 'True':
						self._with_inline = True
					elif kw.value.id == 'False':
						self._with_inline = False
					else:
						raise SyntaxError

				else:
					raise SyntaxError

		elif self._with_js:
			name = self.visit(node.func)
			args = list( map(self.visit, node.args) )

			if name in self._builtin_functions and self._builtin_functions[name]:  ## inlined js
				if args:
					return self._builtin_functions[name] % ','.join(args)
				else:
					return self._builtin_functions[name]

			elif isinstance(node.func, Name) and node.func.id == 'new':
				assert len(args) == 1
				return ' new %s' %args[0]

			elif isinstance(node.func, Name) and node.func.id == 'JS':  ## avoids nested JS
				assert len(args) == 1
				return node.args[0].s  ## string literal

			elif isinstance(node.func, Name) and node.func.id in self._js_classes:
				a = ','.join(args)
				return ' new %s(%s)' %( self.visit(node.func), a )

			elif name in self._global_functions and self._with_inline:
				return self.inline_function( node )

			else:
				a = ','.join(args)
				return '%s(%s)' %( self.visit(node.func), a )

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

				if name in ('list', 'tuple'):
					if args:
						writer.append( '%s = %s[...]' % (args_name, args))  ## test this
					else:
						writer.append( '%s = []' %args_name )
				else:
					writer.append('%s = JSArray(%s)' % (args_name, args))

				if node.starargs:
					writer.append('%s.push.apply(%s, %s[...])' % (args_name, args_name, self.visit(node.starargs)))
				writer.append('%s = JSObject(%s)' % (kwargs_name, kwargs))

				if node.kwargs:
					kwargs = self.visit(node.kwargs)
					code = "JS('for (var name in %s) { %s[name] = %s[...][name]; }')" % (kwargs, kwargs_name, kwargs)
					writer.append(code)

			#######################################

			#if name in self._func_typedefs:
			#	if args and kwargs:
			#		return '%s(%s, %s)' %(args_name, kwargs_name)
			#	elif args:
			#		return '%s(%s, {})' %args_name
			#	elif kwargs:
			#		return '%s([], %s)' %kwargs_name
			#	else:
			#		return '%s()' %name

			if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id in self._func_typedefs:
				type = self._func_typedefs[ node.func.value.id ]
				if type == 'list' and node.func.attr == 'append':
					return '%s[...].push(%s)' %(node.func.value.id, self.visit(node.args[0]))
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
					return '__get__(%s, "__call__")(%s, JSObject(js_object=%s))' % (name, args_name, kwargs_name)
				elif name in ('list', 'tuple'):
					if len(node.args):
						return '__get__(%s, "__call__")([], {js_object:%s})' % (name, args_name)
					else:
						return '__get__(%s, "__call__")([], %s)' % (name, kwargs_name)
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
		if self._with_js:
			return '(function (%s) {return %s})' %(','.join(args), self.visit(node.body))
		else:
			return 'lambda %s: %s' %(','.join(args), self.visit(node.body))

	def visit_FunctionDef(self, node):
		property_decorator = None
		decorators = []
		with_js_decorators = []
		setter = False
		return_type = None
		fastdef = False
		javascript = False
		self._cached_property = None
		self._func_typedefs = {}

		if writer.is_at_global_level():
			self._global_functions[ node.name ] = node  ## save ast-node

		for decorator in reversed(node.decorator_list):
			log('@decorator: %s' %decorator)
			if self._with_js:  ## decorators are special in with-js mode
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

		log('function: %s'%node.name)
		if self._with_js or javascript:
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
		if not GLOBAL_VARIABLE_SCOPE:
			local_vars, global_vars = retrieve_vars(node.body)
			if local_vars-global_vars:
				a = ','.join( local_vars-global_vars )
				writer.write('var(%s)' %a)

		if self._with_js or javascript:
			if node.args.defaults:
				for i, arg in enumerate(node.args.args):
					dindex = i - len(node.args.defaults)
					if dindex >= 0:
						default_value = self.visit( node.args.defaults[dindex] )
						writer.write("""JS("var %s = %s  || %s ")""" % (arg.id, arg.id, default_value))


		elif self._with_fastdef or fastdef:
			for i, arg in enumerate(node.args.args):
				#dindex = i - len(node.args.defaults)  ## TODO - fixme
				#if dindex >= 0 and node.args.defaults:
				#	default_value = self.visit( node.args.defaults[dindex] )
				#	writer.write("""JS("var %s = kwargs[ '%s' ]  || %s ")""" % (arg.id, arg.id, default_value))
				#else:
				writer.write("""JS("var %s = args[ %s ]")""" % (arg.id, i))

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
			writer.write('var(signature, arguments)')

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
			signature = ', '.join(map(lambda x: '%s=%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
			writer.write('signature = JSObject(%s)' % signature)
			writer.write('arguments = get_arguments(signature, args, kwargs)')
			# # then for each argument assign its value
			for arg in node.args.args:
				writer.write("""JS("var %s = arguments['%s']")""" % (arg.id, arg.id))
			if node.args.vararg:
				writer.write("""JS("var %s = arguments['%s']")""" % (node.args.vararg, node.args.vararg))
				# turn it into a list
				expr = '%s = __get__(list, "__call__")(__create_array__(%s), {});'
				expr = expr % (node.args.vararg, node.args.vararg)
				writer.write(expr)
			if node.args.kwarg:
				writer.write("""JS('var %s = arguments["%s"]')""" % (node.args.kwarg, node.args.kwarg))
				expr = '%s = __get__(dict, "__call__")(__create_array__(%s), {});'
				expr = expr % (node.args.kwarg, node.args.kwarg)
				writer.write(expr)
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

		if self._in_js_class:
			return

		## note, in javascript function.name is a non-standard readonly attribute,
		## the compiler creates anonymous functions with name set to an empty string.
		writer.write('%s.NAME = "%s"' %(node.name,node.name))

		writer.write( '%s.args_signature = [%s]' %(node.name, ','.join(['"%s"'%n.id for n in node.args.args])) )
		defaults = ['%s:%s'%(self.visit(x[0]), self.visit(x[1])) for x in zip(node.args.args[-len(node.args.defaults):], node.args.defaults) ]
		writer.write( '%s.kwargs_signature = {%s}' %(node.name, ','.join(defaults)) )
		if self._with_fastdef or fastdef:
			writer.write('%s.fastdef = True' %node.name)

		#types = ['%s:%s'%(self.visit(x[0]), '"%s"'%type(self.visit(x[1])).__name__ ) for x in zip(node.args.args[-len(node.args.defaults):], node.args.defaults) ]
		types = []
		for x in zip(node.args.args[-len(node.args.defaults):], node.args.defaults):
			key = x[0]
			value = x[1]
			if isinstance(value, ast.Name):
				value = value.id
			else:
				value = type(value).__name__.lower()
			types.append( '%s : "%s"' %(self.visit(key), value) )

		writer.write( '%s.types_signature = {%s}' %(node.name, ','.join(types)) )
		if return_type:
			writer.write('%s.return_type = "%s"'%(node.name, return_type))

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


		if not self._with_js and not javascript:
			writer.write('%s.pythonscript_function=True'%node.name)

		# apply decorators
		for decorator in decorators:
			assert not self._with_js
			writer.write('%s = __get__(%s,"__call__")( [%s], JSObject() )' % (node.name, self.visit(decorator), node.name))

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
			if not self.FAST_FOR:
				writer.write('%s = __get__(__iterator__, "next")(JSArray(), JSObject())' % self._for_iterator_target)
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


		if self._with_js:
			if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, Name) and node.iter.func.id == 'range':
				iter_start = '0'
				if len(node.iter.args) == 2:
					iter_start = self.visit(node.iter.args[0])
					iter_end = self.visit(node.iter.args[1])
				else:
					iter_end = self.visit(node.iter.args[0])

				iter_name = node.target.id
				writer.write('var(%s)' %iter_name)
				writer.write('%s = %s' %(iter_name, iter_start))
				writer.write('while %s < %s:' %(iter_name, iter_end))
				writer.push()
				map(self.visit, node.body)
				writer.write('%s += 1' %iter_name )
				writer.pull()


			else:
				writer.write('for %s in %s:' %(self.visit(node.target),self.visit(node.iter)))
				writer.push()
				map(self.visit, node.body)
				writer.pull()
		else:

			## TODO else remove node.target.id from self._instances
			if isinstance(node.iter, Name) and node.iter.id in self._global_typed_lists:
				self._instances[ node.target.id ] = list( self._global_typed_lists[ node.iter.id ] )[0]

			self._for_iterator_target = node.target.id  ## this could break with nested for loops
			writer.write('var(__iterator__, %s)' % node.target.id)
	
			is_range = False
			iter_start = '0'
			iter_end = None
			if self.FAST_FOR and isinstance(node.iter, ast.Call) and isinstance(node.iter.func, Name) and node.iter.func.id == 'range':
				is_range = True
				if len(node.iter.args) == 2:
					iter_start = self.visit(node.iter.args[0])
					iter_end = self.visit(node.iter.args[1])
				else:
					iter_end = self.visit(node.iter.args[0])
			else:
				writer.write('__iterator__ = __get__(__get__(%s, "__iter__"), "__call__")(JSArray(), JSObject())' % self.visit(node.iter))

			if self.FAST_FOR:
				if is_range:
					iter_name = node.target.id
					#range_num = self.visit( node.iter.args[0] )
					writer.write('var(%s)' %iter_name)
					writer.write('%s = %s' %(iter_name, iter_start))
					writer.write('while %s < %s:' %(iter_name, iter_end))
					writer.push()
					map(self.visit, node.body)
					writer.write('%s += 1' %iter_name )
					writer.pull()
				else:
					writer.write('var(__next__)')
					writer.write('__next__ = __get__(__iterator__, "next_fast")')
					writer.write('while __iterator__.index < __iterator__.length:')
					writer.push()
					writer.write('%s = __next__()' % node.target.id)
					map(self.visit, node.body)
					writer.pull()

			else:
				writer.write('try:')
				writer.push()
				writer.write('%s = __get__(__iterator__, "next")(JSArray(), JSObject())' % node.target.id)
				writer.write('while True:')
				writer.push()
				map(self.visit, node.body)
				writer.write('%s = __get__(__iterator__, "next")(JSArray(), JSObject())' % node.target.id)
				writer.pull()
				writer.pull()
				writer.write('except StopIteration:')
				writer.push()
				writer.write('pass')
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
		if isinstance( node.context_expr, Name ) and node.context_expr.id == 'javascript':
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
		elif isinstance(n, With) and isinstance( n.context_expr, Name ) and n.context_expr.id == 'javascript':
			for c in n.body:
				if isinstance(c, Assign) and isinstance(c.targets[0], Name):  ## assignment to local
					local_vars.add( c.targets[0].id )
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



def main(script):
	input = parse(script)
	PythonToPythonJS().visit(input)
	return writer.getvalue()


def command():
	module = None
	module_path = '/tmp'
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


	compiler = PythonToPythonJS( module=module, module_path=module_path )

	data = compiler.preprocess_custom_operators( data )
	compiler.visit( parse(data) )

	compiler.save_module()
	output = writer.getvalue()
	print( output )  ## pipe to stdout


if __name__ == '__main__':
	command()

#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Python to PythonJS Translator
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

import os, sys, copy
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

import typedpython
import ministdlib
import inline_function
import code_writer
from ast_utils import *

## TODO
def log(txt):
	pass


POWER_OF_TWO = [ 2**i for i in range(32) ]

writer = writer_main = code_writer.Writer()

__webworker_writers = dict()
def get_webworker_writer( jsfile ):
	if jsfile not in __webworker_writers:
		__webworker_writers[ jsfile ] = code_writer.Writer()
	return __webworker_writers[ jsfile ]



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
		for name in kwargs.keys():  ## name, methods, properties, attributes, class_attributes, parents
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

class PythonToPythonJS(NodeVisitor, inline_function.Inliner):

	identifier = 0
	_func_typedefs = ()

	def format_error(self, node):
		lines = []
		if self._line_number > 0:
			lines.append( self._source[self._line_number-1] )
		lines.append( self._source[self._line_number] )
		if self._line_number+1 < len(self._source):
			lines.append( self._source[self._line_number+1] )

		msg = 'line %s\n%s\n%s\n' %(self._line_number, '\n'.join(lines), node)
		msg += 'Depth Stack:\n'
		for l, n in enumerate(self._stack):
			#msg += str(dir(n))
			msg += '%s%s line:%s col:%s\n' % (' '*(l+1)*2, n.__class__.__name__, n.lineno, n.col_offset)
                return msg

	def __init__(self, source=None, module=None, module_path=None, dart=False, coffee=False, lua=False, go=False):
		super(PythonToPythonJS, self).__init__()
		self._module_path = module_path  ## used for user `from xxx import *` to load .py files in the same directory.
		self._with_lua = lua
		self._with_coffee = coffee
		self._with_dart = dart
		self._with_go = go

		self._html_tail = []; script = False
		if source.strip().startswith('<html'):
			lines = source.splitlines()
			for line in lines:
				if line.strip().startswith('<script'):
					if 'type="text/python"' in line:
						writer.write( '<script type="text/python">')
						script = list()
					elif 'src=' in line and '~/' in line:  ## external javascripts installed in users home folder
						x = line.split('src="')[-1].split('"')[0]
						if os.path.isfile(os.path.expanduser(x)):
							o = []
							o.append( '<script type="text/javascript">' )
							if x.lower().endswith('.coffee'):
								import subprocess
								proc = subprocess.Popen(
									['coffee','--bare', '--print', os.path.expanduser(x)], 
									stdout=subprocess.PIPE
								)
								o.append( proc.stdout.read() )
							else:
								o.append( open(os.path.expanduser(x), 'rb').read() )
							o.append( '</script>')
							if script is True:
								self._html_tail.extend( o )
							else:
								for y in o:
									writer.write(y)

					else:
						writer.write(line)

				elif line.strip() == '</script>':
					if type(script) is list and len(script):
						source = '\n'.join(script)
						script = True
						self._html_tail.append( '</script>')
					else:
						writer.write( line )

				elif isinstance( script, list ):
					script.append( line )

				elif script is True:
					self._html_tail.append( line )

				else:
					writer.write( line )

		source = typedpython.transform_source( source )

		self.setup_inliner( writer )

		self._in_catch_exception = False

		self._line = None
		self._line_number = 0
		self._stack = []        ## current path to the root

		self._direct_operators = set()  ## optimize "+" and "*" operator
		self._with_ll = False   ## lowlevel
		self._with_js = True
		self._in_lambda = False
		self._in_while_test = False
		self._use_threading = False
		self._use_sleep = False
		self._use_array = False
		self._webworker_functions = dict()
		self._with_webworker = False
		self._with_rpc = None
		self._with_rpc_name = None
		self._with_direct_keys = False

		self._with_glsl = False
		self._in_gpu_main = False
		self._gpu_return_types = set() ## 'array' or float32, or array of 'vec4' float32's.

		self._source = source.splitlines()
		self._classes = dict()    ## class name : [method names]
		self._class_parents = dict()  ## class name : parents
		self._instance_attributes = dict()  ## class name : [attribute names]
		self._class_attributes = dict()
		self._catch_attributes = None
		self._typedef_vars = dict()

		#self._names = set() ## not used?
		## inferred class instances, TODO regtests to confirm that this never breaks ##
		self._instances = dict()  ## instance name : class name

		self._decorator_properties = dict()
		self._decorator_class_props = dict()
		self._function_return_types = dict()
		self._return_type = None


		self._module = module    ## DEPRECATED
		self._typedefs = dict()  ## class name : typedef  (deprecated - part of the old static type finder)

		self._globals = dict()
		self._global_nodes = dict()
		self._with_static_type = None
		self._global_typed_lists = dict()  ## global name : set  (if len(set)==1 then we know it is a typed list)
		self._global_typed_dicts = dict()
		self._global_typed_tuples = dict()
		self._global_functions = dict()

		self._js_classes = dict()
		self._in_js_class = False
		self._in_assign_target = False
		self._with_runtime_exceptions = True  ## this is only used in full python mode.

		self._iter_ids = 0
		self._addop_ids = 0

		self._cache_for_body_calls = False
		self._cache_while_body_calls = False
		self._comprehensions = []
		self._generator_functions = set()

		self._in_loop_with_else = False
		self._introspective_functions = False

		self._custom_operators = {}
		self._injector = []  ## advanced meta-programming hacks
		self._in_class = None
		self._with_fastdef = False
		self.setup_builtins()

		source = self.preprocess_custom_operators( source )

		## check for special imports - TODO clean this up ##
		for line in source.splitlines():
			if line.strip().startswith('import tornado'):
				dirname = os.path.dirname(os.path.abspath(__file__))
				header = open( os.path.join(dirname, os.path.join('fakelibs', 'tornado.py')) ).read()
				source = header + '\n' + source
				self._source = source.splitlines()
			elif line.strip().startswith('import os'):
				dirname = os.path.dirname(os.path.abspath(__file__))
				header = open( os.path.join(dirname, os.path.join('fakelibs', 'os.py')) ).read()
				source = header + '\n' + source
				self._source = source.splitlines()
			elif line.strip().startswith('import tempfile'):
				dirname = os.path.dirname(os.path.abspath(__file__))
				header = open( os.path.join(dirname, os.path.join('fakelibs', 'tempfile.py')) ).read()
				source = header + '\n' + source
				self._source = source.splitlines()
			elif line.strip().startswith('import sys'):
				dirname = os.path.dirname(os.path.abspath(__file__))
				header = open( os.path.join(dirname, os.path.join('fakelibs', 'sys.py')) ).read()
				source = header + '\n' + source
				self._source = source.splitlines()
			elif line.strip().startswith('import subprocess'):
				dirname = os.path.dirname(os.path.abspath(__file__))
				header = open( os.path.join(dirname, os.path.join('fakelibs', 'subprocess.py')) ).read()
				source = header + '\n' + source
				self._source = source.splitlines()


		if '--debug--' in sys.argv:
			try:
				tree = ast.parse( source )
			except SyntaxError:
				raise SyntaxError(source)
		else:
			tree = ast.parse( source )

		self._generator_function_nodes = collect_generator_functions( tree )

		for node in tree.body:
			## skip module level doc strings ##
			if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
				pass
			else:
				self.visit(node)

		if self._html_tail:
			for line in self._html_tail:
				writer.write(line)

        def visit(self, node):
		"""Visit a node."""
		## modified code of visit() method from Python 2.7 stdlib
		self._stack.append(node)
		method = 'visit_' + node.__class__.__name__
		visitor = getattr(self, method, self.generic_visit)
		res = visitor(node)
		self._stack.pop()
		return res

	def has_webworkers(self):
		return len(self._webworker_functions.keys())

	def get_webworker_file_names(self):
		return set(self._webworker_functions.values())

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
			'chr':'new(String.fromCharCode(%s))',
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
				#log('ERROR: class name not in self._classes: %s'%class_name)
				#log('self._classes: %s'%self._classes)
				#raise RuntimeError('class name: %s - not found in self._classes - node:%s '%(class_name, instance))
				return None  ## TODO hook into self._typedef_vars

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


	def visit_Import(self, node):
		'''
		fallback to requirejs or if in webworker importScripts.
		some special modules from pythons stdlib can be faked here like:
			. threading

		nodejs only:
			. tornado
			. os

		'''

		tornado = ['tornado', 'tornado.web', 'tornado.ioloop']

		for alias in node.names:
			if self._with_go:
				writer.write('import %s' %alias.name)
			elif alias.name in tornado:
				pass  ## pythonjs/fakelibs/tornado.py
			elif alias.name == 'tempfile':
				pass  ## pythonjs/fakelibs/tempfile.py
			elif alias.name == 'sys':
				pass  ## pythonjs/fakelibs/sys.py
			elif alias.name == 'subprocess':
				pass  ## pythonjs/fakelibs/subprocess.py
			elif alias.name == 'numpy':
				pass

			elif alias.name == 'json' or alias.name == 'os':
				pass  ## part of builtins.py
			elif alias.name == 'threading':
				self._use_threading = True
				#writer.write( 'Worker = require("/usr/local/lib/node_modules/workerjs")')

				## note: nodewebkit includes Worker, but only from the main script context,
				## there might be a bug in requirejs or nodewebkit where Worker gets lost
				## when code is loaded into main as a module using requirejs, as a workaround
				## allow "workerjs" to be loaded as a fallback, however this appears to not work in nodewebkit.
				writer.write( 'if __NODEJS__==True and typeof(Worker)=="undefined": Worker = require("workerjs")')

			elif alias.asname:
				#writer.write( '''inline("var %s = requirejs('%s')")''' %(alias.asname, alias.name) )
				writer.write( '''inline("var %s = require('%s')")''' %(alias.asname, alias.name.replace('__DASH__', '-')) )

			elif '.' in alias.name:
				raise NotImplementedError('import with dot not yet supported: line %s' % node.lineno)
			else:
				#writer.write( '''inline("var %s = requirejs('%s')")''' %(alias.name, alias.name) )
				writer.write( '''inline("var %s = require('%s')")''' %(alias.name, alias.name) )

	def visit_ImportFrom(self, node):
		if self._with_dart:
			lib = ministdlib.DART
		elif self._with_lua:
			lib = ministdlib.LUA
		else:
			lib = ministdlib.JS

		path = os.path.join( self._module_path, node.module+'.py')

		if node.module == 'time' and node.names[0].name == 'sleep':
			self._use_sleep = True
		elif node.module == 'array' and node.names[0].name == 'array':
			self._use_array = True ## this is just a hint that calls to array call the builtin array

		elif node.module == 'bisect' and node.names[0].name == 'bisect':
			## bisect library is part of the stdlib, 
			## in pythonjs it is a builtin function defined in builtins.py
			pass

		elif node.module in lib:
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

		elif os.path.isfile(path):  
			## user import `from mymodule import *` TODO support files from other folders
			## this creates a sub-translator, because they share the same `writer` object (a global),
			## there is no need to call `writer.write` here.
			## note: the current pythonjs.configure mode here maybe different from the subcontext.
			data = open(path, 'rb').read()
			subtrans = PythonToPythonJS(
				data, 
				module_path=self._module_path
			)
			self._js_classes.update( subtrans._js_classes ) ## TODO - what other typedef info needs to be copied here?

		else:
			msg = 'invalid import - file not found: %s/%s.py'%(self._module_path,node.module)
			raise SyntaxError( self.format_error(msg) )

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
			v = node.values[i]
			if isinstance(v, ast.Lambda):
				v.keep_as_lambda = True
			v = self.visit( v )
			if self._with_dart or self._with_ll or self._with_go:
				a.append( '%s:%s'%(k,v) )
				#if isinstance(node.keys[i], ast.Str):
				#	a.append( '%s:%s'%(k,v) )
				#else:
				#	a.append( '"%s":%s'%(k,v) )
			elif self._with_js:
				a.append( '[%s,%s]'%(k,v) )
			else:
				a.append( 'JSObject(key=%s, value=%s)'%(k,v) )  ## this allows non-string keys

		if self._with_dart or self._with_ll or self._with_go:
			b = ','.join( a )
			return '{%s}' %b
		elif self._with_js:
			b = ','.join( a )
			return '__jsdict( [%s] )' %b
		else:
			b = '[%s]' %', '.join(a)
			return '__get__(dict, "__call__")([], {"js_object":%s})' %b

	def visit_Tuple(self, node):
		node.returns_type = 'tuple'
		#a = '[%s]' % ', '.join(map(self.visit, node.elts))
		a = []
		for e in node.elts:
			if isinstance(e, ast.Lambda):
				e.keep_as_lambda = True
			v = self.visit(e)
			assert v is not None
			a.append( v )
		a = '[%s]' % ', '.join(a)

		if self._with_dart:
			return 'tuple(%s)' %a
		else:
			return a

	def visit_List(self, node):
		node.returns_type = 'list'

		a = []
		for e in node.elts:
			if isinstance(e, ast.Lambda):  ## inlined and called lambda "(lambda x: x)(y)"
				e.keep_as_lambda = True
			v = self.visit(e)
			assert v is not None
			a.append( v )

		a = '[%s]' % ', '.join(a)
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
		writer.write('var(%s)'%cname)

		length = len( node.generators )
		a = ['idx%s'%i for i in range(length)]
		writer.write('var( %s )' %','.join(a) )
		a = ['iter%s'%i for i in range(length)]
		writer.write('var( %s )' %','.join(a) )
		a = ['get%s'%i for i in range(length)]
		writer.write('var( %s )' %','.join(a) )

		if self._with_go:
			assert node.go_listcomp_type
			writer.write('%s = __go__array__(%s)' %(cname, node.go_listcomp_type))
		else:
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
				elif self._with_go:
					writer.write('%s = append(%s, %s )' %(cname, cname,self.visit(node.elt)) )
				else:
					writer.write('%s.push( %s )' %(cname,self.visit(node.elt)) )
				writer.pull()
			else:

				if self._with_dart:
					writer.write('%s.add( %s )' %(cname,self.visit(node.elt)) )
				elif self._with_lua:
					writer.write('table.insert(%s, %s )' %(cname,self.visit(node.elt)) )
				elif self._with_go:
					writer.write('%s = append(%s, %s )' %(cname, cname,self.visit(node.elt)) )
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

	## TODO check if the default visit_Compare always works ##
	#def visit_Compare(self, node):
	#	raise NotImplementedError( node )


	def visit_AugAssign(self, node):
		self._in_assign_target = True
		target = self.visit( node.target )
		self._in_assign_target = False

		op = '%s=' %self.visit( node.op )

		typedef = self.get_typedef( node.target )

		if self._with_lua:

			if isinstance(node.target, ast.Subscript):
				name = self.visit(node.target.value)
				slice = self.visit(node.target.slice)
				op = self.visit(node.op)
				a = '__get__(%s, "__setitem__")( [%s, __get__(%s, "__getitem__")([%s], {}) %s (%s)], {} )'
				a = a %(name, slice, name, slice, op, self.visit(node.value))
				writer.write( a )
				return

			elif op == '+=':
				a = '__add_op(%s,%s)' %(target, self.visit(node.value))
			elif op == '-=':
				a = '(%s - %s)' %(target, self.visit(node.value))
			elif op == '*=':
				a = '(%s * %s)' %(target, self.visit(node.value))
			elif op == '/=' or op == '//=':
				a = '(%s / %s)' %(target, self.visit(node.value))
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
			if isinstance(node.target, ast.Attribute):
				name = self.visit(node.target.value)
				attr = node.target.attr
				target = '%s.%s' %(name, attr)

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
			if isinstance( node.target, ast.Name ) and node.target.id in self._typedef_vars and self._typedef_vars[node.target.id] in typedpython.native_number_types+typedpython.vector_types:
				writer.write(b)

			else:
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
			value = self.visit(node.value)
			#a = '__get__(%s, "__setitem__")( [%s, __get__(%s, "__getitem__")([%s], {}) %s (%s)], {} )'
			fallback = '__get__(%s, "__setitem__")( [%s, __get__(%s, "__getitem__")([%s], {}) %s (%s)], {} )'%(name, slice, name, slice, op, value)
			if isinstance(node.target.value, ast.Name):
				## TODO also check for arr.remote (RPC) if defined then __setitem__ can not be bypassed

				## the overhead of checking if target is an array,
				## and calling __setitem__ directly bypassing a single __get__,
				## is greather than simply calling the fallback
				#writer.write('if instanceof(%s, Array): %s.__setitem__([%s, %s[%s] %s (%s) ], __NULL_OBJECT__)' %(name, name, slice, name,slice, op, value))

				writer.write('if instanceof(%s, Array): %s[%s] %s= %s' %(name, name,slice, op, value))
				writer.write('else: %s' %fallback)
			else:
				writer.write(fallback)

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
		struct_types = dict()

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

			elif isinstance(item, ast.Expr) and isinstance(item.value, ast.Dict):
				sdef = []
				for i in range( len(item.value.keys) ):
					k = self.visit( item.value.keys[ i ] )
					v = self.visit( item.value.values[i] )
					sdef.append( '%s=%s'%(k,v) )

				writer.write('@__struct__(%s)' %','.join(sdef))

		if self._with_go:
			pass
		elif props:
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
			if not self._with_go:
				init.name = node.name
			self.visit(init)

		## methods
		for method in method_list:
			self.visit(method)

		for item in node.body:
			if isinstance(item, ast.With):
				s = self.visit(item)
				if s: writer.write( s )


		if not init and not method_list:
			writer.write( 'pass' )

		writer.pull()

	def is_gpu_method(self, n):
		for dec in n.decorator_list:
			if isinstance(dec, Attribute) and isinstance(dec.value, Name) and dec.value.id == 'gpu':
				if dec.attr == 'method':
					return True


	def _visit_js_classdef(self, node):
		name = node.name
		self._js_classes[ name ] = node
		self._in_js_class = True
		class_decorators = []
		gpu_object = False

		for decorator in node.decorator_list:  ## class decorators
			if isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id == 'gpu':
				if decorator.attr == 'object':
					gpu_object = True
				else:
					raise SyntaxError( self.format_error('invalid gpu class decorator') )
			else:
				class_decorators.append( decorator )

		method_names = []  ## write back in order (required by GLSL)
		methods = {}
		class_vars = []

		for item in node.body:
			if isinstance(item, FunctionDef):
				method_names.append(item.name)
				methods[ item.name ] = item
				if self.is_gpu_method( item ):
					item.args.args[0].id = name  ## change self to the class name, pythonjs.py changes it to 'ClassName self'
				else:
					item.args.args = item.args.args[1:]  ## remove self
					finfo = inspect_function( item )
					for n in finfo['name_nodes']:
						if n.id == 'self':
							n.id = 'this'
			elif isinstance(item, ast.Expr) and isinstance(item.value, Str):  ## skip doc strings
				pass
			else:
				class_vars.append( item )


		#init = methods.pop('__init__')
		init = methods.get( '__init__', None)
		if init:
			args = [self.visit(arg) for arg in init.args.args]
			node._cached_init = init
			if init.args.kwarg:
				args.append( init.args.kwarg )

		else:
			args = []
			init = self._get_js_class_base_init( node )
			if init:
				args = [self.visit(arg) for arg in init.args.args]
				node._cached_init = init

		writer.write('def %s(%s):' %(name,','.join(args)))
		writer.push()
		if init:
			tail = ''
			if gpu_object:
				tail = 'this.__struct_name__="%s"' %name


			#for b in init.body:
			#	line = self.visit(b)
			#	if line: writer.write( line )

			if hasattr(init, '_code'):  ## cached ##
				code = init._code
			elif args:
				code = '%s.__init__(this, %s); %s'%(name, ','.join(args), tail)
				init._code = code
			else:
				code = '%s.__init__(this);     %s'%(name, tail)
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

		#keys = methods.keys()
		#keys.sort()
		for mname in method_names:
			method = methods[mname]
			gpu_method = False
			for dec in method.decorator_list:
				if isinstance(dec, Attribute) and isinstance(dec.value, Name) and dec.value.id == 'gpu':
					if dec.attr == 'method':
						gpu_method = True

			if gpu_method:
				method.name = '%s_%s' %(name, method.name)
				self._in_gpu_method = name  ## name of class
				line = self.visit(method)
				if line: writer.write( line )
				self._in_gpu_method = None

			else:

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

		for item in class_vars:
			if isinstance(item, Assign) and isinstance(item.targets[0], Name):
				item_name = item.targets[0].id
				item.targets[0].id = '__%s_%s' % (name, item_name)
				self.visit(item)  # this will output the code for the assign
				writer.write('%s.prototype.%s = %s' % (name, item_name, item.targets[0].id))

		if gpu_object:
			## TODO check class variables ##
			writer.write('%s.prototype.__struct_name__ = "%s"' %(name,name))

		## TODO support property decorators in javascript-mode ##
		writer.write('%s.prototype.__properties__ = {}' %name)
		writer.write('%s.prototype.__unbound_methods__ = {}' %name)


		self._in_js_class = False

	def visit_ClassDef(self, node):
		if self._with_dart or self._with_go:
			self._visit_dart_classdef(node)
			return
		elif self._with_js:
			self._visit_js_classdef(node)
			return

		name = node.name
		self._in_class = name
		self._classes[ name ] = list()  ## method names
		self._class_parents[ name ] = set()
		self._class_attributes[ name ] = set()
		self._catch_attributes = None
		self._decorator_properties = dict() ## property names :  {'get':func, 'set':func}
		self._decorator_class_props[ name ] = self._decorator_properties
		self._instances[ 'self' ] = name

		self._injector = []  ## DEPRECATED
		class_decorators = []
		gpu_object = False

		for decorator in node.decorator_list:  ## class decorators
			if isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id == 'gpu':
				if decorator.attr == 'object':
					gpu_object = True
				else:
					raise SyntaxError( self.format_error('invalid gpu class decorator') )
			else:
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

				if self.is_gpu_method( item ):
					item.name = '%s_%s' % (name, item_name)
				else:
					item.name = '__%s_%s' % (name, item_name)

				self.visit(item)  # this will output the code for the function

				if item_name in self._decorator_properties or self.is_gpu_method( item ):
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

		## DEPRECATED
		#if 'init' in self._injector:
		#	writer.write('%s.init_callbacks = JSArray()' %name)
		#self._injector = []

		for dec in class_decorators:
			writer.write('%s = __get__(%s,"__call__")( [%s], JSObject() )' % (name, self.visit(dec), name))

	def visit_And(self, node):
		return ' and '

	def visit_Or(self, node):
		return ' or '

	def visit_BoolOp(self, node):
		op = self.visit(node.op)
		#raise SyntaxError(op)
		return '('+ op.join( [self.visit(v) for v in node.values] ) + ')'

	def visit_If(self, node):
		if self._with_dart and writer.is_at_global_level():
			raise SyntaxError( self.format_error('if statements can not be used at module level in dart') )
		elif self._with_lua:
			writer.write('if __test_if_true__(%s):' % self.visit(node.test))

		elif isinstance(node.test, ast.Dict):
			if self._with_js:
				writer.write('if Object.keys(%s).length:' % self.visit(node.test))
			else:
				writer.write('if %s.keys().length:' % self.visit(node.test))

		elif isinstance(node.test, ast.List):
			writer.write('if %s.length:' % self.visit(node.test))

		elif self._with_ll or self._with_glsl:
			writer.write('if %s:' % self.visit(node.test))
		elif isinstance(node.test, ast.Compare):
			writer.write('if %s:' % self.visit(node.test))
		else:
			writer.write('if __test_if_true__(%s):' % self.visit(node.test))

		writer.push()
		map(self.visit, node.body)
		writer.pull()
		if node.orelse:
			writer.write('else:')
			writer.push()
			map(self.visit, node.orelse)
			writer.pull()

	def visit_TryExcept(self, node):
		if len(node.handlers)==0:
			raise SyntaxError(self.format_error('no except handlers'))

		## by default in js-mode some expections will not be raised,
		## this allows those cases to throw proper errors.
		if node.handlers[0].type:
			self._in_catch_exception = self.visit(node.handlers[0].type)
		else:
			self._in_catch_exception = None

		writer.write('try:')
		writer.push()
		map(self.visit, node.body)
		writer.pull()
		map(self.visit, node.handlers)

	def visit_Raise(self, node):
		#if self._with_js or self._with_dart:
		#	writer.write('throw Error')
		#else:
		#writer.write('raise %s' % self.visit(node.type))
		if isinstance(node.type, ast.Name):
			writer.write('raise %s' % node.type.id)

		elif isinstance(node.type, ast.Call):
			if len(node.type.args) > 1:
				raise SyntaxError( self.format_error('raise Error(x) can only have a single argument') )
			if node.type.args:
				writer.write( 'raise %s(%s)' %(self.visit(node.type.func), self.visit(node.type.args[0])) )
			else:
				writer.write( 'raise %s()' %self.visit(node.type.func) )

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
					return 'null'

		return node.id

	def visit_Num(self, node):
		return str(node.n)

	def visit_Return(self, node):
		if node.value:
			if isinstance(node.value, Call) and isinstance(node.value.func, Name) and node.value.func.id in self._classes:
				self._return_type = node.value.func.id
			elif isinstance(node.value, Name) and node.value.id == 'self' and 'self' in self._instances:
				self._return_type = self._instances['self']


			if self._with_glsl and self._in_gpu_main:
				## _id_ is inserted into all function headers by pythonjs.py for glsl functions.
				if not self._gpu_return_types:
					raise SyntaxError( self.format_error('function return type unknown - required decorator `@returns(array/vec4=[w,h])`') )

				## only one return type is allowed ##
				if 'array' in self._gpu_return_types:
					writer.write('out_float = %s' %self.visit(node.value))
				elif 'vec4' in self._gpu_return_types:
					writer.write('out_float4 = %s' %self.visit(node.value))
				elif 'mat4' in self._gpu_return_types:
					nv = self.visit(node.value)
					writer.write('inline("mat4 _res_ = %s; int _row = matrix_row();")' %nv)

					r0 = 'vec4(_res_[0][0],_res_[0][1],_res_[0][2],_res_[0][3])'
					r1 = 'vec4(_res_[1][0],_res_[1][1],_res_[1][2],_res_[1][3])'
					r2 = 'vec4(_res_[2][0],_res_[2][1],_res_[2][2],_res_[2][3])'
					r3 = 'vec4(_res_[3][0],_res_[3][1],_res_[3][2],_res_[3][3])'

					writer.write('if _row==0: out_float4 = %s'   % r0)
					writer.write('elif _row==1: out_float4 = %s'%r1)
					writer.write('elif _row==2: out_float4 = %s'%r2)
					writer.write('else: out_float4 = %s'%r3)

				else:
					raise SyntaxError( self.format_error('invalid GPU return type: %s' %self._gpu_return_types) )

			elif self._inline:
				writer.write('__returns__%s = %s' %(self._inline[-1], self.visit(node.value)) )
				if self._inline_breakout:
					writer.write('break')

			elif isinstance(node.value, ast.Lambda):
				self.visit( node.value )
				writer.write( 'return __lambda__' )

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

		is_go_listcomp = False
		if self._with_go:
			if op == '<<':
				if isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id=='__go__array__':
					if isinstance(node.right, ast.GeneratorExp):
						is_go_listcomp = True
						node.right.go_listcomp_type = node.left.args[0].id


		right = self.visit(node.right)

		if self._with_glsl:
			return '(%s %s %s)' % (left, op, right)
		elif self._with_go:
			if is_go_listcomp:
				return right
			else:
				return '(%s %s %s)' % (left, op, right)

		elif op == '|':
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
			if len(node.left.elts) == 1 and isinstance(node.left.elts[0], ast.Name) and node.left.elts[0].id == 'None':
				if self._with_dart:
					return 'JS("__create_list(%s)")' %self.visit(node.right)
				elif self._with_lua:
					return 'JS("__create_list(%s)")' %self.visit(node.right)
				else:
					return 'JS("new Array(%s)")' %self.visit(node.right)
			elif isinstance(node.right,ast.Num):
				n = node.right.n
			elif isinstance(node.right, Name):
				if node.right.id in self._global_nodes:
					n = self._global_nodes[ node.right.id ].n
				else:
					raise SyntaxError( self.format_error(node) )
			else:
				#raise SyntaxError( self.format_error(node) )
				return '__mul_op(%s,%s)'%(left, right)

			elts = [ self.visit(e) for e in node.left.elts ]
			expanded = []
			for i in range( n ): expanded.extend( elts )

			if self._with_lua:
				return 'list.__call__([], {pointer:[%s], length:%s})' %(','.join(expanded), n)
			else:
				return '[%s]' %','.join(expanded)

		elif not self._with_dart and left in self._typedef_vars and self._typedef_vars[left]=='long':
			if op == '*':
				return '%s.multiply(%s)'%(left, right)
			elif op == '+':
				return '%s.add(%s)'%(left, right)
			elif op == '-':
				return '%s.subtract(%s)'%(left, right)
			elif op == '/' or op == '//':
				return '%s.div(%s)'%(left, right)
			elif op == '%':
				return '%s.modulo(%s)'%(left, right)
			else:
				raise NotImplementedError('long operator: %s'%op)

		elif not self._with_dart and op == '*' and left in self._typedef_vars and self._typedef_vars[left]=='int' and isinstance(node.right, ast.Num) and node.right.n in POWER_OF_TWO:
			power = POWER_OF_TWO.index( node.right.n )
			return '%s << %s'%(left, power)

		elif not self._with_dart and op == '//' and left in self._typedef_vars and self._typedef_vars[left]=='int' and isinstance(node.right, ast.Num) and node.right.n in POWER_OF_TWO:
			power = POWER_OF_TWO.index( node.right.n )
			return '%s >> %s'%(left, power)

		elif not self._with_dart and op == '*' and '*' in self._direct_operators:
			return '(%s * %s)'%(left, right)

		elif not self._with_dart and not self._with_js and op == '*':
			if left in self._typedef_vars and self._typedef_vars[left] in typedpython.native_number_types:
				return '(%s * %s)'%(left, right)
			else:
				return '__mul_op(%s,%s)'%(left, right)

		elif op == '//':
			if self._with_dart:
				return '(%s/%s).floor()' %(left, right)				
			else:
				return 'Math.floor(%s/%s)' %(left, right)

		elif op == '**':
			return 'Math.pow(%s,%s)' %(left, right)

		elif op == '+' and not self._with_dart:
			if '+' in self._direct_operators:
				return '%s+%s'%(left, right)
			elif left in self._typedef_vars and self._typedef_vars[left] in typedpython.native_number_types:
				return '%s+%s'%(left, right)

			elif self._with_lua or self._in_lambda or self._in_while_test:
				## this is also required when in an inlined lambda like "(lambda a,b: a+b)(1,2)"
				return '__add_op(%s, %s)'%(left, right)
			else:
				## the ternary operator in javascript is fast, the add op needs to be fast for adding numbers, so here typeof is
				## used to check if the first variable is a number, and if so add the numbers, otherwise fallback to using the
				## __add_op function, the __add_op function checks if the first variable is an Array, and if so then concatenate;
				## else __add_op will call the "__add__" method of the left operand, passing right as the first argument.
				l = '__left%s' %self._addop_ids
				self._addop_ids += 1
				r = '__right%s' %self._addop_ids
				writer.write('var(%s,%s)' %(l,r))
				self._addop_ids += 1
				writer.write('%s = %s' %(l,left))
				writer.write('%s = %s' %(r,right))
				return '__ternary_operator__( typeof(%s)=="number", %s + %s, __add_op(%s, %s))'%(l, l, r, l, r)

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
			if i==0 and isinstance(node.left, ast.Name) and node.left.id in self._typedef_vars and self._typedef_vars[node.left.id] == 'long':
				if isinstance(node.ops[i], ast.Eq):
					comp = ['%s.equals(%s)' %(left, self.visit(node.comparators[i]))]
				elif isinstance(node.ops[i], ast.Lt):
					comp = ['%s.lessThan(%s)' %(left, self.visit(node.comparators[i]))]
				elif isinstance(node.ops[i], ast.Gt):
					comp = ['%s.greaterThan(%s)' %(left, self.visit(node.comparators[i]))]

				elif isinstance(node.ops[i], ast.LtE):
					comp = ['%s.lessThanOrEqual(%s)' %(left, self.visit(node.comparators[i]))]
				elif isinstance(node.ops[i], ast.GtE):
					comp = ['%s.greaterThanOrEqual(%s)' %(left, self.visit(node.comparators[i]))]

				else:
					raise NotImplementedError( node.ops[i] )

			elif isinstance(node.ops[i], ast.In) or isinstance(node.ops[i], ast.NotIn):
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

		## TODO check if this is always safe.
		if isinstance(node.value, Name):
			typedef = self.get_typedef( instance=node.value )
		elif hasattr(node.value, 'returns_type'):
			typedef = self.get_typedef( class_name=node.value.returns_type )
		else:
			typedef = None


		node_value = self.visit(node.value)
		if self._with_glsl:
			#if node_value not in self._typedef_vars:  ## dynamic var  DEPRECATED
			#	return 'glsl_inline(%s.%s)' %(node_value, node.attr)
			#else:
			return '%s.%s' %(node_value, node.attr)
		elif self._with_dart or self._with_ll or self._with_go:
			return '%s.%s' %(node_value, node.attr)

		elif self._with_js:
			if self._in_catch_exception == 'AttributeError':
				return '__getfast__(%s, "%s")' % (node_value, node.attr)
			else:
				return '%s.%s' %(node_value, node.attr)

		elif self._with_lua and self._in_assign_target:  ## this is required because lua has no support for inplace assignment ops like "+="
			return '%s.%s' %(node_value, node.attr)

		elif typedef and node.attr in typedef.attributes:  ## optimize away `__get__`
			return '%s.%s' %(node_value, node.attr)

		elif hasattr(node, 'lineno'):
			src = self._source[ node.lineno-1 ]
			src = src.replace('"', '\\"')
			err = 'missing attribute `%s` - line %s: %s'	%(node.attr, node.lineno, src.strip())
			return '__get__(%s, "%s", "%s")' % (node_value, node.attr, err)
		else:
			return '__get__(%s, "%s")' % (node_value, node.attr)


	def visit_Index(self, node):
		return self.visit(node.value)

	def visit_Subscript(self, node):
		name = self.visit(node.value)

		if isinstance(node.slice, ast.Ellipsis):
			#return '%s["$wrapped"]' %name
			return '%s[...]' %name

		elif self._with_ll or self._with_glsl or self._with_go:
			return '%s[%s]' %(name, self.visit(node.slice))

		elif self._with_js or self._with_dart:
			if isinstance(node.slice, ast.Slice):  ## allow slice on Array
				if self._with_dart:
					## this is required because we need to support slices on String ##
					return '__getslice__(%s, %s)'%(name, self.visit(node.slice))
				else:
					if not node.slice.lower and not node.slice.upper and not node.slice.step:
						return '%s.copy()' %name
					else:
						return '%s.__getslice__(%s)'%(name, self.visit(node.slice))


			elif isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.Num):
				if node.slice.value.n < 0:
					## the problem with this is it could be a dict with negative numbered keys
					return '%s[ %s.length+%s ]' %(name, name, self.visit(node.slice))
				else:
					return '%s[ %s ]' %(name, self.visit(node.slice))

			elif self._with_dart:  ## --------- dart mode -------
				return '%s[ %s ]' %(name, self.visit(node.slice))


			else:  ## ------------------ javascript mode ------------------------
				if self._in_catch_exception == 'KeyError':
					value = self.visit(node.value)
					slice = self.visit(node.slice)
					return '__get__(%s, "__getitem__")([%s], __NULL_OBJECT__)' % (value, slice)

				elif isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.BinOp):
					## TODO keep this optimization? in js mode `a[x+y]` is assumed to a direct key,
					## it would be safer to check if one of the operands is a number literal,
					## in that case it is safe to assume that this is a direct key.
					return '%s[ %s ]' %(name, self.visit(node.slice))

				elif self._with_direct_keys:
					return '%s[ %s ]' %(name, self.visit(node.slice))

				else:
					s = self.visit(node.slice)
					#return '%s[ __ternary_operator__(%s.__uid__, %s) ]' %(name, s, s)
					check_array = '__ternary_operator__( instanceof(%s,Array), JSON.stringify(%s), %s )' %(s, s, s)
					return '%s[ __ternary_operator__(%s.__uid__, %s) ]' %(name, s, check_array)

		elif isinstance(node.slice, ast.Slice):
			return '__get__(%s, "__getslice__")([%s], __NULL_OBJECT__)' % (
				self.visit(node.value),
				self.visit(node.slice)
			)

		elif name in self._func_typedefs and self._func_typedefs[name] == 'list':
			#return '%s[...][%s]'%(name, self.visit(node.slice))
			return '%s[%s]'%(name, self.visit(node.slice))

		elif name in self._instances:  ## support x[y] operator overloading
			klass = self._instances[ name ]
			if '__getitem__' in self._classes[ klass ]:
				return '__%s___getitem__([%s, %s], JSObject())' % (klass, name, self.visit(node.slice))
			else:
				return '__get__(%s, "__getitem__")([%s], __NULL_OBJECT__)' % (
					self.visit(node.value),
					self.visit(node.slice)
				)
		else:
			err = ""
			if hasattr(node, 'lineno'):
				src = self._source[ node.lineno-1 ]
				src = src.replace('"', '\\"')
				err = 'line %s: %s'	%(node.lineno, src.strip())

			value = self.visit(node.value)
			slice = self.visit(node.slice)
			fallback = '__get__(%s, "__getitem__", "%s")([%s], __NULL_OBJECT__)' % (value, err, slice)
			if not self._with_lua and isinstance(node.value, ast.Name):
				return '__ternary_operator__(instanceof(%s, Array), %s[%s], %s)' %(value, value,slice, fallback)
			else:
				return fallback

	def visit_Slice(self, node):
		if self._with_go:
			lower = upper = step = None
		elif self._with_dart:
			lower = upper = step = 'null'
		elif self._with_js:
			lower = upper = step = 'undefined'
		else:
			lower = upper = step = 'undefined'
		if node.lower:
			lower = self.visit(node.lower)
		if node.upper:
			upper = self.visit(node.upper)
		if node.step:
			step = self.visit(node.step)

		if self._with_go:
			if lower and upper:
				return '%s:%s' %(lower,upper)
			elif upper:
				return ':%s' %upper
			elif lower:
				return '%s:'%lower
		else:
			return "%s, %s, %s" % (lower, upper, step)

	def visit_Assign(self, node):
		use_runtime_errors = not (self._with_js or self._with_ll or self._with_dart or self._with_coffee or self._with_lua or self._with_go)
		use_runtime_errors = use_runtime_errors and self._with_runtime_exceptions

		lineno = node.lineno
		if node.lineno < len(self._source):
			src = self._source[ node.lineno ]
			self._line_number = node.lineno
			self._line = src


		if use_runtime_errors:
			writer.write('try:')
			writer.push()

		targets = list( node.targets )
		target = targets[0]
		if isinstance(target, ast.Name) and target.id in typedpython.types:
			if len(targets)==2 and isinstance(targets[1], ast.Name):
				self._typedef_vars[ targets[1].id ] = target.id
				if target.id == 'long' and isinstance(node.value, ast.Num):
					## requires long library ##
					writer.write('%s = long.fromString("%s")' %(targets[1].id, self.visit(node.value)))
					return None
				else:
					targets = targets[1:]
			elif len(targets)==1 and isinstance(node.value, ast.Name) and target.id in typedpython.types:
				self._typedef_vars[ node.value.id ] = target.id
				return None
			else:
				raise SyntaxError( self.format_error(targets) )

		elif self._with_rpc_name and isinstance(target, Attribute) and isinstance(target.value, Name) and target.value.id == self._with_rpc_name:
			writer.write('__rpc_set__(%s, "%s", %s)' %(self._with_rpc, target.attr, self.visit(node.value)))
			return None
		elif self._with_rpc_name and isinstance(node.value, Attribute) and isinstance(node.value.value, Name) and node.value.value.id == self._with_rpc_name:
			writer.write('%s = __rpc_get__(%s, "%s")' %(self.visit(target), self._with_rpc, node.value.attr))
			return None

		#############################################
		for target in targets:
			self._visit_assign_helper( node, target )
			node = ast.Expr( value=target )

		if use_runtime_errors:
			writer.pull()
			writer.write('except:')
			writer.push()
			if lineno-1 < len(self._source):
				src = self._source[ lineno-1 ]
				src = src.replace('"', '\\"')
				src = 'line %s: %s'	%(lineno, src.strip())
				writer.write('console.trace()')
				writer.write('console.error(__exception__, __exception__.message)')
				writer.write('console.error("""%s""")' %src)
				writer.write('raise RuntimeError("""%s""")' %src)
			else:
				writer.write('raise RuntimeError("no source code")')

			writer.pull()



	def _visit_assign_helper(self, node, target):
		if isinstance(node.value, ast.Lambda):
			self.visit(node.value)  ## writes function def
			writer.write('%s = __lambda__' %self.visit(target))

		elif isinstance(node.value, ast.Dict) and self._with_go:
			key_type = None
			val_type = None

			for i in range( len(node.value.keys) ):
				k = node.value.keys[ i ]
				v = node.value.values[i]
				if isinstance(k, ast.Str):
					key_type = 'string'
				elif isinstance(k, ast.Num):
					key_type = 'int'

				if isinstance(v, ast.Str):
					val_type = 'string'
				elif isinstance(v, ast.Num):
					if isinstance(v.n, int):
						val_type = 'int'
					else:
						val_type = 'float64'

			if not key_type:
				raise SyntaxError(  self.format_error('can not determine dict key type')  )
			if not val_type:
				raise SyntaxError(  self.format_error('can not determine dict value type')  )

			t = self.visit(target)
			v = self.visit(node.value)
			writer.write('%s = __go__map__(%s, %s) << %s' %(t, key_type, val_type, v))


		elif isinstance(node.value, ast.List) and self._with_go:
			guess_type = None
			for elt in node.value.elts:
				if isinstance(elt, ast.Num):
					if isinstance(elt.n, int):
						guess_type = 'int'
					else:
						guess_type = 'float64'
				elif isinstance(elt, ast.Str):
					guess_type = 'string'

			if guess_type:
				t = self.visit(target)
				v = self.visit(node.value)
				writer.write('%s = __go__array__(%s) << %s' %(t, guess_type, v))
			else:
				raise SyntaxError(self.format_error('can not determine type of array'))

		elif isinstance(target, Subscript):
			name = self.visit(target.value)  ## target.value may have "returns_type" after being visited

			if isinstance(target.slice, ast.Ellipsis):
				#code = '%s["$wrapped"] = %s' %(self.visit(target.value), self.visit(node.value))
				code = '%s[...] = %s' %(self.visit(target.value), self.visit(node.value))

			elif isinstance(target.slice, ast.Slice):
				code = '%s.__setslice__(%s, %s)' %(self.visit(target.value), self.visit(target.slice), self.visit(node.value))

			elif self._with_dart or self._with_ll or self._with_glsl or self._with_go:
				code = '%s[ %s ] = %s'
				code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))

			elif self._with_js:
				s = self.visit(target.slice.value)
				if isinstance(target.slice.value, ast.Num) or isinstance(target.slice.value, ast.BinOp):
					code = '%s[ %s ] = %s' % (self.visit(target.value), s, self.visit(node.value))
				elif self._with_direct_keys:
					code = '%s[ %s ] = %s' % (self.visit(target.value), s, self.visit(node.value))
				else:
					check_array = '__ternary_operator__( instanceof(%s,Array), JSON.stringify(%s), %s )' %(s, s, s)
					code = '%s[ __ternary_operator__(%s.__uid__, %s) ] = %s' %(self.visit(target.value), s, check_array, self.visit(node.value))

			elif name in self._func_typedefs and self._func_typedefs[name] == 'list':
				code = '%s[%s] = %s'%(name, self.visit(target.slice.value), self.visit(node.value))

			else:
				code = "__get__(__get__(%s, '__setitem__'), '__call__')([%s, %s], JSObject())"
				code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))

			writer.write(code)

		elif isinstance(target, Attribute):
			self._in_assign_target = True
			target_value = self.visit(target.value)  ## target.value may have "returns_type" after being visited
			self._in_assign_target = False
			typedef = None
			if isinstance(target.value, Name):
				if target.value.id == 'self' and isinstance(self._catch_attributes, set):
					self._catch_attributes.add( target.attr )
				typedef = self.get_typedef( instance=target.value )
			elif hasattr(target.value, 'returns_type'):
				typedef = self.get_typedef( class_name=target.value.returns_type )

			#####################################

			if self._with_js or self._with_dart or self._with_go:
				writer.write( '%s.%s=%s' %(target_value, target.attr, self.visit(node.value)) )
			elif typedef and target.attr in typedef.properties and 'set' in typedef.properties[ target.attr ]:
				setter = typedef.properties[ target.attr ]['set']
				writer.write( '%s( [%s, %s], JSObject() )' %(setter, target_value, self.visit(node.value)) )

			#elif typedef and target.attr in typedef.class_attributes:
			#	writer.write( '''%s['__class__']['%s'] = %s''' %(target_value, target.attr, self.visit(node.value)))

			elif typedef and target.attr in typedef.attributes:
				writer.write( '%s.%s = %s' %(target_value, target.attr, self.visit(node.value)))

			elif typedef and typedef.parents:
				parent_prop = typedef.check_for_parent_with( property=target.attr )
				#parent_classattr = typedef.check_for_parent_with( class_attribute=target.attr )
				parent_setattr = typedef.check_for_parent_with( method='__setattr__' )
				if parent_prop and 'set' in parent_prop.properties[target.attr]:
					setter = parent_prop.properties[target.attr]['set']
					writer.write( '%s( [%s, %s], JSObject() )' %(setter, target_value, self.visit(node.value)) )

				#elif parent_classattr:
				#	writer.write( "__%s_attrs.%s = %s" %(parent_classattr.name, target.attr, self.visit(node.value)) )

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

		elif isinstance(target, Name) and self._with_glsl:  ## assignment to variable
			if target.id not in self._typedef_vars:
				raise SyntaxError(self.format_error('untyped variable'))
			node_value = self.visit( node.value )  ## node.value may have extra attributes after being visited

			if node_value in self._typedef_vars:
				writer.write('%s = %s' % (self.visit(target), self.visit(node.value)))

			elif isinstance(node.value, ast.Subscript) and isinstance(node.value.slice, ast.Ellipsis):
				writer.write('glsl_inline_assign_from_iterable("%s", "%s", %s)'%(self._typedef_vars[target.id], target.id, self.visit(node.value.value)) )

			else:

				## also assign variable in current javascript scope ##
				if not isinstance(node.value, (ast.BinOp, ast.Call)):
					if isinstance(node.value, ast.Subscript) and isinstance(node.value.slice, ast.Slice):
						x = node_value.split('(')[-1].split(')')[0].split('[')[0]
						writer.write('glsl_inline_push_js_assign("%s", %s.__getslice__(%s))'%(target.id, x, self.visit(node.value.slice)) )
					else:
						writer.write('glsl_inline_push_js_assign("%s", %s)'%(target.id, self.visit(node.value)) )
				else:
					writer.write('%s = %s' % (target.id, self.visit(node.value)))

			return None


		elif isinstance(target, Name):  ## assignment to variable
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

		elif self._with_lua:  ## Tuple - lua supports destructured assignment
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
					fallback = "__get__(__get__(%s, '__getitem__'), '__call__')([%s], __NULL_OBJECT__)" %(r, i)
					writer.write("%s = __ternary_operator__(instanceof(%s,Array), %s[%s], %s)" % (self.visit(target), r, r,i, fallback ))

	def visit_Print(self, node):
		writer.write('print(%s)' % ', '.join(map(self.visit, node.values)))

	def visit_Str(self, node):
		s = node.s.replace('\\','\\\\').replace('\n', '\\n').replace('\r', '\\r').replace('\0', '\\0')
		s = s.replace('\"', '\\"')

		if self._with_dart and s == '\\0':  ## TODO other numbers
			return 'new(String.fromCharCode(0))'

		elif self._with_js or self._with_dart:
			return '"%s"' %s.encode('utf-8')
		else:
			if len(s) == 0:
				return '""'
			elif s.startswith('"') or s.endswith('"'):
				return "'''%s'''" %s.encode('utf-8')
			else:
				return '"""%s"""' %s.encode('utf-8')

	def visit_Expr(self, node):
		if node.lineno < len(self._source):
			src = self._source[ node.lineno ]
			## TODO raise SyntaxErrors with the line number and line source
			self._line_number = node.lineno
			self._line = src

		use_runtime_errors = not (self._with_js or self._with_ll or self._with_dart or self._with_coffee or self._with_lua or self._with_go)
		use_runtime_errors = use_runtime_errors and self._with_runtime_exceptions

		if use_runtime_errors:
			writer.write('try:')
			writer.push()

		line = self.visit(node.value)
		if line:
			#writer.write('('+line+')')
			writer.write( line )
		elif use_runtime_errors:
			writer.write('pass')

		if use_runtime_errors:
			writer.pull()
			writer.write('except:')
			writer.push()
			if node.lineno-1 < len(self._source):
				src = self._source[ node.lineno-1 ]
				src = src.replace('"', '\\"')
				src = 'line %s: %s'	%(node.lineno, src.strip())
				writer.write('console.trace()')
				writer.write('console.error(__exception__, __exception__.message)')
				writer.write('console.error("""%s""")' %src)
				writer.write('raise RuntimeError("""%s""")' %src)
			else:
				writer.write('raise RuntimeError("no source code")')

			writer.pull()


	def visit_Call(self, node):
		if isinstance(node.func, ast.Lambda):  ## inlined and called lambda "(lambda x: x)(y)"
			node.func.keep_as_lambda = True

		for a in node.args:
			if isinstance(a, ast.Lambda):
				a.keep_as_lambda = True

		for kw in node.keywords:
			if isinstance(kw.value, ast.Lambda):
				kw.value.keep_as_lambda = True


		name = self.visit(node.func)
		if name in typedpython.GO_SPECIAL_CALLS:
			name = typedpython.GO_SPECIAL_CALLS[ name ]
			args = [self.visit(e) for e in node.args ]
			return '%s( %s )' %(name, ','.join(args))

		if self._with_rpc:
			if not self._with_rpc_name:
				return '__rpc__( %s, "%s", [%s] )' %(self._with_rpc, name, ','.join([self.visit(a) for a in node.args]))
			elif self._with_rpc_name:
				if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id == self._with_rpc_name:
					name = name[ len(self._with_rpc_name)+1 : ]
					return '__rpc__( %s, "%s", [%s] )' %(self._with_rpc, name, ','.join([self.visit(a) for a in node.args]))

		###############################################

		if name == 'open':  ## do not overwrite window.open ##
			name = '__open__'
			node.func.id = '__open__'

		###############################################
		if not self._with_dart and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id in self._typedef_vars and self._typedef_vars[node.func.value.id]=='list':
			if node.func.attr == 'append':
				#return '%s.append( [%s], __NULL_OBJECT__)' %(node.func.value.id, self.visit(node.args[0]) )
				return '%s.push( %s )' %(node.func.value.id, self.visit(node.args[0]) )
			else:
				raise SyntaxError( self.format_error(node) )


		elif self._with_webworker and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'self' and node.func.attr == 'terminate':
			return 'self.postMessage({"type":"terminate"})'

		elif self._use_threading and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'threading':
			if node.func.attr == 'start_new_thread' or node.func.attr == '_start_new_thread':
				return '__start_new_thread( %s, %s )' %(self.visit(node.args[0]), self.visit(node.args[1]))
			elif node.func.attr == 'start_webworker':
				return '__start_new_thread( %s, %s )' %(self.visit(node.args[0]), self.visit(node.args[1]))
			else:
				raise SyntaxError( self.format_error(node.func.attr) )

		elif self._with_webworker and name in self._global_functions:
			node.calling_from_worker = True
			args = [self.visit(arg) for arg in node.args]
			return 'self.postMessage({"type":"call", "function":"%s", "args":[%s]})' %(name, ','.join(args))

		elif self._with_js and self._use_array and name == 'array':
			args = [self.visit(arg) for arg in node.args]
			#return 'array.__call__([%s], __NULL_OBJECT__)' %','.join(args)  ## this breaks `arr[ INDEX ]`
			return '__js_typed_array(%s)' %','.join(args)

		#########################################
		if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'numpy' and node.func.attr == 'array':
			args = [self.visit(arg) for arg in node.args]
			if node.keywords:
				kwargs = [ '%s=%s' %(x.arg, self.visit(x.value)) for x in node.keywords]
				return 'numpy.array(%s, %s)' %( ','.join(args), ','.join(kwargs) )
			else:
				return 'numpy.array(%s)' %','.join(args)

		elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'pythonjs' and node.func.attr == 'configure':
			for kw in node.keywords:
				if kw.arg == 'javascript':
					if kw.value.id == 'True':
						self._with_js = True
						writer.with_javascript = True
					elif kw.value.id == 'False':
						self._with_js = False
						writer.with_javascript = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'dart':
					if kw.value.id == 'True':
						self._with_dart = True
					elif kw.value.id == 'False':
						self._with_dart = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'coffee':
					if kw.value.id == 'True':
						self._with_coffee = True
					elif kw.value.id == 'False':
						self._with_coffee = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'lua':
					if kw.value.id == 'True':
						self._with_lua = True
					elif kw.value.id == 'False':
						self._with_lua = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'inline_functions':
					if kw.value.id == 'True':
						self._with_inline = True
					elif kw.value.id == 'False':
						self._with_inline = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'runtime_exceptions':
					if kw.value.id == 'True':
						self._with_runtime_exceptions = True
					elif kw.value.id == 'False':
						self._with_runtime_exceptions = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'direct_keys':
					if kw.value.id == 'True':
						self._with_direct_keys = True
					elif kw.value.id == 'False':
						self._with_direct_keys = False
					else:
						raise SyntaxError( self.format_error(node) )

				elif kw.arg == 'direct_operator':
					if kw.value.s.lower() == 'none':
						self._direct_operators = set()
					else:
						self._direct_operators.add( kw.value.s )

				else:
					raise SyntaxError( self.format_error('invalid keyword option') )

		elif self._with_ll or name == 'inline' or self._with_glsl:
			F = self.visit(node.func)
			args = [self.visit(arg) for arg in node.args]
			if hasattr(self, '_in_gpu_method') and self._in_gpu_method and isinstance(node.func, ast.Attribute):
				fv = self.visit(node.func.value)
				if fv == 'self':
					clsname = self._in_gpu_method
					args.insert(0, 'self')
				else:
					fvt = fv.split('.')[-1]
					clsname = self._typedef_vars[ fvt ]
					args.insert(0, fv)

				F = '%s_%s' %(clsname, node.func.attr)

			elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id in self._typedef_vars:
				#raise RuntimeError(node.func.value.id)
				clsname = self._typedef_vars[ node.func.value.id ]
				F = '%s_%s' %(clsname, node.func.attr)
				args.insert(0, node.func.value.id)


			if node.keywords:
				args.extend( [self.visit(x.value) for x in node.keywords] )
				return '%s(%s)' %( F, ','.join(args) )

			else:
				return '%s(%s)' %( F, ','.join(args) )

		elif self._with_go:
			args = list( map(self.visit, node.args) )
			if node.keywords:
				args.extend( ['%s=%s'%(x.arg,self.visit(x.value)) for x in node.keywords] )
			if node.starargs:
				args.append('*%s' %self.visit(node.starargs))

			if isinstance(node.func, Name) and node.func.id in self._js_classes:
				return '__new__%s(%s)' %( self.visit(node.func), ','.join(args) )
			else:
				return '%s(%s)' %( self.visit(node.func), ','.join(args) )

		elif self._with_js or self._with_dart:
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

			elif name == 'new':
				assert len(args) == 1
				return 'new(%s)' %args[0]

			elif name == 'isinstance':
				assert len(args) == 2
				if args[1] == 'dict':
					args[1] = 'Object'  ## this fails when testing "isinstance(a, dict)==False" when a is an instance of some class.
				elif args[1] == 'list':
					args[1] = 'Array'
				return 'instanceof(%s, %s)' %(args[0], args[1])

			elif isinstance(node.func, ast.Attribute) and not self._with_dart:  ## special method calls
				anode = node.func
				self._in_assign_target = True
				method = self.visit( node.func )
				self._in_assign_target = False
				if anode.attr == 'get' and len(args) > 0 and len(args) <= 2:
					return '__jsdict_get(%s, %s)' %(self.visit(anode.value), ','.join(args) )

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

				elif anode.attr == 'sort' and not args:
					return '__sort_method(%s)' %self.visit(anode.value)

				elif anode.attr == 'replace' and len(node.args)==2:
					return '__replace_method(%s, %s)' %(self.visit(anode.value), ','.join(args) )

				else:
					ctx = '.'.join( self.visit(node.func).split('.')[:-1] )
					if node.keywords:
						kwargs = [ '%s:%s'%(x.arg, self.visit(x.value)) for x in node.keywords ]

						if args:
							if node.starargs:
								a = ( method, ctx, ','.join(args), self.visit(node.starargs), ','.join(kwargs) )
								## note: this depends on the fact that [].extend in PythonJS returns self (this),
								## which is different from regular python where list.extend returns None
								return '%s.apply( %s, [].extend([%s]).extend(%s).append({%s}) )' %a
							else:
								return '%s(%s, {%s})' %( method, ','.join(args), ','.join(kwargs) )

						else:
							if node.starargs:
								a = ( self.visit(node.func),ctx, self.visit(node.starargs), ','.join(kwargs) )
								return '%s.apply(%s, [].extend(%s).append({%s}) )' %a

							else:
								return '%s({%s})' %( method, ','.join(kwargs) )

					else:
						if node.starargs:
							a = ( self.visit(node.func), ctx, ','.join(args), self.visit(node.starargs) )
							return '%s.apply(%s, [].extend([%s]).extend(%s))' %a

						else:
							return '%s(%s)' %( method, ','.join(args) )


			elif isinstance(node.func, Name) and node.func.id in self._js_classes:
				if node.keywords:
					kwargs = [ '%s:%s'%(x.arg, self.visit(x.value)) for x in node.keywords ]
					if args:
						a = ','.join(args)
						return 'new( %s(%s, {%s}) )' %( self.visit(node.func), a, ','.join(kwargs) )
					else:
						return 'new( %s({%s}) )' %( self.visit(node.func), ','.join(kwargs) )
				else:
					if node.kwargs:
						args.append( self.visit(node.kwargs) )

					a = ','.join(args)
					return 'new( %s(%s) )' %( self.visit(node.func), a )

			elif name in self._global_functions and self._with_inline and not self._with_lua:
				return self.inline_function( node )

			elif self._with_dart:  ## ------------------ DART --------------------------------------

				if isinstance(node.func, ast.Attribute):  ## special method calls
					anode = node.func
					self._in_assign_target = True
					method = self.visit( node.func )
					self._in_assign_target = False

					if anode.attr == 'replace' and len(node.args)==2:
						return '__replace_method(%s, %s)' %(self.visit(anode.value), ','.join(args) )
					elif anode.attr == 'split' and len(node.args)==0:
						return '__split_method(%s)' %self.visit(anode.value)
					elif anode.attr == 'upper' and len(node.args)==0:
						return '__upper_method(%s)' %self.visit(anode.value)
					elif anode.attr == 'lower' and len(node.args)==0:
						return '__lower_method(%s)' %self.visit(anode.value)

				## default ##
				if node.keywords:
					kwargs = ','.join( ['%s=%s'%(x.arg, self.visit(x.value)) for x in node.keywords] )
					if args:
						return '%s(%s, %s)' %( self.visit(node.func), ','.join(args), kwargs )
					else:
						return '%s( %s )' %( self.visit(node.func), kwargs )

				else:
					a = ','.join(args)
					return '%s(%s)' %( self.visit(node.func), a )

			else:  ## ----------------------------- javascript mode ------------------------
				if node.keywords:
					kwargs = [ '%s:%s'%(x.arg, self.visit(x.value)) for x in node.keywords ]
					if args:
						if node.starargs:
							a = ( self.visit(node.func), self.visit(node.func), ','.join(args), self.visit(node.starargs), ','.join(kwargs) )
							return '%s.apply( %s, [].extend([%s]).extend(%s).append({%s}) )' %a
						else:
							return '%s(%s, {%s})' %( self.visit(node.func), ','.join(args), ','.join(kwargs) )
					else:
						if node.starargs:
							a = ( self.visit(node.func),self.visit(node.func), self.visit(node.starargs), ','.join(kwargs) )
							return '%s.apply(%s, [].extend(%s).append({%s}) )' %a
						else:
							func_name = self.visit(node.func)
							if func_name == 'dict':
								return '{%s}' %','.join(kwargs)
							else:
								return '%s({%s})' %( func_name, ','.join(kwargs) )

				else:
					if node.starargs:
						a = ( self.visit(node.func), self.visit(node.func), ','.join(args), self.visit(node.starargs) )
						return '%s.apply(%s, [].extend([%s]).extend(%s))' %a
					else:
						return '%s(%s)' %( self.visit(node.func), ','.join(args) )


		elif isinstance(node.func, Name) and node.func.id in self._generator_functions:
			args = list( map(self.visit, node.args) )
			if name in self._generator_functions:
				return 'JS("new %s(%s)")' %(name, ','.join(args))

		elif name == 'new':
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
			if isinstance(node.func, ast.Attribute) and node.func.attr in ('get', 'keys', 'values', 'pop', 'items', 'split', 'replace', 'sort') and not self._with_lua:
				anode = node.func
				if anode.attr == 'get' and len(node.args) > 0 and len(node.args) <= 2:
					return '__jsdict_get(%s, %s)' %(self.visit(anode.value), args )

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

				elif anode.attr == 'sort' and not args:
					return '__sort_method(%s)' %self.visit(anode.value)

				elif anode.attr == 'split' and len(node.args) <= 1:
					if not args:
						return '__split_method(%s)' %self.visit(anode.value)
					else:
						return '__split_method(%s, %s)' %(self.visit(anode.value), args)

				elif anode.attr == 'replace' and len(node.args)==2:
					return '__replace_method(%s, %s)' %(self.visit(anode.value), args )

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
					return '%s([%s], {%s})' %(name, args, kwargs)
				elif args:
					return '%s([%s], __NULL_OBJECT__)' %(name,args)
				elif kwargs:
					return '%s([], {%s})' %(name,kwargs)
				else:
					return '%s()' %name

			elif name in self._global_functions and self._with_inline and not self._with_lua:
				return self.inline_function( node )

			elif call_has_args_only:
				if name in self._global_functions:
					return '%s( [%s], __NULL_OBJECT__)' %(name,args)
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

		##'__INLINE_FUNCTION__' from typedpython.py

		if hasattr(node, 'keep_as_lambda') or args and args[0]=='__INLINE_FUNCTION__':
			## TODO lambda keyword args
			self._in_lambda = True
			a = '(lambda %s: %s)' %(','.join(args), self.visit(node.body))
			self._in_lambda = False
			return a
		else:
			node.name = '__lambda__'
			node.decorator_list = []
			node.body = [node.body]
			b = node.body[-1]
			node.body[-1] = ast.Return( b )
			return self.visit_FunctionDef(node)

	def visit_FunctionDef(self, node):
		global writer

		if node in self._generator_function_nodes:
			log('generator function: %s'%node.name)
			self._generator_functions.add( node.name )
			if '--native-yield' in sys.argv:
				raise NotImplementedError  ## TODO
			else:
				GeneratorFunctionTransformer( node, compiler=self )
				return

		writer.functions.append(node.name)

		is_worker_entry = False
		property_decorator = None
		decorators = []
		with_js_decorators = []
		with_dart_decorators = []
		setter = False
		return_type = None
		return_type_keywords = {}
		fastdef = False
		javascript = False
		inline = False
		threaded = self._with_webworker
		jsfile = None

		self._typedef_vars = dict()  ## clear typed variables: filled in below by @typedef or in visit_Assign
		self._gpu_return_types = set()
		gpu = False
		gpu_main = False
		gpu_vectorize = False
		gpu_method = False
		local_typedefs = []
		typedef_chans = []
		func_expr = None

		## deprecated?
		self._cached_property = None
		self._func_typedefs = {}

		if writer.is_at_global_level() and not self._with_webworker and not self._with_glsl:
			self._global_functions[ node.name ] = node  ## save ast-node

		for decorator in reversed(node.decorator_list):
			log('@decorator: %s' %decorator)
			if isinstance(decorator, Name) and decorator.id == 'gpu':
				gpu = True

			elif isinstance(decorator, Call) and decorator.func.id == 'expression':
				assert len(decorator.args)==1
				func_expr = self.visit(decorator.args[0])

			elif isinstance(decorator, Call) and decorator.func.id in ('typedef', 'typedef_chan'):
				c = decorator
				assert len(c.args) == 0 and len(c.keywords)
				for kw in c.keywords:
					#assert isinstance( kw.value, Name)
					kwval = self.visit(kw.value)
					self._typedef_vars[ kw.arg ] = kwval
					self._instances[ kw.arg ] = kwval
					self._func_typedefs[ kw.arg ] = kwval
					local_typedefs.append( '%s=%s' %(kw.arg, kwval))
					if decorator.func.id=='typedef_chan':
						typedef_chans.append( kw.arg )
						writer.write('@__typedef_chan__(%s=%s)' %(kw.arg, kwval))
					else:
						writer.write('@__typedef__(%s=%s)' %(kw.arg, kwval))


			elif isinstance(decorator, Name) and decorator.id == 'inline':
				inline = True
				self._with_inline = True

			elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == 'webworker':
				if not self._with_dart:
					threaded = True
					assert len(decorator.args) == 1
					jsfile = decorator.args[0].s

			elif isinstance(decorator, Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == 'returns':
				if decorator.keywords:
					for k in decorator.keywords:
						key = k.arg
						assert key == 'array' or key == 'vec4'
						self._gpu_return_types.add(key)  ## used in visit_Return ##
						return_type_keywords[ key ] = self.visit(k.value)

				else:
					assert len(decorator.args) == 1
					assert isinstance( decorator.args[0], Name)
					return_type = decorator.args[0].id
					if return_type in typedpython.glsl_types:
						self._gpu_return_types.add( return_type )

			elif isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id == 'gpu':
				gpu = True
				if decorator.attr == 'vectorize':
					gpu_vectorize = True
				elif decorator.attr == 'main':
					gpu_main = True
				elif decorator.attr == 'method':
					gpu_method = True
				else:
					raise NotImplementedError(decorator)

			elif self._with_dart:
				with_dart_decorators.append( self.visit(decorator) )

			elif self._with_js:  ## decorators are special in with-js mode
				self._in_assign_target = True
				with_js_decorators.append( self.visit( decorator ) )
				self._in_assign_target = False

			elif isinstance(decorator, Name) and decorator.id == 'fastdef':
				fastdef = True

			elif isinstance(decorator, Name) and decorator.id == 'javascript':
				javascript = True

			elif isinstance(decorator, Name) and decorator.id == 'property':
				property_decorator = decorator
				n = node.name + '__getprop__'
				self._decorator_properties[ node.original_name ] = dict( get=n, set=None )
				node.name = n
				#if decorator.id == 'cached_property':  ## TODO DEPRECATE
				#	self._cached_property = node.original_name

			elif isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id in self._decorator_properties:
				if decorator.attr == 'setter':
					if self._decorator_properties[ decorator.value.id ]['set']:
						raise SyntaxError( self.format_error("decorator.setter is used more than once") )
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


			else:
				decorators.append( decorator )


		if gpu:
			restore_with_glsl = self._with_glsl
			self._with_glsl = True
			if gpu_main:  ## sets float
				self._in_gpu_main = True
				writer.write('@gpu.main')



		if threaded:
			if not jsfile: jsfile = 'worker.js'
			writer_main.write('%s = "%s"' %(node.name, jsfile))
			self._webworker_functions[ node.name ] = jsfile

			writer = get_webworker_writer( jsfile )
			if len(writer.functions) <= 1:
				is_worker_entry = True
				## TODO: two-way list and dict sync
				writer.write('__wargs__ = []')
				writer.write('def onmessage(e):')
				writer.push()
				## need a better way to quit the worker after work is done, check if threading._blocking_callback is waiting, else terminate
				writer.write(  'if e.data.type=="execute":' )
				writer.push()
				writer.write(		'%s.apply(self, e.data.args)'%node.name )
				writer.write(		'if not threading._blocking_callback: self.postMessage({"type":"terminate"})')
				writer.pull()
				writer.write(  'elif e.data.type=="append": __wargs__[ e.data.argindex ].push( e.data.value )' )
				writer.write(  'elif e.data.type=="__setitem__": __wargs__[ e.data.argindex ][e.data.key] = e.data.value' )
				writer.write(  'elif e.data.type=="return_to_blocking_callback": threading._blocking_callback( e.data.result )' )
				#writer.push()
				#writer.write(		'if instanceof(__wargs__[e.data.argindex], Array): __wargs__[ e.data.argindex ][e.data.key] = e.data.value')
				#writer.write(		'else: __wargs__[ e.data.argindex ][e.data.key] = e.data.value')
				#writer.pull()

				writer.pull()
				writer.write('self.onmessage = onmessage' )



		## force python variable scope, and pass user type information to second stage of translation.
		## the dart backend can use this extra type information for speed and debugging.
		## the Go and GLSL backends require this extra type information.
		vars = []
		local_typedef_names = set()
		if not self._with_coffee:
			try:
				local_vars, global_vars = retrieve_vars(node.body)
			except SyntaxError as err:
				raise SyntaxError( self.format_error(err) )

			local_vars = local_vars-global_vars
			inlined_long = False
			if local_vars:
				args_typedefs = []
				args = [ a.id for a in node.args.args ]

				for v in local_vars:
					usertype = None
					if '=' in v:
						t,n = v.split('=')  ## unpack type and name
						if self._with_dart and t in typedpython.simd_types:
							t = t[0].upper() + t[1:]
						v = '%s=%s' %(n,t)  ## reverse
						local_typedef_names.add( n )
						if t == 'long' and inlined_long == False:
							inlined_long = True
							writer.write('''inline("if (__NODEJS__==true) var long = require('long')")''')  ## this is ugly

						if n in args:
							args_typedefs.append( v )
						else:
							local_typedefs.append( v )
					elif v in args or v in local_typedef_names: pass
					else: vars.append( v )

				if args_typedefs:
					writer.write('@__typedef__(%s)' %','.join(args_typedefs))

		if func_expr:
			writer.write('@expression(%s)' %func_expr)


		if not self._with_dart and not self._with_lua and not self._with_js and not javascript and not self._with_glsl:
			writer.write('@__pyfunction__')

		if return_type or return_type_keywords:
			if return_type_keywords and return_type:
				kw = ['%s=%s' %(k,v) for k,v in return_type_keywords.items()]
				writer.write('@returns(%s, %s)' %(return_type,','.join(kw)) )
			elif return_type_keywords:
				writer.write('@returns(%s)' %','.join( ['%s=%s' %(k,v) for k,v in return_type_keywords.items()] ))
			else:
				writer.write('@returns(%s)' %return_type)

		if gpu_vectorize:
			writer.write('@gpu.vectorize')
		if gpu_method:
			writer.write('@gpu.method')


		if self._with_dart:
			## dart supports optional positional params [x=1, y=2], or optional named {x:1, y:2}
			## but not both at the same time.
			if node.args.kwarg:
				raise SyntaxError( self.format_error('dart functions can not take variable keyword arguments (**kwargs)' ) )

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
					raise SyntaxError( self.format_error('dart functions can not use variable arguments (*args) and have keyword arguments' ) )

				args.append('__variable_args__%s' %node.args.vararg)

			writer.write( 'def %s( %s ):' % (node.name, ','.join(args)) )

		elif self._with_go:

			args = []
			offset = len(node.args.args) - len(node.args.defaults)
			for i, arg in enumerate(node.args.args):
				a = arg.id
				dindex = i - offset
				if dindex >= 0 and node.args.defaults:
					default = self.visit(node.args.defaults[dindex])
					args.append( '%s=%s' %(a, default))
				else:
					args.append( a )

			if node.args.vararg:
				args.append( '*%s' %node.args.vararg )

			writer.write( 'def %s( %s ):' % (node.name, ','.join(args)) )


		elif self._with_js or javascript or self._with_ll or self._with_glsl or self._with_go:

			if self._with_glsl:
				writer.write('@__glsl__')

			if node.args.vararg:
				#raise SyntaxError( 'pure javascript functions can not take variable arguments (*args)' )
				writer.write('#WARNING - NOT IMPLEMENTED: javascript-mode functions with (*args)')
			kwargs_name = node.args.kwarg or '_kwargs_'

			args = []
			offset = len(node.args.args) - len(node.args.defaults)
			for i, arg in enumerate(node.args.args):
				a = arg.id
				dindex = i - offset
				if dindex >= 0 and node.args.defaults:
					pass
				else:
					args.append( a )

			if len(node.args.defaults) or node.args.kwarg:
				if args:
					writer.write( 'def %s( %s, %s ):' % (node.name, ','.join(args), kwargs_name ) )
				else:
					writer.write( 'def %s( %s ):' % (node.name, kwargs_name) )
			else:
				writer.write( 'def %s( %s ):' % (node.name, ','.join(args)) )

		else:
			if len(node.args.defaults) or node.args.kwarg or len(node.args.args) or node.args.vararg:
				writer.write('def %s(args, kwargs):' % node.name)
			else:
				writer.write('def %s():' % node.name)

		writer.push()

		## write local typedefs and var scope ##
		a = ','.join( vars )
		if local_typedefs:
			if a: a += ','
			a += ','.join(local_typedefs)
		writer.write('var(%s)' %a)

		#####################################################################
		if self._with_dart or self._with_glsl or self._with_go:
			pass

		elif self._with_js or javascript or self._with_ll:
			if node.args.defaults:
				kwargs_name = node.args.kwarg or '_kwargs_'
				lines = [ 'if (!( %s instanceof Object )) {' %kwargs_name ]
				a = ','.join( ['%s: arguments[%s]' %(arg.id, i) for i,arg in enumerate(node.args.args)] )
				lines.append( 'var %s = {%s}' %(kwargs_name, a))
				lines.append( '}')
				for a in lines:
					writer.write("JS('''%s''')" %a)

				offset = len(node.args.args) - len(node.args.defaults)
				for i, arg in enumerate(node.args.args):
					dindex = i - offset
					if dindex >= 0:
						default_value = self.visit( node.args.defaults[dindex] )
						a = (kwargs_name, kwargs_name, arg.id, arg.id, default_value, arg.id, kwargs_name, arg.id)
						b = "if (%s === undefined || %s.%s === undefined) {var %s = %s} else {var %s=%s.%s}" %a
						c = "JS('''%s''')" %b
						writer.write( c )

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
			signature = ', '.join(map(lambda x: '%s:%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
			writer.write('__sig__ = {%s}' % signature)

			# First check the arguments are well formed 
			# ie. that this function is not a callback of javascript code

			if not self._with_go:
				writer.write("""if instanceof(args,Array) and Object.prototype.toString.call(kwargs) == '[object Object]' and arguments.length==2:""")
				writer.push()
				writer.write('pass')  # do nothing if it's not called from javascript
				writer.pull()

				writer.write('else:')
				writer.push()
				# If it's the case, move use ``arguments`` to ``args`` 
				writer.write('args = Array.prototype.slice.call(arguments, 0, __sig__.args.length)')
				# This means you can't pass keyword argument from javascript but we already knew that
				writer.write('kwargs = JSObject()')
				writer.pull()



			writer.write('__args__ = __getargs__("%s", __sig__, args, kwargs)' %node.name)
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


		if threaded and is_worker_entry:
			for i,arg in enumerate(node.args.args):
				writer.write( '%s = __webworker_wrap(%s, %s)' %(arg.id, arg.id, i))
				writer.write('__wargs__.push(%s)'%arg.id)

		#if self._cached_property:  ## DEPRECATED
		#	writer.write('if self["__dict__"]["%s"]: return self["__dict__"]["%s"]' %(self._cached_property, self._cached_property))

		self._return_type = None # tries to catch a return type in visit_Return

		## write function body ##
		## if sleep() is called or a new webworker is started, the following function body must be wrapped in
		## a closure callback and called later by setTimeout 
		timeouts = []
		#continues = []
		for b in node.body:

			if self._use_threading and isinstance(b, ast.Assign) and isinstance(b.value, ast.Call): 
				if isinstance(b.value.func, ast.Attribute) and isinstance(b.value.func.value, Name) and b.value.func.value.id == 'threading':
					if b.value.func.attr == 'start_new_thread':
						self.visit(b)
						writer.write('__run__ = True')
						writer.write('def __callback%s():' %len(timeouts))
						writer.push()
						## workerjs for nodejs requires at least 100ms to initalize onmessage/postMessage
						timeouts.append(0.2)
						continue
					elif b.value.func.attr == 'start_webworker':
						self.visit(b)
						writer.write('__run__ = True')
						writer.write('def __callback%s():' %len(timeouts))
						writer.push()
						## workerjs for nodejs requires at least 100ms to initalize onmessage/postMessage
						timeouts.append(0.2)
						continue

				elif self._with_webworker and isinstance(b, ast.Assign) and isinstance(b.value, ast.Call) and isinstance(b.value.func, ast.Name) and b.value.func.id in self._global_functions:
					#assert b.value.calling_from_worker
					#raise SyntaxError(b)
					self.visit(b)
					writer.write('def __blocking( %s ):' %self.visit(b.targets[0]))
					writer.push()
					timeouts.append('BLOCKING')
					continue


			elif self._use_sleep:
				c = b
				if isinstance(b, ast.Expr):
					b = b.value

				if isinstance(b, ast.Call) and isinstance(b.func, ast.Name) and b.func.id == 'sleep':
					writer.write('__run__ = True')
					writer.write('def __callback%s():' %len(timeouts))
					writer.push()
					timeouts.append( self.visit(b.args[0]) )
					continue

				elif isinstance(b, ast.While):  ## TODO
					has_sleep = False
					for bb in b.body:
						if isinstance(bb, ast.Expr):
							bb = bb.value
						if isinstance(bb, ast.Call) and isinstance(bb.func, ast.Name) and bb.func.id == 'sleep':
							has_sleep = float(self.visit(bb.args[0]))

					if has_sleep > 0.0:
						has_sleep = int(has_sleep*1000)
						#writer.write('__run_while__ = True')
						writer.write('__continue__ = True')
						writer.write('def __while():')
						writer.push()

						for bb in b.body:
							if isinstance(bb, ast.Expr):
								bb = bb.value
							if isinstance(bb, ast.Call) and isinstance(bb.func, ast.Name) and bb.func.id == 'sleep':
								continue
								#TODO - split body and generate new callback - now sleep is only valid at the end of the while loop

							else:
								e = self.visit(bb)
								if e: writer.write( e )

						writer.write( 'if %s: __run_while__ = True' %self.visit(b.test))
						writer.write( 'else: __run_while__ = False')

						writer.write('if __run_while__: setTimeout(__while, %s)' %(has_sleep))
						writer.write('elif __continue__: setTimeout(__callback%s, 0)' %len(timeouts))

						writer.pull()

						writer.write('setTimeout(__while, 0)')
						writer.write('__run__ = True')
						writer.write('def __callback%s():' %len(timeouts))
						writer.push()
						timeouts.append(None)
						continue

					else:
						self.visit(b)

					continue

				b = c  ## replace orig b

			self.visit(b)

		i = len(timeouts)-1
		while timeouts:
			ms = timeouts.pop()
			if ms == 'BLOCKING':
				writer.write(	'threading._blocking_callback = None')
				writer.pull()
				writer.write('threading._blocking_callback = __blocking')
			elif ms is not None:
				writer.pull()

				ms = float(ms)
				ms *= 1000
				writer.write('if __run__: setTimeout(__callback%s, %s)' %(i, ms))
				writer.write('elif __continue__: setTimeout(__callback%s, %s)' %(i+1, ms))
			i -= 1

		if self._return_type:       ## check if a return type was caught
			if return_type:
				assert return_type == self._return_type
			else:
				return_type = self._return_type
			self._function_return_types[ node.name ] = self._return_type
		self._return_type = None


		############################################################
		### DEPRECATED
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
		############################################################

		writer.pull()  ## end function body

		#if not self._with_dart and not self._with_lua and not self._with_js and not javascript and not self._with_glsl:
		#	writer.write('%s.pythonscript_function=True'%node.name)


		if gpu:
			self._with_glsl = restore_with_glsl
			if gpu_main:
				self._in_gpu_main = False

		self._typedef_vars = dict()  ## clear typed variables

		if inline:
			self._with_inline = False

		if self._in_js_class:
			writer = writer_main
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
			if self._introspective_functions:
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



		if self._with_js and with_js_decorators:
			for dec in with_js_decorators:
				if '.prototype.' in dec:
					## these with-js functions are assigned to a some objects prototype,
					## here we assume that they depend on the special "this" variable,
					## therefore this function can not be marked as f.pythonscript_function,
					## because we need __get__(f,'__call__') to dynamically bind "this"
					#writer.write( '%s=%s'%(dec,node.name) )

					## TODO - @XXX.prototype.YYY sets properties with enumerable as False,
					## this fixes external javascript that is using `for (var i in anArray)`
					head, tail = dec.split('.prototype.')
					a = (head, tail, node.name)
					## these props need to be writeable so that webworkers can redefine methods like: push, __setitem__
					## note to overwrite one of these props Object.defineProperty needs to be called again (ob.xxx=yyy will not work)
					writer.write('Object.defineProperty(%s.prototype, "%s", {enumerable:False, value:%s, writeable:True, configurable:True})' %a)

				elif dec == 'javascript':
					pass
				elif dec == 'fastdef':
					pass
				else:
					## TODO: check ifdecorators in javascript mode are working properly
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

		#if threaded:
		#	writer.write('%s()' %node.name)
		#	writer.write('self.termintate()')


		writer = writer_main


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
		if self._in_loop_with_else:
			writer.write('__break__ = True')
		writer.write('break')

	def visit_For(self, node):
		if node.orelse:
			raise SyntaxError( self.format_error('the syntax for/else is deprecated') )

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

		if self._with_glsl or self._with_go:
			writer.write( 'for %s in %s:' %(self.visit(node.target), self.visit(node.iter)) )
			writer.push()
			map(self.visit, node.body)
			writer.pull()
			return None

		if self._with_rpc_name and isinstance(node.iter, ast.Attribute) and isinstance(node.iter.value, ast.Name) and node.iter.value.id == self._with_rpc_name:
			target = self.visit(node.target)
			writer.write('def __rpc_loop__():')
			writer.push()
			writer.write(	'%s = __rpc_iter__(%s, "%s")' %(target, self._with_rpc, node.iter.attr) )
			writer.write(	'if %s == "__STOP_ITERATION__": __continue__()' %target)
			writer.write(	'else:')
			writer.push()
			map( 				self.visit, node.body )
			writer.write(		'__rpc_loop__()')
			writer.pull()
			writer.pull()
			writer.write('__rpc_loop__()')

			writer.write('def __continue__():')  ## because this def comes after, it needs to be `hoisted` up by the javascript VM
			writer.push()
			return None


		iterid = self._iter_ids
		self._iter_ids += 1

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
			vars.append( '__mtarget__%s' %iterid)
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
				writer.write('var(%s, %s__end__)' %(iter_name, iter_name))
				writer.write('%s = %s' %(iter_name, iter_start))
				writer.write('%s__end__ = %s' %(iter_name, iter_end))
				writer.write('while %s < %s__end__:' %(iter_name, iter_name))

				writer.push()
				map(self.visit, node.body)
				writer.write('%s += 1' %iter_name )

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()

			elif isinstance(iter, ast.Call) and isinstance(iter.func, Name) and iter.func.id in self._generator_functions:
				iter_name = self.visit(target)
				writer.write('var(%s, __generator__%s)' %(iter_name,iterid))
				writer.write('__generator__%s = %s' %(iterid,self.visit(iter)))
				writer.write('while __generator__%s.__done__ != 1:'%iterid)
				writer.push()
				writer.write('%s = __generator__%s.next()'%(iter_name,iterid))
				map(self.visit, node.body)
				writer.pull()

			else:
				if multi_target:
					writer.write('var(%s)' % ','.join(vars))
					writer.write('for __mtarget__%s in %s:' %(iterid,self.visit(iter)))
					writer.push()
					for i,elt in enumerate(multi_target):
						writer.write('%s = __mtarget__%s[%s]' %(elt,iterid,i))

				else:
					a = self.visit(target)
					self._in_assign_target = True
					b = self.visit(iter)
					self._in_assign_target = False
					writer.write('for %s in %s:' %(a, b))
					writer.push()


				map(self.visit, node.body)

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()
		else:

			## TODO else remove node.target.id from self._instances
			if isinstance(iter, Name) and iter.id in self._global_typed_lists:
				self._instances[ target.id ] = list( self._global_typed_lists[ iter.id ] )[0]


			vars.append('__iterator__%s'%iterid)
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
				if hasattr(node, 'lineno'):
					src = self._source[ node.lineno-1 ]
					src = src.replace('"', '\\"')
					err = 'no iterator - line %s: %s'	%(node.lineno, src.strip())
					writer.write('__iterator__%s = __get__(__get__(%s, "__iter__", "%s"), "__call__")([], __NULL_OBJECT__)' %(iterid, self.visit(iter), err))

				else:
					writer.write('__iterator__%s = __get__(__get__(%s, "__iter__"), "__call__")([], __NULL_OBJECT__)' %(iterid, self.visit(iter)))

			if is_generator:
				iter_name = self.visit(target)
				if not self._with_coffee:
					writer.write('var(%s, __generator__%s)' %(iter_name, iterid))
				writer.write('__generator__%s = %s' %(iterid,self.visit(iter)))
				writer.write('while __generator__%s.__done__ != 1:'%iterid)
				writer.push()
				writer.write('%s = __generator__%s.next()'%(iter_name,iterid))
				map(self.visit, node.body)
				writer.pull()


			elif is_range:
				iter_name = target.id
				if not self._with_coffee:
					writer.write('var(%s, %s__end__)' %(iter_name, iter_name))
				writer.write('%s = %s' %(iter_name, iter_start))
				writer.write('%s__end__ = %s' %(iter_name, iter_end))   ## assign to a temp variable.
				#writer.write('while %s < %s:' %(iter_name, iter_end))  ## this fails with the ternary __add_op
				writer.write('while %s < %s__end__:' %(iter_name, iter_name))

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
					writer.write('var(__next__%s)'%iterid)
				writer.write('__next__%s = __get__(__iterator__%s, "next")'%(iterid,iterid))
				writer.write('while __iterator__%s.index < __iterator__%s.length:'%(iterid,iterid))

				writer.push()

				if multi_target:
					writer.write('__mtarget__%s = __next__%s()'%(iterid, iterid))
					for i,elt in enumerate(multi_target):
						if self._with_lua:
							writer.write('%s = __mtarget__%s[...][%s]' %(elt,iterid,i+1))
						else:
							writer.write('%s = __mtarget__%s[%s]' %(elt,iterid,i))
				else:
					writer.write('%s = __next__%s()' %(target.id, iterid))

				map(self.visit, node.body)

				if enumtar:
					writer.write('%s += 1'%enumtar.id)

				writer.pull()
	
			return ''

	_call_ids = 0
	def visit_While(self, node):
		if self._cache_while_body_calls:  ## TODO add option for this
			for n in node.body:
				calls = collect_calls(n)
				for c in calls:
					if isinstance(c.func, ast.Name):  ## these are constant for sure
						i = self._call_ids
						writer.write( '__call__%s = __get__(%s,"__call__")' %(i,self.visit(c.func)) )
						c.func.id = '__call__%s'%i
						c.constant = True
						self._call_ids += 1

		if node.orelse:
			raise SyntaxError( self.format_error('the syntax while/else is deprecated'))
			self._in_loop_with_else = True
			writer.write('var(__break__)')
			writer.write('__break__ = False')

		self._in_while_test = True
		writer.write('while %s:' % self.visit(node.test))
		self._in_while_test = False
		writer.push()
		map(self.visit, node.body)
		writer.pull()

		if node.orelse:
			self._in_loop_with_else = False
			writer.write('if __break__ == False:')
			writer.push()
			map(self.visit, node.orelse)
			writer.pull()

	def visit_With(self, node):
		global writer

		if isinstance( node.context_expr, Name ) and node.context_expr.id == 'glsl':
			if not isinstance(node.optional_vars, ast.Name):
				raise SyntaxError( self.format_error('wrapper function name must be given: `with glsl as myfunc:`') )
			main_func = None
			writer.inline_glsl = True
			self._with_glsl = True
			for b in node.body:
				if isinstance(b, ast.FunctionDef) and b.name == 'main':
					main_func = True
					writer.write('@__glsl__.%s' %node.optional_vars.id)
				a = self.visit(b)
				if a: writer.write(a)
			self._with_glsl = False
			writer.inline_glsl = False
			if not main_func:
				raise SyntaxError( self.format_error('a function named `main` must be defined as the entry point for the shader program') )

		elif isinstance( node.context_expr, ast.Call ) and isinstance(node.context_expr.func, ast.Name) and node.context_expr.func.id == 'rpc':
			self._with_rpc = self.visit( node.context_expr.args[0] )
			if isinstance(node.optional_vars, ast.Name):
				self._with_rpc_name = node.optional_vars.id
			for b in node.body:
				a = self.visit(b)
				if a: writer.write(a)
			self._with_rpc = None
			self._with_rpc_name = None

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'webworker':
			self._with_webworker = True
			writer = get_webworker_writer( 'worker.js' )

			#writer.write('if typeof(process) != "undefined": requirejs = require("requirejs")')
			#writer.write('if typeof(process) != "undefined": requirejs = require')
			writer.write('if typeof(require) != "undefined": requirejs = require')  ## compatible with nodewebkit
			writer.write('else: importScripts("require.js")')

			for b in node.body:
				a = self.visit(b)
				if a: writer.write(a)
			self._with_webworker = False
			writer = writer_main

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'inline':
			writer.write('with inline:')
			writer.push()
			for b in node.body:
				a = self.visit(b)
				if a: writer.write(a)
			writer.pull()
		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'lowlevel':
			self._with_ll = True
			#map(self.visit, node.body)
			for b in node.body:
				a = self.visit(b)
				if a: writer.write(a)
			self._with_ll = False
		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'javascript':
			self._with_js = True
			map(self.visit, node.body)
			self._with_js = False
		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'python':
			if not self._with_js:
				raise SyntaxError('"with python:" is only used inside of a "with javascript:" block')
			self._with_js = False
			map(self.visit, node.body)
			self._with_js = True

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'fastdef':
			self._with_fastdef = True
			map(self.visit, node.body)
			self._with_fastdef = False

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'static':
			self._with_static_type = True
			map(self.visit, node.body)
			self._with_static_type = False

		elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'inline_function':
			self._with_inline = True
			map(self.visit, node.body)
			self._with_inline = False

		elif isinstance( node.context_expr, Name ) and node.context_expr.id in EXTRA_WITH_TYPES:
			writer.write('with %s:' %self.visit(node.context_expr))
			writer.push()
			for b in node.body:
				a = self.visit(b)
				if a: writer.write(a)
			writer.pull()

		elif isinstance( node.context_expr, ast.Call ) and isinstance(node.context_expr.func, ast.Name) and node.context_expr.func.id in EXTRA_WITH_TYPES:

			restore = self._with_js
			self._with_js = True
			if node.context_expr.keywords:
				assert len(node.context_expr.keywords)==1
				k = node.context_expr.keywords[0].arg
				v = self.visit(node.context_expr.keywords[0].value)
				a = 'with %s(%s=%s):' %( self.visit(node.context_expr.func), k,v )
				writer.write(a)
			else:
				writer.write('with %s:' %self.visit(node.context_expr))


			self._with_js = restore

			writer.push()
			for b in node.body:
				a = self.visit(b)
				if a: writer.write(a)
			writer.pull()

		else:
			raise SyntaxError('invalid use of "with" statement')

EXTRA_WITH_TYPES = ('__switch__', '__default__', '__case__', '__select__')

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
		assert '_stack' in dir(compiler)
		#self.__dict___ = compiler.__dict__  ## share all state
		for name in dir(compiler):
			if name not in dir(self):
				setattr(self, name, (getattr(compiler, name)))

		self._head_yield = False
		self.visit( node )
		compiler._addop_ids = self._addop_ids ## note: need to keep id index insync

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



def main(script, dart=False, coffee=False, lua=False, go=False, module_path=None):
	translator = PythonToPythonJS(
		source = script, 
		dart   = dart or '--dart' in sys.argv,
		coffee = coffee,
		lua    = lua,
		go     = go,
		module_path = module_path
	)

	code = writer.getvalue()

	if translator.has_webworkers():
		res = {'main':code}
		for jsfile in translator.get_webworker_file_names():
			res[ jsfile ] = get_webworker_writer( jsfile ).getvalue()
		return res
	else:
		if '--debug' in sys.argv:
			try:
				open('/tmp/python-to-pythonjs.debug.py', 'wb').write(code)
			except:
				pass
		return code



if __name__ == '__main__':
	## if run directly prints source transformed to python-js-subset, this is just for debugging ##
	scripts = []
	if len(sys.argv) > 1:
		argv = sys.argv[1:]
		for i,arg in enumerate(argv):
			if arg.endswith('.py'):
				scripts.append( arg )

	if len(scripts):
		a = []
		for script in scripts:
			a.append( open(script, 'rb').read() )
		data = '\n'.join( a )
	else:
		data = sys.stdin.read()


	compiler = PythonToPythonJS(
		source=data, 
		dart='--dart' in sys.argv
	)
	output = writer.getvalue()
	print( output )  ## pipe to stdout

#!/usr/bin/env python
# PythonJS to Go Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import os, sys
import ast
import pythonjs

go_types = 'bool string int float64'.split()

def transform_gopherjs( node ):
	gt = GopherjsTransformer()
	gt.visit( node )
	return node

class GopherjsTransformer( ast.NodeVisitor ):
	#def visit_Assign(self, node):
	#	writer.write( '%s.Set("%s", %s)' %(target_value, target.attr, self.visit(node.value)) )


	def visit_Attribute(self, node):
		#return '%s.Get("%s")' %(self.visit(node.value), node.attr)
		args = [ ast.Str(node.attr) ]
		f = ast.Call( ast.Name('Get', None), args, [], None, None )
		node.__dict__ = f.__dict__

	def visit_Call(self, node):
		#if isinstance(self._stack[-2], ast.Expr):
		#	pass
		#else:
		#	raise SyntaxError( self._stack )
		if isinstance(node.func, ast.Attribute):
			args = [ ast.Str(node.func.attr) ]
			args.extend( node.args )
			#f = ast.Call( ast.Name('Call', None), args, node.keywords, node.starargs, node.kwargs )
			#raise SyntaxError(node)

			f = ast.Call( ast.Name('__js_global_get_'+node.func.value.id, None), args, node.keywords, node.starargs, node.kwargs )

			#x = ast.Attribute( ast.Name('js',None), 'Global', None )
			#a = ast.Call( ast.Name('__js_global_get_',None), [ast.Str(node.func.value.id)], [], None, None )

			node.__dict__ = f.__dict__


class GoGenerator( pythonjs.JSGenerator ):

	def __init__(self, requirejs=False, insert_runtime=False):
		pythonjs.JSGenerator.__init__(self, requirejs=False, insert_runtime=False)

		self._with_gojs = False
		self._class_stack = list()
		self._classes = dict()		## name : node
		self._class_props = dict()

		self._vars = set()
		self._known_vars = set()
		self._kwargs_type_ = dict()

		self._imports = []
		self._ids = 0

	def visit_Is(self, node):
		return '=='
	def visit_IsNot(self, node):
		return '!='

	def visit_If(self, node):
		out = []
		test = self.visit(node.test)
		if test.startswith('(') and test.endswith(')'):
			out.append( 'if %s {' %test )
		else:
			out.append( 'if (%s) {' %test )

		self.push()

		for line in list(map(self.visit, node.body)):
			if line is None: continue
			out.append( self.indent() + line )

		orelse = []
		for line in list(map(self.visit, node.orelse)):
			orelse.append( self.indent() + line )

		self.pull()

		if orelse:
			out.append( self.indent() + '} else {')
			out.extend( orelse )

		out.append( self.indent() + '}' )

		return '\n'.join( out )

	def visit_Name(self, node):
		if node.id == 'None':
			return 'nil'
		elif node.id == 'True':
			return 'true'
		elif node.id == 'False':
			return 'false'
		#elif node.id == 'null':
		#	return 'nil'
		return node.id

	def visit_ClassDef(self, node):
		self._class_stack.append( node )
		node._parents = set()
		node._struct_def = dict()
		node._subclasses = set()  ## required for generics generator
		out = []
		sdef = dict()
		props = set()
		bases = set()
		base_classes = set()

		self._classes[ node.name ] = node
		self._class_props[ node.name ] = props


		for base in node.bases:
			n = self.visit(base)
			if n == 'object':
				continue
			node._parents.add( n )

			bases.add( n )
			if n in self._class_props:
				props.update( self._class_props[n] )
				base_classes.add( self._classes[n] )
			#else:  ## special case - subclassing a builtin like `list`
			#	continue

			for p in self._classes[ n ]._parents:
				bases.add( p )
				props.update( self._class_props[p] )
				base_classes.add( self._classes[p] )

			self._classes[ n ]._subclasses.add( node.name )


		for decor in node.decorator_list:  ## class decorators
			if isinstance(decor, ast.Call):
				assert decor.func.id=='__struct__'
				#props.update( [self.visit(a) for a in decor.args] )
				for kw in decor.keywords:
					props.add( kw.arg )
					T = kw.value.id
					if T == 'interface': T = 'interface{}'
					sdef[ kw.arg ] = T


		init = None
		method_names = set()
		for b in node.body:
			if isinstance(b, ast.FunctionDef):
				method_names.add( b.name )
				if b.name == '__init__':
					init = b
			elif isinstance(b, ast.Expr) and isinstance(b.value, ast.Dict):
				for i in range( len(b.value.keys) ):
					k = self.visit( b.value.keys[ i ] )
					if isinstance(b.value.values[i], ast.Str):
						v = b.value.values[i].s
					else:
						v = self.visit( b.value.values[i] )
					if v == 'interface': v = 'interface{}'
					sdef[k] = v

		node._struct_def.update( sdef )

		parent_init = None
		if base_classes:
			for bnode in base_classes:
				for b in bnode.body:
					if isinstance(b, ast.FunctionDef):
						if b.name in method_names:
							self.catch_call.add( '%s.%s' %(bnode.name, b.name))
							n = b.name
							b.name = '%s_%s'%(bnode.name, b.name)
							out.append( self.visit(b) )
							b.name = n
							continue
						if b.name == '__init__':
							parent_init = {'class':bnode, 'init':b}
							#continue
						out.append( self.visit(b) )


		out.append( 'type %s struct {' %node.name)
		if base_classes:
			for bnode in base_classes:
				## Go only needs the name of the parent struct and all its items are inserted automatically ##
				out.append('%s' %bnode.name)

		for name in sdef:
			out.append('%s %s' %(name, sdef[name]))
		out.append('}')


		for b in node.body:
			if isinstance(b, ast.FunctionDef):
				out.append( self.visit(b) )

		if init or parent_init:
			if parent_init:
				classname = parent_init['class'].name
				init = parent_init['init']
			else:
				classname = node.name

			out.append( 'func __new__%s( %s ) *%s {' %(node.name, init._args_signature, node.name))
			out.append( '  ob := %s{}' %node.name )
			out.append( '  ob.__init__(%s)' %','.join(init._arg_names))
			out.append( '  return &ob')
			out.append('}')

		else:
			out.append( 'func __new__%s() *%s { return &%s{} }' %(node.name, node.name, node.name))




		self.catch_call = set()
		self._class_stack.pop()
		return '\n'.join(out)


	def _visit_call_special( self, node ):
		fname = self.visit(node.func)
		assert fname in self.catch_call
		assert len(self._class_stack)
		if len(node.args):
			if isinstance(node.args[0], ast.Name) and node.args[0].id == 'self':
				node.args.remove( node.args[0] )

		#name = '_%s_' %self._class_stack[-1].name
		name = 'self.'
		name += fname.replace('.', '_')
		return self._visit_call_helper(node, force_name=name)


	def _visit_subscript_ellipsis(self, node):
		name = self.visit(node.value)
		#return '%s["$wrapped"]' %name
		raise NotImplementedError


	def visit_Subscript(self, node):
		if isinstance(node.slice, ast.Ellipsis):
			if self._glsl:
				#return '%s[_id_]' % self.visit(node.value)
				return '%s[matrix_index()]' % self.visit(node.value)
			else:
				return self._visit_subscript_ellipsis( node )
		else:
			## deference pointer and then index
			return '(*%s)[%s]' % (self.visit(node.value), self.visit(node.slice))


	def visit_Slice(self, node):
		lower = upper = step = None
		if node.lower:
			lower = self.visit(node.lower)
		if node.upper:
			upper = self.visit(node.upper)
		if node.step:
			step = self.visit(node.step)

		if lower and upper:
			return '%s:%s' %(lower,upper)
		elif upper:
			return ':%s' %upper
		elif lower:
			return '%s:'%lower
		else:
			raise SyntaxError('TODO slice')


	def visit_Print(self, node):
		r = []
		for e in node.values:
			s = self.visit(e)
			if isinstance(e, ast.List):
				r.append('fmt.Println(%s);' %s[1:-1])
			else:
				r.append('fmt.Println(%s);' %s)
		return ''.join(r)

	def visit_Expr(self, node):
		return self.visit(node.value)

	def visit_Import(self, node):
		r = [alias.name.replace('__SLASH__', '/') for alias in node.names]
		if r:
			for name in r:
				self._imports.append('import("%s");' %name)
		return ''

	def visit_Module(self, node):
		header = [
			'package main',
			'import "fmt"',
		]
		lines = []

		for b in node.body:
			line = self.visit(b)

			if line:
				for sub in line.splitlines():
					if sub==';':
						raise SyntaxError(line)
					else:
						lines.append( sub )
			else:
				if isinstance(b, ast.Import):
					pass
				else:
					raise SyntaxError(b)

		lines.append('type _kwargs_type_ struct {')
		for name in self._kwargs_type_:
			type = self._kwargs_type_[name]
			lines.append( '  %s %s' %(name,type))
			lines.append( '  __use__%s bool' %name)
		lines.append('}')

		lines = header + self._imports + lines
		return '\n'.join( lines )


	def visit_Compare(self, node):
		comp = [ '(']
		comp.append( self.visit(node.left) )
		comp.append( ')' )

		for i in range( len(node.ops) ):
			comp.append( self.visit(node.ops[i]) )

			if isinstance(node.comparators[i], ast.BinOp):
				comp.append('(')
				comp.append( self.visit(node.comparators[i]) )
				comp.append(')')
			else:
				comp.append( self.visit(node.comparators[i]) )

		return ' '.join( comp )

	def visit_For(self, node):
		target = self.visit(node.target)
		lines = []
		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):

			if node.iter.func.id == 'range':
				if len(node.iter.args)==1:
					iter = self.visit(node.iter.args[0])
					lines.append('for %s := 0; %s < %s; %s++ {' %(target, target, iter, target))
				elif len(node.iter.args)==2:
					start = self.visit(node.iter.args[0])
					iter = self.visit(node.iter.args[1])
					lines.append('for %s := %s; %s < %s; %s++ {' %(target, start, target, iter, target))
				else:
					raise SyntaxError('invalid for range loop')

			elif node.iter.func.id == 'enumerate':
				iter = self.visit(node.iter.args[0])
				idx = self.visit(node.target.elts[0])
				tar = self.visit(node.target.elts[1])
				lines.append('for %s,%s := range %s {' %(idx,tar, iter))

			else: ## generator function
				gfunc = node.iter.func.id
				gargs = ','.join( [self.visit(e) for e in node.iter.args] )
				lines.append('__gen%s := __new__%s(%s)' %(gfunc,gfunc, gargs))
				lines.append('for __gen%s.__done__ != 1 {' %gfunc)
				lines.append('	%s := __gen%s.next()' %(self.visit(node.target), gfunc))

		elif isinstance(node.target, ast.List) or isinstance(node.target, ast.Tuple):
			iter = self.visit( node.iter )
			key = self.visit(node.target.elts[0])
			val = self.visit(node.target.elts[1])
			lines.append('for %s,%s := range %s {' %(key,val, iter))

		else:
			iter = self.visit( node.iter )
			lines.append('for _,%s := range %s {' %(target, iter))

		self.push()
		for b in node.body:
			lines.append( self.indent()+self.visit(b) )
		self.pull()
		lines.append( self.indent()+'}' )  ## end of for loop
		return '\n'.join(lines)


	def _visit_call_helper(self, node, force_name=None):
		fname = force_name or self.visit(node.func)
		is_append = False
		if fname.endswith('.append'):
			is_append = True
			arr = fname.split('.append')[0]

		if fname=='__DOLLAR__': fname = '$'
		elif fname == 'range':
			assert len(node.args)
			fname += str(len(node.args))
		elif fname == 'len':
			return 'len(*%s)' %self.visit(node.args[0])
		#elif fname.startswith('__js_global_get_'):
		#	gname = fname.split('_')[-1]
		#	fname = 'js.Global.Get("%s").Call' %gname


		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''

		if node.keywords:
			if args: args += ','
			args += '_kwargs_type_{'
			x = ['%s:%s' %(kw.arg,self.visit(kw.value)) for kw in node.keywords]
			x.extend( ['__use__%s:true' %kw.arg for kw in node.keywords] )
			args += ','.join( x )
			args += '}'

		if node.starargs:
			if args: args += ','
			args += '%s...' %self.visit(node.starargs)

		if is_append:
			## deference pointer as first arg to append, assign to temp variable, then set the pointer to the new array.
			id = self._ids
			self._ids += 1
			return '__%s := append(*%s,%s); *%s = __%s;' % (id, arr, args, arr, id)

		elif self._with_gojs:
			if isinstance(node.func, ast.Attribute):
				fname = node.func.attr
				obname = self.visit(node.func.value)
				return 'Get("%s").Call("%s",%s)' % (obname, fname, args)

			else:
				return 'Call("%s",%s)' % (fname, args)

		else:
			return '%s(%s)' % (fname, args)

	def _visit_call_helper_go(self, node):
		name = self.visit(node.func)
		if name == '__go__':
			return 'go %s' %self.visit(node.args[0])
		elif name == '__go_make__':
			if len(node.args)==2:
				return 'make(%s, %s)' %(self.visit(node.args[0]), self.visit(node.args[1]))
			elif len(node.args)==3:
				return 'make(%s, %s, %s)' %(self.visit(node.args[0]), self.visit(node.args[1]), self.visit(node.args[1]))
			else:
				raise SyntaxError('go make requires 2 or 3 arguments')
		elif name == '__go_make_chan__':
			return 'make(chan %s)' %self.visit(node.args[0])
		elif name == '__go__array__':
			if isinstance(node.args[0], ast.BinOp):# and node.args[0].op == '<<':  ## todo assert right is `typedef`
				a = self.visit(node.args[0].left)
				if a in go_types:
					return '*[]%s' %a
				else:
					return '*[]*%s' %a

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


	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)

		if op == '>>' and left == '__new__':
			return ' new %s' %right

		elif op == '<<':
			if left in ('__go__receive__', '__go__send__'):
				return '<- %s' %right
			elif isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id in ('__go__array__', '__go__arrayfixed__', '__go__map__', '__go__func__'):
				if node.left.func.id == '__go__func__':
					raise SyntaxError('TODO - go.func')
				elif node.left.func.id == '__go__map__':
					key_type = self.visit(node.left.args[0])
					value_type = self.visit(node.left.args[1])
					if value_type == 'interface': value_type = 'interface{}'
					return '&map[%s]%s%s' %(key_type, value_type, right)
				else:
					if not right.startswith('{') and not right.endswith('}'):
						right = '{%s}' %right[1:-1]

					if node.left.func.id == '__go__array__':
						T = self.visit(node.left.args[0])
						if T in go_types:
							return '&[]%s%s' %(T, right)
						else:
							return '&[]*%s%s' %(T, right)
					elif node.left.func.id == '__go__arrayfixed__':
						asize = self.visit(node.left.args[0])
						atype = self.visit(node.left.args[1])
						if atype not in go_types:
							if right != '{}': raise SyntaxError('todo init array of objects with args')
							return '&make([]*%s, %s)' %(atype, asize)
						else:
							return '&[%s]%s%s' %(asize, atype, right)
			elif isinstance(node.left, ast.Name) and node.left.id=='__go__array__' and op == '<<':
				return '*[]%s' %self.visit(node.right)

		if left in self._typed_vars and self._typed_vars[left] == 'numpy.float32':
			left += '[_id_]'
		if right in self._typed_vars and self._typed_vars[right] == 'numpy.float32':
			right += '[_id_]'

		return '(%s %s %s)' % (left, op, right)

	def visit_Return(self, node):
		if isinstance(node.value, ast.Tuple):
			return 'return %s' % ', '.join(map(self.visit, node.value.elts))
		if node.value:
			return 'return %s' % self.visit(node.value)
		return 'return'

	def _visit_function(self, node):
		is_closure = False
		if self._function_stack[0] is node:
			self._vars = set()
			self._known_vars = set()
		elif len(self._function_stack) > 1:
			## do not clear self._vars and _known_vars inside of closure
			is_closure = True

		args_typedefs = {}
		chan_args_typedefs = {}
		return_type = None
		generics = set()
		for decor in node.decorator_list:
			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef__':
				for key in decor.keywords:
					if isinstance( key.value, ast.Str):
						args_typedefs[ key.arg ] = key.value.s
					else:
						args_typedefs[ key.arg ] = self.visit(key.value)

					## check for super classes - generics ##
					if args_typedefs[ key.arg ] in self._classes:
						if node.name=='__init__':
							#raise SyntaxError('generic in init')
							args_typedefs[ key.arg ] = 'interface{}'
							#self._class_stack[-1]._struct_def[ key.arg ] = 'interface{}'
						else:
							classname = args_typedefs[ key.arg ]
							generics.add( classname ) # switch v.(type) for each
							generics = generics.union( self._classes[classname]._subclasses )
							args_typedefs[ key.arg ] = 'interface{}'

			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef_chan__':
				for key in decor.keywords:
					chan_args_typedefs[ key.arg ] = self.visit(key.value)
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'returns':
				if decor.keywords:
					raise SyntaxError('invalid go return type')
				elif isinstance(decor.args[0], ast.Name):
					return_type = decor.args[0].id
				else:
					return_type = decor.args[0].s

				if return_type == 'self':
					return_type = '*' + self._class_stack[-1].name


		node._arg_names = args_names = []
		args = []
		oargs = []
		offset = len(node.args.args) - len(node.args.defaults)
		varargs = False
		varargs_name = None
		is_method = False
		for i, arg in enumerate(node.args.args):
			arg_name = arg.id

			if arg_name not in args_typedefs.keys()+chan_args_typedefs.keys():
				if arg_name=='self':
					assert i==0
					is_method = True
					continue
				else:
					err = 'error in function: %s' %node.name
					err += '\n  missing typedef: %s' %arg.id
					raise SyntaxError(err)

			if arg_name in args_typedefs:
				arg_type = args_typedefs[arg_name]
				if generics and (i==0 or (is_method and i==1)):
					a = '__gen__ %s' %arg_type
				else:
					a = '%s %s' %(arg_name, arg_type)
			else:
				arg_type = chan_args_typedefs[arg_name]
				a = '%s chan %s' %(arg_name, arg_type)

			dindex = i - offset

			if a.startswith('__variable_args__'): ## TODO support go `...` varargs
				#varargs_name = a.split('__')[-1]
				#varargs = ['_vararg_%s'%n for n in range(16) ]
				#args.append( '[%s]'%','.join(varargs) )
				raise SyntaxError('TODO *args')

			elif dindex >= 0 and node.args.defaults:
				default_value = self.visit( node.args.defaults[dindex] )
				self._kwargs_type_[ arg_name ] = arg_type
				oargs.append( (arg_name, default_value) )
			else:
				args.append( a )
				node._arg_names.append( arg_name )

		if oargs:
			#args.append( '[%s]' % ','.join(oargs) )
			#args.append( '{%s}' % ','.join(oargs) )
			args.append( '__kwargs _kwargs_type_')
			node._arg_names.append( '__kwargs' )

		if node.args.vararg:
			starargs = node.args.vararg
			assert starargs in args_typedefs
			args.append( '%s ...%s' %(starargs, args_typedefs[starargs]))
			node._arg_names.append( starargs )

		node._args_signature = ','.join(args)

		####
		if is_method:
			assert self._class_stack
			method = '(self *%s)  ' %self._class_stack[-1].name
		else:
			method = ''
		out = []
		if is_closure:
			if return_type:
				out.append( self.indent() + '%s := func (%s) %s {\n' % (node.name, ', '.join(args), return_type) )
			else:
				out.append( self.indent() + '%s := func (%s) {\n' % (node.name, ', '.join(args)) )
		else:
			if return_type:
				out.append( self.indent() + 'func %s%s(%s) %s {\n' % (method, node.name, ', '.join(args), return_type) )
			else:
				out.append( self.indent() + 'func %s%s(%s) {\n' % (method, node.name, ', '.join(args)) )
		self.push()

		if oargs:
			for n,v in oargs:
				out.append('%s := %s' %(n,v))
				out.append('if __kwargs.__use__%s {' %n )
				out.append( '  %s = __kwargs.%s' %(n,n))
				out.append('}')
				#out.append('} else { %s := %s }' %(n,v))

		if generics:
			out.append(self.indent() + 'switch __gen__.(type) {')
			self.push()
			for gt in generics:
				out.append(self.indent() + 'case *%s:' %gt)
				self.push()
				out.append(self.indent() + '%s,_ := __gen__.(*%s)' %(args_names[0],gt) )
				for b in node.body:
					v = self.visit(b)
					if v: out.append( self.indent() + v )
				self.pull()
			self.pull()
			out.append('}')
			if return_type == 'int':
				out.append('return 0')
			elif return_type == 'float':
				out.append('return 0.0')
			elif return_type == 'string':
				out.append('return ""')
			elif return_type == 'bool':
				out.append('return false')
			elif return_type:
				#raise NotImplementedError('TODO other generic function return types', return_type)
				out.append('return %s' %(return_type.replace('*','&')+'{}'))

		else:
			for b in node.body:
				v = self.visit(b)
				if v: out.append( self.indent() + v )

		self.pull()
		out.append( self.indent()+'}' )
		return '\n'.join(out)

	def _visit_call_helper_var(self, node):
		args = [ self.visit(a) for a in node.args ]
		#if args:
		#	out.append( 'var ' + ','.join(args) )
		if node.keywords:
			for key in node.keywords:
				args.append( key.arg )

		for name in args:
			if name not in self._vars:
				self._vars.add( name )

		#out = []
		#for v in args:
		#	out.append( self.indent() + 'var ' + v + ' int')

		#return '\n'.join(out)
		return ''

	def visit_With(self, node):
		r = []
		is_switch = False
		if isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'gojs':
			#transform_gopherjs( node )
			self._with_gojs = True
			for b in node.body:
				a = self.visit(b)
				if a: r.append(a)
			self._with_gojs = False
			return '\n'.join(r)

		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == '__default__':
			r.append('default:')
		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == '__select__':
			r.append('select {')
			is_switch = True
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
					a = '%s := %s' %(name, self.visit(node.context_expr.keywords[0].value))
				else:
					a = '%s = %s' %(name, self.visit(node.context_expr.keywords[0].value))

			if node.context_expr.func.id == '__case__':
				r.append('case %s:' %a)
			elif node.context_expr.func.id == '__switch__':
				r.append('switch (%s) {' %self.visit(node.context_expr.args[0]))
				is_switch = True
			else:
				raise SyntaxError( 'invalid use of with')
		else:
			raise SyntaxError( 'invalid use of with')


		for b in node.body:
			a = self.visit(b)
			if a: r.append(a)

		if is_switch:
			r.append('}')

		return '\n'.join(r)

	def visit_Assign(self, node):
		if isinstance(node.targets[0], ast.Tuple):
			raise NotImplementedError('TODO')

		target = self.visit( node.targets[0] )

		if isinstance(node.value, ast.BinOp) and self.visit(node.value.op)=='<<' and isinstance(node.value.left, ast.Name) and node.value.left.id=='__go__send__':
			value = self.visit(node.value.right)
			return '%s <- %s;' % (target, value)

		elif not self._function_stack:
			value = self.visit(node.value)
			return 'var %s = %s;' % (target, value)

		elif isinstance(node.targets[0], ast.Name) and node.targets[0].id in self._vars:
			value = self.visit(node.value)
			self._vars.remove( target )
			self._known_vars.add( target )
			return '%s := %s;' % (target, value)

		else:
			value = self.visit(node.value)
			#if '<-' in value:
			#	raise RuntimeError(target+value)
			if value.startswith('&make('):
				#raise SyntaxError(value)
				v = value[1:]
				return '_tmp := %s; %s = &_tmp;' %(v, target)
			else:
				return '%s = %s;' % (target, value)

	def visit_While(self, node):
		cond = self.visit(node.test)
		if cond == 'true' or cond == '1': cond = ''
		body = [ 'for %s {' %cond]
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def _inline_code_helper(self, s):
		return s
		#return 'js.Global.Call("eval", "%s")' %s ## TODO inline JS()





def main(script, insert_runtime=True):

	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'go_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	#raise RuntimeError(script)
	return GoGenerator().visit(tree)
	try:
		return GoGenerator().visit(tree)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err



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

	out = main( data )
	print( out )


if __name__ == '__main__':
	command()

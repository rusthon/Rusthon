#!/usr/bin/env python
# PythonJS to Dart Translator
# by Brett Hartshorn - copyright 2013
# License: "New BSD"
import sys
import ast
import pythonjs


class TransformSuperCalls( ast.NodeVisitor ):
	def __init__(self, node, class_names):
		self._class_names = class_names
		self.visit(node)

	def visit_Call(self, node):
		if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id in self._class_names:
			node.func.attr = '__' + node.func.attr

class CollectNames(ast.NodeVisitor):
	def __init__(self):
		self._names = []
	def visit_Name(self, node):
		self._names.append( node )

def collect_names(node):
	a = CollectNames()
	a.visit( node )
	return a._names


class DartGenerator( pythonjs.JSGenerator ):

	def __init__(self, requirejs=False, insert_runtime=False):
		pythonjs.JSGenerator.__init__(self, requirejs=False, insert_runtime=False)
		self._classes = dict()
		self._class_props = dict()
		self._raw_dict = False

	def visit_With(self, node):
		s = []
		for b in node.body:
			a = self.visit(b)
			a = a.replace('\\n', '\n')
			a = a.strip()[1:-2] # strip `"x";` to `x`
			s.append( a )
		return '\n'.join(s)

	def _visit_subscript_ellipsis(self, node):
		name = self.visit(node.value)
		return '%s.$wrapped' %name

	def visit_List(self, node):
		return 'new list([%s])' % ', '.join(map(self.visit, node.elts))

	def visit_Dict(self, node):
		a = []
		for i in range( len(node.keys) ):
			k = self.visit( node.keys[ i ] )
			v = self.visit( node.values[i] )
			a.append( '%s:%s'%(k,v) )
		b = ','.join( a )
		if self._raw_dict:
			return '{%s}' %b
		else:
			return 'new dict( {%s} )' %b

	def visit_ClassDef(self, node):
		node._parents = set()
		out = []
		extends = False ## Dart has no support for multiple inheritance!
		props = set(['$wrapped'])
		bases = set()
		base_classes = set()

		self._classes[ node.name ] = node
		self._class_props[ node.name ] = props
		for decor in node.decorator_list:  ## class decorators
			if isinstance(decor, ast.Call):
				props.update( [self.visit(a) for a in decor.args] )
			elif isinstance(decor, ast.Attribute) and isinstance(decor.value, ast.Name) and decor.value.id == 'dart':
				if decor.attr == 'extends':
					extends = True
					props.add('$wrapped')
					for name_node in collect_names( node ):
						if name_node.id == 'self':
							name_node.id = 'this'
			else:
				raise SyntaxError


		for base in node.bases:
			n = self.visit(base)
			if n == 'object':
				continue
			node._parents.add( n )

			bases.add( n )
			if n in self._class_props:
				props.update( self._class_props[n] )
				base_classes.add( self._classes[n] )
			else:  ## special case - subclassing a builtin like `list`
				continue

			for p in self._classes[ n ]._parents:
				bases.add( p )
				props.update( self._class_props[p] )
				base_classes.add( self._classes[p] )

		if bases:
			if extends:
				assert len(bases) == 1
				out.append('class %s extends %s {'%(node.name, ','.join(bases)))
			else:
				#if bases[0] == 'object':
				#	out.append('class %s {' %node.name)
				#else:
				out.append('class %s implements %s {'%(node.name, ', '.join(bases)))


		else:
			out.append('class %s {' %node.name)
		self.push()

		for p in props:
			out.append(self.indent()+ 'var %s;'%p)

		method_names = set()
		for b in node.body:

			if isinstance(b, ast.With):
				out.append( self.visit(b) )
			elif isinstance(b, ast.FunctionDef) and len(b.decorator_list):  ##getter/setters
				for name_node in collect_names( b ):
					if name_node.id == 'self':
						name_node.id = 'this'

				b.args.args = b.args.args[1:]
				out.append( self.visit(b) )

			elif extends:
				if isinstance(b, ast.FunctionDef):
					b.args.args = b.args.args[1:]
					if b.name == node.name:
						args = [self.visit(a) for a in b.args.args]
						args = ','.join(args)
						out.append(
							self.indent()+'%s(%s) : super() { this.__init__(%s); }'%(node.name, args, args)
						)
						b.name = '__init__'
					elif b.name == '__getitem__':
						b.name = ''
						b._prefix = 'operator []'
					elif b.name == '__setitem__':
						b.name = ''
						b._prefix = 'void operator []='
					elif b.name == '__add__':
						b.name = ''
						b._prefix = 'operator +'
					elif b.name == '__iadd__':
						b.name = ''
						b._prefix = 'void operator +='
					elif b.name == '__sub__':
						b.name = ''
						b._prefix = 'operator -'
					elif b.name == '__mul__':
						b.name = ''
						b._prefix = 'operator *'
					elif b.name == '__div__':
						b.name = ''
						b._prefix = 'operator /'

					elif b.name == '__or__':
						b.name = ''
						b._prefix = 'operator |'
					elif b.name == '__xor__':
						b.name = ''
						b._prefix = 'operator ^'



				line = self.visit(b)
				out.append( line )

			elif isinstance(b, ast.FunctionDef) and b.name == node.name:
				args, kwargs = self.get_args_kwargs_from_funcdef(b, skip_self=True)
				kwargs_init = ['%s:%s' %(x.split(':')[0], x.split(':')[0]) for x in kwargs]

				#args = [self.visit(a) for a in b.args.args][1:]
				#args = ','.join(args)
				b._prefix = 'static void'
				b.name = '__init__'
				out.append( self.visit(b) )
				if args:
					args = ','.join(args)
					if kwargs:
						out.append(
							self.indent()+'%s(%s, {%s}) {%s.__init__(this,%s,%s);}'%(node.name, args, ','.join(kwargs), node.name, args, ','.join(kwargs_init))
						)

					else:
						out.append(
							self.indent()+'%s(%s) {%s.__init__(this,%s);}'%(node.name, args, node.name, args)
						)
				elif kwargs:
					out.append(
						self.indent()+'%s( {%s} ) {%s.__init__(this,%s);}'%(node.name, ','.join(kwargs), node.name, ','.join(kwargs_init))
					)

				else:
					out.append(
						self.indent()+'%s() {%s.__init__(this);}'%(node.name, node.name)
					)

			elif isinstance(b, ast.FunctionDef):
				method_names.add( b.name )
				TransformSuperCalls( b, bases )

				operator = False
				if b.name == '__getitem__':
					operator = 'operator []'
				elif b.name == '__setitem__':
					operator = 'operator []='
				elif b.name == '__add__':
					operator = 'operator +'
				elif b.name == '__sub__':
					operator = 'operator -'
				elif b.name == '__mul__':
					operator = 'operator *'
				elif b.name == '__div__':
					operator = 'operator /'
				elif b.name == '__and__':
					operator = 'operator &'
				elif b.name == '__or__':
					operator = 'operator |'
				elif b.name == '__xor__':
					operator = 'operator ^'
				elif b.name == '__lshift__':
					operator = 'operator <<'
				elif b.name == '__rshift__':
					operator = 'operator >>'

				args = [self.visit(a) for a in b.args.args][1:]
				args = ','.join(args)
				if operator and args:
					out.append(self.indent()+ '%s(%s) { return %s.__%s(this,%s); }'%(operator, args, node.name, b.name, args) )

				elif operator:
					out.append(self.indent()+ '%s() { return %s.__%s(this); }'%(operator, node.name, b.name) )

				elif args:
					out.append(self.indent()+ '%s(%s) { return %s.__%s(this,%s); }'%(b.name, args, node.name, b.name, args) )
				else:
					out.append(self.indent()+ '%s() { return %s.__%s(this); }'%(b.name, node.name, b.name) )

				b._prefix = 'static'
				name = b.name
				b.name = '__%s'%name
				out.append( self.visit(b) )
				b.name = name

			else:
				line = self.visit(b)
				if line.startswith('var '):
					out.append( self.indent()+line )
				else:
					out.append( line )

		if not extends and base_classes:
			for bnode in base_classes:
				for b in bnode.body:
					if isinstance(b, ast.FunctionDef):
						if b.name == '__init__': continue
						if b.name in method_names: continue

						args = [self.visit(a) for a in b.args.args][1:]
						args = ','.join(args)
						if args:
							out.append(self.indent()+ '%s(%s) { return %s.__%s(this,%s); }'%(b.name, args, bnode.name, b.name, args) )
						else:
							out.append(self.indent()+ '%s() { return %s.__%s(this); }'%(b.name, bnode.name, b.name) )


		self.pull()
		out.append('}')
		return '\n'.join(out)

	def get_args_kwargs_from_funcdef(self, node, skip_self=False):
		args = []
		kwargs = []
		if skip_self: nargs = node.args.args[1:]
		else: nargs = node.args.args

		offset = len(nargs) - len(node.args.defaults)
		for i, arg in enumerate(nargs):
			a = arg.id
			dindex = i - offset
			if dindex >= 0 and node.args.defaults:
				default_value = self.visit( node.args.defaults[dindex] )
				kwargs.append( '%s:%s' %(a, default_value) )
			else:
				args.append( a )

		return args, kwargs


	def _visit_for_prep_iter_helper(self, node, out, iter_name):
		out.append(
			#self.indent() + 'if (%s is dict) { %s = %s.keys(); }' %(iter_name, iter_name, iter_name)
			self.indent() + 'if (%s is dict) %s = %s.keys();' %(iter_name, iter_name, iter_name)
		)


	def visit_Expr(self, node):
		s = self.visit(node.value)
		if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'JS':
			if s.endswith('}') and 'return' in s.split(' '):
				pass
			elif not s.endswith(';'):
				s += ';'
		elif not s.endswith(';'):
			s += ';'
		return s



	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		if len(args) > 1:
			s = 'print([%s]);' % ', '.join(args)
		else:
			s = 'print(%s);' % ', '.join(args)
		return s


	def visit_Assign(self, node):
		assert len(node.targets) == 1
		target = node.targets[0]
		if isinstance(target, ast.Tuple):
			#raise NotImplementedError
			elts = [self.visit(e) for e in target.elts]
			if self.indent():
				return '%s = %s' % (','.join(elts), self.visit(node.value))
			else:
				return 'var %s = %s' % (','.join(elts), self.visit(node.value))

		else:
			target = self.visit(target)
			value = self.visit(node.value)
			if self.indent():
				code = '%s = %s;' % (target, value)
			else:
				code = 'var %s = %s;' % (target, value)
			return code

	def _visit_function(self, node):
		getter = False
		setter = False
		for decor in node.decorator_list:
			if isinstance(decor, ast.Name) and decor.id == 'property':
				getter = True
			elif isinstance(decor, ast.Attribute) and isinstance(decor.value, ast.Name) and decor.attr == 'setter':
				setter = True
			else:
				raise SyntaxError

		args = []  #self.visit(node.args)
		oargs = []
		offset = len(node.args.args) - len(node.args.defaults)
		varargs = False
		varargs_name = None
		for i, arg in enumerate(node.args.args):
			a = arg.id
			dindex = i - offset
			if a.startswith('__variable_args__'):
				varargs_name = a.split('__')[-1]
				varargs = ['_vararg_%s'%n for n in range(16) ]
				args.append( '[%s]'%','.join(varargs) )

			elif dindex >= 0 and node.args.defaults:
				default_value = self.visit( node.args.defaults[dindex] )
				oargs.append( '%s:%s' %(a, default_value) )
			else:
				args.append( a )

		if oargs:
			#args.append( '[%s]' % ','.join(oargs) )
			args.append( '{%s}' % ','.join(oargs) )

		buffer = self.indent()
		if hasattr(node,'_prefix'): buffer += node._prefix + ' '

		if getter:
			buffer += 'get %s {\n' % node.name
		elif setter:
			buffer += 'set %s(%s) {\n' % (node.name, ', '.join(args))
		else:
			buffer += '%s(%s) {\n' % (node.name, ', '.join(args))
		self.push()

		if varargs:
			buffer += 'var %s = new list([]);\n' %varargs_name
			for i,n in enumerate(varargs):
				buffer += 'if (%s != null) %s.append(%s);\n' %(n, varargs_name, n)

		body = list()
		for child in node.body:
			if isinstance(child, ast.Str):
				continue
			else:
				body.append( self.indent() + self.visit(child) )

		buffer += '\n'.join(body)
		self.pull()
		buffer += '\n%s}\n' %self.indent()
		return buffer


	def visit_Is(self, node):
		return '=='

	def visit_IsNot(self, node):
		return '!='

	def visit_NotEq(self, node):
		return '!='

	def _visit_call_helper(self, node):
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''

		if node.keywords:
			kwargs = ','.join( ['%s:%s'%(x.arg, self.visit(x.value)) for x in node.keywords] )
			if args:
				return '%s(%s, %s)' %( self.visit(node.func), ','.join(args), kwargs )
			else:
				return '%s( %s )' %( self.visit(node.func), kwargs )

		else:
			return '%s(%s)' % (self.visit(node.func), args)

	def _visit_call_helper_list(self, node):
		name = self.visit(node.func)
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = '[]'  ## the dart list builtin requires an argument
		return '%s(%s)' % (name, args)


	def _visit_call_helper_instanceof(self, node):
		args = map(self.visit, node.args)
		if len(args) == 2:
			if args[1] == 'Number':
				args[1] = 'num'
			return '%s is %s' %tuple(args)
		else:
			raise SyntaxError( args )

	def visit_ExceptHandler(self, node):
		return '\n'.join( [self.visit(n) for n in node.body] )

	def visit_Compare(self, node):
		specials = {
			'<' : '__lt__',
			'>' : '__gt__', 
			'<=' : '__lte__', 
			'>=' : '__gte__'
		}
		comp = []
		if len(node.ops) == 0:

			comp.append('(')
			comp.append( self.visit(node.left) )
			comp.append( ')' )

		else:
			if self.visit(node.ops[0]) in specials:
				pass
			else:
				comp.append('(')
				comp.append( self.visit(node.left) )
				comp.append( ')' )

			for i in range( len(node.ops) ):
				op = self.visit(node.ops[i])

				if op in specials:
					comp.append( specials[op] + '(%s,' %self.visit(node.left) )
				else:
					comp.append( op )

				if isinstance(node.comparators[i], ast.BinOp):
					comp.append('(')
					comp.append( self.visit(node.comparators[i]) )
					comp.append(')')
				else:
					comp.append( self.visit(node.comparators[i]) )

				if op in specials:
					comp.append( ')' )


		return ' '.join( comp )

def main(script):
	tree = ast.parse(script)
	return DartGenerator().visit(tree)


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
	command()

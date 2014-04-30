#!/usr/bin/env python
# PythonJS to CoffeeScript Translator
# by Brett Hartshorn - copyright 2014
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


class CoffeeGenerator( pythonjs.JSGenerator ):
	_classes = dict()
	_class_props = dict()

	def _visit_call_helper_var(self, node):
		return ''

	def _inline_code_helper(self, s):
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
		return '`' + s + '`'  ## enclose with backticks to inline javascript in coffeescript

	def visit_While(self, node):
		body = [ 'while %s' %self.visit(node.test)]
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		return '\n'.join( body )

	def _visit_subscript_ellipsis(self, node):
		name = self.visit(node.value)
		return '%s.$wrapped' %name

	def visit_Pass(self, node):
		return '###pass###'

	def visit_If(self, node):
		out = []
		out.append( 'if %s' %self.visit(node.test) )
		self.push()

		for line in list(map(self.visit, node.body)):
			out.append( self.indent() + line )

		orelse = []
		for line in list(map(self.visit, node.orelse)):
			orelse.append( self.indent() + line )

		self.pull()

		if orelse:
			out.append( self.indent() + 'else')
			out.extend( orelse )

		return '\n'.join( out )


	def visit_List(self, node):
		return '[%s]' % ', '.join(map(self.visit, node.elts))

	def visit_Dict(self, node):
		a = []
		for i in range( len(node.keys) ):
			k = self.visit( node.keys[ i ] )
			v = self.visit( node.values[i] )
			a.append( '%s:%s'%(k,v) )
		b = ','.join( a )
		return '{%s}' %b

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

			if isinstance(b, ast.FunctionDef) and len(b.decorator_list):  ##getter/setters
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
				args = [self.visit(a) for a in b.args.args][1:]
				args = ','.join(args)
				b._prefix = 'static void'
				b.name = '__init__'
				out.append( self.visit(b) )
				if args:
					out.append(
						self.indent()+'%s(%s) {%s.__init__(this,%s);}'%(node.name, args, node.name, args)
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

	def _visit_for_prep_iter_helper(self, node, out, iter_name):
		out.append(
			#self.indent() + 'if (%s is dict) { %s = %s.keys(); }' %(iter_name, iter_name, iter_name)
			self.indent() + 'if (%s is dict) %s = %s.keys();' %(iter_name, iter_name, iter_name)
		)


	def visit_Expr(self, node):
		return self.visit(node.value)


	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		return 'console.log(%s)' % ', '.join(args)


	def visit_Assign(self, node):
		assert len(node.targets) == 1
		target = node.targets[0]
		if isinstance(target, ast.Tuple):
			raise NotImplementedError
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			code = '%s = %s;' % (target, value)
			return code

	def _visit_function(self, node):
		getter = False
		setter = False
		klass = None
		for decor in node.decorator_list:
			if isinstance(decor, ast.Name) and decor.id == 'property':
				getter = True
			elif isinstance(decor, ast.Attribute) and isinstance(decor.value, ast.Name) and decor.attr == 'setter':
				setter = True
			elif isinstance(decor, ast.Attribute) and isinstance(decor.value, ast.Name) and decor.attr == 'prototype':
				klass = self.visit(decor)
			else:
				raise SyntaxError(decor)

		args = []  #self.visit(node.args)
		oargs = []
		offset = len(node.args.args) - len(node.args.defaults)
		varargs = False
		varargs_name = None
		for i, arg in enumerate(node.args.args):
			a = arg.id
			dindex = i - offset

			if dindex >= 0 and node.args.defaults:
				default_value = self.visit( node.args.defaults[dindex] )
				oargs.append( '%s=%s' %(a, default_value) )
			else:
				args.append( a )

		if oargs:
			args.extend( ','.join(oargs) )

		buffer = self.indent()
		if hasattr(node,'_prefix'): buffer += node._prefix + ' '

		#if getter:
		#	buffer += 'get %s {\n' % node.name
		#elif setter:
		#	buffer += 'set %s(%s) {\n' % (node.name, ', '.join(args))
		#else:
		if klass:
			buffer += '%s.%s = (%s) ->\n' % (klass, node.name, ', '.join(args))
		else:
			buffer += '%s = (%s) ->\n' % (node.name, ', '.join(args))
		self.push()

		#if varargs:
		#	buffer += 'var %s = new list([]);\n' %varargs_name
		#	for i,n in enumerate(varargs):
		#		buffer += 'if (%s != null) %s.append(%s);\n' %(n, varargs_name, n)

		body = list()
		for child in node.body:
			if isinstance(child, ast.Str):
				continue
			else:
				body.append( self.indent() + self.visit(child) )

		if not isinstance(node.body[-1], ast.Return):
			body.append( self.indent() + '0' )

		buffer += '\n'.join(body)
		self.pull()
		return buffer


	def visit_Is(self, node):
		return ' is '

	def visit_IsNot(self, node):
		return ' isnt '

	def _visit_call_helper_instanceof(self, node):
		args = map(self.visit, node.args)
		if len(args) == 2:
			if args[1] == 'Number':
				args[1] = 'num'
			return '%s is %s' %tuple(args)
		else:
			raise SyntaxError( args )

	def visit_TryExcept(self, node):
		out = ['try']
		self.push()
		for n in node.body:
			out.append( self.indent() + self.visit(n) )
		self.pull()
		out.append( self.indent() + 'catch error' )
		self.push()
		for n in node.handlers:
			out.append( self.visit(n) )
		self.pull()
		return '\n'.join( out )

	def visit_ExceptHandler(self, node):
		## TODO check exception type
		out = []
		if node.type:
			out.append( self.indent() + '###exception: %s' %self.visit(node.type) )
		for n in node.body:
			out.append( self.indent() + self.visit(n) )

		return '\n'.join(out)


def main(script):
	tree = ast.parse(script)
	return CoffeeGenerator().visit(tree)


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

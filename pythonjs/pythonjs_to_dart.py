#!/usr/bin/env python
# PythonJS to Dart Translator
# by Brett Hartshorn - copyright 2013
# License: "New BSD"
import os, sys
import ast
import pythonjs

class DartGenerator( pythonjs.JSGenerator ):
	_classes = dict()
	_class_props = dict()
	def visit_ClassDef(self, node):
		out = []
		extends = False ## Dart has no support for multiple inheritance!
		props = set()

		self._classes[ node.name ] = node
		self._class_props[ node.name ] = props
		for decor in node.decorator_list:  ## class decorators
			if isinstance(decor, ast.Call):
				props.update( [self.visit(a) for a in decor.args] )



		bases = []
		base_classes = []
		for base in node.bases:
			n = self.visit(base)
			bases.append( n )
			props.update( self._class_props[n] )
			base_classes.append( self._classes[n] )
		if bases:
			if extends:
				assert len(bases) == 1
				out.append('class %s extends %s {'%(node.name, ','.join(bases)))
			else:
				out.append('class %s implements %s {'%(node.name, ', '.join(bases)))


		else:
			out.append('class %s {' %node.name)
		self.push()

		for p in props:
			out.append(self.indent()+ 'var %s;'%p)


		for b in node.body:

			if isinstance(b, ast.FunctionDef) and b.name == node.name:
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
				args = [self.visit(a) for a in b.args.args][1:]
				args = ','.join(args)
				if args:
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
						#out.append( self.visit(b) )
						args = [self.visit(a) for a in b.args.args][1:]
						args = ','.join(args)
						if args:
							out.append(self.indent()+ '%s(%s) { return %s.__%s(this,%s); }'%(b.name, args, bnode.name, b.name, args) )
						else:
							out.append(self.indent()+ '%s() { return %s.__%s(this); }'%(b.name, bnode.name, b.name) )


		self.pull()
		out.append('}')
		return '\n'.join(out)

	def _visit_for_prep_iter_helper(self, node, out):
		pass


	def visit_Expr(self, node):
		# XXX: this is UGLY
		s = self.visit(node.value)
		if not s.endswith(';'):
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
			raise NotImplementedError
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			if self.indent():
				code = '%s = %s;' % (target, value)
			else:
				code = 'var %s = %s;' % (target, value)
			return code

	def visit_FunctionDef(self, node):

		args = self.visit(node.args)
		buffer = self.indent()
		if hasattr(node,'_prefix'):
			buffer += node._prefix + ' '
		buffer += '%s(%s) {\n' % (node.name, ', '.join(args))
		self.push()
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

	def _visit_call_helper_instanceof(self, node):
		args = map(self.visit, node.args)
		if len(args) == 2:
			return '%s is %s' %tuple(args)
		else:
			raise SyntaxError( args )



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

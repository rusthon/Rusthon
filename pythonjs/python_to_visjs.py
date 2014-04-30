import ast
#from cStringIO import StringIO as StringIO
from StringIO import StringIO as StringIO

head = """
<div id="mygraph"></div>
<script type="text/javascript">
nodes = [];
edges = [];
stack = [];
"""

tail = """
con = document.getElementById('mygraph');
data = {
	nodes: nodes,
	edges: edges
}
options = { stabilize: false, clustering: false, hierarchicalLayout:false };
graph = new vis.Graph(con, data, options);
</script>
"""

def main(script):
	PythonToVisJS( source=script )
	return head + writer.getvalue() + tail


class Writer(object):

	def __init__(self):
		self.level = 0
		self.buffer = list()
		self.output = StringIO()
		self.nodes = []
		self.ids = 0
		self.title_blocks = False
		self.use_indent = False
		self.classes = {}  ## name : id

	def push_block(self, s='', shape="box", size=1, font_size=13, color=None):
		id = self.ids
		self.ids += 1
		class_name = None
		if s.startswith('class '):
			x = s.split()
			class_name = x[1]
			if len(x)==3:
				class_parents = x[2].split(',')
			else:
				class_parents = []
			self.classes[ class_name ] = id

			for pname in class_parents:
				if pname in self.classes:
					pid = self.classes[ pname ]
					self.output.write('edges.push({from:%s, to:%s, length:200, style:"arrow"})\n' %(pid,id))

			s = 'class \\n\\n'+class_name


		if self.nodes:
			if self.level <= 1 and s.startswith( 'def' ) or class_name:
				pass
			else:
				if self.title_blocks:
					self.output.write('stack[stack.length-1].label += "--block%s-->\\n"\n' %id)
				else:
					self.output.write('stack[stack.length-1].label += ""\n')

				prev = self.nodes[-1]
				style = 'dash-line'
				width = 1
				length = 100
				if prev.startswith('if '):
					style = 'arrow'
				elif prev.startswith('for '):
					style = 'arrow-center'
					length = 150
					self.output.write('edges.push({from:%s, to:stack[stack.length-1].id, style: "%s", width: 1, length: %s})\n' %(id, style, length))
				elif prev.startswith('class '):
					style = 'line'
					width = 3
					length = 200
				self.output.write('edges.push({to:%s, from:stack[stack.length-1].id, style: "%s", width: %s, length: %s})\n' %(id, style, width, length))

		if s:
			s += '\\n'
		if self.title_blocks:
			s = ('BLOCK-%s\\n'%id) + s

		if color is None:
			color = 'undefined'
		else:
			if type(color) is tuple:
				color = '{background:"%s", border:"%s"}'%color
			else:
				color = '{background:"%s"}'%color

		self.output.write('var block = {id:%s, label:"%s", shape:"%s", value:%s, fontSize:%s, color:%s};\n' %(id, s, shape, size, font_size, color))

		self.output.write('nodes.push( block );')
		self.output.write('stack.push( block );\n')
		self.nodes.append( s )
		self.level += 1

	def pull_block(self):
		self.level -= 1
		self.nodes.pop()
		self.output.write('block = stack.pop();\n')

	def push(self):
		self.push_block()

	def pull(self):
		self.pull_block()

	def append(self, code):
		self.buffer.append(code)

	def write(self, code):
		for content in self.buffer:
			self._write(content)
		self.buffer = list()
		self._write(code)

	def _write(self, code):
		if self.use_indent:
			indentation = self.level * 4 * ' '
		else:
			indentation = ''
		if code.startswith('if '):
			s = '"%s%s";' % (indentation, code)
		else:
			s = '"%s%s\\n";' % (indentation, code)
		self.output.write('stack[stack.length-1].label += %s\n' %s)

	def getvalue(self):
		s = self.output.getvalue()
		self.output = StringIO()
		return s

writer = Writer()


class PythonToVisJS(ast.NodeVisitor):
	def __init__(self, source=None):
		super(PythonToVisJS, self).__init__()
		tree = ast.parse( source )
		writer.push_block('#module#', shape='circle', color=('lightyellow', 'red'))
		self.visit( tree )
		writer.pull_block()

	def visit_Print(self, node):
		return 'print %s' % ', '.join(map(self.visit, node.values))

	def visit_Expr(self, node):
		return self.visit(node.value)

	def visit_If(self, node):
		#writer.write('if %s:' %self.visit(node.test))
		writer.push_block('if \\n%s' %self.visit(node.test), color=('lightgreen', 'green'), size=5, font_size=16)
		writer.push()

		for n in node.body:
			res = self.visit(n)
			if res: writer.write(res)

		writer.pull()
		if node.orelse:
			writer.push_block('else:', color=('pink', 'red'), size=5, font_size=16)
			writer.push()
			for n in node.orelse:
				res = self.visit(n)
				if res: writer.write(res)
			writer.pull()
			writer.pull_block()

		writer.pull_block()


	def visit_Compare(self, node):
		left = self.visit(node.left)
		comp = [ left ]
		for i in range( len(node.ops) ):
			comp.append( self.visit(node.ops[i]) )
			comp.append( self.visit(node.comparators[i]) )
		return ' '.join( comp )


	def visit_For(self, node):
		a = 'for \\n%s in %s' %(self.visit(node.target), self.visit(node.iter))
		writer.push_block(a, color=('cyan', 'orange'), size=5, font_size=16)

		writer.push()
		for n in node.body:
			res = self.visit(n)
			if res: writer.write( res )
		writer.pull()

		writer.pull_block()


	def visit_While(self, node):
		writer.push_block('while \\n%s' % self.visit(node.test))
		writer.push()
		for n in node.body:
			res = self.visit(n)
			if res: writer.write( res )
		writer.pull()
		writer.pull_block()


	def visit_Call(self, node):
		args = [self.visit(arg) for arg in node.args]
		if node.keywords:
			args.extend( [self.visit(x.value) for x in node.keywords] )
			return '%s(%s)' %( self.visit(node.func), ','.join(args) )

		else:
			return '%s(%s)' %( self.visit(node.func), ','.join(args) )


	def visit_ClassDef(self, node):
		bases = []
		for base in node.bases:
			bases.append( self.visit(base) )
		if bases:
			a = 'class %s %s'%(node.name, ','.join(bases))
		else:
			a = 'class %s' %node.name

		writer.push_block(a, color=('orange', 'black'), font_size=16, shape='database')
		for n in node.body:
			if isinstance(n, ast.FunctionDef):
				self.visit(n)
		writer.pull_block()


	def visit_FunctionDef(self, node):
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
			args.append('*%s' %node.args.vararg)
		if node.args.kwarg:
			args.append('**%s' %node.args.kwarg)

		a = 'def %s\\n%s' % (node.name, ',\\n'.join(args))
		writer.push_block( a, color=('yellow', 'orange'), font_size=16 )
		writer.push()
		for n in node.body:
			res = self.visit(n)
			if res: writer.write(res)
		writer.pull()
		writer.pull_block()

	def visit_Return(self, node):
		if node.value:
			writer.write('return %s' % self.visit(node.value))
		return ''

	def visit_Attribute(self, node):
		node_value = self.visit(node.value)
		return '%s.%s' %(node_value, node.attr)


	def visit_Pass(self, node):
		return 'pass'

	def visit_Str(self, node):
		return '`%s`' %node.s.replace('"','&quot;').replace('\n', '\\n').replace('&', '&amp;').replace('<','&lt;').replace('>','&gt;')

	def visit_Name(self, node):
		return node.id

	def visit_Num(self, node):
		return str(node.n)

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

	def visit_And(self, node):
		return ' and '

	def visit_Or(self, node):
		return ' or '

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

	def visit_In(self, node):
		return ' in '

	def visit_NotIn(self, node):
		return ' not in '

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

	def visit_BoolOp(self, node):
		op = self.visit(node.op)
		return op.join( [self.visit(v) for v in node.values] )


	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)
		return '(%s %s %s)' % (left, op, right)

	def visit_Subscript(self, node):
		name = self.visit(node.value)
		return '%s[ %s ]' %(name, self.visit(node.slice))


	def visit_Assign(self, node):
		#assert len(node.targets) == 1
		target = node.targets[0]
		if isinstance(target, ast.Tuple):
			elts = [self.visit(e) for e in target.elts]
			code = '%s = %s' % (','.join(elts), self.visit(node.value))

		else:
			target = self.visit(target)
			value = self.visit(node.value)
			code = '%s = %s' % (target, value)

		writer.write(code)

	def visit_AugAssign(self, node):
		target = self.visit( node.target )
		op = '%s=' %self.visit( node.op )
		a = '%s %s %s' %(target, op, self.visit(node.value))
		writer.write(a)

	def visit_Assert(self, node):
		writer.write('assert %s'%self.visit(node.test))


	def visit_TryExcept(self, node):
		writer.push_block('try')
		for n in node.body:
			res = self.visit(n)
			if res: writer.write( res )

		#map(self.visit, node.handlers)
		writer.pull_block()

	def visit_Raise(self, node):
		writer.write('raise %s' % self.visit(node.type))


	def visit_Tuple(self, node):
		return '(%s)' % ', '.join(map(self.visit, node.elts))

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

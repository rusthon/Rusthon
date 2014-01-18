# Brython AST to Python AST Bridge
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

def brython_tokenize(src):
	module = 'test'
	return JS('__BRYTHON__.$tokenize(src, module)')

_decorators = []
def push_decorator(ctx):
	_decorators.append( ctx )
def pop_decorators():
	arr = list( _decorators )
	_decorators.length = 0  ## javascript style
	return arr

class Pass:
	def __init__(self, ctx, node):
		pass

class Not:
	def __init__(self, ctx, node):
		self.value = to_ast_node(ctx.tree[0])  ## not standard python

class List:
	def __init__(self, ctx, node):
		self.elts = []
		#self.ctx = 'Load' # 'Store' is (x,y,z) = w
		for a in ctx.tree:
			self.elts.append( to_ast_node(a) )

class Tuple:
	def __init__(self, ctx, node):
		self.elts = []
		#self.ctx = 'Load' # 'Store' is (x,y,z) = w
		for a in ctx.tree:
			self.elts.append( to_ast_node(a) )

class Dict:
	def __init__(self, ctx, node):
		self.keys = []
		self.values = []
		#for i in range(0, len(ctx.items), 2):  ## TODO fix me
		i = 0
		while i < len(ctx.items):
			key = ctx.items[i]
			val = ctx.items[i+1]
			self.keys.append( to_ast_node(key) )
			self.values.append( to_ast_node(val) )
			i += 2

class Subscript:
	def __init__(self, ctx, node):
		self.value = to_ast_node(ctx.value)
		self.slice = Index(value=to_ast_node(ctx.tree[0]))
		#self.ctx = 'Load', 'Store', 'Del'

class Index:
	def __init__(self, value=None):
		self.value = value

class Assign:
	def _collect_targets(self, ctx):
		if ctx.type == 'expr' and ctx.name == 'id':
			a = ctx.tree[0]
			if a.type == 'id':
				self.targets.append( Name(ctx.tree[0]) )
			elif a.type == 'attribute' and a.func == 'getattr' and a.value.type == 'id':
				self.targets.append( Attribute(a,None) )
			else:
				raise TypeError

		elif ctx.type == 'assign':
			self._collect_targets( ctx.tree[0] )
			self._collect_targets( ctx.tree[1] )
		else:
			print('_collect_targets ERROR')
			print( ctx )
			raise TypeError

	def __init__(self, ctx, node):
		print('assign node.........')
		print(ctx)
		self.targets = []
		self._collect_targets( ctx.tree[0] )
		self.value = to_ast_node( ctx.tree[1] )  ## should be an: expr.name==operand

class AugAssign:
	_previous = None
	def __init__(self, ctx, node):
		AugAssign._previous = self
		self.target = None
		self.op = None
		self.value = to_ast_node(ctx.tree[1])

class Num:
	def __init__(self, ctx, node):
		self.n = ctx.value

class Str:
	def __init__(self, ctx, node):
		#self.s = ctx.value  ## old brython
		if len(ctx.tree) == 1:
			self.s = ctx.tree[0]
		else:
			raise TypeError

class Name:
	def __init__(self, ctx=None, name=None):
		if name:
			self.id = name
		elif ctx.type == 'id':
			self.id = ctx.value
		else:
			print ctx
			raise TypeError

class UnaryOp:
	'''
	note: this is constructed directly from an abstract_expr
	'''
	def __init__(self, op=None, operand=None):
		self.op = op
		self.operand = operand

class BinOp:
	def __init__(self, ctx, node):
		print 'BinOp', ctx
		if len(ctx.tree) != 2:
			raise TypeError
		self.left = to_ast_node( ctx.tree[0] )
		self.right = to_ast_node( ctx.tree[1] )
		self.op = ctx.op  ## should be: +,-,*, etc...



class _arguments:
	def __init__(self, ctx):
		self.args = []  ## in Python2 these are Name nodes, in Py3 they are "arg" objects with: `arg`=raw-string and `annotation`=astnode
		self.vararg = None  # string
		self.kwarg = None	# string
		self.defaults = []
		self.kw_defaults = []

		if ctx.type != 'func_args':
			raise TypeError
		for c in ctx.tree:
			if c.type == 'func_arg_id':
				self.args.append( Name(name=c.name) )
				if len(c.tree):
					self.defaults.append( to_ast_node(c.tree[0]) )

			elif c.type == 'func_star_arg' and c.op=='*':
				self.vararg = c.name
			elif c.type == 'func_star_arg' and c.op=='**':
				self.kwarg = c.name
			else:
				raise TypeError

class FunctionDef:
	def __init__(self, ctx, node):
		self.name = ctx.name  ## raw string
		self.args = _arguments( ctx.tree[0] )
		self.body = []
		self.decorator_list = pop_decorators()
		self.returns = None ## python3 returns annotation
		print 'FunctionDef::', ctx
		for child in node.children:
			anode = to_ast_node( child.get_ctx(), node=child )
			if anode:  ## ctx of type: 'single_kw' and token elif/else do not return an ast node
				self.body.append( anode )


class Return:
	def __init__(self, ctx, node):
		self.value = to_ast_node( ctx.tree[0] )


class _keyword:
	def __init__(self, arg, value):
		self.arg = arg  ## raw string
		self.value = value  ## astnode

class Call:
	def __init__(self, ctx, node):
		self.func = to_ast_node( ctx.func )
		self.args = []
		self.keywords = []
		self.starargs = None
		self.kwargs = None

		for c in ctx.tree:
			if c.type == 'call_arg':
				sub = c.tree[0]
				if sub.type == 'kwarg':
					k = _keyword(
						sub.tree[0].value,
						to_ast_node(sub.tree[1])
					)
					self.keywords.append( k )
				else:
					self.args.append( to_ast_node(c.tree[0]) )

			else:
				raise TypeError

class Expr:
	def __init__(self, ctx, node):
		self.value = to_ast_node(ctx.tree[0])

class ClassDef:
	def __init__(self, ctx, node):
		self.name = ctx.name
		self.bases = []
		self.body = []
		self.decorator_list = pop_decorators()

		if len(ctx.tree) == 1:
			e = ctx.tree[0]
			if e.type == 'expr' and e.name == 'tuple':
				t = e.tree[0]
				for b in t.tree:
					self.bases.append( Name(b.tree[0]) )
			else:
				raise TypeError

		for child in node.children:
			if child.get_ctx():
				anode = to_ast_node( child.get_ctx() )
				print 'class body:', anode
				self.body.append( anode )


class Attribute:
	def __init__(self, ctx, node):
		self.value = to_ast_node(ctx.value)
		self.attr = ctx.name
		self._func = ctx.func  ## brython-extra: getattr/setattr


class IfExp:
	'''
	if/elif/else could be translated to javascript switch/case more easily if we track elif statements,
	but the python standard simply treats elif statements as nested if statements in .orelse.
	In the future we can bend this rule when PythonJS becomes fully self-hosted.
	'''
	_previous = None
	def __init__(self, ctx, node):
		if ctx.token == 'if':  ## can also be "elif" and "else"
			IfExp._previous = self
		self.test = to_ast_node( ctx.tree[0] )
		self.body = []
		self.orelse = []
		for child in node.children:
			self.body.append( to_ast_node(child.get_ctx()) )

class For:
	def __init__(self, ctx, node):
		targets = ctx.tree[0]
		if targets.type != 'target_list':
			raise TypeError
		if len(targets.tree) == 1:
			self.target = to_ast_node( targets.tree[0] )
		else:  ## pack into a ast.Tuple
			print('TODO pack for-loop targets into ast.Tuple')
			raise TypeError

		self.iter = to_ast_node( ctx.tree[1] )
		self.body = []
		for child in node.children:
			self.body.append( to_ast_node(child.get_ctx()) )

class While:
	def __init__(self, ctx, node):
		self.test = to_ast_node( ctx.tree[0] )
		self.body = []
		for child in node.children:
			anode = to_ast_node(child.get_ctx())
			if anode:
				self.body.append( anode )


__MAP = {
	'def'		: FunctionDef,
	'assign'	: Assign,
	'return'	: Return,
	'expr'		: Expr,
	'call'		: Call,
	'int'		: Num,
	'str'		: Str,
	'id'		: Name,
	'class'		: ClassDef,
	'op'		: BinOp,
	'attribute' : Attribute,
	'pass'		: Pass,
	'for'		: For,
	'not'		: Not,
	'sub'		: Subscript,
}

def to_ast_node( ctx, node=None ):
	print 'to-ast-node', ctx

	if ctx.type == 'node':
		print 'NODE::', ctx.node
		return to_ast_node( ctx.tree[0], node=ctx.node )

	elif ctx.type == 'assign' and ctx.tree[0].type == 'id' and ctx.tree[0].value == '$temp':
		return AugAssign(ctx, node)

	elif ctx.type in __MAP:
		return __MAP[ ctx.type ]( ctx, node )

	elif ctx.type == 'list_or_tuple':
		if ctx.real == 'list':
			return List(ctx, node)
		elif ctx.real == 'tuple':
			return Tuple(ctx, node)
		else:
			raise TypeError

	elif ctx.type == 'dict_or_set':
		if ctx.real == 'dict':
			return Dict(ctx, node)

	elif ctx.type == 'decorator':
		push_decorator( to_ast_node(ctx.tree[0]) )

	elif ctx.type == 'condition' and ctx.token == 'while':
		return While( ctx, node )

	elif ctx.type == 'condition' and ctx.token == 'if':
		return IfExp( ctx, node )
	elif ctx.type == 'condition' and ctx.token == 'elif':
		a = IfExp( ctx, node )
		IfExp._previous.orelse.append( a )
		IfExp._previous = a

	elif ctx.type == 'single_kw':
		if ctx.token == 'else' or ctx.token == 'elif':
			orelse = IfExp._previous.orelse
			for child in node.children:
				walk_nodes( child, orelse )

		else:
			print 'unknown token for single_kw'
			print ctx
			raise TypeError

	elif ctx.type == 'node_js':
		## special brython inline javascript ##
		if len(ctx.tree) == 1 and '__iadd__' in ctx.tree[0]:
			AugAssign._previous.op = '+'
		elif len(ctx.tree) == 1 and ctx.tree[0].startswith("if($temp.$fast_augm"):
			a,b = ctx.tree[0].split('$globals')
			c = b.split('"')
			if len(c) == 3:
				AugAssign._previous.target = Name( name=c[1] )
			else:
				print(c)
				raise TypeError

		elif len(ctx.tree) == 1 and ctx.tree[0] == 'else':
			pass
		else:
			print '--------special node_js error-------'
			print(ctx)
			raise TypeError

	elif ctx.type == 'abstract_expr':
		if len(ctx.tree)==1 and ctx.tree[0].type=='expr' and ctx.tree[0].name=='call' and len(ctx.tree[0].tree)==1:
			call = ctx.tree[0].tree[0]
			assert call.type=='call'
			func = call.func
			if func.type=='attribute' and func.func=='getattr':
				if func.name=='__neg__':
					return UnaryOp(op='-', operand=to_ast_node(func.value))
				else:
					raise TypeError
			else:
				print '---------abstract_expr error----------'
				print ctx
				raise TypeError
		else:
			print '---------abstract_expr error----------'
			print ctx
			raise TypeError

	else:
		print '---------error----------'
		print node
		print ctx
		raise TypeError


def walk_nodes( node, module ):
	print 'node.type:', node.type

	if node.type == 'expression':
		if node.get_ctx():
			anode = to_ast_node( node.get_ctx(), node=node )
			if anode:  ## decorators do not return
				module.append( anode )
	elif node.get_ctx():
		anode = to_ast_node( node.get_ctx(), node=node )
		if anode:
			module.append( anode )
		#else:
		#	for child in node.children:
		#		walk_nodes( child, module )

	else:
		for child in node.children:
			walk_nodes( child, module )


def parse(source):
	a = brython_tokenize( source )
	module = list()
	walk_nodes( a, module )
	return module


class NodeVisitor:
	def __init__(self, module):
		for node in module:
			self.visit( node )

	def visit(self, node):
		if node is None:
			raise TypeError
		f = getattr(
			self, 
			'visit_'+type(node).__name__, 
		)
		return f( node )

	def visit_Expr(self, node):
		return self.visit(node.value)

	def visit_Str(self, node):
		return node.s

	def visit_Num(self, node):
		return node.n

	def visit_Name(self, node):
		return node.id

	def visit_Pass(self, node):
		return 'pass'

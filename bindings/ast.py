
def brython_tokenize(src):
	module = 'test'
	return JS('$tokenize(src, module)')  ## Brython tokenizer


class Assign:
	def __init__(self, ctx, node):
		self.targets = []
		self.targets.append( to_ast_node(ctx.tree[0]) ) ## should be: expr.name==id
		self.value = to_ast_node( ctx.tree[1] )  ## should be an: expr.name==operand

class Num:
	def __init__(self, ctx, node):
		self.n = ctx.value

class Str:
	def __init__(self, ctx, node):
		self.s = ctx.value

class Name:
	def __init__(self, ctx=None, name=None):
		if name:
			self.id = name
		elif ctx.type == 'id':
			self.id = ctx.value
		else:
			print ctx
			raise TypeError




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
		self.decorator_list = []
		self.returns = None ## python3 returns annotation
		print 'FunctionDef::', ctx
		for child in node.children:
			anode = to_ast_node( child.get_ctx() )
			if anode is None: raise TypeError
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
}

def to_ast_node( ctx, node=None ):
	print 'to-ast-node', ctx

	if ctx.type == 'node':
		print 'NODE::', ctx.node
		return to_ast_node( ctx.tree[0], node=ctx.node )

	elif ctx.type in __MAP:
		return __MAP[ ctx.type ]( ctx, node )

	else:
		print '-------------------------'
		print ctx
		raise TypeError


def walk_nodes( node, module ):
	print 'node.type:', node.type

	if node.type == 'expression':
		if node.get_ctx():
			anode = to_ast_node( node.get_ctx(), node=node )
			module.append( anode )
	elif node.get_ctx():
		anode = to_ast_node( node.get_ctx(), node=node )
		module.append( anode )		
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

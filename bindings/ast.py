
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
		print 'Num:', ctx.value
		self.n = ctx.value

class Str:
	def __init__(self, ctx, node):
		print 'Str:', ctx.value
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

		print 'Name:', self.id

class _arguments:
	def __init__(self, ctx):
		self.args = []
		self.vararg = None  # string
		self.kwarg = None	# string
		self.defaults = []
		self.kw_defaults = []

		if ctx.type != 'func_args':
			raise TypeError
		for c in ctx.tree:
			if c.type == 'func_arg_id':
				self.args.append( Name(name=c.name) )
			elif c.type == 'func_star_arg' and c.op=='*':
				self.vararg = c.name
			elif c.type == 'func_star_arg' and c.op=='**':
				self.kwarg = c.name
			else:
				raise TypeError



class BinOp:
	def __init__(self, ctx, node):
		print 'BinOp', ctx
		self.left = to_ast_node( ctx.tree[0] )
		self.right = to_ast_node( ctx.tree[1] )
		self.op = ctx.op  ## should be: +,-,*, etc...

class Return:
	def __init__(self, ctx, node):
		self.value = to_ast_node( ctx.tree[0] )

class FunctionDef:
	def __init__(self, ctx, node):
		self.name = ctx.name
		self.args = _arguments( ctx.tree[0] )
		self.body = []
		self.decorator_list = []
		self.returns = None ## python3 returns annotation
		print 'FunctionDef::', node
		for child in node.children:
			anode = to_ast_node( child.get_ctx() )
			self.body.append( anode )


class Call:
	def __init__(self, ctx, node):
		self.func = None
		self.args = []
		self.keywords = []
		self.starargs = None
		self.kwargs = None

		for c in ctx.tree:
			if c.type == 'call_arg':
				self.args.append( to_ast_node(c.tree[0]) )

class Expr:
	def __init__(self, ctx, node):
		self.value = to_ast_node(ctx.tree[0])

class ClassDef:
	def __init__(self, ctx, node):
		print 'CLAss', 
		print ctx
		print node
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
}

def to_ast_node( ctx, node=None ):
	print 'to-ast-node', ctx
	print 'NODE::', node

	if ctx.type == 'node':

		return to_ast_node( ctx.tree[0], node=ctx.node )

	elif ctx.type == 'expr' and ctx.name == 'operand':
		return BinOp( ctx.tree[0] )

	elif ctx.type in __MAP:
		return __MAP[ ctx.type ]( ctx, node )


	else:
		print '-------------------------'
		print ctx
		raise TypeError


def walk_nodes( node, module ):
	print 'node.type:', node.type
	print node

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
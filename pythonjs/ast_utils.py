import ast

class CollectNames(ast.NodeVisitor):
	_names_ = []
	def visit_Name(self, node):
		self._names_.append( node )

def collect_names(node):
	CollectNames._names_ = names = []
	CollectNames().visit( node )
	return names


class CollectReturns(ast.NodeVisitor):
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
		if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):  ## assignment to local - TODO support `a=b=c`
			local_vars.add( n.targets[0].id )
		elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple):
			for c in n.targets[0].elts:
				local_vars.add( c.id )
		elif isinstance(n, ast.Global):
			global_vars.update( n.names )
		elif hasattr(n, 'body') and not isinstance(n, ast.FunctionDef):
			# do a recursive search inside new block except function def
			l, g = retrieve_vars(n.body)
			local_vars.update(l)
			global_vars.update(g)
			if hasattr(n, 'orelse'):
				l, g = retrieve_vars(n.orelse)
				local_vars.update(l)
				global_vars.update(g) 

	return local_vars, global_vars

def retrieve_properties(body):
	props = set()
	for n in body:
		if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Attribute) and isinstance(n.targets[0].value, ast.Name) and n.targets[0].value.id == 'self':
			props.add( n.targets[0].attr )
		elif hasattr(n, 'body') and not isinstance(n, ast.FunctionDef):
			props.update( retrieve_properties(n.body) )
	return props
	
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
		if isinstance(decorator, ast.Call) and decorator.func.id == 'typedef':
			c = decorator
			assert len(c.args) == 0 and len(c.keywords)
			for kw in c.keywords:
				assert isinstance( kw.value, ast.Name)
				typedefs[ kw.arg ] = kw.value.id

	info = {
		'locals':local_vars, 
		'globals':global_vars, 
		'name_nodes':names, 
		'return_nodes':returns,
		'typedefs': typedefs
	}
	return info

def inspect_method( node ):
	info = inspect_function( node )
	info['properties'] = retrieve_properties( node.body )
	return info
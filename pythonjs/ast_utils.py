import ast
import typedpython

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
		if isinstance(n, ast.Expr):
			if isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id=='__let__':
				if isinstance(n.value.args[0], ast.Name):  ## could be ast.Attribute, `let self.x : int = n`
					local_vars.add( n.value.args[0].id )

		elif isinstance(n, ast.Assign):
			user_typedef = None
			self_typedef = None
			if len(n.targets) == 2:
				if isinstance(n.targets[1], ast.Attribute) and isinstance(n.targets[1].value, ast.Name) and n.targets[1].value.id=='self':
					continue

			for i,u in enumerate(n.targets):
				if isinstance(u, ast.Name):

					if i==0:
						## dirty hack that catches `int = x = 1` or `int = x`,
						## this should be deprecated because it is not rust style,
						## and only works with reserved standard types like:
						## float, int, and str in typedpython.types
						if u.id in typedpython.types:
							user_typedef = u.id
						else:
							local_vars.add( u.id )
					elif user_typedef:
						local_vars.add( '%s=%s' %(user_typedef, u.id) )
						user_typedef = None

					else:  ## regular local variable ##
						local_vars.add( u.id )

				elif isinstance(u, ast.Tuple):
					for uu in u.elts:
						if isinstance(uu, ast.Name):
							local_vars.add( uu.id )
						else:
							raise NotImplementedError(uu)
				else:
					pass  ## skips assignment to an attribute `a.x = y`

			if user_typedef:  ## `int x`
				if  isinstance(n.value, ast.Name):
					x = '%s=%s' %(user_typedef, n.value.id)
					#raise SyntaxError(x)
					#if len(n.targets)==2: raise SyntaxError(n.targets)
					local_vars.add( x )
				elif isinstance(n.value, ast.Num):
					x = '%s=%s' %(user_typedef, n.value.n)
					#if len(n.targets)==2: raise SyntaxError(n.targets)
					local_vars.add( x )
				else:
					#raise SyntaxError(n.targets)
					#raise SyntaxError(n.value.func.value.id)
					#raise SyntaxError(user_typedef)
					pass

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
				if isinstance( kw.value, ast.Name):
					typedefs[ kw.arg ] = kw.value.id
				elif isinstance( kw.value, ast.Str):
					typedefs[ kw.arg ] = '"%s"' %kw.value.s
				else:
					raise SyntaxError(kw.value)

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
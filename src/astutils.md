Ast Utils
---------

ast helper functions and classes

```python

go_types = 'bool string int float64'.split()
go_hacks = ('__go__array__', '__go__arrayfixed__', '__go__map__', '__go__func__')
COLLECTION_TYPES = go_hacks


class NodeVisitorBase( ast.NodeVisitor ):
	def __init__(self, source_code):
		self._line = None
		self._line_number = 0
		self._stack = []        ## current path to the root
		self._source = source_code.splitlines()

	def visit(self, node):
		"""Visit a node."""
		## modified code of visit() method from Python 2.7 stdlib
		self._stack.append(node)
		if hasattr(node, 'lineno'):
			lineno = node.lineno
			if node.lineno < len(self._source):
				src = self._source[ node.lineno ]
				self._line_number = node.lineno
				self._line = src

		method = 'visit_' + node.__class__.__name__
		visitor = getattr(self, method, self.generic_visit)
		res = visitor(node)
		self._stack.pop()
		return res

	def format_error(self, node):
		lines = []
		if self._line_number > 0:
			n = self._line_number-1
			lines.append( '%s:	%s '%(n, self._source[n]) )

		lines.append( '%s:	%s '%(self._line_number, self._source[self._line_number]) )

		for i in range(1,2):
			if self._line_number+i < len(self._source):
				n = self._line_number + i
				lines.append( '%s:	%s '%(n, self._source[n]) )

		msg = 'line %s\n%s\n%s\n' %(self._line_number, '\n'.join(lines), node)
		msg += 'Depth Stack:\n'
		for l, n in enumerate(self._stack):
			#msg += str(dir(n))
			if isinstance(n, ast.Module):
				pass
			else:
				msg += '%s%s line:%s col:%s\n' % (' '*(l+1)*2, n.__class__.__name__, n.lineno-1, n.col_offset)
		return msg



class TransformSuperCalls( ast.NodeVisitor ):  ## used by dart and lua backend
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
				if len(n.value.args)==0:	## syntax: `let mut x = n`  ## requires rustc to infer type
					assert n.value.keywords
					for kw in n.value.keywords:
						if kw.arg=='mutable': continue  ## TODO rename to __mutable__
						else: local_vars.add(kw.arg)
				elif isinstance(n.value.args[0], ast.Name):  ## could be ast.Attribute, `let self.x : int = n`
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
				elif isinstance( kw.value, ast.Call) and isinstance(kw.value.func, ast.Name) and kw.value.func.id=='__arg_array__':
					typedefs[ kw.arg ] = '"%s"' %kw.value.args[0].s
				elif isinstance( kw.value, ast.Call) and isinstance(kw.value.func, ast.Name) and kw.value.func.id=='__arg_map__':
					typedefs[ kw.arg ] = '"%s"' %kw.value.args[0].s
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

```

Special Exceptions
------------------
these a special exceptions that are raise to signal the caller to do special hacks.

```python

## used by Go backend ##
class GenerateGenericSwitch( SyntaxError ): pass
class GenerateTypeAssert( SyntaxError ): pass
class GenerateSlice( SyntaxError ): pass  ## c++ backend
class GenerateListComp( SyntaxError ): pass  ## c++ and rust backend


```
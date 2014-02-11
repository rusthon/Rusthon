# _*_ coding: utf-8 _*_
# PythonJS to LuaJS Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"

import ast
import pythonjs_to_lua

class LuajsGenerator( pythonjs_to_lua.LuaGenerator ):

	def _visit_call_helper_get_call_special(self, node):
		'''
		lua.js has a bug where an extra "()" is required around `__get__(x,'__call__')({},{})`
		this causes a syntax error in normal Lua.
		'''
		name = self.visit(node.func)
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		return '(%s(%s))' % (name, args)


	def visit_Import(self, node):
		#for alias in node.names:
		#	return 'require "%s"' %alias.name
		return ''

	def _inline_code_helper(self, s):
		if 'function() return socket.gettime() end' in s:
			s = s.replace('socket.gettime()', 'os.clock()')
		return s



def main(script):
	tree = ast.parse(script)
	return LuajsGenerator().visit(tree)


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

	lua = main( data )
	print( lua )


if __name__ == '__main__':
	command()
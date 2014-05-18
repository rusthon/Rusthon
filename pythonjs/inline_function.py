# AST Function Inliner
# by Brett Hartshorn - copyright 2013
# License: "New BSD"
import ast, copy
from ast_utils import *

class Inliner:
	def setup_inliner(self, writer):
		self.writer = writer
		self._with_inline = False
		self._inline = []
		self._inline_ids = 0
		self._inline_breakout = False

	def inline_helper_remap_names(self, remap):
		return "JS('var %s')" %','.join(remap.values())

	def inline_helper_return_id(self, return_id):
		return "JS('var __returns__%s = null')"%return_id

	def inline_function(self, node):
		name = self.visit(node.func)
		fnode = self._global_functions[ name ]
		fnode = copy.deepcopy( fnode )
		finfo = inspect_function( fnode )
		remap = {}
		for n in finfo['name_nodes']:
			if n.id not in finfo['locals']: continue

			if isinstance(n.id, ast.Name):
				raise RuntimeError

			if n.id not in remap:
				new_name = n.id + '_%s'%self._inline_ids
				remap[ n.id ] = new_name
				self._inline_ids += 1

			n.id = remap[ n.id ]

		if remap:
			self.writer.write( self.inline_helper_remap_names(remap) )
			for n in remap:
				if n in finfo['typedefs']:
					self._func_typedefs[ remap[n] ] = finfo['typedefs'][n]

		offset = len(fnode.args.args) - len(fnode.args.defaults)
		for i,ad in enumerate(fnode.args.args):
			if i < len(node.args):
				ac = self.visit( node.args[i] )
			else:
				assert fnode.args.defaults
				dindex = i - offset
				ac = self.visit( fnode.args.defaults[dindex] )

			ad = remap[ self.visit(ad) ]
			self.writer.write( "%s = %s" %(ad, ac) )


		return_id = name + str(self._inline_ids)
		self._inline.append( return_id )

		self.writer.write( self.inline_helper_return_id( return_id ))
		#if len( finfo['return_nodes'] ) > 1:  ## TODO fix me
		if True:
			self._inline_breakout = True
			self.writer.write('while True:')
			self.writer.push()
			for b in fnode.body:
				self.visit(b)

			if not len( finfo['return_nodes'] ):
				self.writer.write('break')
			self.writer.pull()
			#self._inline_breakout = False
		else:
			for b in fnode.body:
				self.visit(b)

		if self._inline.pop() != return_id:
			raise RuntimeError

		for n in remap:
			gname = remap[n]
			for n in finfo['name_nodes']:
				if n.id == gname:
					n.id = n

		return '__returns__%s' %return_id

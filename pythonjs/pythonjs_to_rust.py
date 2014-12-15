#!/usr/bin/env python
# PythonJS to Go Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import os, sys
import ast
import pythonjs_to_go

go_types = 'bool string int float64'.split()
rust_hacks = ('__rust__array__', '__rust__arrayfixed__', '__rust__map__', '__rust__func__')
go_hacks = ('__go__array__', '__go__arrayfixed__', '__go__map__', '__go__func__')
COLLECTION_TYPES = rust_hacks + go_hacks

class GenerateGenericSwitch( SyntaxError ): pass
class GenerateTypeAssert( SyntaxError ): pass


class RustGenerator( pythonjs_to_go.GoGenerator ):

	def __init__(self, requirejs=False, insert_runtime=False):
		pythonjs_to_go.GoGenerator.__init__(self, requirejs=False, insert_runtime=False)
		self._globals = {
			'string' : set()
		}
		self._cpp = False
		self._cheader = []
		self._cppheader = []

	def reset(self):
		self._cheader = []
		self._cppheader = []


	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		#return '"%s"' % s
		if self._function_stack: return '"%s".to_string()' % s
		else: return '"%s"' % s


	def visit_Is(self, node):
		return '=='

	def visit_IsNot(self, node):
		return '!='

	def visit_If(self, node):
		out = []
		test = self.visit(node.test)
		if test.startswith('(') and test.endswith(')'):
			out.append( 'if %s {' %test )
		else:
			out.append( 'if (%s) {' %test )

		self.push()

		for line in list(map(self.visit, node.body)):
			if line is None: continue
			out.append( self.indent() + line )

		orelse = []
		for line in list(map(self.visit, node.orelse)):
			orelse.append( self.indent() + line )

		self.pull()

		if orelse:
			out.append( self.indent() + '} else {')
			out.extend( orelse )

		out.append( self.indent() + '}' )

		return '\n'.join( out )

	## can not assume that all numbers are signed integers
	#def visit_Num(self, node):
	#	if type(node.n) is int: return str(node.n) + 'i'
	#	else: return str(node.n)

	def visit_Index(self, node):
		if isinstance(node.value, ast.Num):
			return str(node.value.n)
		else:
			return self.visit(node.value)


	def visit_Name(self, node):
		if node.id == 'None':
			return 'nil'
		elif node.id == 'True':
			return 'true'
		elif node.id == 'False':
			return 'false'
		#elif node.id == 'null':
		#	return 'nil'
		return node.id

	def get_subclasses( self, C ):
		'''
		returns all sibling subclasses, C can be a subclass or the base class
		'''
		subclasses = set()
		self._collect_subclasses(C, subclasses)
		return subclasses

	def _collect_subclasses(self, C, subclasses):
		node = self._classes[ C ]
		if len(node._parents)==0:
			for sub in node._subclasses:
				subclasses.add( sub )
		else:
			for parent in node._parents:
				self._collect_subclasses(parent, subclasses)


	def visit_ClassDef(self, node):
		self._class_stack.append( node )
		if not hasattr(node, '_parents'):  ## only setup on the first pass
			node._parents = set()
			node._struct_def = dict()
			node._subclasses = set()  ## required for generics generator
			## subclasses must be a struct union so that Go can convert between struct types
			node._subclasses_union = dict()

		out = []
		sdef = dict()
		props = set()
		bases = set()
		base_classes = set()

		self._classes[ node.name ] = node
		self._class_props[ node.name ] = props
		if node.name not in self.method_returns_multiple_subclasses:
			self.method_returns_multiple_subclasses[ node.name ] = set()
		
		#self.interfaces[ node.name ] = set()


		for base in node.bases:
			n = self.visit(base)
			if n == 'object':
				continue
			node._parents.add( n )

			bases.add( n )
			if n in self._class_props:
				props.update( self._class_props[n] )
				base_classes.add( self._classes[n] )
			#else:  ## special case - subclassing a builtin like `list`
			#	continue

			for p in self._classes[ n ]._parents:
				bases.add( p )
				props.update( self._class_props[p] )
				base_classes.add( self._classes[p] )

			self._classes[ n ]._subclasses.add( node.name )


		for decor in node.decorator_list:  ## class decorators
			if isinstance(decor, ast.Call):
				assert decor.func.id=='__struct__'
				#props.update( [self.visit(a) for a in decor.args] )
				for kw in decor.keywords:
					props.add( kw.arg )
					T = kw.value.id
					sdef[ kw.arg ] = T


		init = None
		method_names = set()
		for b in node.body:
			if isinstance(b, ast.FunctionDef):
				method_names.add( b.name )
				if b.name == '__init__':
					init = b
			elif isinstance(b, ast.Expr) and isinstance(b.value, ast.Dict):
				for i in range( len(b.value.keys) ):
					k = self.visit( b.value.keys[ i ] )
					if isinstance(b.value.values[i], ast.Str):
						v = b.value.values[i].s
					else:
						v = self.visit( b.value.values[i] )
					sdef[k] = v

		for k in sdef:
			v = sdef[k]
			#if v=='interface{}':  ## deprecated
			#	self.interfaces[node.name].add(k)

		node._struct_def.update( sdef )
		unionstruct = dict()
		unionstruct.update( sdef )
		for pname in node._parents:
			parent = self._classes[ pname ]
			parent._subclasses_union.update( sdef )        ## first pass
			unionstruct.update( parent._subclasses_union ) ## second pass


		parent_init = None
		if base_classes:
			for bnode in base_classes:
				for b in bnode.body:
					if isinstance(b, ast.FunctionDef):
						if b.name in method_names:
							self.catch_call.add( '%s.%s' %(bnode.name, b.name))
							n = b.name
							b.name = '%s_%s'%(bnode.name, b.name)
							out.append( self.visit(b) )
							b.name = n
							continue
						if b.name == '__init__':
							parent_init = {'class':bnode, 'init':b}
							#continue
						out.append( self.visit(b) )

		if self._cpp:
			out.append( 'class %s {' %node.name)
			out.append( '  public:')
		else:
			out.append( 'struct %s {' %node.name)
			#out.append( '	__class__ : String,')

		if base_classes:
			for bnode in base_classes:
				## Go only needs the name of the parent struct and all its items are inserted automatically ##
				out.append('%s' %bnode.name)
				## Go allows multiple a variable to redefined by the sub-struct,
				## but this can throw an error: `invalid operation: ambiguous selector`
				## removing the duplicate name here fixes that error.
				for key in bnode._struct_def.keys():
					#if key in sdef:
					#	sdef.pop(key)
					if key in unionstruct:
						unionstruct.pop(key)

		node._struct_init_names = []  ## save order of struct layout

		for name in unionstruct:
			if unionstruct[name]=='interface{}': raise SyntaxError('interface{} is deprecated')
			node._struct_init_names.append( name )

			if self._cpp:
				out.append('	%s  %s;' %(unionstruct[name], name ))
			else:
				out.append('	%s : %s,' %(name, unionstruct[name]))


		self._rust_trait = []
		self._cpp_class_header = []
		impl  = []
		self.push()
		for b in node.body:
			if isinstance(b, ast.FunctionDef):
				impl.append( self.visit(b) )
		self.pull()

		if self._cpp:
			for impl_def in self._cpp_class_header:
				out.append( '\t' + impl_def )

			if init:
				out.append('	%s( %s ) { this->__init__( %s ); }' %(node.name, init._args_signature, ','.join(init._arg_names)) )

			out.append('};')
		else:
			out.append('}')


		if self._cpp:
			for impl_def in impl: out.append( impl_def )

		else:
			## using a trait is not required, a struct type can be directly implemented.
			## note: methods require a lambda wrapper to be passed to another function.
			#out.append('trait %s {' %node.name)
			#for trait_def in self._rust_trait: out.append( '\t'+ trait_def )
			#out.append('}')
			#out.append('impl %s for %sStruct {' %(node.name, node.name))
			#for impl_def in impl: out.append( impl_def )
			#out.append('}')

			out.append('impl %s {' %node.name)
			for impl_def in impl: out.append( impl_def )
			out.append('}')


			if False:  ## this will not work in rust because we need to pass in a lifetime variable
				if init or parent_init:
					if parent_init:
						classname = parent_init['class'].name
						init = parent_init['init']
					else:
						classname = node.name

					out.append( 'fn __new__%s( %s ) -> %s {' %(node.name, init._args_signature, node.name))
					out.append( '  let ob = %s{ __class__:"%s".to_string() };' %(node.name, node.name) )
					out.append( '  ob.__init__(%s);' %','.join(init._arg_names))
					out.append( '  return ob;')
					out.append('}')

				else:
					out.append( 'fn __new__%s() -> %s {' %(node.name, node.name))
					out.append( '  let ob = %s{ __class__:"%s".to_string() };' %(node.name, node.name) )
					out.append( '  return ob;')
					out.append('}')



		self.catch_call = set()
		self._class_stack.pop()
		return '\n'.join(out)


	def _visit_call_special( self, node ):
		fname = self.visit(node.func)
		assert fname in self.catch_call
		assert len(self._class_stack)
		if len(node.args):
			if isinstance(node.args[0], ast.Name) and node.args[0].id == 'self':
				node.args.remove( node.args[0] )

		#name = '_%s_' %self._class_stack[-1].name
		name = 'self.'
		name += fname.replace('.', '_')
		return self._visit_call_helper(node, force_name=name)


	def visit_Subscript(self, node):
		if isinstance(node.slice, ast.Ellipsis):
			raise NotImplementedError( 'ellipsis')
		else:
			## deference pointer and then index
			if isinstance(node.slice, ast.Slice):
				r = '&(*%s)[%s]' % (self.visit(node.value), self.visit(node.slice))
			else:
				r = '(*%s)[%s]' % (self.visit(node.value), self.visit(node.slice))

			if isinstance(node.value, ast.Name) and node.value.id in self._known_arrays:
				target = node.value.id
				#value = self.visit( node.value )
				cname = self._known_arrays[target]
				#raise GenerateGenericSwitch( {'target':target, 'value':r, 'class':cname} )
				raise GenerateGenericSwitch( {'value':r, 'class':cname} )

			return r



	def visit_Slice(self, node):
		# http://doc.rust-lang.org/std/slice/
		#![feature(slicing_syntax)]

		lower = upper = step = None
		if node.lower:
			lower = self.visit(node.lower)
		if node.upper:
			upper = self.visit(node.upper)
		if node.step:
			step = self.visit(node.step)

		if lower and upper:
			return '%s..%s' %(lower,upper)
		elif upper:
			return '0..%s' %upper
		elif lower:
			return '%s..'%lower
		else:
			raise SyntaxError('TODO slice')


	def visit_Print(self, node):
		r = []
		for e in node.values:
			s = self.visit(e)
			if isinstance(e, ast.List):
				r.append('println!("{}", %s);' %s[1:-1])
			else:
				r.append('println!("{}", %s);' %s)
		return ''.join(r)

	#def visit_Expr(self, node):
	#	return self.visit(node.value)
	def visit_Expr(self, node):
		# XXX: this is UGLY
		s = self.visit(node.value)
		if s.strip() and not s.endswith(';'):
			s += ';'
		if s==';': return ''
		else: return s

	def visit_Import(self, node):
		r = [alias.name.replace('__SLASH__', '/') for alias in node.names]
		if r:
			for name in r:
				self._imports.add('import("%s");' %name)
		return ''

	def visit_Module(self, node):
		header = [
			'#![allow(unknown_features)]',
			'#![feature(slicing_syntax)]',
			'#![feature(asm)]',
			'#![allow(unused_parens)]',
			'#![allow(non_camel_case_types)]',
			'#![allow(dead_code)]',
			'#![allow(non_snake_case)]',
			'#![allow(unused_mut)]',  ## if the compiler knows its unused - then it still can optimize it...?
			'#![allow(unused_variables)]',
			'extern crate libc;',
			'use libc::{c_int, size_t};',
		]
		lines = []

		for b in node.body:
			line = self.visit(b)

			if line:
				for sub in line.splitlines():
					if sub==';':
						#raise SyntaxError('bad semicolon')
						pass
					else:
						lines.append( sub )
			else:
				if isinstance(b, ast.Import):
					pass
				else:
					raise SyntaxError(b)

		if len(self._kwargs_type_.keys())==0:
			lines.append('struct _kwargs_type_;')
		else:
			lines.append('struct _kwargs_type_ {')
			for name in self._kwargs_type_:
				type = self._kwargs_type_[name]
				if self._cpp:
					lines.append( '  %s %s;' %(type,name))
					lines.append( '  bool __use__%s;' %name)
				else:
					lines.append( '  %s : %s,' %(name,type))
					lines.append( '  __use__%s : bool,' %name)
			lines.append('}')

		lines.append('mod rusthon {')
		## copy string globals into rusthon module
		lines.append('}')

		if len(self._cheader):
			header.append('extern "C" {')
			for line in self._cheader:
				header.append(line)
				raise SyntaxError(line)
			header.append('}')

		lines = header + list(self._imports) + lines
		return '\n'.join( lines )


	def visit_Compare(self, node):
		comp = [ '(']
		comp.append( self.visit(node.left) )
		comp.append( ')' )

		for i in range( len(node.ops) ):
			comp.append( self.visit(node.ops[i]) )

			if isinstance(node.comparators[i], ast.BinOp):
				comp.append('(')
				comp.append( self.visit(node.comparators[i]) )
				comp.append(')')
			else:
				comp.append( self.visit(node.comparators[i]) )

		return ' '.join( comp )

	def visit_For(self, node):
		target = self.visit(node.target)
		lines = []
		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):

			if node.iter.func.id == 'range':
				if len(node.iter.args)==1:
					iter = self.visit(node.iter.args[0])
					lines.append('for %s in range(0u, %s) {' %(target, iter))
				elif len(node.iter.args)==2:
					start = self.visit(node.iter.args[0])
					iter = self.visit(node.iter.args[1])
					lines.append('for %s in range(%s as uint, %s as uint) {' %(target, start, iter))
				else:
					raise SyntaxError('invalid for range loop')

			elif node.iter.func.id == 'enumerate':
				iter = self.visit(node.iter.args[0])
				idx = self.visit(node.target.elts[0])
				tar = self.visit(node.target.elts[1])
				lines.append('for %s,%s := range *%s {' %(idx,tar, iter))

			else: ## generator function
				gfunc = node.iter.func.id
				gargs = ','.join( [self.visit(e) for e in node.iter.args] )
				lines.append('__gen%s := __new__%s(%s)' %(gfunc,gfunc, gargs))
				lines.append('for __gen%s.__done__ != 1 {' %gfunc)
				lines.append('	%s := __gen%s.next()' %(self.visit(node.target), gfunc))

		elif isinstance(node.target, ast.List) or isinstance(node.target, ast.Tuple):
			iter = self.visit( node.iter )
			key = self.visit(node.target.elts[0])
			val = self.visit(node.target.elts[1])
			lines.append('for %s,%s := range *%s {' %(key,val, iter))

		else:

			if not hasattr(node.iter, 'uid'):
				## in the first rustc pass we assume regular references using `&X`,
				## for loops over an array of String's requires the other type using just `X` or `ref X`
				node.iter.uid = self.uid()
				node.iter.is_ref = True
				self.unodes[ node.iter.uid ] = node.iter


			iter = self.visit( node.iter )
			if node.iter.is_ref:
				lines.append('for &%s in %s.iter() { //magic:%s' %(target, iter, node.iter.uid))
			else:
				lines.append('for %s in %s.iter() { //magic:%s' %(target, iter, node.iter.uid))

		self.push()
		for b in node.body:
			lines.append( self.indent()+self.visit(b) )
		self.pull()
		lines.append( self.indent()+'}' )  ## end of for loop
		return '\n'.join(lines)

	def _gccasm_to_llvmasm(self, asmcode):
		r = []
		for i,char in enumerate(asmcode):
			if i+1==len(asmcode): break
			next = asmcode[i+1]
			if next.isdigit() and char == '%':
				r.append( '$' )
			else:
				r.append( char )
		r.append('"')
		a = ''.join(r)
		return a.replace('%%', '%')

	def _visit_call_helper(self, node, force_name=None):
		fname = force_name or self.visit(node.func)
		is_append = False

		if fname.endswith('.append'): ## TODO - deprecate append to pushX ?
			is_append = True
			arr = fname.split('.append')[0]

		if fname == '__asm__':
			ASM_WRITE_ONLY = '='  ## write constraint
			ASM_ANY_REG    = 'r'  ## register name: r, eax, ax, al,  ebx, bx, bl
			ASM_OUT_DEFAULT = ASM_WRITE_ONLY + ASM_ANY_REG

			code = []
			if self._cpp:
				code.append('asm')
			else:
				# http://doc.rust-lang.org/guide-unsafe.html#inline-assembly
				code.append('unsafe{ asm!')

			volatile = False
			alignstack = False
			outputs = []
			inputs = []
			clobber = []
			asmcode = None
			for kw in node.keywords:
				if kw.arg == 'volatile' and kw.value.id.lower()=='true':
					volatile = True
				elif kw.arg == 'alignstack' and kw.value.id.lower()=='true':
					alignstack = True
				elif kw.arg == 'outputs':
					write_mode = ASM_OUT_DEFAULT
					if isinstance(kw.value, ast.List):
						mode = kw.value.elts[0].s
						output = kw.value.elts[1].id
						outputs.append('"%s" (%s)' %(mode, output))
					else:
						outputs.append('"%s" (%s)' %(write_mode, kw.value.id))

				elif kw.arg == 'inputs':
					if isinstance(kw.value, ast.List):
						for elt in kw.value.elts:
							if isinstance(elt, ast.List):
								register = elt.elts[0].s
								input = elt.elts[1].id
								inputs.append('"%s" (%s)' %(register, input))
							else:
								inputs.append('"%s" (%s)' %(ASM_ANY_REG,elt.id))
					else:
						inputs.append('"%s" (%s)' %(ASM_ANY_REG,kw.value.id))
				elif kw.arg == 'clobber':
					if isinstance(kw.value, ast.List):
						clobber.extend( ['"%s"' %elt.s for elt in kw.value.elts] )
					else:
						clobber.extend(
							['"%s"'%clob for clob in kw.value.s.split(',') ]
						)

				elif kw.arg == 'code':
					asmcode = '"%s"' %kw.value.s

			if volatile:
				if self._cpp:
					code.append( 'volatile' )

			assert asmcode
			if not self._cpp:
				## rust asm uses llvm as its backend,
				## llvm asm syntax is slightly different from regular gcc,
				## input arguments in gcc are given as `%N`,
				## while in llvm they are given as `$N`
				asmcode = self._gccasm_to_llvmasm(asmcode)

			code.append( '(' )
			code.append( asmcode )
			code.append( ':' )
			if outputs:
				code.append( ','.join(outputs) )
			code.append( ':' )
			if inputs:
				code.append( ','.join(inputs) )
			code.append( ':' )
			if clobber:
				code.append( ','.join(clobber) )

			if self._cpp:
				code.append( ');')
			else:
				code.append( ':' )  ## rust options
				ropts = []
				if volatile:
					ropts.append('"volatile"')
				if alignstack:
					ropts.append('"alignstack"')

				code.append( ','.join(ropts) )
				code.append( '); } // end unsafe' )


			return ' '.join( code )

		elif fname == '__let__' and isinstance(node.args[0], ast.Name):
			if self._function_stack:
				self._known_vars.add( node.args[0].id )
				self._vars.remove( node.args[0].id )
				V = 'let'
			else:
				V = 'static'

			mutable = False
			for kw in node.keywords:
				if kw.arg=='mutable':
					if kw.value.id.lower()=='true':
						mutable = True

			if len(node.args) == 1:
				return '%s %s			/* declared */' %(V, node.args[0].id)
			elif len(node.args) == 2:
				if self._cpp:
					return '%s  %s' %(node.args[1].s, node.args[0].id)
				else:
					if mutable:
						return '%s mut %s : %s' %(V, node.args[0].id, node.args[1].s)
					else:
						return '%s %s : %s' %(V, node.args[0].id, node.args[1].s)

			elif len(node.args) == 3:
				if self._cpp:
					return '%s  %s = %s' %(node.args[1].s, node.args[0].id, self.visit(node.args[2]))
				else:
					if mutable:
						return '%s mut %s : %s = %s' %(V, node.args[0].id, node.args[1].s, self.visit(node.args[2]))
					else:
						return '%s %s : %s = %s' %(V, node.args[0].id, node.args[1].s, self.visit(node.args[2]))
			else:
				raise SyntaxError('TODO __let__ %s' %len(node.args))

		elif fname == '__let__' and isinstance(node.args[0], ast.Attribute):
			if isinstance(node.args[0].value, ast.Name) and node.args[0].value.id=='self':
				if self._cpp:
					return 'this->%s = %s' %(node.args[0].attr, self.visit(node.args[-1]))
				else:
					return 'self.%s = %s' %(node.args[0].attr, self.visit(node.args[-1]))

		elif fname=='str' and not self._cpp:
			if self._cpp:
				#return 'static_cast<std::ostringstream*>( &(std::ostringstream() << %s) )->str()' %self.visit(node.args[0])
				return 'std::to_string(%s)' %self.visit(node.args[0])  ## only works with number types
			else:
				return '%s.to_string()' %self.visit(node.args[0])

		elif fname == 'range':  ## TODO - some syntax for mutable
			assert len(node.args)
			fname = '&mut ' + fname
			fname += str(len(node.args))

		elif fname == 'len':
			return '%s.len()' %self.visit(node.args[0])

		elif fname == 'go.type_assert':
			val = self.visit(node.args[0])
			type = self.visit(node.args[1])
			#return '%s(*%s)' %(type, val )
			raise GenerateTypeAssert( {'type':type, 'value':val} )


		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''

		if node.keywords:
			if args: args += ','
			args += '_kwargs_type_{'
			x = ['%s:%s' %(kw.arg,self.visit(kw.value)) for kw in node.keywords]
			x.extend( ['__use__%s:true' %kw.arg for kw in node.keywords] )
			args += ','.join( x )
			args += '}'

		if node.starargs:
			if args: args += ','
			args += '*%s...' %self.visit(node.starargs)

		if is_append: ## this is a bad rule, it is better the user must call `push` instead of `append`
			item = args
			#if item in self._known_instances:
			#	classname = self._known_instances[ item ]
			#	if arr in self._known_arrays and classname != self._known_arrays[arr]:
			return '%s.push( %s )' %(arr, item)

		elif self._with_gojs:
			if isinstance(node.func, ast.Attribute):
				fname = node.func.attr
				obname = self.visit(node.func.value)
				return 'Get("%s").Call("%s",%s)' % (obname, fname, args)

			else:
				return 'Call("%s",%s)' % (fname, args)

		else:

			if isinstance(node.func, ast.Attribute) and False:
				if isinstance(node.func.value, ast.Name):
					varname = node.func.value.id
					if varname in self._known_vars:
						#raise SyntaxError(varname + ' is known class::' + self._known_instances[varname] + '%s(%s)' % (fname, args))
						cname = self._known_instances[varname]
						if node.func.attr in self.method_returns_multiple_subclasses[ cname ]:
							raise SyntaxError('%s(%s)' % (fname, args))


			return '%s(%s)' % (fname, args)

	def _visit_call_helper_go(self, node):
		name = self.visit(node.func)
		if name == '__go__':
			return 'go %s' %self.visit(node.args[0])
		elif name == '__go_make__':
			if len(node.args)==2:
				return 'make(%s, %s)' %(self.visit(node.args[0]), self.visit(node.args[1]))
			elif len(node.args)==3:
				return 'make(%s, %s, %s)' %(self.visit(node.args[0]), self.visit(node.args[1]), self.visit(node.args[1]))
			else:
				raise SyntaxError('go make requires 2 or 3 arguments')
		elif name == '__go_make_chan__':
			return 'make(chan %s)' %self.visit(node.args[0])
		elif name == '__go__array__':
			if isinstance(node.args[0], ast.BinOp):# and node.args[0].op == '<<':  ## todo assert right is `typedef`
				a = self.visit(node.args[0].left)
				if a in go_types:
					return '*[]%s' %a
				else:
					return '*[]*%s' %a  ## todo - self._catch_assignment_array_of_obs = true

			else:
				a = self.visit(node.args[0])
				if a in go_types:
					return '[]%s{}' %a
				else:
					return '[]*%s{}' %a
		elif name == '__go__addr__':
			return '&%s' %self.visit(node.args[0])
		else:
			raise SyntaxError(name)


	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)

		if op == '>>' and left == '__new__':
			return ' new %s' %right

		elif op == '<<':
			rust_hacks = ('__rust__array__', '__rust__arrayfixed__', '__rust__map__', '__rust__func__')
			go_hacks = ('__go__array__', '__go__arrayfixed__', '__go__map__', '__go__func__')

			if left in ('__go__receive__', '__go__send__'):
				return '<- %s' %right

			elif isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id in rust_hacks:
				if node.left.func.id == '__rust__func__':
					raise SyntaxError('TODO - rust.func')
				elif node.left.func.id == '__rust__map__':
					key_type = self.visit(node.left.args[0])
					value_type = self.visit(node.left.args[1])
					if value_type == 'interface': value_type = 'interface{}'
					return '&map[%s]%s%s' %(key_type, value_type, right)
				else:
					right = []
					for elt in node.right.elts:
						if isinstance(elt, ast.Num):
							right.append( str(elt.n)+'i' )
						else:
							right.append( self.visit(elt) )
					right = '(%s)' %','.join(right)

					if node.left.func.id == '__rust__array__':
						T = self.visit(node.left.args[0])
						if T in go_types:
							#return '&vec!%s%s' %(T, right)
							return '&mut vec!%s' %right
						else:
							self._catch_assignment = {'class':T}  ## visit_Assign catches this
							return '&[]*%s%s' %(T, right)

					elif node.left.func.id == '__rust__arrayfixed__':
						asize = self.visit(node.left.args[0])
						atype = self.visit(node.left.args[1])
						if atype not in go_types:
							if right != '{}': raise SyntaxError('todo init array of objects with args')
							return '&make([]*%s, %s)' %(atype, asize)
						else:
							#return '&[%s]%s%s' %(asize, atype, right)
							return '&vec!%s' %right

			elif isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id in go_hacks:
				if node.left.func.id == '__go__func__':
					raise SyntaxError('TODO - go.func')
				elif node.left.func.id == '__go__map__':
					key_type = self.visit(node.left.args[0])
					value_type = self.visit(node.left.args[1])
					if value_type == 'interface': value_type = 'interface{}'
					return '&map[%s]%s%s' %(key_type, value_type, right)
				else:
					right = []
					for elt in node.right.elts:
						if isinstance(elt, ast.Num):
							right.append( str(elt.n)+'i' )
						else:
							right.append( self.visit(elt) )
					right = '(%s)' %','.join(right)

					if node.left.func.id == '__go__array__':
						T = self.visit(node.left.args[0])
						if T in go_types:
							#return '&vec!%s%s' %(T, right)
							return '&mut vec!%s' %right
						else:
							self._catch_assignment = {'class':T}  ## visit_Assign catches this
							return '&[]*%s%s' %(T, right)

					elif node.left.func.id == '__go__arrayfixed__':
						asize = self.visit(node.left.args[0])
						atype = self.visit(node.left.args[1])
						if atype not in go_types:
							if right != '{}': raise SyntaxError('todo init array of objects with args')
							return '&make([]*%s, %s)' %(atype, asize)
						else:
							#return '&[%s]%s%s' %(asize, atype, right)
							return '&vec!%s' %right


			elif isinstance(node.left, ast.Name) and node.left.id=='__go__array__':
				return '*[]%s' %self.visit(node.right)

			elif isinstance(node.right, ast.Name) and node.right.id=='__as__':
				return '%s as ' %self.visit(node.left)

			elif isinstance(node.left, ast.BinOp) and isinstance(node.left.right, ast.Name) and node.left.right.id=='__as__':
				return '%s %s' %(self.visit(node.left), right)



		if left in self._typed_vars and self._typed_vars[left] == 'numpy.float32':
			left += '[_id_]'
		if right in self._typed_vars and self._typed_vars[right] == 'numpy.float32':
			right += '[_id_]'

		return '(%s %s %s)' % (left, op, right)

	def visit_Return(self, node):
		if isinstance(node.value, ast.Tuple):
			return 'return %s;' % ', '.join(map(self.visit, node.value.elts))
		if node.value:
			try:
				v = self.visit(node.value)
			except GenerateTypeAssert as err:
				G = err[0]
				type = G['type']
				if type == 'self':
					type = self._class_stack[-1].name


				if not hasattr(node.value, 'uid'):
					node.value.uid = self.uid()

				id = '__magic__%s' % node.value.uid
				if id not in self.unodes: self.unodes[ id ] = node.value

				if hasattr(node.value, 'is_struct_pointer'):

					out = [
						'%s := %s( *%s )' %(id, type, G['value']),
						'return &%s' %id,
					]
				else:
					out = [
						'%s := %s.( *%s )' %(id, G['value'], type),
						'return %s' %id,
					]

				return '\n'.join(out)



			if v.startswith('&'):
				return '_hack := %s; return &_hack' %v[1:]
			else:
				return 'return %s;' % v
		return 'return;'


	def visit_Lambda(self, node):
		args = [self.visit(a) for a in node.args.args]
		if args and args[0]=='__INLINE_FUNCTION__':
			raise SyntaxError('TODO inline lambda/function hack')
		elif self._cpp:
			assert len(node.args.args)==len(node.args.defaults)
			args = []
			for i,a in  enumerate(node.args.args):  ## typed args lambda hack
				s = '%s  %s' %(node.args.defaults[i].s, self.visit(a))
				args.append( s )
			## TODO support multiline lambda, and return the last line
			return '[&](%s){ return %s; }' %(','.join(args), self.visit(node.body))
		else:
			return '|%s| %s ' %(','.join(args), self.visit(node.body))


	def _visit_function(self, node):
		is_closure = False
		if self._function_stack[0] is node:
			self._vars = set()
			self._known_vars = set()
			self._known_strings = set()
		elif len(self._function_stack) > 1:
			## do not clear self._vars and _known_vars inside of closure
			is_closure = True

		args_typedefs = {}
		chan_args_typedefs = {}
		return_type = None
		generic_base_class = None
		generics = set()
		args_generics = dict()
		returns_self = False
		func_pointers = set()

		for decor in node.decorator_list:
			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef__':
				if len(decor.args) == 3:
					vname = self.visit(decor.args[0])
					vtype = self.visit(decor.args[1])
					vptr = decor.args[2].s
					args_typedefs[ vname ] = '%s %s' %(vptr, vtype)  ## space is required because it could have the `mut` keyword

				else:
					for key in decor.keywords:
						if isinstance( key.value, ast.Str):
							args_typedefs[ key.arg ] = key.value.s
						else:
							args_typedefs[ key.arg ] = self.visit(key.value)

						if args_typedefs[key.arg].startswith('func(') or args_typedefs[key.arg].startswith('lambda('):
							is_lambda_style = args_typedefs[key.arg].startswith('lambda(')
							func_pointers.add( key.arg )
							funcdef = args_typedefs[key.arg]
							## TODO - better parser
							hack = funcdef.replace(')', '(').split('(')
							lambda_args = hack[1].strip()
							lambda_return  = hack[3].strip()
							if self._cpp:
								if is_lambda_style:
									if lambda_return:  ## c++11
										args_typedefs[ key.arg ] = 'std::function<%s(%s)>  %s' %(lambda_return, lambda_args, key.arg)
									else:
										args_typedefs[ key.arg ] = 'std::function<void(%s)>  %s' %(lambda_args, key.arg)

								else:  ## old C style function pointers
									if lambda_return:
										args_typedefs[ key.arg ] = '%s(*%s)(%s)' %(lambda_args, key.arg, lambda_return)
									else:
										args_typedefs[ key.arg ] = 'void(*%s)(%s)' %(key.arg, lambda_args)

							else:
								if lambda_return:
									args_typedefs[ key.arg ] = '|%s|->%s' %(lambda_args, lambda_return)
								else:
									args_typedefs[ key.arg ] = '|%s|' %lambda_args

						## check for super classes - generics ##
						if args_typedefs[ key.arg ] in self._classes:
							raise SyntaxError('DEPRECATED')
							if node.name=='__init__':
								## generics type switch is not possible in __init__ because
								## it is used to generate the type struct, where types are static.
								## as a workaround generics passed to init always become `interface{}`
								args_typedefs[ key.arg ] = 'interface{}'
								#self._class_stack[-1]._struct_def[ key.arg ] = 'interface{}'
							else:
								classname = args_typedefs[ key.arg ]
								generic_base_class = classname
								generics.add( classname ) # switch v.(type) for each
								generics = generics.union( self._classes[classname]._subclasses )
								args_typedefs[ key.arg ] = 'interface{}'
								args_generics[ key.arg ] = classname

			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef_chan__':
				for key in decor.keywords:
					chan_args_typedefs[ key.arg ] = self.visit(key.value)
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'returns':
				if decor.keywords:
					raise SyntaxError('invalid go return type')
				elif isinstance(decor.args[0], ast.Name):
					return_type = decor.args[0].id
				else:
					return_type = decor.args[0].s

				if return_type == 'self':
					return_type = '*' + self._class_stack[-1].name
					returns_self = True
					self.method_returns_multiple_subclasses[ self._class_stack[-1].name ].add(node.name)

		is_main = node.name == 'main'
		if is_main and self._cpp:  ## g++ requires main returns an integer
			return_type = 'int'


		node._arg_names = args_names = []
		args = []
		oargs = []
		offset = len(node.args.args) - len(node.args.defaults)
		varargs = False
		varargs_name = None
		is_method = False
		for i, arg in enumerate(node.args.args):
			arg_name = arg.id

			if arg_name not in args_typedefs.keys()+chan_args_typedefs.keys():
				if arg_name=='self':
					assert i==0
					is_method = True
					continue
				else:
					err = 'error in function: %s' %node.name
					err += '\n  missing typedef: %s' %arg.id
					raise SyntaxError(err)

			if arg_name in args_typedefs:
				arg_type = args_typedefs[arg_name]
				#if generics and (i==0 or (is_method and i==1)):
				if generics and arg_name in args_generics.keys():  ## TODO - multiple generics in args
					a = '__gen__ %s' %arg_type
				else:


					if self._cpp:
						if arg_type == 'string': arg_type = 'std::string'  ## standard string type in c++
						if arg_name in func_pointers:
							## note C has funky function pointer syntax, where the arg name is in the middle
							## of the type, the arg name gets put there when parsing above.
							a = arg_type
						else:
							a = '%s %s' %(arg_type, arg_name)
					else:
						if arg_type == 'string': arg_type = 'String'  ## standard string type in rust
						a = '%s:%s' %(arg_name, arg_type)
			else:
				arg_type = chan_args_typedefs[arg_name]
				a = '%s chan %s' %(arg_name, arg_type)

			dindex = i - offset


			if dindex >= 0 and node.args.defaults:
				default_value = self.visit( node.args.defaults[dindex] )
				self._kwargs_type_[ arg_name ] = arg_type
				oargs.append( (arg_name, default_value) )
			else:
				args.append( a )
				node._arg_names.append( arg_name )

		##############################################
		if oargs:
			node._arg_names.append( '__kwargs' )
			if self._cpp:
				args.append( '_kwargs_type_  __kwargs')
			else:
				args.append( '__kwargs : _kwargs_type_')

		starargs = None
		if node.args.vararg:
			starargs = node.args.vararg
			assert starargs in args_typedefs
			args.append( '__vargs__ : Vec<%s>' %args_typedefs[starargs])
			node._arg_names.append( starargs )

		node._args_signature = ','.join(args)

		####
		if is_method:
			assert self._class_stack
			method = '(self *%s)  ' %self._class_stack[-1].name
		else:
			method = ''
		out = []
		if is_closure:
			if return_type:
				out.append( self.indent() + '%s := func (%s) -> %s {\n' % (node.name, ', '.join(args), return_type) )
			else:
				out.append( self.indent() + '%s := func (%s) {\n' % (node.name, ', '.join(args)) )
		else:
			if return_type:
				if self._cpp: ## c++ ##
					if is_method:
						classname = self._class_stack[-1].name
						sig = '%s %s::%s(%s)' % (return_type, classname, node.name, ', '.join(args))
						out.append( self.indent() + '%s {\n' % sig )
						sig = '%s %s(%s)' % (return_type, node.name, ', '.join(args))
						self._cpp_class_header.append(sig + ';')

					else:
						sig = '%s %s(%s)' % (return_type, node.name, ', '.join(args))
						out.append( self.indent() + '%s {\n' % sig )
						if not is_main: self._cheader.append( sig + ';' )

				else:  ## rust ##
					if is_method:
						self._rust_trait.append('fn %s(&mut self, %s) -> %s;' %(node.name, ', '.join(args), return_type) )
						out.append( self.indent() + 'fn %s(&mut self, %s) -> %s {\n' % (node.name, ', '.join(args), return_type) )
					else:
						out.append( self.indent() + 'fn %s(%s) -> %s {\n' % (node.name, ', '.join(args), return_type) )
			else:

				if self._cpp: ## c++ ##
					if is_method:
						classname = self._class_stack[-1].name
						sig = 'void %s::%s(%s)' %(classname, node.name, ', '.join(args))
						out.append( self.indent() + '%s {\n' % sig  )

						sig = 'void %s(%s)' % (node.name, ', '.join(args))
						self._cpp_class_header.append(sig + ';')

					else:
						sig = 'void %s(%s)' %(node.name, ', '.join(args))
						out.append( self.indent() + '%s {\n' % sig  )
						if not is_main: self._cheader.append( sig + ';' )

				else:         ## rust ##
					if is_method:
						self._rust_trait.append('fn %s(&mut self, %s);' %(node.name, ', '.join(args)) )
						out.append( self.indent() + 'fn %s(&mut self, %s) {\n' % (node.name, ', '.join(args)) )
					else:
						out.append( self.indent() + 'fn %s(%s) {\n' % (node.name, ', '.join(args)) )
		self.push()

		if oargs:
			for n,v in oargs:
				if self._cpp:
					out.append(self.indent() + '%s  %s = %s;' %(args_typedefs[n],n,v))
				else:
					out.append(self.indent() + 'let mut %s = %s;' %(n,v))
				out.append(self.indent() + 'if (__kwargs.__use__%s == true) {' %n )
				out.append(self.indent() +  '  %s = __kwargs.%s;' %(n,n))
				out.append(self.indent() + '}')

		if starargs:
			out.append(self.indent() + 'let %s = &__vargs__;' %starargs)

		if self._cpp and is_method:
			out.append(self.indent() + '%s self = *this;' %self._class_stack[-1].name )

		if generics:
			gname = args_names[ args_names.index(args_generics.keys()[0]) ]

			#panic: runtime error: invalid memory address or nil pointer dereference
			#[signal 0xb code=0x1 addr=0x0 pc=0x402440]
			##out.append(self.indent() + '__type__ := __gen__.(object).getclassname()')


			out.append(self.indent() + '__type__ := "INVALID"')
			out.append(self.indent() + '__super__, __ok__ := __gen__.(object)')

			#out.append(self.indent() + '__type__ = __super__.getclassname();')        ## TODO FIX ME
			#out.append(self.indent() + 'fmt.Println(__type__); ')
			#out.append(self.indent() + 'if __type__=="" { fmt.Println(__gen__.(object).__class__); }')

			out.append(self.indent() + 'if __ok__ { __type__ = __super__.getclassname();')
			out.append(self.indent() + '} else { fmt.Println("Gython RuntimeError - struct must implement the `object` interface"); }')

			out.append(self.indent() + 'switch __type__ {')
			#out.append(self.indent() + 'switch __gen__.(type) {')  ## this is not always correct
			#out.append('fmt.Println("class name: ", __type__)')

			self.push()
			gsorted = list(generics)
			gsorted.sort()
			gsorted.reverse()
			#for gt in generics:
			## this fails with a struct returned from a super method that returns self,
			## the generic function will fail with a nil struct, while it still works when passed the instance directly.
			for gt in gsorted:
				assert gt in self._classes
				#if node.name in self._classes[gt]._subclasses:
				#if len(self._classes[gt]._parents) == 0:

				## if in super class ##
				if self._class_stack and len(self._classes[self._class_stack[-1].name]._parents) == 0:
					if return_type=='*'+gt or not is_method: pass
					else: continue
				elif len(self._classes[gt]._parents) == 0: ## or if the generic is the super class skip it.
					if return_type=='*'+gt or not is_method: pass
					else: continue

				######out.append(self.indent() + 'case *%s:' %gt)
				out.append(self.indent() + 'case "%s":' %gt)
				self.push()

				#out.append(self.indent() + '%s,_ := __gen__.(*%s)' %(gname,gt) )  ## can not depend on the struct type, because subclasses are unions.
				out.append(self.indent() + '%s,__ok__ := __gen__.(*%s)' %(gname,gt) )  ## can not depend on the struct type, because subclasses are unions.

				out.append(self.indent() + 'if __ok__ {')

				for b in node.body:
					v = self.visit(b)
					if v:
						if returns_self:
							v = self._hack_return(v, return_type, gname, gt, node)
						out.append( self.indent() + v )

				out.append(self.indent() + '} else {' )
				if generic_base_class == gt or returns_self:
					out.append(' fmt.Println("Generics RuntimeError - generic argument is not a pointer to a struct", %s);' %gname)
					out.append(' fmt.Println("struct: ",__gen__);' )
				else:
					# __gen__.(C).foo();
					# this fails because the go compiler thinks that __gen__ is *B, when infact its *C
					# panic: interface conversion: interface is *main.B, not *main.C,
					# workaround: switch on type go thinks it is, and then recast to the real type.
					# s := C( *__gen__.(*B) )
					self.push()
					out.append( self.indent() + 'switch __gen__.(type) {' )
					self.push()
					for gt2 in gsorted:
						if gt2 != gt:
							out.append(self.indent() + 'case *%s:' %gt2)
							self.push()
							if gt2 == generic_base_class:
								## TODO panic here
								out.append(' fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", %s);' %gname)
							else:
								out.append(self.indent() + '%s := %s( *__gen__.(*%s) )' %(gname, gt, gt2) )
								for b2 in node.body:
									v = self.visit(b2)
									if v:
										#if returns_self:
										#	v = self._hack_return(v, return_type, gname, gt, node)
										out.append( self.indent() + v )

							self.pull()

					self.pull()
					out.append(self.indent() + '}')
					self.pull()
				out.append(self.indent() + '}')
				self.pull()
			self.pull()
			out.append(self.indent() + '}')

			## this only helps with debugging when the generic function is expected to return something
			if return_type:
				out.append(self.indent() + 'fmt.Println("Generics RuntimeError - failed to convert type to:", __type__, __gen__)')

			if return_type == 'int':
				out.append(self.indent() + 'return 0')
			elif return_type == 'float':
				out.append(self.indent() + 'return 0.0')
			elif return_type == 'string':
				out.append(self.indent() + 'return ""')
			elif return_type == 'bool':
				out.append(self.indent() + 'return false')
			elif return_type:
				#raise NotImplementedError('TODO other generic function return types', return_type)
				out.append(self.indent() + 'return %s' %(return_type.replace('*','&')+'{}'))

		else:
			body = node.body[:]
			body.reverse()
			#self._scope_stack.append( (self._vars, self._known_vars))
			self.generate_generic_branches( body, out, self._vars, self._known_vars )
			#for b in node.body:
		self._scope_stack = []

		if is_main and self._cpp:
			out.append( self.indent() + 'return 0;' )


		self.pull()
		out.append( self.indent()+'}' )
		return '\n'.join(out)

	def _hack_return(self, v, return_type, gname, gt, node):
		## TODO - fix - this breaks easily
		if v.strip().startswith('return ') and '*'+gt != return_type:
			if gname in v and v.strip() != 'return self':
				if '(' not in v:
					v += '.(%s)' %return_type
					v = v.replace(gname, '__gen__')
					self.method_returns_multiple_subclasses[ self._class_stack[-1].name ].add(node.name)
		return v

	def generate_generic_branches(self, body, out, force_vars, force_used_vars):
		#out.append('/* GenerateGeneric */')
		#out.append('/*vars: %s*/' %self._vars)
		#out.append('/*used: %s*/' %self._known_vars)

		#force_vars, force_used_vars = self._scope_stack[-1]
		self._vars = set(force_vars)
		self._known_vars = set(force_used_vars)

		#out.append('/*force vars: %s*/' %force_vars)
		#out.append('/*force used: %s*/' %force_used_vars)

		prev_vars = None
		prev_used = None
		vars = None
		used = None

		vars = set(self._vars)
		used = set(self._known_vars)

		#out.append('/*Sstack len: %s*/' %len(self._scope_stack))
		#if self._scope_stack:
		#	out.append('/*stack: %s - %s*/' %self._scope_stack[-1])
		#	out.append('/*STAK: %s */' %self._scope_stack)


		while len(body):
			prev_vars = vars
			prev_used = used

			b = body.pop()
			try:
				v = self.visit(b)
				if v: out.append( self.indent() + v )
			except GenerateGenericSwitch as err:
				self._scope_stack.append( (set(self._vars), set(self._known_vars)))

				#out.append('/* 		GenerateGenericSwitch */')
				#out.append('/*	vars: %s*/' %self._vars)
				#out.append('/*	used: %s*/' %self._known_vars)
				#out.append('/*	prev vars: %s*/' %prev_vars)
				#out.append('/*	prev used: %s*/' %prev_used)
				#out.append('/*	stack: %s - %s*/' %self._scope_stack[-1])
				#out.append('/*	stack len: %s*/' %len(self._scope_stack))
				#out.append('/*	stack: %s*/' %self._scope_stack)

				G = err[0]
				if 'target' not in G:
					if isinstance(b, ast.Assign):
						G['target'] = self.visit(b.targets[0])
					else:
						raise SyntaxError('no target to generate generic switch')


				out.append(self.indent()+'__subclass__ := %s' %G['value'])
				out.append(self.indent()+'switch __subclass__.__class__ {')
				self.push()

				subclasses = self.get_subclasses( G['class'] )
				for sub in subclasses:
					out.append(self.indent()+'case "%s":' %sub)
					self.push()
					#out.append(self.indent()+'%s := __subclass__.(*%s)' %(G['target'], sub)) ## error not an interface
					#out.append(self.indent()+'%s := %s(*__subclass__)' %(G['target'], sub))
					out.append(self.indent()+'__addr := %s(*__subclass__)' %sub)
					out.append(self.indent()+'%s := &__addr' %G['target'])

					pv, pu = self._scope_stack[-1]
					self.generate_generic_branches( body[:], out, pv, pu )

					self.pull()
				self._scope_stack.pop()

				self.pull()
				out.append(self.indent()+'}')
				return


	def _visit_call_helper_var(self, node):
		args = [ self.visit(a) for a in node.args ]
		#if args:
		#	out.append( 'var ' + ','.join(args) )
		if node.keywords:
			for key in node.keywords:
				args.append( key.arg )

		for name in args:
			if name not in self._vars:
				self._vars.add( name )

		#out = []
		#for v in args:
		#	out.append( self.indent() + 'var ' + v + ' int')

		#return '\n'.join(out)
		return ''

	def visit_With(self, node):
		r = []
		is_switch = False
		if isinstance( node.context_expr, ast.Name ) and node.context_expr.id == 'gojs':
			#transform_gopherjs( node )
			self._with_gojs = True
			for b in node.body:
				a = self.visit(b)
				if a: r.append(a)
			self._with_gojs = False
			return '\n'.join(r)

		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == '__default__':
			r.append('default:')
		elif isinstance( node.context_expr, ast.Name ) and node.context_expr.id == '__select__':
			r.append('select {')
			is_switch = True
		elif isinstance( node.context_expr, ast.Call ):
			if not isinstance(node.context_expr.func, ast.Name):
				raise SyntaxError( self.visit(node.context_expr))

			if len(node.context_expr.args):
				a = self.visit(node.context_expr.args[0])
			else:
				assert len(node.context_expr.keywords)
				## need to catch if this is a new variable ##
				name = node.context_expr.keywords[0].arg
				if name not in self._known_vars:
					a = 'let %s = %s' %(name, self.visit(node.context_expr.keywords[0].value))
				else:
					a = '%s = %s' %(name, self.visit(node.context_expr.keywords[0].value))

			if node.context_expr.func.id == '__case__':
				r.append('case %s:' %a)
			elif node.context_expr.func.id == '__switch__':
				r.append('switch (%s) {' %self.visit(node.context_expr.args[0]))
				is_switch = True

			elif node.context_expr.func.id == 'extern':
				r.append('extern "C" {')  ## TODO other abi's
				is_switch = True

			else:
				raise SyntaxError( 'invalid use of with')
		else:
			raise SyntaxError( 'invalid use of with')


		for b in node.body:
			a = self.visit(b)
			if a: r.append(a)

		if is_switch:
			r.append('}')

		return '\n'.join(r)

	def visit_AugAssign(self, node):
		## n++ and n-- are slightly faster than n+=1 and n-=1
		target = self.visit(node.target)
		op = self.visit(node.op)
		value = self.visit(node.value)

		if isinstance(node.target, ast.Name) and op=='+' and node.target.id in self._known_strings:
			return '%s.push_str(%s.as_slice())' %(target, value)

		if op=='+' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s ++;' %target
		if op=='-' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s --;' %target
		else:
			a = '%s %s= %s;' %(target, op, value)
		return a


	def visit_Attribute(self, node):
		name = self.visit(node.value)
		attr = node.attr
		if name in self._known_instances and self._cpp:
			## TODO - attribute lookup stack to make this safe for `a.x.y`
			## from the known instance need to check its class type, for any
			## subobjects and deference pointers as required. `a->x->y`
			## TODO - the user still needs a syntax to use `->` for working with
			## external C++ libraries where the variable may or may not be a pointer.
			return '%s->%s' % (name, attr)
		else:
			return '%s.%s' % (name, attr)

	def visit_Assign(self, node):
		if isinstance(node.targets[0], ast.Tuple): raise NotImplementedError('TODO')
		self._catch_assignment = False

		target = self.visit( node.targets[0] )

		if isinstance(node.value, ast.BinOp) and self.visit(node.value.op)=='<<' and isinstance(node.value.left, ast.Name) and node.value.left.id=='__go__send__':
			value = self.visit(node.value.right)
			return '%s <- %s;' % (target, value)

		elif not self._function_stack:
			value = self.visit(node.value)
			#return 'var %s = %s;' % (target, value)
			if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id in self._classes:
				value = '__new__' + value
				return 'let %s *%s = %s;' % (target, node.value.func.id, value)
			else:
				self._globals['string'].add( target )
				if self._cpp:
					return 'const std::string %s = %s;' % (target, value)
				else:
					return 'static %s : string = %s;' % (target, value)  ## TODO other types (`let` will not work at global scope)

		elif isinstance(node.targets[0], ast.Name) and node.targets[0].id in self._vars:
			value = self.visit(node.value)
			self._vars.remove( target )
			self._known_vars.add( target )

			if isinstance(node.value, ast.Str):  ## catch strings for `+=` hack
				self._known_strings.add( target )

			elif isinstance(node.value, ast.Num):
				if type(node.value.n) is int:
					value += 'i'

			#################################################################
			if value.startswith('&[]*') and self._catch_assignment:
				self._known_arrays[ target ] = self._catch_assignment['class']

			if self._cpp and isinstance(node.value, ast.BinOp) and self.visit(node.value.op)=='<<':
				if isinstance(node.value.left, ast.Call) and isinstance(node.value.left.func, ast.Name) and node.value.left.func.id in COLLECTION_TYPES:
					S = node.value.left.func.id
					if S == '__go__map__':
						key_type = self.visit(node.value.left.args[0])
						value_type = self.visit(node.value.left.args[1])
						if key_type=='string': key_type = 'std::string'
						if value_type=='string': value_type = 'std::string'

						a = []
						for i in range( len(node.value.right.keys) ):
							k = self.visit( node.value.right.keys[ i ] )
							v = self.visit( node.value.right.values[i] )
							a.append( '{%s,%s}'%(k,v) )
						v = ', '.join( a )

						## raw pointer
						##return 'std::map<%s, %s> _ref_%s = {%s}; auto %s = &_ref_%s;' %(key_type, value_type, target, v, target, target) 
						## c++11 shared pointer
						#return 'auto %s = std::make_shared<std::map<%s, %s>>({%s});' %(target, key_type, value_type, v)  ## too many args to make_shared?
						maptype = 'std::map<%s, %s>' %(key_type, value_type)
						r = '%s _ref_%s = {%s};' %(maptype, target, v)
						r += 'std::shared_ptr<%s> %s(&_ref_%s);' %(maptype, target, target)
						return r

					elif 'array' in S:
						args = []
						for elt in node.value.right.elts:
							#if isinstance(elt, ast.Num):
							args.append( self.visit(elt) )

						if S=='__go__array__':
							T = self.visit(node.value.left.args[0])
							## note: c++11 says that `=` is optional
							return 'std::vector<%s>  %s = {%s};' %(T, target, ','.join(args))
						elif S=='__go__arrayfixed__':
							asize = self.visit(node.value.left.args[0])
							atype = self.visit(node.value.left.args[1])
							## note: the inner braces are due to the nature of initializer lists, one per template param.
							return 'std::array<%s, %s>  %s = {{%s}};' %(atype, asize, target, ','.join(args))


			if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and isinstance(node.value.func.value, ast.Name):
				varname = node.value.func.value.id
				info = varname + '  '
				if varname in self._known_vars:
					## generics generator ##
					#raise SyntaxError(varname + ' is known class::' + self._known_instances[varname] + '%s(%s)' % (fname, args))
					cname = self._known_instances[varname]
					info += 'class: ' + cname
					if node.value.func.attr in self.method_returns_multiple_subclasses[ cname ]:
						self._known_instances[target] = cname
						raise GenerateGenericSwitch( {'target':target, 'value':value, 'class':cname, 'method':node.value.func.attr} )

				if self._cpp:
					return 'auto %s = %s;			/* %s */' % (target, value, info)
				else:
					return 'let %s = %s;			/* %s */' % (target, value, info)


			elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
				if node.value.func.id in self._classes:
					classname = node.value.func.id
					self._known_instances[ target ] = classname
					if self._cpp:
						return 'auto %s = new %s;' %(target, value)

					else:
						## TODO missing fields, (rust requires all members are initialized)
						args = []
						for i,arg in enumerate(node.value.args):
							args.append( '%s:%s' %(self._classes[classname]._struct_init_names[i], self.visit(arg)))
						if node.value.keywords:
							for kw in node.value.keywords:
								args.append( '%s:%s' %(kw.arg, self.visit(kw.value)))

						## do not cast to trait type, because as a trait can be used to access the data inside the struct
						#return 'let %s = &%sStruct{ %s } as &%s;' %(target, classname, ','.join(args), classname)

						## note: methods are defined with `&mut self`, this requires that
						## a mutable reference is taken so that methods can be called on the instance.
						return 'let %s = &mut %s{ %s };' %(target, classname, ','.join(args))

				else:
					if self._cpp:
						if isinstance(node.value, ast.Expr) and isinstance(node.value.value, ast.BinOp) and self.visit(node.value.value.op)=='<<':
							raise SyntaxError(node.value.value.left)
						else:
							return 'auto %s = %s;			/* new variable */' % (target, value)
					else:
						return 'let %s = %s;			/* new variable */' % (target, value)

			else:
				if self._cpp:
					return 'auto %s = %s;' % (target, value)
				else:
					return 'let mut %s = %s;			/* new muatble */' % (target, value)

		else:
			value = self.visit(node.value)
			#if '<-' in value:
			#	raise RuntimeError(target+value)
			if value.startswith('&make('):
				#raise SyntaxError(value)
				v = value[1:]
				return '_tmp := %s; %s = &_tmp;' %(v, target)
			else:
				#if value.startswith('&[]*') and self._catch_assignment:
				#	raise SyntaxError(value)
				return '%s = %s;' % (target, value)

	def visit_While(self, node):
		cond = self.visit(node.test)
		if cond == 'true' or cond == '1': cond = ''
		body = [ 'for %s {' %cond]
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def _inline_code_helper(self, s):
		return s
		#return 'js.Global.Call("eval", "%s")' %s ## TODO inline JS()





def main(script, insert_runtime=True):

	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'rust_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err

	g = RustGenerator()
	g.visit(tree) # first pass gathers classes
	pass2 = g.visit(tree)

	exe = os.path.expanduser('/usr/local/bin/rustc')
	if not os.path.isfile(exe):
		raise RuntimeError('rustc not found in /usr/local/bin')

	## this hack runs the code generated in the second pass into the Rust compiler to check for errors,
	## in some cases Rusthon may not always track the types inside an array, or other types, and so it
	## it starts off by generating some dumb code that works most of the time.  If it will not pass the
	## Rust compiler, stdout is parsed to check for errors and a magic ID that links to a ast Node.
	import subprocess
	pass2lines = pass2.splitlines()
	path = '/tmp/pass2.rs'
	open(path, 'wb').write( pass2 )
	p = subprocess.Popen([exe, path], cwd='/tmp', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	errors = p.stderr.read().splitlines()
	if len(errors):
		hiterr = False
		for line in errors:
			if 'error:' in line:
				hiterr = True
			elif hiterr:
				hiterr = False
				if '//magic:' in line:
					uid = int( line.split('//magic:')[-1] )
					g.unodes[ uid ].is_ref = False

				else:
					raise SyntaxError(line)
	pass3 = g.visit(tree)
	open('/tmp/pass3.rs', 'wb').write( pass3 )
	return pass3



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

	out = main( data )
	print( out )


if __name__ == '__main__':
	command()

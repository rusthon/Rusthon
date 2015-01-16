# _*_ coding: utf-8 _*_


types = ['string', 'str', 'list', 'dict', 'bool']

glsl_types = ['struct*', 'int*', 'float*', 'vec2', 'vec3', 'vec4', 'mat2', 'mat3', 'mat4']
glsl_xtypes = ['mat2x2', 'mat3x3', 'mat4x4']  ## others not supported in WebGLSL
glsl_types.extend( glsl_xtypes )
glsl_aliases = ['floatPOINTER', 'intPOINTER', 'structPOINTER']

#types.extend( glsl_types )
#types.extend( glsl_aliases )

native_number_types = ['int', 'float', 'double']  ## float and double are the same
simd_types = ['float32x4', 'int32x4']  ## dart
vector_types = ['float32vec']
vector_types.extend( simd_types )
number_types = ['long']  ## requires https://github.com/dcodeIO/Long.js
number_types.extend( native_number_types )

types.extend( number_types)
types.extend( vector_types )


__whitespace = [' ', '\t']

GO_SPECIAL_CALLS = {
	'go'         : '__go__',
	'spawn'      : '__go__',
	'channel'    : '__go_make_chan__',
	'go.channel' : '__go_make_chan__',
	'go.array'   : '__go__array__',
	'go.make'    : '__go_make__',
	'go.addr'    : '__go__addr__',
	'go.func'    : '__go__func__',
}

OPERATORS = {
	'left' : {
		u'⟦' : '__getitem__',
		u'⟪' : '__getpeer__',
		u'⟅' : '__getserver__',
		u'⎨' : '__getclient__'
	},
	'right' : [u'⟧', u'⟫', u'⟆', u'⎬'],
}

def get_indent(s):
	indent = []
	for char in s:
		if char in __whitespace:
			indent.append( char )
		else:
			break
	return ''.join(indent)

def transform_source( source, strip=False ):
	output = []
	output_post = None
	asm_block = False
	asm_block_indent = 0

	for line in source.splitlines():
		if line.strip().startswith('#'):
			continue

		if asm_block:
			dent = get_indent(line)
			if asm_block==True:
				asm_block = 'OK'
				asm_block_indent = len(dent)

			if len(dent) < asm_block_indent:
				asm_block = False
				asm_block_indent = 0
			elif len(dent) > asm_block_indent:
				raise SyntaxError('invalid asm indentation level')
			else:
				assert len(dent)==asm_block_indent
				if line.strip():
					output.append( '%s"%s"' %(dent,line.strip()) )
				else:
					asm_block = False
					asm_block_indent = 0
				continue

		a = []
		hit_go_typedef = False
		hit_go_funcdef = False
		gotype = None
		isindef = False
		inline_wrap = False
		inline_ptr = False
		prevchar = None

		for i,char in enumerate(line):
			if isindef is False and len(a) and ''.join(a).strip().startswith('def '):
				isindef = True

			nextchar = None
			j = i+1
			while j < len(line):
				nextchar = line[j]
				if nextchar.strip(): break
				j += 1

			if prevchar=='=' and char in '&*~':
				inline_ptr = True
				a.append('__inline__["' + char)
			elif inline_ptr and char not in '&*~':
				inline_ptr = False
				a.append('"] << ')
				a.append( char )

			elif char == '(' and nextchar in ('&','@'):
				inline_wrap = True
				a.append('(inline("')
			elif char in '),' and inline_wrap:
				inline_wrap = False
				for u,_ in enumerate(a):
					if _=='@':
						a[u] = 'ref '
				if char == ')':
					a.append('"))')
				else:
					a.append('"),')

			elif not isindef and len(a) and char in OPERATORS['left'] and j==i+1:
				a.append( '<<__op_left__(u"%s")<<' %char)
			elif not isindef and len(a) and char in OPERATORS['right']:
				a.append('<<__op_right__(u"%s")' % char )
			## go array and map syntax ##
			elif not isindef and len(a) and char==']' and j==i+1 and nextchar!=None and nextchar in '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
				assert '[' in a
				hit_go_typedef = True

				gotype = []
				restore = list(a)
				b = a.pop()
				while b != '[':
					gotype.append(b)
					b = a.pop()
				gotype.reverse()
				gotype = ''.join(gotype).strip()  ## fixes spaces inside brackets `[ 1 ]string()`
				if not gotype:
					if nextchar=='[':
						a.append('__go__array__<<')
					else:
						a.append('__go__array__(')
				elif gotype.isdigit():
					p = ''.join(a).split()[-1].strip()
					if p.startswith('[') or p.startswith('='):
						a.append('__go__arrayfixed__(%s,' %gotype)
					else:
						hit_go_typedef = False
						restore.append(char)
						a = restore

				elif ''.join(a[-3:])=='map' and gotype != 'func' and a[-4] in __whitespace+['=']:
					a.pop(); a.pop(); a.pop()
					a.append('__go__map__(%s,' %gotype)
				else:
					hit_go_typedef = False
					restore.append(char)
					a = restore

			elif hit_go_funcdef and char==')' and ')' in ''.join(a).split('func(')[-1] and not ''.join(a).strip().startswith('def '):
				hit_go_funcdef = False
				a.append('))<<')

			elif hit_go_typedef and char=='(':
				if ''.join(a).endswith('func'):
					hit_go_funcdef = True
					a.append( '(' )
				else:
					a.append(')<<(')
				hit_go_typedef = False
			elif hit_go_typedef and char=='{':
				a.append(')<<{')
				hit_go_typedef = False
			elif hit_go_typedef and char==',':
				#a.append(', type=True),')  ## this breaks function annotations that splits on ','
				a.append('<<typedef),')
				hit_go_typedef = False
			elif hit_go_typedef and char in (' ', '\t'):
				aa = []
				for xx in a:
					if xx == '__go__array__(':
						aa.append('__go__array__[')
					else:
						aa.append( xx )
				a = aa
				a.append(']=\t\t\t\t')
				hit_go_typedef = False


			elif a and char in __whitespace:
				b = ''.join(a)
				b = b.strip()
				is_class_type = b.startswith('class:') and len(b.split(':'))==2
				is_pointer = b.startswith('*')
				is_func = b.startswith('func(') and not ''.join(a).strip().startswith('func(')
				if (b in types or is_class_type or is_pointer or is_func) and nextchar != '=':
					if strip:
						a = a[ : -len(b) ]
					elif is_class_type:
						cls = b.split(':')[-1]
						a = a[ : -len('class:')-len(cls)]
						a.append('__go__class__[%s]=\t\t\t\t' %cls)

					elif is_pointer:
						cls = b.split('*')[-1]
						a = a[ : -len('*')-len(cls)]
						a.append('__go__pointer__[%s]=\t\t\t\t' %cls)
					elif is_func:
						u = ''.join(a)
						u = u.replace('func(', '__go__func__["func(')
						u += '"]=\t\t\t\t'
						a = [w for w in u]
					else:
						if a[-1]=='*':
							a.pop()
							a.append('POINTER')
						a.append('=\t\t\t\t')
						#a.append( char )

				else:
					a.append( char )
			else:
				a.append( char )

			if char.strip():
				prevchar = char


		if not a:
			continue


		if a[-1]==';':
			a.pop()
		c = ''.join(a)
		cs = c.strip()

		if cs.startswith('//'):
			continue
		elif cs.startswith('inline(') or cs.startswith('JS('):
			output.append(c)
			continue


		if cs.startswith('var '):
			c = c.replace('var ', '')

		if cs.startswith('let '):
			mut = False
			if cs.startswith('let mut '):
				c = c.replace('let mut ', '__let__(')
				mut = True
			else:
				c = c.replace('let ', '__let__(')

			if ':' in c:
				assert c.count(':')==1
				c = c.replace(':', ',"')
				if '=' in c:
					c = c.replace('=', '", ')
				else:
					c += '"'

			if mut:
				c += ',mutable=True)'
			else:
				c += ')'

		## this conflicts with inline javascript and lua,
		## TODO make the parser smarter, and skip quoted strings
		#if '= function(' in c:
		#	k = '= function('
		#	a,b = c.split(k)
		#	output.append( '@expression(%s)' %a.strip())
		#	c = 'def __NAMELESS__(' + b

		if ' except ' in c and ':' in c:  ## PEP 463 - exception expressions
			s = c.split(' except ')
			if len(s) == 2 and '=' in s[0] and ':' in s[1]:
				indent = []
				for char in s[0]:
					if char in __whitespace:
						indent.append( char )
					else:
						break
				indent = ''.join(indent)
				s0 = s[0].strip()
				output.append('%stry: %s' %(indent, s0) )
				exception, default = s[1].split(':')
				output.append('%sexcept %s: %s=%s' %(indent, exception, s0.split('=')[0], default) )
				c = ''

		if '=\t\t\t\tdef ' in c:  ## todo deprecate
			x, c = c.split('=\t\t\t\tdef ')
			indent = []
			pre = []
			for char in x:
				if char in __whitespace:
					indent.append(char)
				else:
					pre.append( char )
			indent = ''.join(indent)
			pre = ''.join(pre)
			output.append( indent + '@returns(%s)' %pre)
			c = indent+'def '+c
		elif c.strip().startswith('def ') and '->' in c:  ## python3 syntax
			c, rtype = c.split('->')
			c += ':'
			rtype = rtype.strip()[:-1].strip()
			if rtype.startswith('*'):
				rtype = '"%s"' %rtype

			indent = []
			for char in c:
				if char in __whitespace:
					indent.append(char)
				else:
					break
			indent = ''.join(indent)
			output.append( indent + '@returns(%s)' %rtype)

		if c.startswith('import '):
			if '-' in c:
				c = c.replace('-', '__DASH__')
			if '/' in c:
				c = c.replace('/', '__SLASH__')
			if '"' in c:
				c = c.replace('"', '')


		if ' new ' in c:
			c = c.replace(' new ', ' __new__>>')
		if '\tnew ' in c:
			c = c.replace('\tnew ', ' __new__>>')


		## golang

		if c.strip().startswith('switch '):
			c = c.replace('switch ', 'with __switch__(').replace(':', '):')

		if c.strip().startswith('default:'):
			c = c.replace('default:', 'with __default__:')

		if c.strip().startswith('select:'):
			c = c.replace('select:', 'with __select__:')

		if c.strip().startswith('case ') and c.strip().endswith(':'):
			c = c.replace('case ', 'with __case__(').replace(':', '):')

		if '<-' in c:
			if '=' in c:
				c = c.replace('<-', '__go__receive__<<')
			else:
				## keeping `=` allows for compatible transform to stacklessPython API,
				## this is not used now because it is not required by the Go backend.
				c = c.replace('<-', '= __go__send__<<')
				#c = c.replace('<-', '<<__go__send__<<')


		## c++ `->`
		if '->' in c:
			a,b = c.split('->')
			this_name = a.split()[-1].split('=')[-1].split(':')[-1].split(',')[-1]
			method_name = b.split()[0].split('(')[0]
			c = c.replace('->'+method_name, '.__leftarrow__.'+method_name)  ## TODO should be rightarrow

		indent = 0
		for u in c:
			if u == ' ' or u == '\t':
				indent += 1
			else:
				break
		indent = '\t'*indent


		## python3 annotations
		if 'def ' in c and c.count(':') > 1:

			#head, tail = c.split('(')
			head = c[ : c.index('(') ]
			tail = c[ c.index('(')+1 : ]
			args = []
			#tail, tailend = tail.split(')')
			tailend = tail[ tail.rindex(')')+1 : ]
			tail = tail[ : tail.rindex(')') ]


			for x in tail.split(','):
				y = x
				if ':' in y:
					kw = None
					if '=' in y:
						y, kw = y.split('=')
					#arg, typedef = y.split(':')
					arg = y[ : y.index(':') ]
					typedef = y[ y.index(':')+1 : ]

					chan = False
					T = False
					if len(typedef.strip().split()) >= 2:
						parts = typedef.strip().split()
						if 'chan' in parts:  ## go syntax
							chan = True
						else:                ## rust or c++ syntax
							T = ' '.join(parts[:-1])

						#typedef = typedef.strip().split()[-1]
						typedef = parts[-1]

					if '*' in arg:
						arg_name = arg.split('*')[-1]
					else:
						arg_name = arg

					if typedef.startswith('*'):
						typedef = '"%s"' %typedef.strip()
					elif typedef.startswith('[]'):
						#typedef = '"*%s"' %typedef.strip()  ## the pointer hack should not be forced here for arrays
						typedef = '__arg_array__("%s")' %typedef.strip()  ## this parses the go syntax and converts it for each backend

					elif typedef.startswith('map['):
						#typedef = '"*%s"' %typedef.strip()  ## the pointer hack should not be forced here for maps
						typedef = '__arg_map__("%s")' %typedef.strip()  ## this parses the go syntax and converts it for each backend

					elif typedef.startswith('func('):
						typedef = '"%s"' %typedef.strip()
					elif typedef.startswith('lambda('):
						typedef = '"%s"' %typedef.strip()
					elif '<' in typedef and '>' in typedef: ## rust and c++ template/generics syntax
						typedef = '"%s"' %typedef.strip()

					if T:  ## rust or c++ syntax
						output.append('%s@__typedef__(%s, %s, "%s")' %(indent, arg_name, typedef, T))
					elif chan:
						output.append('%s@typedef_chan(%s=%s)' %(indent, arg_name, typedef))
					else:
						output.append('%s@typedef(%s=%s)' %(indent, arg_name, typedef))

					if kw:
						arg += '=' + kw
					args.append(arg)
				else:
					args.append(x)
			c = head +'(' + ','.join(args) + ')'+tailend


		## jquery ##
		## TODO ensure this is not inside quoted text
		if '$(' in c:
			c = c.replace('$(', '__DOLLAR__(')
		if '$' in c and 'def ' in c:  ## $ as function parameter
			c = c.replace('$', '__DOLLAR__')
		if '$.' in c:
			c = c.replace('$.', '__DOLLAR__.')

		if c.strip().startswith('nonlocal '):  ## Python3 syntax
			c = c.replace('nonlocal ', 'global ')  ## fake nonlocal with global

		if ' as ' in c and '(' in c and not c.startswith('except '):
			c = c.replace(' as ', '<<__as__<<')

		if ' def(' in c:
			a,b = c.split(' def(')
			if '=' in a:
				output.append( indent + '@__target__(%s)' %a.split('=')[0])
				output.append( indent + 'def __NAMELESS__(' + b )
		else:
			## regular output
			output.append( c )

		if c.strip().startswith('with asm('):
			asm_block = True

	r = '\n'.join(output)
	return r


test = u'''

## todo deprecate
int a = 1
float b = 1.1
str c = "hi"
int d
int def xxx(): pass


if True:
	d = a[ 'somekey' ] except KeyError: 'mydefault'

## <- becomes __go__send__<<a
g <- a
## = <- becomes __go__receive__<<b
g = <- b

def call_method( cb:func(int)(int) ) ->int:
	return cb(3)

def wrapper(a:int, c:chan int):
	result = longCalculation(a)
	c <- result

switch a.f():
	case 1:
		print(x)
	case 2:
		print(y)
	default:
		break

select:
	case x = <- a:
		y += x
	case x = <- b:
		y += x



def f(a:int, b:int, c:int) ->int:
	return a+b+c

def f(a:int=100, b:int=100) ->int:
	return a+b

def f(*args:int, **kwargs:int) ->int:
	return a+b

a = []int(x for x in range(3))

y = go.make([]float64, 1000)

def plot(id:string, latency:[]float64, xlabel:string, title:string ):
	pass

def f( x:*ABC ) -> *XXX:
	pass

## TODO deprecate
class A:
	def __init__(self):
		int 		self.x = 1
		[]int		self.y = []int()
		class:ABS     self.z = A()
		[]A     self.z = A()
		bool    self.b = xxx()
		*ABS     self.z = A()
		#[]*A     self.z = A()   ## this is ugly

def listpass( a:[]int ):
	pass

def mappass( a:map[string]int ):
	return ConvertDataUnits[unit_type][unit][1][0]

m = map[int]string{ a:'xxx' for a in range(10)}

a = xxx[x][y]
a = xxx⎨Z⎬
a = xxx ⎨Z⎬⎨zzzz⎬

functions = map[string]func(int)(int){}
[]int a = go( f() for f in funtions )

## in go becomes: map[string]int{x,y,z}
## becomes: __go__map__(string, int) << {'x':x, 'y':y, 'z':z}
a = map[string]int{
	"x":x, 
	"y":y, 
	"z":z
}

def f():
    return [[0]]
print f()[0][0]

## in go becomes: []string{x,y,z}
## becomes: __go__array__(string) << (x,y,z)
a = []string(x,y,z)

## in go becomes: [3]int{x,y,z}
## becomes: __go__arrayfixed__(3, string) << (x,y,z)
a = [ 3 ]int(x,y,z)

## Rust
## f(inline('&mut *x'))
f(&mut *x)
## f(inline('ref mut *x'), y.z())
f(@mut *x, y.z())
## f(x << __as__ << uint)
f(x as uint)

## __let__[x :" Vec<(uint, Y<int>)> "]= range(0,1).map().collect()
let x : Vec<(uint, Y<int>)> = range(0,1).map().collect()
let i
i = &**x

def f(a:&mut int) ->int:
	return a

def f():
	with asm( outputs=b, inputs=a, volatile=True ):
		movl %1, %%ebx;
		movl %%ebx, %0;
	return x

let mut x : int = 1
let x : int
def __init__():
	let self.x : int = x
	let mut self.y : int = y

A.callback = B->method
A.callback = B->method()
A.do_something( x,y,z, B->method )
A.do_something( x,y,z, callback=B->method )
A.do_something( x,y,z, B->method(U,W) )
A.do_something( x,y,z, callback=B->method(X,Z) )


def call_method( cb:lambda(int)(int) ) ->int:
	return cb(3)

if self.__map[r][c] in (WALL,PERM_WALL): pass

## allow func to be used as a function name, because it is pretty commom and allowed by most backends.
def func(x=None, callback=None):
	func( callback=xxx )
	x.func( xx=yy )

let mut x = 0

def templated( x : Type<T> ):
	pass
def templated( x : namespace::Type<T> ):
	pass

c.x[0] = def(xx,yy):
	return xx+yy

print xxx
'''

## function expressions, deprecated
## TODO: this would be nice to bring back with a proper parser
#X.func( cb1=def ():
#		return 1,
#	cb2=def (x:int, y:string):
#		return 2
#)
#a = {
#	'cb1': def (x,y):
#		return x+y
#}
#def xxx():
#	b = {
#		'cb1': def (x,y):
#			return x+y,
#		'cb2': def (x,y):
#			return x+y
#	}
#A.do_something( x,y,z, callback=def cb(x):
#	return x+y
#)
#A.do_something( x,y,z, callback=def (x,y,z):
#	return x+y
#)


if __name__ == '__main__':
	out = transform_source(test)
	print(out)
	import ast
	print( ast.parse(out) )
# _*_ coding: utf-8 _*_


types = ['string', 'str', 'list', 'dict', 'bool']

glsl_types = ['struct*', 'int*', 'float*', 'vec2', 'vec3', 'vec4', 'mat2', 'mat3', 'mat4']
glsl_xtypes = ['mat2x2', 'mat3x3', 'mat4x4']  ## others not supported in WebGLSL
glsl_types.extend( glsl_xtypes )
glsl_aliases = ['floatPOINTER', 'intPOINTER', 'structPOINTER']

types.extend( glsl_types )
types.extend( glsl_aliases )

native_number_types = ['int', 'float', 'double']  ## float and double are the same
simd_types = ['float32x4', 'int32x4']
vector_types = ['float32vec']
vector_types.extend( simd_types )
number_types = ['long']  ## requires https://github.com/dcodeIO/Long.js
number_types.extend( native_number_types )

types.extend( number_types)
types.extend( vector_types )


__whitespace = [' ', '\t']

GO_SPECIAL_CALLS = {
	'go'         : '__go__',
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




def transform_source( source, strip=False ):
	output = []
	output_post = None

	for line in source.splitlines():
		if line.strip().startswith('#'):
			continue

		a = []
		hit_go_typedef = False
		hit_go_funcdef = False
		gotype = None
		isindef = False

		for i,char in enumerate(line):
			if isindef is False and len(a) and ''.join(a).strip().startswith('def '):
				isindef = True

			nextchar = None
			j = i+1
			while j < len(line):
				nextchar = line[j]
				if nextchar.strip(): break
				j += 1

			if not isindef and len(a) and char in OPERATORS['left'] and j==i+1:
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

				elif ''.join(a[-3:])=='map' and gotype != 'func':
					a.pop(); a.pop(); a.pop()
					a.append('__go__map__(%s,' %gotype)
				else:
					hit_go_typedef = False
					restore.append(char)
					a = restore

			elif hit_go_funcdef and char==')' and ')' in ''.join(a).split('func(')[-1]:
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
				is_func = b.startswith('func(')
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

		if '= function(' in c:
			k = '= function('
			a,b = c.split(k)
			output.append( '@expression(%s)' %a.strip())
			c = 'def __NAMELESS__(' + b

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


		## X.method.bind(X) shortcut `->`
		if '->' in c:
			a,b = c.split('->')
			this_name = a.split()[-1].split('=')[-1].split(':')[-1].split(',')[-1]
			method_name = b.split()[0].split('(')[0]
			c = c.replace('->'+method_name, '.'+method_name+'.bind(%s)'%this_name)

		## callback=def .. inline function ##
		if '=def ' in c or '= def ' in c or ': def ' in c or ':def ' in c:
			if '=def ' in  c:
				d = '=def '
			elif '= def ' in c:
				d = '= def '
			elif ': def ' in c:
				d = ': def '
			elif ':def ' in c:
				d = ':def '

			if 'def (' in c:
				c = c.replace('def (', 'def __NAMELESS__(')
			c, tail = c.split(d)

			#if d.startswith('='):
			#	if '(' in c:
			#		c += '=lambda __INLINE_FUNCTION__: %s )' %tail.strip().split(':')[0]
			#	else:
			#		c += '=lambda __INLINE_FUNCTION__: %s' %tail.strip().split(':')[0]
			#	output_post = 'def %s'%tail

			if d.startswith('='):
				c += '=lambda __INLINE_FUNCTION__: %s' %tail.strip().split(':')[0]

				if output_post:
					if output_post[-1][-1]==',':
						output_post[-1] = output_post[-1][:-1]
						output[-1] += ','
				else: output_post = list()

				output.append( c )

				c = 'def %s'%tail

			else:
				c += ':lambda __INLINE_FUNCTION__: %s,' %tail.strip().split(':')[0]
				output.append( c )
				if output_post:
					if output_post[-1][-1]==',':
						output_post[-1] = output_post[-1][:-1]
				else: output_post = list()
				c = 'def %s'%tail


		## python3 annotations
		if 'def ' in c and c.count(':') > 1:
			indent = 0
			for u in c:
				if u == ' ' or u == '\t':
					indent += 1
				else:
					break
			indent = '\t'*indent

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
					arg, typedef = y.split(':')
					chan = False
					if len(typedef.strip().split()) == 2:
						chan = True
						typedef = typedef.strip().split()[-1]
					if '*' in arg:
						arg_name = arg.split('*')[-1]
					else:
						arg_name = arg

					if typedef.startswith('*'):
						typedef = '"%s"' %typedef.strip()
					elif typedef.startswith('[]'):
						typedef = '"*%s"' %typedef.strip()
					elif typedef.startswith('map['):
						typedef = '"*%s"' %typedef.strip()
					elif typedef.startswith('func('):
						typedef = '"%s"' %typedef.strip()

					if chan:
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

		if type(output_post) is list:
			output_post.append( c )
		else:
			output.append( c )

		if type(output_post) is str:  ## DEPRECATED
			indent = 0
			for u in output[-1]:
				if u == ' ' or u == '\t':
					indent += 1
				else:
					break
			output.append( ('\t'*indent)+output_post)
			output_post = True
		elif output_post == True:  ## DEPRECATED
			if output[-1].strip()==')':
				output.pop()
				output_post = None

		elif type(output_post) is list:
			if output_post[-1].strip().endswith( ('}',')') ):
				output.append( output_post.pop() )
				indent = 0
				for u in output[-1]:
					if u == ' ' or u == '\t':
						indent += 1
					else:
						break
				for ln in output_post:
					output.append( ('\t'*indent)+ln )

				output_post = None

	r = '\n'.join(output)
	return r


test = u'''
int a = 1
float b = 1.1
str c = "hi"
int d
int def xxx(): pass
if True:
	float* def Y():
		pass

A.callback = B->method
A.do_something( x,y,z, B->method )
A.do_something( x,y,z, callback=B->method )
A.do_something( x,y,z, callback=def cb(x):
	return x+y
)
A.do_something( x,y,z, callback=def (x,y,z):
	return x+y
)
a = {
	'cb1': def (x,y):
		return x+y
}
def xxx():
	b = {
		'cb1': def (x,y):
			return x+y,
		'cb2': def (x,y):
			return x+y
	}

X.func( cb1=def ():
		return 1,
	cb2=def ():
		return 2
)

c = function(x,y):
	return x+y
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

## in go becomes: []string{x,y,z}
## becomes: __go__array__(string) << (x,y,z)
a = []string(x,y,z)

## in go becomes: [3]int{x,y,z}
## becomes: __go__arrayfixed__(3, string) << (x,y,z)
a = [ 3 ]int(x,y,z)



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

'''

if __name__ == '__main__':
	out = transform_source(test)
	print(out)
	import ast
	print( ast.parse(out) )
types = ['str', 'list', 'dict']

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

def transform_source( source, strip=False ):
	output = []
	for line in source.splitlines():
		a = []
		for i,char in enumerate(line):
			nextchar = None
			j = i+1
			while j < len(line):
				nextchar = line[j]
				if nextchar.strip(): break
				j += 1

			if a and char in __whitespace:
				b = ''.join(a)
				b = b.strip()
				if b in types and nextchar != '=':
					if strip:
						a = a[ : -len(b) ]
					else:
						if a[-1]=='*':
							a.pop()
							a.append('POINTER')
						a.append('=')
						a.append( char )
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
		if cs.startswith('var '):
			c = c.replace('var ', '')

		if '= def ' in c:
			x, c = c.split('= def ')
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
		elif c.strip().startswith('def ') and '->' in c:
			c, rtype = c.split('->')
			c += ':'
			rtype = rtype.strip()[:-1]
			indent = []
			for char in c:
				if char in __whitespace:
					indent.append(char)
				else:
					break
			indent = ''.join(indent)
			output.append( indent + '@returns(%s)' %rtype)
		elif c.startswith('import ') and '-' in c:
			c = c.replace('-', '__DASH__')
		elif ' new ' in c:
			c += ')' * c.count(' new ')
			c = c.replace(' new ', ' new(')

		## jquery ##
		if '$(' in c:
			## TODO ensure this is not inside quoted text
			c = c.replace('$(', '__DOLLAR__(')

		output.append( c )

	return '\n'.join(output)


test = '''
int a = 1
float b = 1.1
str c = "hi"
int d
int def xxx(): pass
if True:
	float* def Y():
		pass
'''

if __name__ == '__main__':
	out = transform_source(test)
	print(out)
	import ast
	print( ast.parse(out) )
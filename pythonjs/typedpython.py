whitespace = [' ', '\t']
number_types = ['int', 'float']
types = ['str']
types.extend( number_types)


def transform_source( source, strip=False ):
	output = []
	for line in source.splitlines():
		a = []
		for char in line:
			if a and char in whitespace:
				b = ''.join(a)
				b = b.strip()
				if b in types:
					if strip:
						a = a[ : -len(b) ]
					else:
						a.append('=')
						a.append( char )
				else:
					a.append( char )
			else:
				a.append( char )
		output.append( ''.join(a) )

	return '\n'.join(output)


test = '''
int a = 1
float b = 1.1
str c = "hi"
int d
'''

if __name__ == '__main__':
	out = transform_source(test)
	print(out)
	import ast
	print( ast.parse(out) )
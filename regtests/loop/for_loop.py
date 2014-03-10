'''
for loop tests
'''

def main():

	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	TestError( y==6 )

	z = ''
	arr = ['a', 'b', 'c']
	for v in arr:
		z += v
	TestError( z == 'abc' )

	b = False
	if 'a' in arr:
		b = True
	TestError( b == True )

	s = 'hello world'
	z = ''
	for char in s:
		z += char
	TestError( z == 'hello world' )

	b = False
	if 'hello' in s:
		b = True
	TestError( b==True )

	ob = {'a' : 'A', 'b' : 'B'}
	k = ''
	v = ''
	for key in ob:
		k += key
		v += ob[key]
	TestError(k=='ab' or k=='ba')
	TestError(v=='AB' or v=='BA')

	keys = []
	values = []
	for x,y in ob.items():
		keys.append( x )
		values.append( y )

	TestError( 'a' in keys )
	TestError( 'A' in values )

	ob2 = {'c':'C', 'd':'D'}
	e = 0
	arr = []
	for x,y in ob.items():
		arr.append(x)
		arr.append(y)
		for w,z in ob2.items():
			e += 1
			arr.append(w)
			arr.append(z)

	TestError( e==4 )
	TestError( 'a' in arr)
	TestError( 'b' in arr)
	TestError( 'A' in arr)
	TestError( 'B' in arr)
	TestError( 'c' in arr)
	TestError( 'C' in arr)
	TestError( 'd' in arr)
	TestError( 'D' in arr)



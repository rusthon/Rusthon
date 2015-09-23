from runtime import *
'''
for loop tests
'''

def main():

	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	assert( y==6 )

	z = ''
	arr = ['a', 'b', 'c']
	for v in arr:
		z += v
	assert( z == 'abc' )

	b = False
	if 'a' in arr:
		b = True
	assert( b == True )

	s = 'hello world'
	z = ''
	for char in iter(s):
		z += char
	assert( z == 'hello world' )

	b = False
	if 'hello' in s:
		b = True
	assert( b==True )

	print 'testing for loop over dict'
	ob = {'a' : 'A', 'b' : 'B'}
	k = ''
	v = ''
	for key in iter(ob):
		k += key
		v += ob[key]
	print k
	print v
	assert(k=='ab' or k=='ba')
	assert(v=='AB' or v=='BA')

	keys = []
	values = []
	for x,y in ob.items():
		keys.append( x )
		values.append( y )

	assert( 'a' in keys )
	assert( 'A' in values )

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

	assert( e==4 )
	assert( 'a' in arr)
	assert( 'b' in arr)
	assert( 'A' in arr)
	assert( 'B' in arr)
	assert( 'c' in arr)
	assert( 'C' in arr)
	assert( 'd' in arr)
	assert( 'D' in arr)



main()

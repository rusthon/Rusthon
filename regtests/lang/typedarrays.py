from runtime import *
'''
javascript typed array syntax
'''

def main():
	s = [10,20,30]
	for v in s:
		print v
	print s

	print 'testing javascript typed arrays'
	a = [128]int( 1,2,3 )
	print __is_some_array(a)

	assert len(a)==128
	assert isinstance(a, Int32Array)
	assert a[0]==1
	assert a[1]==2
	assert a[2]==3
	assert a[3]==0

	ii = 0
	#for value in a:  ## will raise a runtime error
	for value in iter(a):
		print value
		ii += 1
		if ii > 10: break
	#print a

	b = [128]int32(1,2,3)
	c = [128]i32(1,2,3)
	assert isinstance(b, Int32Array)
	assert isinstance(c, Int32Array)

	d = [128]float( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float32Array)
	d = [128]float32( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float32Array)
	d = [128]f32( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float32Array)

	d = [128]float64( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float64Array)
	d = [128]f64( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float64Array)
	print d[0]
	print d[1]
	print d[2]


	print 'ok'

main()

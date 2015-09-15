from runtime import *
'''
javascript typed array syntax
'''

def main():
	print 'testing javascript typed arrays'
	a = [128]int( 1,2,3 )
	assert len(a)==128
	assert isinstance(a, Int32Array)
	assert a[0]==1
	assert a[1]==2
	assert a[2]==3
	assert a[3]==0

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

from runtime import *
"""concatenate lists"""

def main():
	a = [1,2]
	b = [3,4]
	n = 1
	w = 100
	with oo:
		c = a + b
		## it is slow to just stick everything under `with oo`
		## because these operations on numbers become much slower.
		n += n
		w = w + w

	assert n == 2
	assert w == 200

	assert( len(c)==4 )
	assert( c[0]==1 )
	assert( c[1]==2 )
	assert( c[2]==3 )
	assert( c[3]==4 )

	## the pythonic way is ugly
	d = a.__add__(b)
	assert len(d)==4

	## the recommend way in rusthon
	e = a.add(b)
	assert len(e)==4

main()

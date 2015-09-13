from runtime import *
"""Defined with {}"""
def f():
    pass
class G(object):
	pass

def main():
	g = G()
	a = {2: 22, 3:33, f:44, G:55, g:66}
	assert(a[2] == 22)
	assert(a[3] == 33)
	#assert(a[f] == 44)
	#assert(a[G] == 55)
	#assert(a[g] == 66)

main()

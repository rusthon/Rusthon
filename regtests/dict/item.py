from runtime import *
"""__getitem__"""
def f():
    pass
class G(object):
    def __init__(self):
        """XXX: Without __init__ the translation with javascript fail"""
        pass
def main():
	g = G()
	a = {'2': 22, 3:33}
	a[f] = 44
	a[g] = 66
	a[G] = 55
	assert(a['2'] == 22)
	assert(a[3] == 33)
	assert(a[f] == 44)
	assert(a[G] == 55)
	assert(a[g] == 66)

	assert(a.get('none', 'default') == 'default')


main()

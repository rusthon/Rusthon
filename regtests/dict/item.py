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
	TestError(a['2'] == 22)
	TestError(a[3] == 33)
	TestError(a[f] == 44)
	TestError(a[G] == 55)
	TestError(a[g] == 66)


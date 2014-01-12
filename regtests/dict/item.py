"""__getitem__"""
def f():
    pass
class G(object):
    def __init__(self):
        """XXX: Without __init__ the translation with javascript fail"""
        pass
g = G()
a = {'2': 22, 3:33}
a[f] = 44
a[g] = 66
a[G] = 55
Error(a['2'] == 22)
Error(a[3] == 33)
Error(a[f] == 44)
Error(a[G] == 55)
Error(a[g] == 66)


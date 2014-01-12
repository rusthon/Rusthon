"""Defined with {}"""
def f():
    pass
class G(object):
    def __init__(self):
        """XXX: Without __init__ the translation with javascript fail"""
        pass
g = G()
a = {'2': 22, 3:33, f:44, G:55, g:66}
Error(a['2'] == 22)
Error(a[3] == 33)
Warning(a[f] == 44)
Warning(a[G] == 55)
Warning(a[g] == 66)

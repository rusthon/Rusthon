from runtime import *
"""instance and class attributes"""

class A:
    g = 6
    def __init__(self):
        self.b = 5

a = None
def main():
    a = A()

    assert(a.b == 5)

    ## this is valid in regular CPython, but not in PythonJS,
    ## the variable `g` is only attached to the class Object,
    ## not the instance.  The builtin `getattr` is smart enough
    ## to check the class object for the attribute, and return
    ## it if it finds it on the class.
    #assert(a.g == 6)

    try:
        x = a.c
        assert(not 'No exception: on undefined attribute')
    except AttributeError:
        pass

    b = a
    assert(getattr(b, 'b') == 5)
    assert(getattr(b, 'g') == 6)
    try:
        getattr(b, 'c')
        assert(not 'No exception: getattr on undefined attribute')
    except AttributeError:
        pass

    b.g = 100
    assert( A.g == 6)
main()

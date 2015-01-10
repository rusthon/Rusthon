"""instance and class attributes"""

class A:
    g = 6
    def __init__(self):
        self.b = 5

a = None
def main():
    a = A()

    TestError(a.b == 5)

    ## this is valid in regular CPython, but not in PythonJS,
    ## the variable `g` is only attached to the class Object,
    ## not the instance.  The builtin `getattr` is smart enough
    ## to check the class object for the attribute, and return
    ## it if it finds it on the class.
    #TestError(a.g == 6)

    try:
        x = a.c
        TestError(not 'No exception: on undefined attribute')
    except AttributeError:
        pass

    b = a
    TestError(getattr(b, 'b') == 5)
    TestError(getattr(b, 'g') == 6)
    try:
        getattr(b, 'c')
        TestError(not 'No exception: getattr on undefined attribute')
    except AttributeError:
        pass

    b.g = 100
    TestError( A.g == 6)
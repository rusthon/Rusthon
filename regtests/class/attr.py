"""instance attributes"""

class A:
    g = 6
    def __init__(self):
        self.b = 5

def main():
    a = A()

    TestError(a.b == 5)
    TestError(a.g == 6)
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
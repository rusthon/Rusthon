"""instance attributes"""

class A:
    g = 6
    def __init__(self):
        self.b = 5

def main():
    a = A()

    TestError(a.b == 5)
    TestWarning(a.g == 6)
    try:
        x = a.c
        TestWarning(not 'No exception: on undefined attribute')
    except AttributeError:
        pass

    TestError(getattr(a, 'b') == 5)
    TestWarning(getattr(a, 'g') == 6)
    # TestWarning(getattr(a, 'c', 42) == 42)
    try:
        getattr(a, 'c')
        TestWarning(not 'No exception: getattr on undefined attribute')
    except AttributeError:
        pass
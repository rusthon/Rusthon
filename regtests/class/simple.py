"""simple class"""

class A:
    def __init__(self):
        self.x = 5

def main():
    a = A()
    TestError(a.x == 5)

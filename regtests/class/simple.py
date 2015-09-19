from runtime import *
"""simple class"""

class A:
    def __init__(self):
        self.x = 5

def main():
    a = A()
    assert(a.x == 5)

main()

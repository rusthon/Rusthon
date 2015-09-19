from runtime import *
'''
test __init__ with keyword arg
'''

def main():
    class Cell:
        def __init__(self, x=1):
            self.x = x

    a = Cell(x=2)
    assert(a.x == 2)
main()

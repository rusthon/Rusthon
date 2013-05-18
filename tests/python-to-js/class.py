class A(B, C):

    def METHOD(self, a, b, c, d=4, e=5):
        return a + b + c + d + e


a = A()
print a.METHOD(1, 2, 3)
print a.METHOD(1, 2, 3, 6, 7)

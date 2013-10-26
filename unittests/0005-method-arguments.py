class A:

    def method(self, a, b, c=3, d=4, *args, **kwargs):
        print a, b, c, d, len(args), len(kwargs)
        return a+b+c+d

print '>>> A().method(1,2)'
print A().method(1,2)
print '>>> A().method(11,22,33,44,55,66)'
print A().method(11,22,33,44,55,66)
print '>>> A().method(1, 2, e=True)'
print A().method(1, 2, e=True)
print '>>> A().method(11,22,33,44,55,66,e=True,f=True)'
print A().method(11,22,33,44,55,66,e=True,f=True)


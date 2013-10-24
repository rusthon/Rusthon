def func(a, b, c=3, d=4, *args, **kwargs):
    print a, b, c, d, len(args), len(kwargs)
    return a+b+c+d

print '>>> func(1,2)'
print func(1,2)
print '>>> func(11,22,33,44,55,66)'
print func(11,22,33,44,55,66)
print '>>> func(1, 2, e=True)'
print func(1, 2, e=True)
print '>>> func(11,22,33,44,55,66,e=True,f=True)'
print func(11,22,33,44,55,66,e=True,f=True)


def func(a=1):
    print a

print '>>> func()'
func()
print '>>> func()'
func(2)

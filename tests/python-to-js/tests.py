class A(B,C):
    pass

a.b = c.d

JS('var a = new Object()')
var(object, args, str)
object = JSObject(spam=7, egg=8)
args = JSArray(5, 6)
str = toString(egg)

# function(1, 2, 3, 4, *args, **kwargs)

@deco_a
@deco_b
def function(a, b, c=3, d=4, *args, **kwargs):
    print a, b, c, d
    sum = a + b + c + d
    print sum
    for arg in args:
        print args
    print kwargs

'''array of objects'''
class A:
    def foo(self) -> string:
        return 'xxxx'
class B(A):
    def foo(self) -> string:
        return 'hello'
class C(A):
    def foo(self) -> string:
        return 'world'


def push( arr:[]int, x:int ):
    arr.append( x )

def push2( arr:[]*A, x:*A ):
    arr.append( x )

def my_generic( s:A ):
    print( s.foo() )


def main():
    arr = []int()
    arr.append(1)
    push( arr, 100)
    TestError( len(arr)==2 )
    print(arr)

    a1 = A(); a2 = A(); a3 = A()
    obarr = []A( a1, a2 )
    print(obarr)

    push2( obarr, a3 )
    print(obarr)
    TestError( len(obarr)==3 )

    b1 = B()
    print(b1)
    #obarr.append( b1 )  ## fails because subclasses can not be cast to their base class

    #################################################
    barr = []B( b1, )  ## todo single item array should not require `,`
    c1 = C()
    barr.append( c1 )
    print(barr)

    bb = barr[0]
    print('bb:', bb)
    print(bb.foo())

    cc = barr[1]
    print('cc:', cc)
    print(cc.foo())

    #ccc = go.type_assert( cc, C )
    #print(ccc.foo())

    print('----testing generic----')
    for subclass in barr:
        print('subclass in bar:', subclass)
        my_generic(subclass)
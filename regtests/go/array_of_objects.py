'''array of objects'''
class A: pass
class B(A): pass
class C(A): pass

def push( arr:[]int, x:int ):
    arr.append( x )

def push2( arr:[]*A, x:*A ):
    arr.append( x )

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
    #obarr.append( b1 )  ## fails

    barr = []B( b1, )  ## todo single item array should not require `,`
    c1 = C()
    barr.append( c1 )
    print(barr)
C++11 std::move
--------------

`std::move` is also used below, this is the fastest way to move strings around without making a copy,
the original variable becomes invalid after moved.
http://en.cppreference.com/w/cpp/utility/move

```rusthon
#backend:c++

def foo( s:string&& ):
	print 'string moved into foo'
	s += 'z'
	print s

def main():
	vec = []string(
		'hello',
		'world'
	)
	print vec[0]
	print vec[1]

	a = 'bar'
	b = 'xxx'
	print 'testing std::move'
	with MV as "std::move(%s)":
		vec.append( MV(a) )
		foo( MV(b) )
	print 'done moving a and b'
	## this prints nothing because std::move was used on a and b
	print a
	print b
	print vec[2]  ## this prints `bar`


```
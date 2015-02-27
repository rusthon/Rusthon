String
------
the c++ backend translates strings into `std::string`.

```rusthon

myglobal = 'hi'
def main():
	u = 'X'
	print len(u)
```

below the end of the string is indexed with `a[-1]`, negative indices must be given as literals.
normal postive indices can be variables like `a[n]`.

```rusthon

	a = 'XYZ'
	print( a[0] == 'X' )
	print( a[-1] == 'Z' )
	print myglobal[-1]

```

string slice syntax
-------------------
just lower and upper slicing is supported, step is not allowed.

```rusthon
	print( a[0:2] == 'XY' )
	print a[0:2]
	print a[:2] == 'XY'

	print a[1:3] == 'YZ'
	print a[1:] == 'YZ'
```

builtins and methods

```rusthon
	print a.lower()

	print ord('A')  ## should be 65
	print chr(65)   ## should be 'A'

	v1 = a.split()
	print v1
	print len(v1)
	print v1[0]

	abc = 'a b c'
	print abc
	print abc.upper()
```

split into a vector, only single character splits are supported now.

```rusthon
	v2 = abc.split()
	print 'string split ok'
	print v2
	print 'should print 3:', len(v2)
	print 'v2[0]'
	print v2[0]
```

test if string is in a string.

```rusthon
	if 'b' in abc:
		print 'b in abc'
	else:
		print 'in test error'

	if 'b' in v2:
		print 'b in vector'
	else:
		print 'in array test error'

	print 'ok'

```

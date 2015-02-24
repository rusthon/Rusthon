String
------
the c++ backend translates strings into `std::string`.

```rusthon

myglobal = 'hi'
def main():
	u = 'X'
	print len(u)

	a = 'XYZ'
	print( a[0] == 'X' )
	print( a[-1] == 'Z' )
	print myglobal[-1]

	print( a[0:2] == 'XY' )
	print a[0:2]
	print a[:2] == 'XY'

	print a[1:3] == 'YZ'
	print a[1:] == 'YZ'

	print 'ok'

```

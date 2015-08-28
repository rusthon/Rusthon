Mini Inline Macros
--------------

Below `T` becomes the macro `std::vector<int>({%s})` used by the transpiler when translating to C++.

```rusthon
#backend:c++

def main():
	with T as "std::vector<int>({%s})":
		print 'testing creating -> std::vector<int>'
		vec = new( T(1,2,3) )
		print vec
		print vec[0]
		print vec[1]
		print vec[2]

```
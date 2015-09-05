Mini Inline Macros
--------------

Below `T` becomes the macro `std::vector<int>({%s})` used by the transpiler when translating to C++.

`std::move` is also used below, this is the fastest way to move strings around without making a copy,
the original variable becomes invalid after moved.
http://en.cppreference.com/w/cpp/utility/move

```rusthon
#backend:c++

def main():
	with T as "std::vector<std::string>({%s})":
		print 'testing creating -> std::vector< std::string >'
		vec = new( T('hello','world','foo') )
		print vec
		print vec[0]
		print vec[1]
		print vec[2]

		a = 'bar'
		print 'testing std::move'
		with MV as "std::move(%s)":
			## note: `vec.append` can not be used here because the transpiler is not aware that
			## vec is an array because it was created via the macro, 
			## in this case you must call `push_back` directly.
			vec.push_back( MV(a) )

		print a       ## this prints nothing because std::move was used
		print vec[3]  ## this prints `bar`


```
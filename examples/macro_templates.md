Mini Inline Macros
--------------

Below `T` becomes the macro `std::vector<int>({%s})` used by the transpiler when translating to C++.

`std::move` is also used below, this is the fastest way to move strings around without making a copy,
the original variable becomes invalid after moved.
http://en.cppreference.com/w/cpp/utility/move


__unicode notes:__
* macros can use unicode characters, these are replaced at compile time with the macro string
* functions with unicode in the mathematical alphanumerics range will be translated into regular ASCII, so `𝓕𝓞𝓞` becomes `FOO`.
* functions with other unicode will be obfuscated, so that `ੴ` beecomes `__x0s0x__N__x0e0x__`, where `N` is the ordinal of the character.
* if the command line option `--obfuscate` is used then heavy obfuscation is used on unicode characters.

```rusthon
#backend:c++

def 𝓕𝓞𝓞( s:string ):
	print s

def ੴ( a:int, b:int ):
	print a+b

def main():
	𝓕𝓞𝓞('foo ok')
	ੴ( 1,2 )

	with T as "std::vector<std::string>({%s})":
		print 'testing creating -> std::vector< std::string >'
		vec = new( T('hello','world','foo') )
		print vec
		print vec[0]
		print vec[1]
		print vec[2]

		a = 'bar'
		print 'testing std::move'
		with 𝓜𝓿 as "std::move(%s)":
			## note: `vec.append` can not be used here because the transpiler is not aware that
			## vec is an array because it was created via the macro, 
			## in this case you must call `push_back` directly.
			vec.push_back( 𝓜𝓿(a) )

		print a       ## this prints nothing because std::move was used
		print vec[3]  ## this prints `bar`


```
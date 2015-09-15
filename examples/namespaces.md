C++ Namespaces
--------------
Macros are used when C++ name spaces need to be used directly.

note `[...]` is syntax for manual pointer deference

```rusthon
#backend:c++

def main():
	vec = []int(1,2,3,4,5,6)
	ref = vec[...]
	with Max as 'std::max_element( std::begin(%s), std::end(%s) )':
		max = Max(ref, ref)
	print max[...]

	with Min as 'std::min_element( std::begin(%s), std::end(%s) )':
		min = Min(ref, ref)
	print min[...]


```
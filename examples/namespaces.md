C++ Namespaces
--------------
note `[...]` is syntax for manual pointer deference

```rusthon
#backend:c++

def main():
	vec = []int(1,2,3,4,5,6)
	max = std::max_element( std::begin(vec[...]), std::end(vec[...]) )
	print max[...]

	min = std::min_element(
		std::begin(vec[...]), 
		std::end(vec[...]) 
	)
	print min[...]


```
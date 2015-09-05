'''
rust pointer and typedefs
'''
# this is just for testing syntax, the rustc may have errors on this code

def f(a:&mut int) ->int:
	return a


def main():
	#f(&mut *x)
	#f(@mut *x, y.z())  ## translates to `ref mut *x`, but this might be deprecated in the latest rust.
	f(x as uint)

	let x : Vec<(uint, Y<int>)> = range(0,1).map().collect()
	let i
	#i = &**x


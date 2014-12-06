'''
gcc inline assembly
'''
#with asm( volatile=True, inputs=(a,b), outputs=(c,d), clobber=("cc", "memory") ):

def test_single_input( a : int ) -> int:
	let b : int = 0
	with asm( outputs=b, inputs=a, volatile=True ):
		movl %1, %%ebx;
		movl %%ebx, %0;
	return b

def test_multi_input( a : int, b : int ) -> int:
	let out : int = 0
	with asm( outputs=out, inputs=(a,b), volatile=True ):
		movl %1, %%ebx;
		addl %2, %%ebx;
		movl %%ebx, %0;
	return out


def main():
	let x : int = test_single_input(999)
	print x  ## should print 999

	let y : int = test_multi_input(400, 20)
	print y  ## should print 420
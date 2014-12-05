'''
gcc inline assembly
'''
#with asm( volatile=True, inputs=(a,b), outputs=(c,d), clobber=("cc", "memory") ):

def test_single_input( a : int ):
	b = 0
	with asm( outputs=b, inputs=a, volatile=True ):
		movl %1, %%ebx;
		movl %%ebx, %0;
	return b



def main():
	x = test_single_input(999)
	print x  ## should print 999
from runtime import *
'''
in (dict contains)
'''

def main():
	d = {'x':1}
	a = 'x' in d
	assert( a==True )
	b = 'y' in d
	assert( b==False )



main()

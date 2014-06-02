'''stdlib array'''
from array import array

def main():
	a = array('i', [1,2,3])
	TestError( len(a)==3 )
	TestError( a[0]==1 )

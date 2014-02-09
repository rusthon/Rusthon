'''
list comprehensions
'''

def main():
	a = [x for x in range(3)]
	TestError( len(a)==3 )
	TestError( a[0]==0 )
	TestError( a[1]==1 )
	TestError( a[2]==2 )

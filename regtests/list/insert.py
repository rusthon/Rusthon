from runtime import *
"""insert"""
def main():
	global a
	print 'testing array.insert'
	print []
	print '----'
	a = [1,2,3,4]
	print a.length
	print Object.keys(a)
	print '____'
	print a
	assert( len(a)==4 )

	a.insert(0, 'hi')
	#print a
	assert( len(a)==5 )
	assert( a[0]=='hi' )

	a.insert(1, a.pop(0))
	#print a
	assert( a[0]==1 )
	assert( a[1]=='hi' )

main()

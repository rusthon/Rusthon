from runtime import *
'''
while else loop (DEPRECATED)
'''

def main():

	a = False
	i = 0
	while i < 10:
		i += 1
	else:
		a = True

	assert( a==True )

	b = False
	i = 0
	while i < 10:
		i += 1
		break
	else:
		b = True

	assert( b==False )


main()

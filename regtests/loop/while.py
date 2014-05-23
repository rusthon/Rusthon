'''
while loop
'''

arr1 = []
arr2 = []

def main():
	a = 0
	i = 0
	while i < 10:
		j = 0
		while j < 10:
			a += 1
			j += 1
		i += 1

	TestError( a==100 )

	while len(arr1)+len(arr2) < 10:
		arr1.append( 1 )
		arr2.append( 2 )

	TestError( len(arr1)==5 )
	TestError( len(arr2)==5 )

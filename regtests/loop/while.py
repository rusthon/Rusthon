'''
while loop
'''

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


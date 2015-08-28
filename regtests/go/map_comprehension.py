'''
map comprehensions
'''

def main():
	m = map[int]string{ 
		key:'xxx' for key in range(10)
	}
	assert m[0]=='xxx'
	assert m[9]=='xxx'
	print m
	print m[0]
	print m[1]

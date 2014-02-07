'''
simple for loop
'''

def main():
	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	TestError( y==6 )
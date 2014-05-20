"""remove"""

def main():
	a = [1,2]
	a.remove(1)
	TestError( len(a) == 1 )


"""The string iterator"""

def main():
	a = list("abc")
	TestError(a[0] == 'a')
	TestError(a[1] == 'b')
	TestError(a[2] == 'c')

	a = []
	for i in "abc":
		a.append(i)
	TestError(a[0] == 'a')
	TestError(a[1] == 'b')
	TestError(a[2] == 'c')

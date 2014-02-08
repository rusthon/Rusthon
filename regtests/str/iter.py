"""The string iterator"""

def main():
	a = list("abc")
	TestError(a[0] == 'a')
	TestError(a[1] == 'b')
	TestError(a[2] == 'c')

	b = ['a']
	for i in "xyz":
		b.append(i)
	TestError(b[0] == 'a')
	TestError(b[1] == 'x')
	TestError(b[2] == 'y')
	TestError(b[3] == 'z')

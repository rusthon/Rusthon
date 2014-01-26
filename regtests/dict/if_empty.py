"""if empty dict then false"""
def main():
	d = {}
	if d:
		err1 = 1
	else:
		err1 = 0

	if {}:
		err2 = 1
	else:
		err2 = 0

	d['x'] = 'xxx'
	if d:
		err3 = 0
	else:
		err3 = 1

	TestError( err1 == 0 )
	TestError( err2 == 0 )
	TestError( err3 == 0 )

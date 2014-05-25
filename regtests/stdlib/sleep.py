from time import sleep

def main():
	sleep(0.01)
	a = []
	sleep(0.1)
	a.append(1)
	sleep(0.1)
	a.append(2)

	TestError( len(a)==2 )
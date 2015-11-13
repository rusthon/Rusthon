from runtime import *
'''
timeout decorator with loop
'''

counter = 0

def main():
	@timeout(1)
	def foo():
		print 'foo'

	@timeout(1, loop=True)
	def bar():
		global counter
		print 'bar:'+counter
		counter += 1
		if counter > 5:
			process.exit()

main()

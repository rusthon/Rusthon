"""Specials chars in strings"""
from runtime import *

class C:
	def __init__(self):
		self.value = None

def main():
	print 'testing special strings'
	assert(len('\\') == 1)
	#a = u'éè'  ## prefixing `u` is invalid, and will cause UnicodeDecodeError

	a = 'éè'
	print a
	assert( a == 'é' + 'è')

	c = C()
	c.value = "é"
	assert( c.value == 'é')

	assert len('éè') == 2
	assert('éè'[::-1] == 'èé')
	print 'ok'

main()
"""Specials chars in strings"""

class C:
	def __init__(self):
		self.value = None

def main():
	TestError(len('\\') == 1)
	TestError(u'éè' == u'é' + u'è')

	c = C()
	c.value = u"é"
	TestError( c.value == u'é')

	if len(u'éè') == 2: # The interpreter assumes UTF8 (all except Python2)
		TestError(u'éè'[::-1] == u'èé')

	else:
		TestError(tuple(u'éè'[::-1]) == (chr(168), chr(195), chr(169), chr(195)))

"""Specials chars in strings"""

class C:
    pass

def main():
	TestError(len('\\') == 1)
	TestError(u'éè' == u'é' + u'è')

	C.value = u"é"
	TestError( C.value == u'é')

	if len(u'éè') == 2: # The interpreter assumes UTF8 (all except Python2)
		TestError(u'éè'[::-1] == u'èé')

	else:
		TestError(tuple(u'éè'[::-1]) == (chr(168), chr(195), chr(169), chr(195)))

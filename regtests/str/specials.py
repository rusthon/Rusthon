"""Specials chars in strings"""

def main():
	TestError(len('\\') == 1)
	TestError('éè' == 'é' + 'è')
	if len('éè') == 2: # The interpreter assumes UTF8 (all except Python2)
		TestError('éè'[::-1] == 'èé')
	else:
		# run.py fails if the right part is defined as strings, must use chr()
		TestError(tuple('éè'[::-1]) == (chr(168), chr(195), chr(169), chr(195)))

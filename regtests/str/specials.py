"""Specials chars in strings"""
Error(len('\\') == 1)
Error('éè' == 'é' + 'è')
if len('éè') == 2: # The interpreter assumes UTF8 (all except Python2)
    Error('éè'[::-1] == 'èé')
else:
    # run.y fail if the right part is defined as strings, must use chr()
    Error(tuple('éè'[::-1]) == (chr(168), chr(195), chr(169), chr(195)))

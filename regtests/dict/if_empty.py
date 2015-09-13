from runtime import *
"""if empty dict then false"""

## if mydict: will not work,
## workaround: `if len(d.keys())`

def main():
	d = {}
	#print __jsdict_keys(d)
	if d.keys().length:
		err1 = 1
	else:
		err1 = 0

	if len({}.keys()):
		err2 = 1
	else:
		err2 = 0

	d['x'] = 'xxx'
	if len(d.keys()):
		err3 = 0
	else:
		err3 = 1

	assert( err1 == 0 )
	assert( err2 == 0 )
	assert( err3 == 0 )

main()

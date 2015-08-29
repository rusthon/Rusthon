import os, sys, subprocess

passed = []
ignore = ()

TODO_FIX = (
)

files = os.listdir('./c++')
files.reverse()
for md in files:
	if md in TODO_FIX:
		print 'skip test: %s (TODO fix later)' %md
		continue
	elif not md.endswith('.py'):
		continue

	print md
	if md.startswith( ignore ):
		continue
	subprocess.check_call([
		'python',
		'../rusthon.py',
		'--c++',
		os.path.join('./c++', md)
	])
	passed.append( md )

print 'TESTS PASSED:'
for md in passed:
	print '	%s' %md

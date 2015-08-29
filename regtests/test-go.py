import os, sys, subprocess

passed = []
ignore = ()

TODO_FIX = (
	'generics_subcls_return_a_subcls.py',
	'generics_mreturns.py',
)

files = os.listdir('./go')
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
		'--go',
		os.path.join('./go', md)
	])
	passed.append( md )

print 'TESTS PASSED:'
for md in passed:
	print '	%s' %md

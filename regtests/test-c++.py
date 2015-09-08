import os, sys, subprocess

passed = {}
ignore = ()

TODO_FIX = (
	'chain.py',
	'generics_subclasses.py',
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

	passed[ md ] = open('/tmp/rusthon-c++-build.cpp').read().split('/*end-builtins*/')[-1]


print 'TESTS PASSED:'
report = [
	'C++11 Backend Regression Tests',
	'-----------------------------',
	'the following tests compiled, and the binary executed without any errors',
]

for md in passed:
	print md
	report.append('* [%s](c++/%s)' %(md,md))
	report.append('')
	report.append('input:')
	report.append('------')
	report.append('```python')
	report.extend( open('./c++/'+md, 'rb').read().splitlines() )
	report.append('```')
	report.append('output:')
	report.append('------')
	report.append('```c++')
	report.extend( passed[md].splitlines() )
	report.append('```')

open('regtest-report-c++.md', 'wb').write('\n'.join(report))

import os, sys, subprocess

passed = {}
ignore = ()

TODO_FIX = (
	'generics_subcls_return_a_subcls.py',
	'generics_mreturns.py',
	'generics_init.py',
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

	passed[ md ] = open('/tmp/rusthon-go-build.go').read().split('/*end-builtins*/')[-1]


print 'TESTS PASSED:'
report = [
	'Go Backend Regression Tests',
	'-----------------------------',
	'the following tests compiled, and the binary executed without any errors',
]

for md in passed:
	print md
	report.append('* [https://github.com/rusthon/Rusthon/tree/master/regtests/go/%s](%s)' %(md,md))
	report.append('input:')
	report.append('------')
	report.append('```python')
	report.extend( open('./go/'+md, 'rb').read().splitlines() )
	report.append('```')
	report.append('output:')
	report.append('------')
	report.append('```c++')
	report.extend( passed[md].splitlines() )
	report.append('```')

open('regtest-report-go.md', 'wb').write('\n'.join(report))

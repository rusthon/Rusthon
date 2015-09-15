import os, sys, subprocess



ignore = (
	'tuple_keys.py',
	'for_else.py',
	'while_else.py',
)

TODO_FIX = (
	'yield.py'
)

for folder in 'list calling str dict loop lang set'.split():
	report = [
		'JavaScript Backend Regression Tests - %s' %folder,
		'-----------------------------',
		'the following tests compiled, and run in nodejs without any errors',
	]


	passed = {}

	print 'testing folder: '+folder
	files = os.listdir('./'+folder)
	files.sort()

	for md in files:
		if md in TODO_FIX:
			print 'skip test: %s (TODO fix later)' %md
			continue
		elif not md.endswith('.py'):
			continue
		print md
		if md.startswith( ignore ):
			continue

		## temp hack old tests to new format ##
		data = open('./'+folder+'/'+md, 'rb').read()
		if 'TestError(' in data:
			print 'hacking test:' + md
			data = data.replace('TestError(', 'assert(')
			data = 'from runtime import *\n' + data + '\nmain()\n'
			open('./'+folder+'/'+md, 'wb').write(data)


		subprocess.check_call([
			'python',
			'../rusthon.py',
			'--javascript',
			'--release',
			os.path.join('./'+folder, md)
		])
		js = md[:-2] + 'js'
		passed[ md ] = open('/tmp/'+js).read().split('/*end-builtins*/')[-1]

	print 'TESTS PASSED:'
	for md in passed:
		print md
		report.append('* [%s](%s/%s)' %(md,folder, md))
		report.append('')
		report.append('input:')
		report.append('------')
		report.append('```python')
		report.extend( open('./'+folder+'/'+md, 'rb').read().splitlines() )
		report.append('```')
		report.append('output:')
		report.append('------')
		report.append('```javascript')
		report.extend( passed[md].splitlines() )
		report.append('```')

	open('regtest-report-js-%s.md'%folder, 'wb').write('\n'.join(report))

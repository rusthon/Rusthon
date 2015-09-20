import os, sys, subprocess

passed = {}

def runbench_py(path, name, interp='python3'):
	data = open(os.path.join(path, name), 'rb').read()
	data = data.replace('from runtime import *', '')
	open('/tmp/input.py', 'wb').write(data)

	subprocess.check_call([
		'python',
		'../rusthon.py',
		'--convert2python=/tmp/output.py',
		'/tmp/input.py'
	])


	proc = subprocess.Popen(
		[interp, '/tmp/output.py',], stdout=subprocess.PIPE
	)
	proc.wait()
	T = proc.stdout.read().splitlines()[0]  ## extra lines could contain compiler warnings, etc.
	return float(T.strip())

def runbench(path, name, backend='javascript'):
	proc = subprocess.Popen([
		'python',
		'../rusthon.py',
		'--'+backend,
		'--release',
		os.path.join(path, name)
	], stdout=subprocess.PIPE)
	proc.wait()
	T = proc.stdout.read().splitlines()[0]  ## extra lines could contain compiler warnings, etc.
	if backend=='javascript':
		js = name[:-2] + 'js'
		passed[ name ] = open('/tmp/'+js).read().split('/*end-builtins*/')[-1]

	return float(T.strip())

BENCHES = [
	'add.py',

]

for name in BENCHES:
	times = {}
	times['javascript'] = runbench('./bench', name, 'javascript')
	#times['rust'] = runbench('./bench', name, 'rust')
	times['go']   = runbench('./bench', name, 'go')
	times['c++']  = runbench('./bench', name, 'c++')
	times['python'] = runbench_py('./bench', name)
	times['pypy'] = runbench_py('./bench', name, interp='pypy')

	print times


def x():
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

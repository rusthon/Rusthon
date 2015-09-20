import os, sys, subprocess

#apt-get install gnuplot transfig

passed = {}

def runbench_rs(path, name):
	data = open(os.path.join(path, name), 'rb').read()
	data = data.replace('from runtime import *', '')
	open('/tmp/input.rapyd', 'wb').write(data)
	tmpjs = '/tmp/rapyd-output.js'
	subprocess.check_call(['rapydscript', '/tmp/input.rapyd', '--screw-ie8', '--bare', '--output', tmpjs])
	#rapydata = open(tmpjs,'rb').read()
	proc = subprocess.Popen(['nodejs', tmpjs], stdout=subprocess.PIPE)
	proc.wait()
	T = proc.stdout.read().splitlines()[0]  ## extra lines could contain compiler warnings, etc.
	return str(float(T.strip()))

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
	return str(float(T.strip()))

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

	return str(float(T.strip()))

BENCHES = [
	'fannkuch.py',
	'add.py',
	'float.py'

]
TYPED = [
	'fannkuch.py',
	'float.py',
]

for name in BENCHES:
	times = {}
	#times['rapyd'] = runbench_rs('./bench', name)

	times['python'] = runbench_py('./bench', name)
	times['pypy'] = runbench_py('./bench', name, interp='pypy')


	times['javascript'] = runbench('./bench', name, 'javascript')
	if name in TYPED:
		nametyped = name.replace('.py','-typed.py')
		#times['rust'] = runbench('./bench', nametyped, 'rust')
		try: times['go']   = runbench('./bench', nametyped, 'go')
		except: pass
		try: times['c++']  = runbench('./bench', nametyped, 'c++')
		except: pass
	else:
		#times['rust'] = runbench('./bench', name, 'rust')
		times['go']   = runbench('./bench', name, 'go')
		times['c++']  = runbench('./bench', name, 'c++')

	print times
	perf_header = [
		'font=Helvetica',
		'fontsz=12',
		'=color_per_datum',
		'yformat=%g',
		'ylabel=seconds',
	]

	perf = [
		'Python3 ' + times['python'],
		'PyPy ' + times['pypy'],
		'Rusthon->JS ' + times['javascript'],
	]
	if 'c++' in times:
		perf.append('Rusthon->C++ ' + times['c++'])

	if 'go' in times:
		perf.append('Rusthon->Go ' + times['go'])


	perf_path = '/tmp/%s.perf' %name
	open( perf_path, 'wb' ).write( '\n'.join( perf_header+perf ).encode('utf-8') )
	os.system( './bargraph.pl -eps %s > /tmp/%s.eps' %(perf_path,name))
	subprocess.check_call([
		'convert', 
		'-density', '300', 
		'/tmp/%s.eps' % name, 
		'-resize', '400x600', 
		'-transparent', 'white',
		'./bench/%s.png' % name
	])

	if False:
		perf = [
			'PyPy ' + times['pypy'],
			'Rusthon->JS ' + times['javascript'],
			'Rusthon->C++ ' + times['c++'],
			'Rusthon->Go ' + times['go'],
		]

		perf_path = '/tmp/%s.perf' %name
		open( perf_path, 'wb' ).write( '\n'.join( perf_header+perf ).encode('utf-8') )
		os.system( './bargraph.pl -eps %s > /tmp/%s.eps' %(perf_path,name))
		subprocess.check_call([
			'convert', 
			'-density', '300', 
			'/tmp/%s.eps' % name, 
			'-resize', '400x600', 
			'-transparent', 'white',
			'./bench/mini-%s.png' % name
		])



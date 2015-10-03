import os, sys, subprocess

#apt-get install gnuplot transfig

passed = {}

def runbench_rs(path, name, strip=False):
	url = os.path.join(path, name)
	if os.path.isfile(url.replace('.py', '-rs.py')):
		url = url.replace('.py', '-rs.py')

	if strip:
		subprocess.check_call([
			'python',
			'../rusthon.py',
			'--convert2python=/tmp/input.rapyd',
			url
		])
	else:
		open('/tmp/input.rapyd','wb').write(open(url,'rb').read())

	data = open('/tmp/input.rapyd', 'rb').read()
	data = data.replace('from runtime import *', '')
	data = data.replace('from time import clock', 'JS("var clock = function(){return (new Date()).getTime()/1000;}")')
	data = 'def list(a): return a\n' + data
	data = 'import stdlib\n' + data
	open('/tmp/input.rapyd', 'wb').write(data)
	tmpjs = '/tmp/rapyd-output.js'
	subprocess.check_call(['nodejs', '/usr/local/bin/rapydscript', '/tmp/input.rapyd', '--bare', '--beautify', '--output', tmpjs])

	#rapydata = open(tmpjs,'rb').read(),
	proc = subprocess.Popen(['nodejs', tmpjs], stdout=subprocess.PIPE)
	proc.wait()
	T = proc.stdout.read().splitlines()[0]  ## extra lines could contain compiler warnings, etc.
	return str(float(T.strip()))

def runbench_py(path, name, interp='python3'):
	data = open(os.path.join(path, name), 'rb').read()
	data = data.replace('from runtime import *', '')
	data = data.replace('with oo:', '')
	lines = []
	for ln in data.splitlines():
		if ln.strip().startswith('v8->('):
			continue
		lines.append(ln)
	open('/tmp/input.py', 'wb').write('\n'.join(lines))

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
		'--v8-natives',
		'--release',
		os.path.join(path, name)
	], stdout=subprocess.PIPE)
	proc.wait()
	T = proc.stdout.read().splitlines()[0]  ## extra lines could contain compiler warnings, etc.
	if backend=='javascript':
		js = name[:-2] + 'js'
		passed[ name ] = open('/tmp/'+js).read().split('/*end-builtins*/')[-1]

	return str(float(T.strip()))

BENCHES = ['richards.py'
]

[
	'fannkuch.py',
	'nbody.py',
	'operator_overloading_functor.py',
	'operator_overloading_nonfunctor.py',
	'operator_overloading.py',
	'add.py',
	'float.py',
	'pystone.py',
]
TYPED = [
	#'fannkuch.py',
	#'float.py',
	#'pystone.py',
]

for name in BENCHES:
	print name
	times = {}
	#try:
	#	times['rapyd'] = runbench_rs('./bench', name)
	#except:
	#	pass

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
	elif False:
		#times['rust'] = runbench('./bench', name, 'rust')
		try: times['go']   = runbench('./bench', name, 'go')
		except: pass
		try: times['c++']  = runbench('./bench', name, 'c++')
		except: pass

	print times
	perf_header = [
		'font=Helvetica',
		'fontsz=12',
		'=color_per_datum',
		'yformat=%g',
	]
	if name=='pystone.py':
		perf_header.append('ylabel=Pystones')
	else:
		perf_header.append('ylabel=seconds')

	perf = [
		'Python3 ' + times['python'],
		'PyPy ' + times['pypy'],
		'Rusthon->JS ' + times['javascript'],
	]
	if 'rapyd' in times:
		perf.append('RapydScript ' + times['rapyd'])
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



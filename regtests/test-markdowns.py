import os, sys, subprocess

passed = []
ignore = ('fails_', 'giws_', 'unreal_', 'verilog', 'nuitka_', 'nim_', 'java_', 'custom_', 'cpython_')
ignoreosx = ['hello_cpython.md']

## rust is broken on fedora? Travis uses Debian.
TODO_FIX = (
	'async_channels_rust.md', # rustc: error while loading shared libraries: librustc_driver-4e7c5e5c.so: cannot open shared object file: No such file or directory
	'hello_nim.md',
	'hello_verilog.md',
	'cpython_multithreaded.md',
	'cpython_multithreaded_raw_capi.md',
	'hello_threejs.md',
	'hello_java.md',
	'hello_caffe.md',
	'hello_nuitka.md',
	'hello_rapydscript.md',
)

files = os.listdir('./examples')
files.reverse()
for md in files:
	if md in TODO_FIX:
		print 'skip test: %s (TODO fix later)' %md
		continue
	elif not md.endswith('.md'):
		continue
	elif sys.platform=='darwin' and md in ignoreosx:
		continue

	print md
	if md.startswith( ignore ):
		continue
	subprocess.check_call([
		'python',
		'./rusthon.py',
		os.path.join('./examples', md)
	])
	passed.append( md )

print 'TESTS PASSED:'
for md in passed:
	print '	%s' %md

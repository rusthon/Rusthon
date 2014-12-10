#!/usr/bin/env python
import os, sys, traceback, json

from python_to_pythonjs import main as python_to_pythonjs
from pythonjs import main as pythonjs_to_javascript
from pythonjs_to_dart import main as pythonjs_to_dart
from pythonjs_to_coffee import main as pythonjs_to_coffee
from pythonjs_to_lua import main as pythonjs_to_lua
from pythonjs_to_luajs import main as pythonjs_to_luajs
from pythonjs_to_go import main as pythonjs_to_go
from pythonjs_to_rust import main as pythonjs_to_rust
from pythonjs_to_cpp import main as pythonjs_to_cpp

cmdhelp = """\
usage: translator.py --output=myfile.js [--stdout|--dart|--coffee|--lua|--go|--rust|--cpp|--visjs|--no-wrapper|--no-runtime|--fast-javascript|--fast-loops|--pure-javascript|--modules|--analyze] file.py
(defaults to javascript mode)

example:
       translator.py --no-wrapper --stdout myscript.py > myscript.js
"""


def main(script, module_path=None):
	if '--visjs' in sys.argv:
		import python_to_visjs
		return python_to_visjs.main( script )
	else:
		code = ''
		res = None

		if '--cpp' in sys.argv:
			a = python_to_pythonjs(script, rust=True, module_path=module_path)
			code = pythonjs_to_cpp( a )
		elif '--rust' in sys.argv:
			a = python_to_pythonjs(script, rust=True, module_path=module_path)
			code = pythonjs_to_rust( a )
		elif '--go' in sys.argv:
			a = python_to_pythonjs(script, go=True, module_path=module_path)
			code = pythonjs_to_go( a )
		elif '--gopherjs' in sys.argv:
			a = python_to_pythonjs(script, go=True, module_path=module_path)
			code = pythonjs_to_go( a )

			exe = os.path.expanduser('~/go/bin/gopherjs')
			if not os.path.isfile(exe):
				raise RuntimeError('gopherjs not installed to ~/go/bin/gopherjs')
			import subprocess
			path = '/tmp/gopherjs-input.go'
			open(path, 'wb').write(code)
			subprocess.check_call([exe, 'build', path], cwd='/tmp')
			code = open('/tmp/gopherjs-input.js', 'rb').read()

		elif '--dart' in sys.argv:
			a = python_to_pythonjs(script, dart=True, module_path=module_path)
			code = pythonjs_to_dart( a )
		elif '--coffee' in sys.argv:
			a = python_to_pythonjs(script, coffee=True, module_path=module_path)
			code = pythonjs_to_coffee( a )
		elif '--lua' in sys.argv:
			a = python_to_pythonjs(script, lua=True, module_path=module_path)
			try: code = pythonjs_to_lua( a )
			except SyntaxError:
				err = traceback.format_exc()
				lineno = 0
				for line in err.splitlines():
					if "<unknown>" in line:
						lineno = int(line.split()[-1])

				b = a.splitlines()[ lineno ]
				sys.stderr.write( '\n'.join([err,b]) )
				
		elif '--luajs' in sys.argv:  ## converts back to javascript
			a = python_to_pythonjs(script, lua=True, module_path=module_path)
			code = pythonjs_to_luajs( a )
		else:
			a = python_to_pythonjs(
				script, 
				module_path=module_path,
				fast_javascript = '--fast-javascript' in sys.argv,
				modules  = '--modules' in sys.argv,
				pure_javascript = '--pure-javascript' in sys.argv
			)

			if isinstance(a, dict):
				res = {}
				for jsfile in a:
					res[ jsfile ] = pythonjs_to_javascript( a[jsfile], webworker=jsfile != 'main' )
				return res
			else:
				## requirejs module is on by default, this wraps the code in a `define` function
				## and returns `__module__`
				## if --no-wrapper is used, then the raw javascript is returned.
				## by default the pythonjs runtime is inserted, this can be disabled with `--no-runtime`
				code = pythonjs_to_javascript(
					a, 
					requirejs='--no-wrapper' not in sys.argv, 
					insert_runtime='--no-runtime' not in sys.argv,
					fast_javascript = '--fast-javascript' in sys.argv,
					fast_loops      = '--fast-loops' in sys.argv
				)
				if isinstance(code, dict):
					assert '--modules' in sys.argv
					path = 'build'
					if os.path.isdir(path):
						for name in code:
							open( os.path.join(path,name), 'wb' ).write( code[name] )
						return 'modules written to: ' + path
					else:
						raise RuntimeError('the option --modules requires a folder named "build" in your current directory')


		if '--analyze' in sys.argv:
			dartanalyzer = os.path.expanduser('~/dart-sdk/bin/dartanalyzer')
			#dart2js = os.path.expanduser('~/dart-sdk/bin/dart2js')
			assert os.path.isfile( dartanalyzer )

			x = python_to_pythonjs(script, dart=True, module_path=module_path)
			dartcode = pythonjs_to_dart( x )
			path = '/tmp/debug.dart'
			open(path, 'wb').write( dartcode )
			import subprocess
			try:
				subprocess.check_output( [dartanalyzer, path] )
			except subprocess.CalledProcessError as err:
				dartcodelines = dartcode.splitlines()
				for line in err.output.splitlines():
					if line.startswith('[error]'):
						a,b = line.split( path )
						a = a[:-1]
						print( '\x1B[0;31m' + a + '\x1B[0m' )
						lineno = int( b.split('line ')[-1].split(',')[0] )
						print('line: %s' %lineno)
						print( dartcodelines[lineno-1] )
				sys.exit(1)

		if res:  ## dict return
			return res
		else:
			return code

def command():
	if '-h' in sys.argv or '--help' in sys.argv:
		print(cmdhelp)
		return

	mpath = None
	scripts = []
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			if arg.endswith('.py') or arg.endswith('.html'):
				scripts.append( arg )
				if mpath is None:
					mpath = os.path.split(arg)[0]

	if len(scripts):
		a = []
		for script in scripts:
			a.append( open(script, 'rb').read() )
		data = '\n'.join( a )
	else:
		data = sys.stdin.read()

	js = main(data, module_path=mpath)
	stdout = '--stdout' in sys.argv
	dump   = False
	for arg in sys.argv:
		if arg.startswith('--output'):
			assert '=' in arg
			dump = arg.split('=')[-1]

	if isinstance(js, dict):
		out = json.dumps(js)
	else:
		out = js

	if stdout: print(out)
	else:
		if not dump:
			raise RuntimeError('no output file given. --output=filename')
		f = open(dump, 'wb')
		f.write( out )
		f.close()


if __name__ == '__main__':
	command()

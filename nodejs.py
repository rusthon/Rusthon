#!/usr/bin/env python
# NodeJS Wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

import os, sys, subprocess

PATHS = dict(
	pythonscript = os.path.abspath('pythonjs'),
	bindings = os.path.abspath('bindings'),
	runtime = os.path.abspath('pythonjs.js'),
	module_cache = '/tmp',
)


def python_to_pythonjs( src, module=None ):
	cmdheader = '#!' + PATHS['module_cache']
	if module:
		assert '.' not in module
		cmdheader += ';' + module
	cmdheader += '\n'

	cmd = ['python2', os.path.join( PATHS['pythonscript'], 'python_to_pythonjs.py')]
	p = subprocess.Popen(
		cmd,
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( (cmdheader + src).encode('utf-8') )
	return stdout.decode('utf-8')

def pythonjs_to_javascript( src ):
	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonscript'],'pythonjs.py')],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( src.encode('utf-8') )
	a = stdout.decode('utf-8')

	return a

def python_to_javascript( src, module=None, debug=False ):
	a = python_to_pythonjs( src, module=module )
	if debug: print( a )
	return pythonjs_to_javascript( a )


if __name__ == '__main__':
	stdin = subprocess.PIPE

	if len(sys.argv) == 1:  ## interactive nodejs console
		nodejs = subprocess.Popen(
			['nodejs'],
			stdin = sys.stdin,
			stdout = sys.stdout,
		)
		nodejs.wait()
	else:
		script = sys.argv[-1]
		assert script.endswith('.py')
		print 'translating script to javascript:', script

		runtime = open( PATHS['runtime'], 'rb').read()

		data = python_to_javascript( open(script, 'rb').read(), debug=True )
		f = open( '/tmp/nodejs-input.js', 'wb')
		f.write( runtime + '\n' + data )
		f.close()
		#print subprocess.check_output( ['nodejs', '/tmp/nodejs-input.js'] )
		print '<<running nodejs>>'
		nodejs = subprocess.Popen(
			['nodejs', '/tmp/nodejs-input.js'],
			stdout = sys.stdout,
		)
		nodejs.wait()


	print 'nodejs.py exit'


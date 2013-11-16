#!/usr/bin/env python
# NodeJS Wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"
# tested with NodeJS v0.10.22

import os, sys, subprocess

PATHS = dict(
	pythonjs = os.path.abspath('pythonjs'),
	nodejs_bindings = os.path.abspath('nodejs/bindings'),
	runtime = os.path.abspath('pythonjs.js'),
	module_cache = '/tmp',
)


def python_to_pythonjs( src, module=None ):
	cmdheader = '#!' + PATHS['module_cache']
	if module:
		assert '.' not in module
		cmdheader += ';' + module
	cmdheader += '\n'

	cmd = ['python2', os.path.join( PATHS['pythonjs'], 'python_to_pythonjs.py')]
	p = subprocess.Popen(
		cmd,
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( (cmdheader + src).encode('utf-8') )
	return stdout.decode('utf-8')

def pythonjs_to_javascript( src ):
	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonjs'],'pythonjs.py')],
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


def get_nodejs_bindings(source):
	bindings = []
	for line in source.splitlines():
		if line.strip().startswith('from nodejs.'):
			if line.strip().endswith('*'):
				name = line.split('.')[-1].split()[0]
				bindings.append( name )

	return bindings

if __name__ == '__main__':

	if len(sys.argv) == 1:  ## interactive nodejs console
		nodejs = subprocess.Popen(
			['node'],
			stdin = sys.stdin,
			stdout = sys.stdout,
		)
		nodejs.wait()
	else:
		#http://stackoverflow.com/questions/12594541/npm-global-install-cannot-find-module
		## node modules installed with "npm install -g xxx" need this
		if 'NODE_PATH' not in os.environ:
			os.environ['NODE_PATH'] = '/usr/local/lib/node_modules/'

		cmd = ['node', '/tmp/nodejs-input.js']
		if len(sys.argv) > 2:
			for arg in sys.argv[2:]:
				print 'ARG', arg
				cmd.append( arg )

		script = sys.argv[1]
		assert script.endswith('.py')
		print 'translating script to javascript:', script

		runtime = open( PATHS['runtime'], 'rb').read()

		header = []
		source = open(script, 'rb').read()
		bindings = get_nodejs_bindings( source )

		for binding in bindings:
			data = open( 
				os.path.join( PATHS['nodejs_bindings'], binding + '.py' ),
				'rb'
			).read()
			header.append( data )

		data = python_to_javascript( '\n'.join(header) + '\n' + source )
		f = open( '/tmp/nodejs-input.js', 'wb')
		f.write( runtime + '\n' + data )
		f.close()
		#print subprocess.check_output( ['nodejs', '/tmp/nodejs-input.js'] )
		print '<<running nodejs>>'
		nodejs = subprocess.Popen(
			cmd,
			stdout = sys.stdout,
		)
		nodejs.wait()


	print 'nodejs.py exit'


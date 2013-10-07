#!/usr/bin/python3
# Test Server for PythonScript
# by Brett Hartshorn - copyright 2013
# License: PSFLv2 - http://www.python.org/psf/license/
# Requires: Python3 and Tornado

try:
	import tornado
except ImportError:
	print('ERROR: Tornado is not installed')
	print('download Tornado from - http://www.tornadoweb.org/en/stable/')
	raise SystemExit

import tornado.ioloop
import tornado.web
import os, sys, subprocess, datetime

PATHS = dict(
	webroot = os.path.dirname(os.path.abspath(__file__)),
	pythonscript = os.path.abspath('../pythonscript'),
	bindings = os.path.abspath('../bindings'),
	closure = os.path.expanduser( '~/closure-compiler/compiler.jar'),
	runtime = os.path.abspath('../pythonscript.js'),
	module_cache = '/tmp',

	runtime_pythonjs = os.path.abspath('../runtime/pythonpythonjs.py'),  ## handwritten pythonjs
	runtime_builtins = os.path.abspath('../runtime/builtins.py'),

)

REGENERATE_RUNTIME = '--regenerate-runtime' in sys.argv

def python_to_pythonjs( src, module=None ):
	cmdheader = '#!%s' %PATHS['module_cache']
	if module:
		assert '.' not in module
		cmdheader += ';' + module
	cmdheader += '\n'

	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonscript'], 'python_to_pythonjs.py')],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( (cmdheader + src).encode('utf-8') )
	return stdout.decode('utf-8')

def pythonjs_to_javascript( src, closure_compiler=False ):
	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonscript'],'pythonjs.py')],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( src.encode('utf-8') )
	a = stdout.decode('utf-8')

	if closure_compiler and os.path.isfile( PATHS['closure'] ):
		x = '/tmp/input.js'; y = '/tmp/output.js';
		f = open(x, 'wb'); f.write( a.encode('utf-8') ); f.close()
		subprocess.call([
			'java', '-jar', PATHS['closure'], 
			'--compilation_level', 'ADVANCED_OPTIMIZATIONS', 
			'--js', x, '--js_output_file', y,
			'--formatting', 'PRETTY_PRINT',
			#'--create_name_map_files', 
		])
		f = open(y, 'rb'); a = f.read().decode('utf-8'); f.close()

	return a

def python_to_javascript( src, module=None, closure_compiler=False, debug=False ):
	a = python_to_pythonjs( src, module=module )
	if debug: print( a )
	return pythonjs_to_javascript( a, closure_compiler=closure_compiler )



#########################################################
def get_main_page():
	root = PATHS['webroot']
	r = ['<html><head><title>index</title></head><body>']
	r.append( '<ul>' )
	for name in os.listdir( root ):
		if name == os.path.split(__file__)[-1]: continue
		path = os.path.join( root, name )
		if os.path.isfile( path ):
			r.append( '<a href="%s"><li>%s</li></a>' %(name,name) )
	r.append('</ul>')
	r.append('</body></html>')
	return ''.join(r)


def convert_python_html_document( data ):
	'''
	rewrites html document, converts python scripts into javascript.
	example:
		<script type="text/python" closure="true">
		print("hello world")
		</script>

	Note:
		we need to parse and compile any python binding scripts that appear in the head,
		because later scripts may use classes from the bindings, and we need have the 
		AST introspected data available here to properly inline and for operator overloading.
	'''
	doc = list()
	script = None
	use_closure = False
	for line in data.splitlines():
		if line.strip().startswith('<script'):
			if 'src="bindings/' in line:
				doc.append( line )
				a,b,c = line.split('"')
				if b.endswith('.py'):  ## make sure the module is cached ##
					name = b.split('/')[-1]
					path = os.path.join( PATHS['bindings'], name )
					src = open(path, 'rb').read().decode('utf-8')
					pyjs = python_to_pythonjs( src, module=name.split('.')[0] )
					print(pyjs)
					print('_'*80)

			elif 'type="text/python"' in line:
				if 'closure="true"' in line.lower(): use_closure = True
				else: use_closure = False
				doc.append( '<script type="text/javascript">')
				script = list()
			else:
				doc.append( line )

		elif line.strip() == '</script>':
			if script:
				src = '\n'.join( script )
				js = python_to_javascript( src, closure_compiler=use_closure, debug=True )
				doc.append( js )
			doc.append( line )
			script = None

		elif isinstance( script, list ):
			script.append( line )

		else:
			doc.append( line )

	return '\n'.join( doc )


def regenerate_runtime():
	print('regenerating pythonscript runtime...')
	global REGENERATE_RUNTIME
	REGENERATE_RUNTIME = False
	a = '// PythonScript Runtime - regenerated on: %s' %datetime.datetime.now().ctime()
	b = pythonjs_to_javascript( open(PATHS['runtime_pythonjs'],'rb').read().decode('utf-8') )
	c = python_to_javascript( open(PATHS['runtime_builtins'],'rb').read().decode('utf-8') )
	src = '\n'.join( [a,b.strip(),c.strip()] )
	file = open( PATHS['runtime'], 'wb')
	file.write( src.encode('utf-8') )
	file.close()
	return src

class MainHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		print('path', path)
		if not path:
			self.write( get_main_page() )
		elif path == 'pythonscript.js':
			if REGENERATE_RUNTIME:
				data = regenerate_runtime()
			else:
				data = open( PATHS['runtime'], 'rb').read()
			self.set_header("Content-Type", "text/javascript; charset=utf-8")
			self.set_header("Content-Length", len(data))
			self.write(data)
		elif path.startswith('bindings/'):
			name = path.split('/')[-1]
			local_path = os.path.join( PATHS['bindings'], name )

			if os.path.isfile( local_path ):
				data = open(local_path, 'rb').read()
			else:
				raise tornado.web.HTTPError(404)

			if path.endswith('.py'):
				print('converting python binding to javascript', name)
				module = name.split('.')[0]
				data = python_to_javascript( data.decode('utf-8'), closure_compiler=False, module=module )

			self.set_header("Content-Type", "text/javascript; charset=utf-8")
			self.set_header("Content-Length", len(data))
			self.write( data )

		else:
			local_path = os.path.join( PATHS['webroot'], path )
			if os.path.isfile( local_path ):
				data = open(local_path, 'rb').read()
				if path.endswith( '.html' ):
					data = convert_python_html_document( data.decode('utf-8') )
					self.set_header("Content-Type", "text/html; charset=utf-8")
				elif path.endswith('.py'):
					data = python_to_javascript( data.decode('utf-8'), closure_compiler=True )
					self.set_header("Content-Type", "text/html; charset=utf-8")

				self.set_header("Content-Length", len(data))
				self.write( data )

			else:
				self.write('Hello World')


LIBS = dict(
	three = {'three.min.js' : os.path.expanduser( '~/three.js/build/three.min.js')},
	tween = {'tween' : os.path.expanduser( '~/tween.js/build/tween.min.js')},
)

class LibsHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		print('path', path)
		module, name = path.split('/')
		assert module in LIBS
		assert name in LIBS[ module ]
		if os.path.isfile( LIBS[module][name] ):
			data = open( LIBS[module][name], 'rb').read()
		else:
			raise tornado.web.HTTPError(404)

		self.set_header("Content-Type", "text/javascript; charset=utf-8")
		self.set_header("Content-Length", len(data))
		self.write( data )


Handlers = [
	(r'/libs/(.*)', LibsHandler),
	(r'/(.*)', MainHandler),  ## order is important, this comes last.
]


if __name__ == '__main__':
	assert os.path.isfile( PATHS['runtime'] )
	assert os.path.isdir( PATHS['pythonscript'] )
	assert os.path.isdir( PATHS['bindings'] )

	app = tornado.web.Application(
		Handlers,
		#cookie_secret = 'some random text',
		#login_url = '/login',
		#xsrf_cookies = False,
	)


	app.listen( 8080 )
	tornado.ioloop.IOLoop.instance().start()
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
import os, subprocess

PATHS = dict(
	webroot = os.path.dirname(os.path.abspath(__file__)),
	pythonscript = os.path.abspath('../pythonscript'),
	bindings = os.path.abspath('../bindings'),
	closure = os.path.expanduser( '~/closure-compiler/compiler.jar'),
	runtime = os.path.abspath('../pythonscript.js'),
)


def python_to_pythonjs( src ):
	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonscript'], 'python_to_pythonjs.py')],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( src.encode('utf-8') )
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
			#'--create_name_map_files', 
		])
		f = open(y, 'rb'); a = f.read().decode('utf-8'); f.close()

	return a

def python_to_javascript( src, closure_compiler=False ):
	a = python_to_pythonjs( src )
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
	'''
	doc = list()
	script = None
	use_closure = False
	for line in data.splitlines():
		if line.strip().startswith('<script') and 'type="text/python"' in line:
			if 'closure="true"' in line.lower(): use_closure = True
			else: use_closure = False
			doc.append( '<script type="text/javascript">')
			script = list()

		elif line.strip() == '</script>':
			if script:
				src = '\n'.join( script )
				js = python_to_javascript( src, closure_compiler=use_closure )
				doc.append( js )
			doc.append( line )
			script = None

		elif isinstance( script, list ):
			script.append( line )

		else:
			doc.append( line )

	return '\n'.join( doc )

class MainHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		print('path', path)
		if not path:
			self.write( get_main_page() )
		elif path == 'pythonscript.js':
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
				data = python_to_javascript( data.decode('utf-8'), closure_compiler=False )

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


Handlers = [
	(r'/(.*)', MainHandler)
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
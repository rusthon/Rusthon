#!/usr/bin/env python3
# Test Server for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"
# Requires: Python3 and Tornado

try:
	import tornado
except ImportError:
	print('ERROR: Tornado is not installed')
	print('download Tornado from - http://www.tornadoweb.org/en/stable/')
	raise SystemExit

import tornado.ioloop
import tornado.web
import tornado.websocket
import os, sys, subprocess, datetime, json

PATHS = dict(
	webroot = os.path.dirname(os.path.abspath(__file__)),
	pythonjs = os.path.abspath('../pythonjs'),
	bindings = os.path.abspath('../bindings'),
	runtime = os.path.abspath('../pythonjs.js'),
	module_cache = '/tmp',

	runtime_pythonjs = os.path.abspath('../runtime/pythonpythonjs.py'),  ## handwritten pythonjs
	runtime_builtins = os.path.abspath('../runtime/builtins.py'),
	runtime_dart = os.path.abspath('../runtime/dart_builtins.py'),

	dart2js = os.path.expanduser( '~/dart/dart-sdk/bin/dart2js'),
	dartanalyzer = os.path.expanduser( '~/dart/dart-sdk/bin/dartanalyzer'),

	closure = os.path.expanduser( '~/closure-compiler/compiler.jar'),

)

DART = '--dart' in sys.argv  ## force dart mode

def python_to_pythonjs( src, module=None, dart=False ):

	cmd = ['python2', os.path.join( PATHS['pythonjs'], 'python_to_pythonjs.py')]
	if dart:
		cmd.append( '--dart' )

		header = open( PATHS['runtime_dart'], 'rb' ).read().decode('utf-8')
		src = header + '\n' + src

	if module:
		cmd.append( '--module' )
		cmd.append( module )

	p = subprocess.Popen(
		cmd,
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( src.encode('utf-8') )
	return stdout.decode('utf-8')

def pythonjs_to_dart(src):
	if os.path.isfile('/tmp/dart2js-output.js'):
		os.unlink('/tmp/dart2js-output.js')
	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonjs'],'pythonjs_to_dart.py')],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	dart_input = '/tmp/dart2js-input.dart'
	stdout, stderr = p.communicate( src.encode('utf-8') )
	open( dart_input, 'wb').write( stdout )
	ecode = subprocess.call( [PATHS['dartanalyzer'], dart_input] )
	if ecode == 2:
		raise SyntaxError

	cmd = [
		PATHS['dart2js'],
		#'-c', ## insert runtime checks
		'-o', '/tmp/dart2js-output.js',
		dart_input
	]
	subprocess.call( cmd )
	return open('/tmp/dart2js-output.js', 'rb').read().decode('utf-8')

def pythonjs_to_javascript( src ):
	p = subprocess.Popen(
		['python2', os.path.join( PATHS['pythonjs'],'pythonjs.py')],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE
	)
	stdout, stderr = p.communicate( src.encode('utf-8') )
	a = stdout.decode('utf-8')


	if False and os.path.isfile( PATHS['closure'] ):
		x = '/tmp/closure-input.js'; y = '/tmp/closure-output.js';
		f = open(x, 'wb'); f.write( a.encode('utf-8') ); f.close()
		subprocess.call([
			'java', '-jar', PATHS['closure'], 
			#'--compilation_level', 'ADVANCED_OPTIMIZATIONS', 
			'--js', x, '--js_output_file', y,
			'--formatting', 'PRETTY_PRINT',
		])
		f = open(y, 'rb'); a = f.read().decode('utf-8'); f.close()

	return a

def python_to_javascript( src, module=None, dart=False, debug=False, dump=False ):
	a = python_to_pythonjs( src, module=module, dart=dart )
	if debug: print( a )
	if dump:
		if isinstance(dump, str):
			open(dump, 'wb').write( a.encode('utf-8') )
		else:
			open('/tmp/pythonjs.dump', 'wb').write( a.encode('utf-8') )
	if dart:
		return pythonjs_to_dart( a )
	else:
		return pythonjs_to_javascript( a )



#########################################################
def get_main_page():
	root = PATHS['webroot']
	r = ['<html><head><title>index</title></head><body>']
	r.append( '<ul>' )
	files = os.listdir( root )
	files.sort()
	for name in files:
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
		<script type="text/python" dart="true">
		print("hello world")
		</script>

	Note:
		we need to parse and compile any python binding scripts that appear in the head,
		because later scripts may use classes from the bindings, and we need have the 
		AST introspected data available here to properly inline and for operator overloading.
	'''
	doc = list()
	script = None
	use_dart = DART
	for line in data.splitlines():
		if line == 'source = $PYTHONJS':
			line = open('../pythonjs/python_to_pythonjs.py', 'rb').read().decode('utf-8')

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
				if 'dart="true"' in line.lower(): use_dart = True
				else: use_closure = False
				doc.append( '<script type="text/javascript">')
				#doc.append( '<script type="application/javascript;version=1.7">')  ## firefox needs this when using native yield
				script = list()
			else:
				doc.append( line )

		elif line.strip() == '</script>':
			if script:
				src = '\n'.join( script )
				js = python_to_javascript( src, debug=True, dart=use_dart )
				doc.append( js )
			doc.append( line )
			script = None

		elif isinstance( script, list ):
			script.append( line )

		else:
			doc.append( line )

	return '\n'.join( doc )


def regenerate_runtime():
	print('regenerating pythonjs runtime...')
	a = '// PythonJS Runtime - regenerated on: %s' %datetime.datetime.now().ctime()
	b = pythonjs_to_javascript(
		open(PATHS['runtime_pythonjs'],'rb').read().decode('utf-8'),
	)
	if not b.strip():
		raise RuntimeError
	c = python_to_javascript(
		open(PATHS['runtime_builtins'],'rb').read().decode('utf-8'),
		dump='/tmp/runtime-builtins.dump.py',
	)
	if not c.strip():
		raise RuntimeError

	src = '\n'.join( [a,b.strip(),c.strip()] )
	file = open( PATHS['runtime'], 'wb')
	file.write( src.encode('utf-8') )
	file.close()
	return src


UploadDirectory = '/tmp'
ResourcePaths = []
if os.path.isdir( os.path.expanduser('~/blockly-read-only') ):
	ResourcePaths.append( os.path.expanduser('~/blockly-read-only') )

class MainHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		print('path', path)
		if not path:
			self.write( get_main_page() )
		elif path == 'pythonscript.js' or path == 'pythonjs.js':
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
				data = python_to_javascript( data.decode('utf-8'), module=module )
				if '--dump-js' in sys.argv:
					f = open( os.path.join('/tmp',name+'.js'), 'wb' )
					f.write(data.encode('utf-8'))
					f.close()

			self.set_header("Content-Type", "text/javascript; charset=utf-8")
			self.set_header("Content-Length", len(data))
			self.write( data )

		elif path.startswith('uploads/'):
			name = path.split('/')[-1]
			local_path = os.path.join( UploadDirectory, name )

			if os.path.isfile( local_path ):
				data = open(local_path, 'rb').read()
			else:
				raise tornado.web.HTTPError(404)

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
					data = python_to_javascript( data.decode('utf-8') )
					self.set_header("Content-Type", "text/html; charset=utf-8")

				self.set_header("Content-Length", len(data))
				self.write( data )

			else:
				found = False
				for root in ResourcePaths:
					local_path = os.path.join( root, path )
					if os.path.isfile(local_path):
						data = open(local_path, 'rb').read()
						self.set_header("Content-Length", len(data))
						self.write( data )
						found = True
						break

				if not found:
					print( 'FILE NOT FOUND', path)


LIBS = dict(
	three = {
		'three.min.js' : os.path.expanduser( '~/three.js/build/three.min.js'),
		'FlyControls.js' : os.path.expanduser( '~/three.js/examples/js/controls/FlyControls.js'),
		'OrbitControls.js' : os.path.expanduser( '~/three.js/examples/js/controls/OrbitControls.js'),
		'TrackballControls.js' : os.path.expanduser( '~/three.js/examples/js/controls/TrackballControls.js'),

	},
	tween = {'tween.min.js' : os.path.expanduser( '~/tween.js/build/tween.min.js')},
	fonts = {
		'gentilis_bold.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/gentilis_bold.typeface.js'),
		'gentilis_regular.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/gentilis_regular.typeface.js'),
		'optimer_bold.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/optimer_bold.typeface.js'),
		'optimer_regular.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/optimer_regular.typeface.js'),
		'helvetiker_bold.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/helvetiker_bold.typeface.js'),
		'helvetiker_regular.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/helvetiker_regular.typeface.js'),
		'droid_sans_regular.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/droid/droid_sans_regular.typeface.js'),
		'droid_sans_bold.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/droid/droid_sans_bold.typeface.js'),
		'droid_serif_regular.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/droid/droid_serif_regular.typeface.js'),
		'droid_serif_bold.typeface.js' : os.path.expanduser( '~/three.js/examples/fonts/droid/droid_serif_bold.typeface.js'),
	},
	ace = {
		'ace.js': os.path.expanduser( '~/ace-builds/src-noconflict/ace.js'),
		'theme-monokai.js':os.path.expanduser( '~/ace-builds/src-noconflict/theme-monokai.js'),
		'mode-python.js':os.path.expanduser( '~/ace-builds/src-noconflict/mode-python.js'),
		'mode-javascript.js':os.path.expanduser( '~/ace-builds/src-noconflict/mode-javascript.js'),
		'worker-javascript.js':os.path.expanduser( '~/ace-builds/src-noconflict/worker-javascript.js'),
	},
	physijs = {
		'physi.js' : os.path.expanduser( '~/Physijs/physi.js'),
		'physijs_worker.js' : os.path.expanduser( '~/Physijs/physijs_worker.js'),
	},
	ammo = {
		'ammo.js' : os.path.expanduser( '~/Physijs/examples/js/ammo.js'),
	},
	pixi = {
		'pixi.js' : os.path.expanduser( '~/pixi.js/bin/pixi.js'),	
	},
	brython = {
		'py2js.js' : os.path.expanduser( '../brython/py2js.js'),	
	}

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


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print( self.request.connection )

	def on_message(self, msg):
		if hasattr(self.ws_connection, 'previous_command') and self.ws_connection.previous_command and self.ws_connection.previous_command.get('binary', False):
			if self.ws_connection.previous_command['command'] == 'upload':
				path = os.path.join(
					UploadDirectory, 
					self.ws_connection.previous_command['file_name']
				)
				f = open( path, 'wb' )
				f.write( msg )
				f.close()

			self.ws_connection.previous_command = None

		else:
			print('on json message', msg)

			ob = json.loads( msg )
			if isinstance(ob, dict):
				if 'command' in ob:
					if ob['command'] == 'compile':
						js = python_to_javascript( ob['code'] )
						self.write_message( {'eval':js})
					elif ob['command'] == 'upload':
						print('ready for upload...')
						print( ob['file_name'] )

					self.ws_connection.previous_command = ob

			else:
				self.write_message('"hello client"')

	def on_close(self):
		print('websocket closed')
		if self.ws_connection:
			self.close()


Handlers = [
	(r'/websocket', WebSocketHandler),
	(r'/libs/(.*)', LibsHandler),
	(r'/(.*)', MainHandler),  ## order is important, this comes last.
]


if __name__ == '__main__':
	assert os.path.isfile( PATHS['runtime'] )
	assert os.path.isdir( PATHS['pythonjs'] )
	assert os.path.isdir( PATHS['bindings'] )

	if '--regenerate-runtime' in sys.argv:
		data = regenerate_runtime()
		print(data)

	else:
		print('running server...')
		print('http://localhost:8080')
		app = tornado.web.Application(
			Handlers,
			#cookie_secret = 'some random text',
			#login_url = '/login',
			#xsrf_cookies = False,
		)
		app.listen( 8080 )
		tornado.ioloop.IOLoop.instance().start()

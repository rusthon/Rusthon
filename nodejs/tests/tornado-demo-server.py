from nodejs.io import *
from nodejs.os import *
from nodejs.tornado import *

#import os, sys, subprocess, json

PATHS = dict(
	webroot = os.path.abspath('tests'),
	pythonjs = os.path.abspath('pythonjs'),
	bindings = os.path.abspath('bindings'),
	runtime = os.path.abspath('pythonjs.js'),
)



def python_to_pythonjs( src, callback, module=None ):
	path = '/tmp/input1.py'
	open( path, 'w' ).write( src )
	args = [
		os.path.join( PATHS['pythonjs'], 'python_to_pythonjs.py'),
		path
	]
	p = subprocess.call('python2', args, callback=callback )

def pythonjs_to_javascript( src, callback ):
	path = '/tmp/input2.py'
	open( path, 'w' ).write( src )
	args = [
		os.path.join( PATHS['pythonjs'], 'pythonjs.py'),
		path
	]
	p = subprocess.call('python2', args, callback=callback )

def python_to_javascript(source, callback):
	func = lambda data: pythonjs_to_javascript(data, callback)
	python_to_pythonjs( source, func )



#########################################################
def get_main_page():
	print 'get_main_page......'
	root = PATHS['webroot']
	r = ['<html><head><title>index</title></head><body>']
	r.append( '<ul>' )
	files = os.listdir( root )
	files.sort()
	for name in files:
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
		<script type="text/python">
		print("hello world")
		</script>

	Note:
		we need to parse and compile any python binding scripts that appear in the head,
		because later scripts may use classes from the bindings, and we need have the 
		AST introspected data available here to properly inline and for operator overloading.
	'''
	doc = list()
	script = None

	for line in data.splitlines():
		if line.strip().startswith('<script'):
			if 'src="bindings/' in line:
				doc.append( line )

				a,b,c = line.split('"')  ## TODO unpack assign

				if b.endswith('.py'):  ## make sure the module is cached ##
					name = b.split('/')[-1]
					path = os.path.join( PATHS['bindings'], name )
					src = open(path, 'rb').read().decode('utf-8')
					pyjs = python_to_pythonjs( src, module=name.split('.')[0] )


			elif 'type="text/python"' in line:
				doc.append( '<script type="text/javascript">')
				script = list()
			else:
				doc.append( line )

		elif line.strip() == '</script>':
			if script:
				src = '\n'.join( script )
				js = python_to_javascript( src )
				doc.append( js )
			doc.append( line )
			script = None

		elif isinstance( script, list ):
			script.append( line )

		else:
			doc.append( line )

	return '\n'.join( doc )





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

				#############################################################
				data = python_to_javascript( data, module=module )


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
					data = convert_python_html_document( data )
					self.set_header("Content-Type", "text/html; charset=utf-8")

				elif path.endswith('.py'):
					data = python_to_javascript( data )
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
					print( 'FILE NOT FOUND' )
					self.finish()


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

	def on_message(self, msg, flags=None):
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
	('/websocket', WebSocketHandler),
	('/libs/', LibsHandler),
	('/', MainHandler)
]



app = tornado.web.Application( Handlers )
app.listen( 8080 )
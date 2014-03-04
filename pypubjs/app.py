# PythonJS Integrated Development Environment "pypubjs"
# by Brett Hartshorn - copyright 2014
# License: "New BSD"

nw_gui = require('nw.gui')
Reader = new( FileReader() )
Editors = {}
Images = []

css_editor = ace.edit( 'EDITOR_CSS' )
css_editor.setTheme("ace/theme/monokai")
css_editor.getSession().setMode("ace/mode/css")
css_editor.setValue( 'body {\n  background-color:lightgray;\n}\n' )

js_body_editor = ace.edit( 'EDITOR_BODY_JS' )
js_body_editor.setTheme("ace/theme/monokai")
js_body_editor.getSession().setMode("ace/mode/javascript")
js_body_editor.setValue( 'console.log("hello world")' )

js_head_editor = ace.edit( 'EDITOR_HEAD_JS' )
js_head_editor.setTheme("ace/theme/monokai")
js_head_editor.getSession().setMode("ace/mode/javascript")
js_head_editor.setValue( '' )

_pycode_ = """
demo = None
world = None

def create_blob(N=10, M=10, k=1000, d=10, l=0.35, m=1):
	bodies = []

	#// Create particle bodies
	particleShape = new(p2.Particle())
	for i in range(N):
		bodies.push([])
		for j in range(M):
			p = new(p2.Body(
				mass=m,
				position=[(i-N/2)*l*1.05, (j-M/2)*l*1.05]
			))
			p.addShape(particleShape)
			bodies[i].push(p)
			world.addBody(p)

	#// Vertical springs
	for i in range(N):
		for j in range(M-1):
			bodyA = bodies[i][j];
			bodyB = bodies[i][j+1];
			spring = new(p2.Spring(
				bodyA,bodyB,
				stiffness=k,
				restLength=l,
				damping=d
			))
			world.addSpring(spring)

	#// Horizontal springs
	for i in range(N-1):
		for j in range(M):
			bodyA = bodies[i][j];
			bodyB = bodies[i+1][j];
			spring = new( p2.Spring(
				bodyA,bodyB,
				stiffness=k,
				restLength=l,
				damping=d
			))
			world.addSpring(spring)

	#// Diagonal right/down springs
	for i in range(N-1):
		for j in range(M-1):
			a = bodies[i][j]
			b = bodies[i+1][j+1]
			spring = new(p2.Spring(
				a,b,
				stiffness=k,
				restLength=Math.sqrt(l*l + l*l)
			))
			world.addSpring(spring)

	#// Diagonal left/down springs
	for i in range(N-1):
		for j in range(M-1):
			a = bodies[i+1][j]
			b = bodies[i][j+1]
			spring = new(p2.Spring(
				a,b,
				stiffness=k,
				restLength=Math.sqrt(l*l + l*l)
			))
			world.addSpring(spring)


def main():
	global demo, world
	bp = new( p2.SAPBroadphase() )

	world = new(
		p2.World(
			doProfiling=True,
			gravity = [0, -10],
			broadphase = bp
		)
	)

	create_blob( N=5, M=5 )


	planeShape = new( p2.Plane() )
	plane = new( p2.Body(position=[0,-2]) )
	plane.addShape( planeShape )
	world.addBody( plane )

	concaveBody = new(
		p2.Body( mass=1, position=[0,2] )
	)
	path = [
		[-1, 1],
		[-1, 0],
		[1, 0],
		[1, 1],
		[0.5, 0.5]
	]
	concaveBody.fromPolygon(path)
	world.addBody(concaveBody)

	demo = new(PixiDemo(world))
	demo.setState(Demo.DRAWPOLYGON)

	def on_add_body(evt):
		evt.body.setDensity(1)

	world.on("addBody",on_add_body)

"""

py_body_editor = ace.edit( 'EDITOR_BODY_PY' )
py_body_editor.setTheme("ace/theme/monokai")
py_body_editor.getSession().setMode("ace/mode/python")
py_body_editor.setValue( _pycode_ )

py_head_editor = ace.edit( 'EDITOR_HEAD_PY' )
py_head_editor.setTheme("ace/theme/monokai")
py_head_editor.getSession().setMode("ace/mode/python")
py_head_editor.setValue( '' )


_html_ = """
<div class="navbar">
	<button class="btn btn-inverse" onclick="javascript:main()">run</button>
	<button class="btn btn-warning" onclick="javascript:demo.setState(Demo.DEFAULT)">move</button>
	<button class="btn" onclick="javascript:demo.setState(Demo.DRAWPOLYGON)">draw shape</button>
	<button class="btn btn-info" onclick="javascript:demo.setState(Demo.DRAWCIRCLE)">draw circle</button>
</div>

<div class="well" id="demo_container"></div>

"""

html_editor = ace.edit( 'EDITOR_HTML' )
html_editor.setTheme("ace/theme/monokai")
html_editor.getSession().setMode("ace/mode/html")
html_editor.setValue( _html_ )

## setup default imports ##
def _make_list_item( url, ul, manager ):
	li = document.createElement('li')
	ul.appendChild( li )
	manager.append( url )
	li.setAttribute('class', 'well')

	edit = document.createElement('button')
	edit.setAttribute('class', 'btn btn-mini btn-success')
	edit.appendChild( document.createTextNode('edit') )
	def func():
		print('opening', url)
		open_editor_window( url, open(os.path.join('pypubjs',url), 'r').read() )

	edit.addEventListener('click', func)

	li.appendChild( edit )

	rem = document.createElement('button')
	rem.setAttribute('class', 'btn btn-mini btn-danger')
	rem.appendChild( document.createTextNode('remove') )
	def func():
		print('removing:', url)
		li.style.display = 'none'
		manager.remove(url)

	rem.addEventListener('click', func)
	li.appendChild( rem )

	input = document.createElement('input')
	input.setAttribute('type', 'text')
	input.setAttribute('class', 'input-medium span5 pull-right')
	input.setAttribute('placeholder', url)
	li.appendChild( input )


CssImports = []
def add_css_import( url ):
	ul = document.getElementById('IMPORTS_CSS')
	_make_list_item( url, ul, CssImports )

for url in ['../external/css/bootstrap.css', '../external/css/darkstrap.css']:
	add_css_import( url )

JsImports = []
def add_js_import( url ):
	ul = document.getElementById('IMPORTS_JS')
	_make_list_item( url, ul, JsImports )

_DEFAULT_EXTERN_JS = [
	'../pythonjs.js', 
	'../external/jquery/jquery-latest.js', 
	'../external/bootstrap/bootstrap.min.js',
	'../external/p2.js/p2.min.js',
	'../external/p2.js/p2.extras.js',
	'../external/pixi.js/pixi.dev.js',
	'../external/p2.js/Demo.js',
	'../external/p2.js/PixiDemo.js',
]
for url in _DEFAULT_EXTERN_JS:
	add_js_import( url )

#################### app compiler #####################
win = None
def preview_app():
	global win
	if win is None:
		win = nw_gui.Window.open(
			'',
			width=480,
			height=350,
			toolbar=False,
			frame=True
		)
		win.on(
			'loaded', 
			lambda : compile_app( preview=True, css_imports=CssImports, js_imports=JsImports )
		)

	else:
		#win.window.document.documentElement.innerHTML=""  ## broken?
		win.window.document.body.innerHTML=""
		compile_app( preview=True, css_imports=CssImports, js_imports=JsImports )

def export_phonegap():
	project_name = 'testing'
	tmpdir = tempfile.gettempdir()
	args = ['create', project_name, '--name', project_name, '--id', 'com.example.hello']

	def callback1( stdout ):
		print('-------phonegap project created---------')
		print(stdout)

		rootdir = os.path.join( tmpdir, project_name )
		wwwdir = os.path.join( rootdir, 'www')
		jsdir = os.path.join( wwwdir, 'js' )
		cssdir = os.path.join( wwwdir, 'css' )
		imgdir = os.path.join( wwwdir, 'img')

		js_imports = ['phonegap.js']
		for path in JsImports:
			filename = os.path.split(path)[-1]
			data = open( os.path.join('pypubjs', path), 'r' ).read()
			open( os.path.join(jsdir, filename), 'w').write( data )
			js_imports.append( 'js/'+filename )

		css_imports = []
		for path in CssImports:
			filename = os.path.split(path)[-1]
			data = open( os.path.join('pypubjs', path), 'r' ).read()
			open( os.path.join(cssdir, filename), 'w').write( data )
			css_imports.append( 'css/'+filename )

		for path in Images:
			filename = os.path.split(path)[-1]
			data = open( path, 'rb' ).read()
			open( os.path.join(imgdir, filename), 'wb').write( data )

		def callback2( html ):
			print('-----------saving phonegap html------------')

			for path in Images:
				filename = os.path.basename(path)
				html = html.replace(path, 'img/'+filename)

			open( os.path.join(wwwdir, 'index.html'), 'w').write( html )

			def callback3( stdout ):
				print('-----------phonegap project built------------')
				print(stdout)
				#apk = open( 'platforms/android/bin/%s-debug.apk' %project_name, 'rb' ).read()
				subprocess.call( 'phonegap', ['install', 'android', '--emulator'], cwd=rootdir )

			subprocess.call(
				'phonegap', 
				['local', 'build', 'android'], 
				cwd=rootdir, 
				stdout=subprocess.PIPE, 
				callback=callback3
			)

		compile_app( preview=False, css_imports=css_imports, js_imports=js_imports, callback=callback2 )

	subprocess.call( 'phonegap', args, cwd=tmpdir, stdout=subprocess.PIPE, callback=callback1 )




def compile_app( preview=False, css_imports=None, js_imports=None, callback=None ):

	if preview:
		dev = win.showDevTools()
		dev.resizeTo( win.width, 130)
		dev.moveTo( win.x, win.y + win.height + 20 )

	out = ['<html><head>']

	if css_imports:
		for url in css_imports:
			out.append('<link rel="stylesheet" href="%s"/>' %url)

	out.append('<style type="text/css">')
	out.append( css_editor.getValue() )
	out.append('</style>')

	if js_imports:
		for url in js_imports:
			out.append( '<script type="text/javascript" src="%s"></script>'%url )
	
	out.append('<script type="text/javascript">')
	out.append( js_head_editor.getValue() )
	out.append('</script>')

	def _callback1(js):
		out.append('<script type="text/javascript">')
		out.append( js )
		out.append('</script>')
		out.append('</head>')

		out.append('<body>')
		out.append( html_editor.getValue() )

		## post init scripts ##
		out.append('<script type="text/javascript">')
		out.append( js_body_editor.getValue() )
		out.append('</script>')

		def _callback2(js):
			out.append('<script type="text/javascript">')
			out.append( js )
			out.append('</script>')
			out.append('</body></html>')
			data = '\n'.join(out)
			if preview:
				win.window.document.write( data )

			if callback:
				callback( data )

		translate( {'data':py_body_editor.getValue(),'callback': _callback2} )

	translate( {'data':py_head_editor.getValue(),'callback': _callback1} )



def open_editor_window( filename, data ):
	win = nw_gui.Window.open(
		'editor.html',
		title=filename,
		width=700,
		height=550,
		toolbar=False,
		frame=True
	)
	def loaded():
		win.window.editor.setValue(data)
	win.on('loaded', loaded)
	Editors[ filename ] = win

viswin = None
def vis_python():
	print('vis_python..............')
	global viswin

	def loaded():
		def callback(code):
			viswin.window.document.body.innerHTML = ""
			out = [
				'<html><head>',
				'<script src="../external/vis.js/vis.min.js"></script>',
				'<body>'
			]
			out.append( code )
			out.append('</body></html>')
			data = '\n'.join(out)
			print(data)
			viswin.window.document.write( data )

		translate( {'data':py_body_editor.getValue(),'callback': callback, 'vis':True} )

	if viswin is None:
		viswin = nw_gui.Window.open(
			'_blank',
			title='code graph',
			width=500,
			height=600,
			toolbar=False,
			frame=True
		)
		viswin.on('loaded', loaded)
	else:
		loaded()


def allow_drop(e):
	e.preventDefault()

def on_drop(e):
	print 'on-drop', e
	e.preventDefault()
	#url = e.dataTransfer.getData("text/uri-list")
	#url = e.dataTransfer.getData("text/plain")
	if e.dataTransfer.files.length:
		file = e.dataTransfer.files[0]
		print file.path

		if file.path.endswith('.css'):
			add_css_import( file.path )
		elif file.path.endswith('.js'):
			add_js_import( file.path )
		elif file.path.endswith('.jpg') or file.path.endswith('.png'):
			if file.path in Images:
				pass
			else:
				ul = document.getElementById('IMAGES')
				li = ul.getElementsByTagName('li')[-1]
				img = document.createElement('img')
				img.setAttribute('src', file.path)
				img.setAttribute('class', 'well img-rounded')
				img.setAttribute('width', '25%')
				li.appendChild( img )

				txt = html_editor.getValue()
				html_editor.setValue(txt+'\n<img src="%s"/>'%file.path)
				Images.append( file.path )

				img = document.createElement('img')
				img.setAttribute('src', file.path)
				img.setAttribute('class', 'img-rounded')
				img.setAttribute('width', '64px')
				div = document.getElementById('PIXI_SPRITES')
				div.appendChild( img )


		elif file.path.endswith('.mp4'):
			ul = document.getElementById('VIDEOS')
			li = ul.getElementsByTagName('li')[-1]
			video = document.createElement('video')
			video.setAttribute('width', '320')
			video.setAttribute('height', '240')
			video.setAttribute('controls', 'true')
			source = document.createElement('source')
			source.setAttribute('src', file.path)
			source.setAttribute('type', 'video/mp4')
			video.appendChild( source )
			li.appendChild( video )

		elif file.path.endswith('.mp3'):
			ul = document.getElementById('AUDIO')
			li = ul.getElementsByTagName('li')[-1]
			audio = document.createElement('audio')
			audio.setAttribute('autoplay', 'autoplay')
			audio.setAttribute('src', file.path)
			audio.setAttribute('controls', 'controls')
			source = document.createElement('source')
			source.setAttribute('src', file.path)
			source.setAttribute('type', 'audio/mpeg')
			audio.appendChild( source )
			li.appendChild( audio )

		elif file.path.endswith('.py'):
			def on_load(event):
				contents = event.target.result
				py_body_editor.setValue( contents )

			Reader.onload = on_load
			Reader.readAsText( file )



worker = new( Worker('../pythonjs/empythoned-webworker.js') )
def empythoned_output( output ):
	document.getElementById('EMPYTHONED_OUTPUT').value += output.data

def empythoned_eval( code ):
	worker.postMessage( code )
worker.addEventListener('message', empythoned_output)

def update_empythoned_console( input ):
	document.getElementById('EMPYTHONED_OUTPUT').value += '\n>>>' + input.value + '\n'
	empythoned_eval(input.value+'\n')
	input.value=''

############################################################


with javascript:
	def on_drag( data ):
		if this.dragging:

			if this.data.originalEvent.button == 0:
				newPosition = this.data.getLocalPosition(this.parent)
				this.position.x = newPosition.x
				this.position.y = newPosition.y

			else:
				dx = data['global'].x - this.drag_start_x
				dy = data['global'].y - this.drag_start_y
				dx *= 0.005
				dy *= 0.005
				dx += this.drag_scale_x
				dy += this.drag_scale_y
				this.scale.x = dx
				this.scale.y = dx

	def on_pressed( data ):
		print 'on-pressed'
		this.dragging = True
		this.data = data
		e = data.originalEvent
		e.preventDefault()
		e.stopPropagation()
		this.drag_start_x = data['global'].x
		this.drag_start_y = data['global'].y
		this.drag_scale_x = this.scale.x
		this.drag_scale_y = this.scale.y


	def on_released( data ):
		print 'on-released'
		this.dragging = False
		this.data = null
		e = data.originalEvent
		e.preventDefault()


def create_sprite( url ):
	tex = PIXI.Texture.fromImage( url )
	sprite = new( PIXI.Sprite(tex) )
	sprite.anchor.x = 0.5
	sprite.anchor.y = 0.5
	sprite.position.x = 200
	sprite.position.y = 150

	sprite.interactive = True
	sprite.button = True
	sprite.mousemove = on_drag
	sprite.mousedown = on_pressed
	sprite.mouseup   = on_released

	stage.addChild( sprite )

def on_drop_pixi(e):
	e.preventDefault()
	#e.stopPropagation(True)
	if e.dataTransfer.files.length:
		file = e.dataTransfer.files[0]
		create_sprite( file.path )

pixi_renderer = new( PIXI.WebGLRenderer(600,480, None, False, True) )

document.getElementById('PIXI_WORKSPACE').appendChild(pixi_renderer.view);
stage = new( PIXI.Stage(0,True) )


def animate():
	requestAnimationFrame( animate )
	pixi_renderer.render(stage)

animate()

print('app ready')
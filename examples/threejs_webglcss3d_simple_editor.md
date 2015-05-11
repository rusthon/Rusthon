Tornado Server
-------------

for local testing run:
```
./rusthon.py ./examples/threejs_webglcss3d_simple_editor.md --run=myserver.py
```

@myserver.py
```python
#!/usr/bin/python

PORT = int(os.environ.get("PORT", 8000))

## inlines rusthon into script ##
from rusthon import *
import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import os, sys, subprocess, datetime, json, time, mimetypes


class MainHandler( tornado.web.RequestHandler ):

	def get(self, path=None):
		print('path', path)
		guess = path
		if not path or path == '/': guess = 'index.html'
		mime_type, encoding = mimetypes.guess_type(guess)
		if mime_type: self.set_header("Content-Type", mime_type)

		if path == 'favicon.ico' or path.endswith('.map'):
			self.write('')
		elif path and '.' in path:
			self.write( open(path).read() )
		else:
			self.write( open('index.html').read() )


class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print( 'websocket open' )
		print( self.request.connection )

	def on_message(self, msg):
		print 'got %s bytes' %len(msg)

		ob = json.loads( msg )
		## if a simple test string ##
		if isinstance(ob, str):
			self.write_message('hello client')
		## otherwise a object
		elif isinstance(ob, dict):
			print 'got object from client'
			if 'translate' in ob:
				code = ob['code']
				if ob['translate'] == 'python to javascript':
					js = rusthon.translate( code, mode='javascript' )
					reply = {'type':'javascript', 'data':js, 'id':ob['id']}
					self.write_message(json.dumps(reply))

				elif ob['translate'] == 'python to c++':
					js = rusthon.translate( code, mode='c++' )
					reply = {'type':'c++', 'data':js, 'id':ob['id']}
					self.write_message(json.dumps(reply))

				print code


	def on_close(self):
		print('websocket closed')
		if self.ws_connection:
			self.close()



## Tornado Handlers ##
Handlers = [
	(r'/websocket', WebSocketHandler),
	(r'/(.*)', MainHandler),  ## order is important, this comes last.
]

## main ##
def main():
	print('<starting tornado server>')
	app = tornado.web.Application(
		Handlers,
		#cookie_secret = 'some random text',
		#login_url = '/login',
		#xsrf_cookies = False,
	)
	app.listen( PORT )
	tornado.ioloop.IOLoop.instance().start()

## start main ##
main()

```

Three.js App
-----------

Below is translated to javascript and inserted into the html at the bottom.

note: most of the code is in [dddom.py](https://github.com/rusthon/Rusthon/blob/master/examples/dddom.py)

@myapp
```rusthon
#backend:javascript
from runtime import *
from random import random
from dddom import *

camera = scene = renderer = None
geometry = material = mesh = None
renderer2 = renderer3 = None
controls = gizmo = composer = None
Elements = []

TUTORIALS = [
	'print "hi"',
	'self.window.rotation.x += 0.1',
	"self.container.appendChild(document.createTextNode('hi'))",
	'self.window.collada.scale.x *= 0.88',
	'window.alert("hi")',
]

ws = None

def on_open_ws():
	print 'websocket open'
	#ws.send(JSON.stringify('hello server'))

def on_close_ws():
	print 'websocket close'

def on_message_ws(event):
	print 'on message', event

	if instanceof(event.data, ArrayBuffer):
		print 'got binary bytes', event.data.byteLength
		arr = new(Uint8Array(event.data))
		txt = String.fromCharCode.apply(None, arr)
		print txt
	else:
		now = new(Date())
		if event.data[0] == '{':
			print 'got json data'
			msg = JSON.parse(event.data)
			ta = document.getElementById( msg.id )
			while ta.firstChild:
				ta.removeChild( ta.firstChild )
			ta.appendChild(document.createTextNode(msg.data))

			if msg.type=='javascript':
				print msg.data
				eval( msg.data )

		else:
			print 'got unknown data'

def connect_ws():
	global ws
	print location.host
	addr = 'ws://' + location.host + '/websocket'
	print 'websocket test connecting to:', addr
	ws = new( WebSocket(addr) )
	ws.binaryType = 'arraybuffer'
	ws.onmessage = on_message_ws
	ws.onopen = on_open_ws
	ws.onclose = on_close_ws
	print ws


def init():
	print 'init...'
	global camera, scene, scene3, renderer, renderer2, renderer3
	global geometry, material, mesh
	global controls, gizmo, composer

	SCREEN_WIDTH = window.innerWidth
	SCREEN_HEIGHT = window.innerHeight

	camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 10000 );
	camera.position.set( 200, 150, 800 );
	selectman = SelectManager( camera )

	controls = new THREE.TrackballControls( camera );
	camera.smooth_target = controls.target.clone()

	controls.rotateSpeed = 1.0;
	controls.zoomSpeed = 1.2;
	controls.panSpeed = 0.8;

	controls.noZoom = false;
	controls.noPan = false;

	controls.staticMoving = false;
	controls.dynamicDampingFactor = 0.3;

	controls.keys = [ 65, 83, 68 ];

	scene = new THREE.Scene();
	scene3 = new THREE.Scene();


	geometry = new THREE.BoxGeometry( 800, 400, 3800 );
	material = new THREE.MeshPhongMaterial( color=0xc1c1c1, transparent=true, opacity=0.27 );
	mesh = new THREE.Mesh( geometry, material );
	mesh.position.z = -400
	mesh.position.y = -220
	scene.add( mesh );
	mesh.receiveShadow = true;

	renderer = new THREE.WebGLRenderer(alpha=True, antialiasing=True);
	renderer.shadowMapEnabled = true
	renderer.shadowMapType = THREE.PCFSoftShadowMap
	renderer.shadowMapSoft = true
	print renderer

	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.domElement.style.position = 'absolute'
	renderer.domElement.style.top = 0
	renderer.domElement.style.zIndex = 10
	renderer.domElement.style.pointerEvents = 'none'

	gizmo = new THREE.TransformControls( camera, renderer.domElement )
	scene.add( gizmo )

	light = new(
		THREE.SpotLight( 0xffffff, 1, 0, Math.PI / 2, 1 )
	)
	light.position.set( 0, 1400, 100 )
	light.target.position.set( 0, 0, 0 )

	light.castShadow = True
	light.shadowCameraNear = 400
	light.shadowCameraFar = 1900
	light.shadowCameraFov = 64
	light.shadowCameraVisible = True
	light.shadowBias = 0.0001
	light.shadowDarkness = 0.4
	light.shadowMapWidth = 512
	light.shadowMapHeight = 512
	scene.add( light )

	global pointlight
	pointlight = new( THREE.PointLight(0xffffff, 0.75, 1500) )
	pointlight.position.set( 10, 100, 300 )
	scene.add( pointlight )


	renderer.sortObjects = false
	renderer.autoClear = false
	print 'setup rendertarget'
	renderTarget = new(
		THREE.WebGLRenderTarget(
			SCREEN_WIDTH, 
			SCREEN_HEIGHT, 
			minFilter = THREE.LinearFilter, 
			magFilter = THREE.LinearFilter, 
			format = THREE.RGBAFormat,  ## RGBA format is required to composite over css3d render
			stencilBuffer = false
		)
	)
	print renderTarget


	hblur = new(THREE.ShaderPass( THREE.HorizontalTiltShiftShader ))
	vblur = new(THREE.ShaderPass( THREE.VerticalTiltShiftShader ))

	bluriness = 1.5;
	hblur.uniforms[ 'h' ].value = bluriness / SCREEN_WIDTH
	vblur.uniforms[ 'v' ].value = bluriness / SCREEN_HEIGHT

	hblur.uniforms[ 'r' ].value = 0.1
	vblur.uniforms[ 'r' ].value = 0.1

	## broken with rgba ##
	#effectFXAA = new THREE.ShaderPass( THREE.FXAAShader )
	#effectFXAA.uniforms[ 'resolution' ].value.set( 1.0 / SCREEN_WIDTH, 1.0 / SCREEN_HEIGHT )

	effectBloom = new(THREE.BloomPass( 0.45 ))
	effectCopy = new(THREE.ShaderPass( THREE.CopyShader ))

	print 'setup composer'
	composer = new(THREE.EffectComposer( renderer, renderTarget ))

	renderModel = new(THREE.RenderPass( scene, camera ))

	#vblur.renderToScreen = true;
	composer.addPass( renderModel )
	#composer.addPass( effectFXAA )
	composer.addPass( hblur )
	composer.addPass( vblur )

	composer.addPass( effectBloom )
	effectCopy.renderToScreen = True
	composer.addPass( effectCopy )


	test_options = ['javascript', 'python to javascript', 'python to c++']

	def onclick():
		this.firstChild.nodeValue='run script'
		this.setAttribute('class', 'btn btn-warning btn-small')
		this.parentNode.appendChild(document.createTextNode(' mode:'))
		modedd = this.element3D.create_select_dropdown(test_options)
		this.parentNode.appendChild( modedd )

		this.parentNode.appendChild( document.createTextNode('mycheckbox:') )
		this.parentNode.appendChild( create_checkbox(true) )

		this.parentNode.appendChild(document.createElement('br'))

		con = document.createElement('div')
		this.parentNode.appendChild(con)
		ta = create_textarea()
		con.appendChild( ta )
		if TUTORIALS.length:
			ta.appendChild(document.createTextNode(TUTORIALS.pop()))

		#pointlight.position.copy( this.element3D.object.position )
		#pointlight.position.z += 40
		gizmo.attach( this.element3D.right_bar )
		camera.smooth_target.copy( this.element3D.object.position )
		camera.smooth_target.y = 400
		this.element3D.active=True


		def ondrop(evt):
			print(evt)
			evt.preventDefault()
			if evt.dataTransfer.files.length==0:
				url = evt.dataTransfer.getData("text/plain")
				iframe = this.element3D.create_iframe( url, renderer3.domElement )
				container.appendChild(iframe)
			else:
				handle_drop_event(evt.dataTransfer.files, this.parentNode, this.element3D)

		this.parentNode.ondrop = ondrop.bind(this)
		this.parentNode.ondragover = lambda evt: evt.preventDefault()

		## helper variables for eval ##
		self = {
			'container':con,
			'window': this.element3D
		}
		def click2(evt):
			m = modedd.options[modedd.selectedIndex].value
			if m == 'javascript':
				eval( ta.value )
			else:
				if this._output_ta is None:
					this._output_ta = create_textarea()
					con.appendChild( this._output_ta )
				msg = {
					'translate' : m,
					'code': ta.value,
					'id'  : this._output_ta.getAttribute('id')
				}
				ws.send(JSON.stringify(msg))

		this._output_ta = None
		this.onclick = click2.bind(this)


	for i in range(10):

		var element = document.createElement( 'div' );
		element.setAttribute('class', 'well')
		b = document.createElement('button')
		b.appendChild(document.createTextNode('click me'))
		b.setAttribute('class', 'btn btn-inverse btn-small')
		b.onclick = onclick
		element.appendChild(b)

		x = Math.random() * 800 - 200;
		y = Math.random() * 200 + 100;
		z = Math.random() * 1800 - 1000;

		## the Window3D instance is set as this.element3D ##
		e = Window3D( element, scene, scene3, [x,y,z], [1,1,1] )
		b.element3D = e
		Elements.append( e )


	print 'setup css3d renderer'

	renderer3 = new THREE.CSS3DRenderer();
	renderer3.setSize( window.innerWidth, window.innerHeight );
	renderer3.domElement.style.position = 'absolute';
	renderer3.domElement.style.top = 0;
	#renderer3.domElement.style.opacity = 0.5;
	renderer3.domElement.style.zIndex=0;

	document.body.appendChild( renderer.domElement );
	document.body.appendChild( renderer3.domElement );

	print 'init done.'
	try:
		connect_ws()
	except:
		print 'connect to websocket failed'

	animate()


def handle_drop_event(files, container, element3D):
	for file in files:
		## note: `file.path` is only available in NodeWebkit,
		## for simple testing we will fake it here.
		file.path = file.name

		if file.path.endswith('.dae'):
			loader = new THREE.ColladaLoader();
			loader.options.convertUpAxis = true;
	
			def onload(evt):
				parser = new DOMParser()
				collada = loader.parse(
					parser.parseFromString(evt.target.result, "application/xml") 
				)
				print(collada)
				collada.scene.scale.set(0.25, 0.25, 0.25)
				collada.scene.position.set(0, -100, 200)
				element3D.root.add( collada.scene )
				element3D.collada = collada.scene

				menu = element3D.create_tab_menu()
				container.appendChild( menu.root )

				for i,model in enumerate(collada.skins):
					page = menu.add_tab( model.name )
					div = document.createElement('div')
					div.setAttribute('class', 'well')
					page.appendChild( div )
					
					if hasattr(model, 'material'): ## could be THREE.Mesh or THREE.SkinnedMesh
						print(model.material)
						ui = gen_material_ui(model)
						div.appendChild( ui )
					else:
						print 'model missing material'

			reader = new FileReader()
			reader.onload = onload
			reader.readAsText( file )

		else:
			window.alert('can only load collada files')



def gen_material_ui(model):
	print('gen material ui')
	def onchange(val):
		model.material.opacity = val
	slider = create_slider( model.material.opacity, onchange=onchange, name='opacity' )
	return slider

def animate():
	requestAnimationFrame( animate )

	gizmo.update()

	d = camera.smooth_target.clone()
	d.sub(controls.target)
	controls.target.add( d.multiplyScalar(0.03) )
	controls.update()
	pointlight.position.copy( controls.target )
	pointlight.position.z += 140
	pointlight.position.x += 40

	for e in Elements:
		#e.object.rotation.z += 0.001
		e.update()


	renderer.clear()
	composer.render( scene, camera )

	renderer3.render( scene3, camera )


init()


```

HTML
-----

@index.html
```html
<html>
	<head>
		<meta charset="utf-8">


<link href='~/bootstrap-3.3.4-dist/css/bootstrap.css' rel='stylesheet' />

<style>
	body {
		background: rgb(223,225,228); /* Old browsers */
		margin: 0;
		font-family: Arial;
		overflow: hidden;

	}

    .pp-slider { width: 150px; float:left;  -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -o-user-select: none; user-select: none; height: 30px; }
    .pp-slider .pp-slider-scale { background-color: #aaa; height: 10px; border-bottom: 1px solid #efefef; width: 120px; margin-top: 6px; float: left; }
    .pp-slider .pp-slider-scale .pp-slider-button { width: 12px; border-radius: 4px; border: 3px solid #adadad; height: 26px; position: relative; top: -7px; left: 0px; background-color: #efefef; cursor: pointer; }
    .pp-slider .pp-slider-scale .pp-slider-button .pp-slider-divies { border-left: 1px solid #adadad; border-right: 1px solid #adadad; position: relative; left: 3px; top: 3px; width: 4px; height: 10px; }
    .pp-slider .pp-slider-scale .pp-slider-button:hover { border-color: #777; background-color: #eee;  }
    .pp-slider .pp-slider-scale .pp-slider-tooltip { width: 24px; height: 20px; position: relative; top: -5px; left: 0px; text-align: center; font-size: 10px; color: #aaa; }
    .pp-slider .pp-slider-min { float: left; width: 15px; color: #aaa; font-size: 10px; }
    .pp-slider .pp-slider-max { float: left; width: 15px; color: #aaa; font-size: 10px; text-align: right; }
</style>

<script src="~/jquery/jquery-2.1.3.min.js"></script>
<script src="~/bootstrap-3.3.4-dist/js/bootstrap.min.js"></script>

	</head>
	<body>
		<script src="~/three.js/build/three.min.js"></script>

		<script src="~/three.js/examples/js/controls/TrackballControls.js"></script>
		<script src="~/three.js/examples/js/controls/TransformControls.js"></script>

		<script src="~/three.js/examples/js/renderers/CSS3DRenderer.js"></script>

		<script src="~/three.js/examples/js/postprocessing/RenderPass.js"></script>
		<script src="~/three.js/examples/js/postprocessing/ShaderPass.js"></script>
		<script src="~/three.js/examples/js/postprocessing/EffectComposer.js"></script>


		<script src="~/three.js/examples/js/postprocessing/BloomPass.js"></script>
		<script src="~/three.js/examples/js/postprocessing/ShaderPass.js"></script>
		<script src="~/three.js/examples/js/postprocessing/MaskPass.js"></script>
		<script src="~/three.js/examples/js/postprocessing/SavePass.js"></script>

		<script src="~/three.js/examples/js/shaders/ConvolutionShader.js"></script>
		<script src="~/three.js/examples/js/shaders/CopyShader.js"></script>
		<script src="~/three.js/examples/js/shaders/FXAAShader.js"></script>
		<script src="~/three.js/examples/js/shaders/HorizontalTiltShiftShader.js"></script>
		<script src="~/three.js/examples/js/shaders/VerticalTiltShiftShader.js"></script>
		<script src="~/three.js/examples/js/shaders/VignetteShader.js"></script>
		<script src="~/three.js/examples/js/shaders/EdgeShader2.js"></script>

		<script src="~/three.js/examples/js/loaders/ColladaLoader.js"></script>


<@myapp>

<div style="position:absolute">
	<h3><a href="http://rusthon.github.io/Rusthon/">created with Rusthon</a></h3>
	<h4><a href="http://threejs.org/">and THREE.js</a></h4>
	<h5><a href="https://github.com/rusthon/Rusthon/blob/master/examples/threejs_webglcss3d_simple_editor.md">source code</a>
	</h5>
</div>

</body>
</html>
```
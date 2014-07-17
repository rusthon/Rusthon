# Three.js HTML UI Generator
# by Brett Hartshorn - copyright 2014
# You may destribute this file using the "New BSD" or MIT license

pythonjs.configure(javascript=True)
from dddom import *  ## provides Window3D and SelectManager


class Editor( Window3D ):
	def __init__(self, engine, position=None):
		element = document.createElement( 'div' )
		Window3D.__init__(self, element, engine.scene, engine.scene2, engine.scene3, position, [1,1,1] )
		element.setAttribute('class', 'well')
		self.engine = engine

		b = document.createElement('button')
		b.appendChild(document.createTextNode('run script'))
		b.setAttribute('class', 'btn btn-inverse btn-small')
		element.appendChild(b)

		opts = ['javascript', 'python']
		element.appendChild(document.createTextNode(' mode:'))
		element.appendChild( self.create_select_dropdown(opts) )

		element.appendChild(document.createElement('br'))

		con = document.createElement('div')
		element.appendChild(con)
		ta = create_textarea()
		con.appendChild( ta )

		def ondrop(evt):
			print(evt)
			evt.preventDefault()
			if evt.dataTransfer.files.length==0:
				url = evt.dataTransfer.getData("text/plain")
				self.open_iframe(url)
			else:
				self.handle_drop_event(evt.dataTransfer.files)

		element.ondrop = ondrop.bind( self )
		element.ondragover = lambda evt: evt.preventDefault()


		def onclick(evt):
			eval( ta.value )
		b.onclick = onclick.bind(self)

	def open_iframe(self, url):
		iframe = self.create_iframe( url, self.engine.renderer3.domElement )
		self.element.appendChild(iframe)

	def _gen_material_ui(self, model):
		print(model.material)
		div = document.createElement('div')

		## Material.js
		faceopts = ['FrontSide', 'BackSide', 'DoubleSide']
		div.appendChild(document.createTextNode(' face direction:'))
		dd = self.create_select_dropdown(faceopts)
		div.appendChild( dd )
		div.appendChild( document.createElement('br') )
		def onchange(evt):
			opt = faceopts[this.selectedIndex]
			print(opt)
			model.material.side = eval('THREE.'+opt)
		dd.onchange = onchange

		blendopts = ['NormalBlending', 'AdditiveBlending', 'SubtractiveBlending', 'NoBlending']
		div.appendChild(document.createTextNode(' blending:'))
		dd = self.create_select_dropdown(blendopts)
		div.appendChild( dd )
		div.appendChild( document.createElement('br') )
		def change_blending(evt):
			opt = blendopts[this.selectedIndex]
			print(opt)
			model.material.blending = eval('THREE.'+opt)
		dd.onchange = change_blending

		def change_wireframe(evt): model.material.wireframe = this.checked
		div.appendChild(document.createTextNode(' wireframe:'))
		checkbox = create_checkbox( model.material.wireframe, onchange=change_wireframe )
		div.appendChild( checkbox )

		def change_wireframe_width(val): model.material.wireframeLinewidth = val * 10
		slider = create_slider( model.material.wireframeLinewidth*0.1, onchange=change_wireframe_width )
		div.appendChild( slider )

		div.appendChild( document.createElement('br') )


		def change_opacity(val):
			model.material.opacity = val
		slider = create_slider( model.material.opacity, onchange=change_opacity )
		div.appendChild( document.createTextNode('opacity:') )
		div.appendChild( slider )

		div.appendChild( document.createElement('br') )


		well = document.createElement('div')
		well.setAttribute('class', 'well')
		div.appendChild( well )

		## MeshBasicMaterial.js
		well.appendChild(document.createTextNode(' diffuse:'))
		input = document.createElement('input')
		input.setAttribute('type', 'color')
		input.style.width=64; input.style.height=32
		well.appendChild( input )
		def change_diffuse(evt):
			hex = int( '0x'+this.value[1:] )
			model.material.color.setHex( hex )
			print(model.material.color)
		## oninput fails, can only get update after use has picked color
		input.onchange = change_diffuse


		## MeshPhongMaterial.js
		if hasattr(model.material, 'ambient'):
			well.appendChild(document.createTextNode(' ambient:'))
			input = document.createElement('input')
			input.setAttribute('type', 'color')
			input.style.width=64; input.style.height=32
			well.appendChild( input )
			def change_ambient(evt):
				hex = int( '0x'+this.value[1:] )
				model.material.ambient.setHex( hex )
				print(model.material.ambient)
			input.onchange = change_ambient

		if hasattr(model.material, 'emissive'):
			well.appendChild(document.createTextNode(' emissive:'))
			input = document.createElement('input')
			input.setAttribute('type', 'color')
			input.style.width=64; input.style.height=32
			well.appendChild( input )
			def change_emissive(evt):
				hex = int( '0x'+this.value[1:] )
				model.material.emissive.setHex( hex )
				print(model.material.emissive)
			input.onchange = change_emissive

		if hasattr(model.material, 'specular'):
			#div.appendChild( document.createElement('br') )

			div.appendChild(document.createTextNode(' specular:'))

			def change_shininess(val):
				model.material.shininess = val * 100
			slider = create_slider( model.material.shininess*0.01, onchange=change_shininess )
			#div.appendChild( document.createTextNode(' shininess:') )
			div.appendChild( slider )

			input = document.createElement('input')
			input.setAttribute('type', 'color')
			input.style.width=64; input.style.height=32
			div.appendChild( input )
			def change_specular(evt):
				hex = int( '0x'+this.value[1:] )
				model.material.specular.setHex( hex )
				print(model.material.specular)
			input.onchange = change_specular



		return div


	def _gen_ui_single(self, model):
		div = document.createElement('div')
		div.setAttribute('class', 'well')
		#h3 = document.createElement('h3')
		#h3.appendChild( document.createTextNode(model.name) )
		#div.appendChild( h3 )

		div.appendChild( document.createTextNode(' position:') )

		def set_pos_x(evt): model.position.x = this.value
		input = create_float_input( model.position.x, onchange=set_pos_x)
		div.appendChild( input )

		def set_pos_y(evt): model.position.y = this.value
		input = create_float_input( model.position.y, onchange=set_pos_y)
		div.appendChild( input )

		def set_pos_z(evt): model.position.z = this.value
		input = create_float_input( model.position.z, onchange=set_pos_z)
		div.appendChild( input )

		div.appendChild( document.createElement('br') )

		div.appendChild( document.createTextNode(' rotation:') )

		def set_rot_x(evt): model.rotation.x = this.value
		input = create_float_input( model.rotation.x, onchange=set_rot_x)
		div.appendChild( input )

		def set_rot_y(evt): model.rotation.y = this.value
		input = create_float_input( model.rotation.y, onchange=set_rot_y)
		div.appendChild( input )

		def set_rot_z(evt): model.rotation.z = this.value
		input = create_float_input( model.rotation.z, onchange=set_rot_z)
		div.appendChild( input )

		div.appendChild( document.createElement('br') )

		div.appendChild( document.createTextNode(' scale:') )

		def set_scale_x(evt): model.scale.x = this.value
		input = create_float_input( model.scale.x, onchange=set_scale_x)
		div.appendChild( input )

		def set_scale_y(evt): model.scale.y = this.value
		input = create_float_input( model.scale.y, onchange=set_scale_y)
		div.appendChild( input )

		def set_scale_z(evt): model.scale.z = this.value
		input = create_float_input( model.scale.z, onchange=set_scale_z)
		div.appendChild( input )




		if hasattr(model, 'material'): ## could be THREE.Mesh or THREE.SkinnedMesh
			ui = self._gen_material_ui(model)
			div.appendChild( ui )
		return div

	def _gen_ui_multi(self, arr):
		menu = self.create_tab_menu()
		for i,model in enumerate(arr):
			page = menu.add_tab( model.name )
			div = self._gen_ui_single( model )
			page.appendChild( div )
		return menu.root

	def _gen_ui(self, o):

		if instanceof(o, Array):
			return self._gen_ui_multi(o)
		elif instanceof(o, THREE.Object3D):
			return self._gen_ui_single(o)
		else:
			raise RuntimeError('can not generate ui for type:'+o)



	def handle_drop_event(self, files):
		self.engine.pointlight1.position.copy( self.position )
		self.engine.pointlight1.position.z += 40
		self.engine.gizmo.attach( self.right_bar )

		images = []
		videos = []
		for file in files:
			## note: `file.path` is only available in NodeWebkit,
			## for simple testing we will fake it here.
			file.path = '/home/brett/Desktop/'+file.name

			if file.path.endswith('.dae'):
				loader = new THREE.ColladaLoader();
				loader.options.convertUpAxis = true;
				#def on_load(collada):
				#	print(collada)
				#	element3D.root.add( collada.scene )
				#loader.load( 'http://localhost:8000'+file.path, on_load )
		
				def onload(evt):
					parser = new DOMParser()
					collada = loader.parse( parser.parseFromString(evt.target.result, "application/xml") )
					print(collada.scene)
					collada.scene.scale.set(0.25, 0.25, 0.25)
					collada.scene.position.set(0, -100, 200)
					self.root.add( collada.scene )
					self.collada = collada.scene

					self.element.appendChild( self._gen_ui(collada.scene.children) )

				reader = new FileReader()
				reader.onload = onload.bind(self)
				reader.readAsText( file )

			elif file.path.endswith('.html'):
				iframe = element3D.create_iframe( file.path, renderer3.domElement )
				self.element.appendChild(iframe)

			elif file.path.endswith('.css'):
				print( 'TODO css' )
			elif file.path.endswith('.js'):
				print( 'TODO js' )
			elif file.path.endswith('.jpg') or file.path.endswith('.png') or file.path.endswith('.gif'):

				li = document.createElement('li')
				images.append(li)
				img = document.createElement('img')
				img.setAttribute('src', file.path)
				img.setAttribute('class', 'well img-rounded')
				li.appendChild( img )


			elif file.path.endswith('.mp4'):
				li = document.createElement('li')
				video = self.create_video( mp4=file.path )
				li.appendChild( video )
				videos.append( li )

			## note, nodewebkit is missing libffmpegsumo, then it only plays ogv videos
			elif file.path.endswith('.ogv'):
				#li = document.createElement('li')
				video = self.create_video( ogv=file.path )
				self.element.appendChild(video)
				#li.appendChild( video )
				#videos.append( li )

			elif file.path.endswith('.py'):
				def on_load(event):
					contents = event.target.result
					py_body_editor.setValue( contents )

				Reader.onload = on_load
				Reader.readAsText( file )

		if images:
			print('loading images')
			ul = document.createElement('ul')
			self.element.appendChild(ul)
			for li in images:
				ul.appendChild(li)

		if videos:
			print('loading videos')
			ul = document.createElement('ul')
			self.element.appendChild(ul)
			for li in videos:
				ul.appendChild(li)



class Engine:
	def Editor(self, **kw):
		e = Editor(self, **kw)
		self.windows.append( e )
		return e


	def __init__(self):
		self.windows = []

		SCREEN_WIDTH = window.innerWidth
		SCREEN_HEIGHT = window.innerHeight

		self.camera = camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 10000 );
		camera.position.set( 200, 250, 800 );

		self._selectman = SelectManager(self.camera)

		self.controls = controls = new THREE.TrackballControls( camera );
		camera.smooth_target = controls.target.clone()
		camera.smooth_target.y = 300

		controls.rotateSpeed = 1.0;
		controls.zoomSpeed = 1.2;
		controls.panSpeed = 0.8;

		controls.noZoom = false;
		controls.noPan = false;

		controls.staticMoving = false;
		controls.dynamicDampingFactor = 0.3;

		controls.keys = [ 65, 83, 68 ];

		self.scene = scene = new THREE.Scene();
		self.scene3 = scene3 = new THREE.Scene();


		self.renderer = renderer = new THREE.WebGLRenderer(alpha=True);
		renderer.shadowMapEnabled = true
		renderer.shadowMapType = THREE.PCFSoftShadowMap
		renderer.shadowMapSoft = true


		renderer.setSize( window.innerWidth, window.innerHeight );
		renderer.domElement.style.position = 'absolute';
		renderer.domElement.style.top = 0;
		renderer.domElement.style.zIndex = 1;

		self.gizmo = new THREE.TransformControls( camera, renderer.domElement )
		scene.add( self.gizmo )

		self.spotlight = light = new(
			THREE.SpotLight( 0xffffff, 1, 0, Math.PI / 2, 1 )
		)
		light.position.set( 0, 1400, 400 )
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

		scene.add( light );

		self.pointlight1 = pointlight = new( THREE.PointLight(0xffffff, 2, 500) )
		pointlight.position.set( 10, 100, 300 )
		scene.add( pointlight )

		self.pointlight2 = pointlight = new( THREE.PointLight(0xffffff, 2, 500) )
		pointlight.position.set( -10, -100, 200 )
		scene.add( pointlight )

		renderer.sortObjects = false
		renderer.autoClear = false

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


		hblur = new(THREE.ShaderPass( THREE.HorizontalTiltShiftShader ))
		vblur = new(THREE.ShaderPass( THREE.VerticalTiltShiftShader ))

		bluriness = 1.7;
		hblur.uniforms[ 'h' ].value = bluriness / SCREEN_WIDTH;
		vblur.uniforms[ 'v' ].value = bluriness / SCREEN_HEIGHT;

		hblur.uniforms[ 'r' ].value = 0.1
		vblur.uniforms[ 'r' ].value = 0.1


		self.composer = composer = new(THREE.EffectComposer( renderer, renderTarget ))

		renderModel = new(THREE.RenderPass( scene, camera ))

		vblur.renderToScreen = true;
		composer.addPass( renderModel );
		composer.addPass( hblur );
		composer.addPass( vblur );


		self.scene2 = scene2 = new THREE.Scene();


		self.renderer2 = renderer2 = new THREE.CSS3DRenderer();
		renderer2.setSize( window.innerWidth, window.innerHeight );
		renderer2.domElement.style.position = 'absolute';
		renderer2.domElement.style.top = 0;
		renderer2.domElement.style.zIndex = 0;
		document.body.appendChild( renderer2.domElement );

		self.renderer3 = renderer3 = new THREE.CSS3DRenderer();
		renderer3.setSize( window.innerWidth, window.innerHeight );
		renderer3.domElement.style.position = 'absolute';
		renderer3.domElement.style.top = 0;
		renderer3.domElement.style.opacity = 0.1;
		renderer3.domElement.style.zIndex=4;

		document.body.appendChild( renderer2.domElement );
		document.body.appendChild( renderer.domElement );
		document.body.appendChild( renderer3.domElement );



	def animate(self):
		requestAnimationFrame( self.animate.bind(self) );
		self.gizmo.update()

		d = self.camera.smooth_target.clone()
		d.sub(self.controls.target)
		self.controls.target.add( d.multiplyScalar(0.03) )
		self.controls.update()

		for win in self.windows: win.update()
		self.renderer2.render( self.scene2, self.camera )
		self.renderer.clear()
		self.composer.render( self.scene, self.camera )
		self.renderer3.render( self.scene3, self.camera )

	def run(self):
		#self.animate()
		setTimeout(self.animate.bind(self), 1000)

threepy = {
	'Engine' : lambda : Engine(),
}

#pythonjs.configure(javascript=False)
#threepy.Editor = lambda **kw: Engine(**kw)

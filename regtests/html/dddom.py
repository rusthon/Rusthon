pythonjs.configure(javascript=True)

__sid = 0

def create_textarea():
	global __sid
	__sid += 1
	ta = document.createElement('textarea')
	ta.setAttribute('id', '__sid'+__sid)
	def func(): ta.focus()  ## this allows normal keyboard input
	ta.onclick = func
	ta.style.backgroundColor = 'black'
	ta.style.color = 'green'
	ta.style.fontWeight = 'bold'
	ta.setAttribute('class', 'focused alert alert-info')
	return ta


class Element3D:
	def __init__(self, element, scene, shadow_scene, interact_scene, position, scale ):
		## required for select dropdowns because `selectedIndex` is not updated by `e.cloneNode()` ##
		self._sid = 0
		self.interact_scene = interact_scene
		self.shadow_scene = shadow_scene
		self.object = object = new THREE.CSS3DObject( element )
		self.position = object.position
		self.rotation = object.rotation
		self.scale = object.scale

		self.shadow = new THREE.CSS3DObject( element.cloneNode() )
		self.element = element
		self.active = False

		## shadow_images is required because every frame the entire dom is cloned to be rendered under webgl layer,
		## image data is lazy loaded, so even if the image is shown on the top interactive layer and cloned,
		## it still takes time before the clone will lazy load the image data,
		## below shadow_images holds a mapping of url and image, these must be inserted into the cloned dom each update.
		self.shadow_images = {}

		self.dropdown = None

		x,y,z = position
		self.object.position.set(x,y,z+1)
		self.shadow.position.set(x,y,z)

		x,y,z = scale
		self.object.scale.set(x,y,z)
		self.shadow.scale.set(x,y,z)

		shadow_scene.add( self.shadow )
		interact_scene.add( self.object )

		self.root = new THREE.Object3D()
		scene.add( self.root )

		self.create_windowframe()

	def display_dropdown(self, e, options):
		if not self.dropdown:
			self.create_dropdown( e, options )
		else:
			self.object.remove( self.dropdown )
			self.shadow.remove( self.dropdown_clone )
			self.root.remove( self._ddmesh1 )
			self.root.remove( self._ddmesh2 )
			self.dropdown = None

	def hide_dropdown(self):  ## not working, three.js bug?
		self.dropdown.visible = false
		self.dropdown_clone.visible = false


	def create_dropdown(self, e, options):
		global sel
		sel = document.createElement('select')
		sel.setAttribute('multiple', 'multiple')
		self._sid += 1
		sel.setAttribute('id', '_sid'+self._sid)
		for i,opt in enumerate(options):
			o = document.createElement('option')
			o.setAttribute('index', i)
			o.appendChild( document.createTextNode(opt) )
			sel.appendChild( o )

		##print('clientHeight', sel.clientHeight)
		## sel.clientHeight can not be used here because the dom has not been updated,
		## as a simple workaround guess height based on number of options,
		## this needs to be done anyways because `sel` must be given a height in pixels,
		## to force it to display all the options, and not display a scroll bar (which are not synced).
		H = 18 * options.length
		if H < 150: H = 150
		sel.style.height = H #'100%'

		## create dropdown css object and add it to self.object,
		## this makes it part of the interactive scene,
		## it is also needs its own shadow clone to be updated.
		self.dropdown = new THREE.CSS3DObject( sel )
		self.object.add( self.dropdown )
		self.dropdown_clone = new THREE.CSS3DObject(sel.cloneNode())
		self.shadow.add( self.dropdown_clone )

		self.dropdown.position.x = e.offsetLeft / 2
		self.dropdown.position.y -= (H/2) - e.offsetTop
		self.dropdown.position.z += 20
		self.dropdown_clone.position.copy( self.dropdown.position )
		self.dropdown_clone.position.z -= 1

		sel.focus()
		def onclick(evt):
			#sel.focus()  ## this triggers a bug that offsets the interactive layer
			print(evt.toElement.getAttribute('index'))
			e.selectedIndex = sel.selectedIndex = int(evt.toElement.getAttribute('index'))
		sel.onclick = onclick



		geo = new THREE.BoxGeometry( 1.1, H*1.1, 3 );
		mat = new THREE.MeshBasicMaterial( {'color': 0x00ffff, 'transparent':true, 'opacity':0.18, 'blending':THREE.AdditiveBlending } );
		self._ddmesh1 = m = new THREE.Mesh( geo, mat );
		self.root.add( m );
		m.castShadow = true;
		m.position.x = e.offsetLeft / 2
		m.position.y -= (H/2) - e.offsetTop
		m.position.y += 10
		m.position.z = 1
		m.scale.x = e.clientWidth

		geo = new THREE.BoxGeometry( 1.07, H, 3 );
		mat = new THREE.MeshBasicMaterial( {'color': 0xffffff, 'transparent':true, 'opacity':0.48, 'blending':THREE.SubtractiveBlending } );
		self._ddmesh2 = m = new THREE.Mesh( geo, mat );
		self.root.add( m );
		m.castShadow = true;
		m.position.x = e.offsetLeft / 2
		m.position.y -= (H/2) - e.offsetTop
		m.position.y += 10
		m.position.z = 15
		m.scale.x = e.clientWidth


	def create_select_dropdown(self, options ):
		self._sid += 1
		a = document.createElement('select')
		a.setAttribute('id', '_sid'+self._sid)

		def onclick(e):
			a.focus()  ## allows the enter key to display options
			self.display_dropdown(a, options)
		a.onclick = onclick.bind(self)

		for opt in options:
			o = document.createElement('option')
			o.appendChild(document.createTextNode(opt))
			a.appendChild(o)

		return a


	def create_windowframe(self):
		geo = new THREE.BoxGeometry( 1, 1, 1 );
		mat = new THREE.MeshBasicMaterial( color=0x000000, opacity=0 )
		mat.blending = THREE.NoBlending
		self.mask = r = new THREE.Mesh( geo, mat );
		self.root.add( r );
		#r.position.copy( self.object.position )
		r.position.z -= 5

		geo = new THREE.BoxGeometry( 0.7, 1, 20 );
		mat = new THREE.MeshPhongMaterial( {'color': 0xffffff, 'transparent':true, 'opacity':0.8, 'blending':THREE.AdditiveBlending } );
		self.shaded_border = m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.z -= 12
		m.castShadow = true;
		m.receiveShadow = true;

		geo = new THREE.BoxGeometry( 1.1, 1.1, 1 );
		mat = new THREE.MeshBasicMaterial( {'color': 0x00ffff, 'transparent':true, 'opacity':0.18, 'blending':THREE.AdditiveBlending } );
		self.glowing_border = m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.z -= 2

		geo = new THREE.BoxGeometry( 1.1, 1.1, 50 );
		mat = new THREE.MeshBasicMaterial( {'color': 0x00ffff, 'transparent':true, 'opacity':0.28, 'blending':THREE.AdditiveBlending, 'wireframe':true } );
		m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.z -= 40


		geo = new THREE.BoxGeometry( 0.025, 0.5, 30 );
		mat = new THREE.MeshPhongMaterial( {'color': 0xffffff } );
		self.right_bar = m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.y += 0.3
		m.position.x -= 0.55
		m.position.z -= 10
		m.castShadow = true;

		geo = new THREE.BoxGeometry( 0.9, 0.1, 20 );
		mat = new THREE.MeshPhongMaterial( color=0xffff00, transparent=True, opacity=0.84 );
		self.footer = m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.y -= 0.6
		m.position.z -= 5
		m.castShadow = true;


	def update(self):
		if self.shadow.element.parentNode:
			self.shadow.element.parentNode.removeChild( self.shadow.element )

		if self.active and self.object.position.y < 400:
			self.object.position.y += 10

		self.root.position.copy( self.object.position )
		self.root.rotation.copy( self.object.rotation )

		self.shadow.position.copy( self.object.position )
		self.shadow.rotation.copy( self.object.rotation )

		w = self.element.clientWidth * 0.01
		h = self.element.clientHeight * 0.01

		self.mask.scale.x = w*99
		self.mask.scale.y = h*99

		self.shadow.element = self.element.cloneNode()  ## this is just to display content

		a = self.element.getElementsByTagName('SELECT')
		b = self.shadow.element.getElementsByTagName('SELECT')
		c = {}
		for sel in b:
			c[ sel.getAttribute('id') ] = sel

		for sel in a:
			clone = c[ sel.getAttribute('id') ]
			clone.selectedIndex = sel.selectedIndex
			#clone.scrollTop = sel.scrollTop  ## this will not work to sync scrollbars


		a = self.element.getElementsByTagName('TEXTAREA')
		b = self.shadow.element.getElementsByTagName('TEXTAREA')
		c = {}
		for sel in b:
			c[ sel.getAttribute('id') ] = sel

		for sel in a:
			c[ sel.getAttribute('id') ].value = sel.value


		## insert lazy loading images into shadow dom ##
		images = self.shadow.element.getElementsByTagName('IMG')
		for img in images:
			if img.src in self.shadow_images:
				lazy = self.shadow_images[ img.src ]
				img.parentNode.replaceChild(lazy, img)
			else:
				self.shadow_images[ img.src ] = img

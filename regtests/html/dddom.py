# PythonJS WebGL/CSS3D Hybrid Toolkit
# by Brett Hartshorn - copyright 2014
# You may destribute this file using the "New BSD" or MIT license
# requires: Twitter Bootstrap and jQuery

pythonjs.configure(javascript=True)

def __setup_slider_class( $ ):

	def PPSliderClass(el, opts):
		var element = $(el);
		var options = opts;
		var isMouseDown = false;
		var currentVal = 0;

		element.wrap('<div/>')
		var container = $(el).parent();  ## this requires that the slider html element has a parent

		container.addClass('pp-slider');
		container.addClass('clearfix');

		container.append('<div class="pp-slider-min">-</div><div class="pp-slider-scale"><div class="pp-slider-button"><div class="pp-slider-divies"></div></div><div class="pp-slider-tooltip"></div></div><div class="pp-slider-max">+</div>');
		
		#if (typeof(options) != 'undefined' && typeof(options.hideTooltip) != 'undefined' && options.hideTooltip == true)
		#{
		#  container.find('.pp-slider-tooltip').hide();
		#}

		if typeof(options.width) != 'undefined':
			container.css('width',(options.width+'px'));

		container.find('.pp-slider-scale').css('width',(container.width()-30)+'px');

		def startSlide(e):
			nonlocal isMouseDown, startMouseX, lastElemLeft
			isMouseDown = true;
			var pos = getMousePosition(e);
			startMouseX = pos.x;		  
			lastElemLeft = ($(this).offset().left - $(this).parent().offset().left);
			updatePosition(e);
			return False
		
		def getMousePosition(e):
			var posx = 0;
			var posy = 0;
			if not e: e = window.event;
			if (e.pageX or e.pageY):
				posx = e.pageX;
				posy = e.pageY;
			elif (e.clientX or e.clientY):
				posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
				posy = e.clientY + document.body.scrollTop  + document.documentElement.scrollTop;

			return { 'x': posx, 'y': posy }

		def updatePosition(e):
			var pos = getMousePosition(e);
			var spanX = (pos.x - startMouseX);
			var newPos = (lastElemLeft + spanX)
			var upperBound = (container.find('.pp-slider-scale').width()-container.find('.pp-slider-button').width());
			newPos = Math.max(0,newPos);
			newPos = Math.min(newPos,upperBound);
			currentVal = Math.round((newPos/upperBound)*100,0);
			container.find('.pp-slider-button').css("left", newPos);
			container.find('.pp-slider-tooltip').html(currentVal+'%');
			container.find('.pp-slider-tooltip').css('left', newPos-6);
			if typeof(options.onInput) == 'function':
				options.onInput( newPos/upperBound )

		def moving(e):
			if isMouseDown:
				updatePosition(e);
				return False

		def dropCallback(e):
			nonlocal isMouseDown
			isMouseDown = False
			element.val(currentVal);
			if typeof(options.onChanged) == 'function':
				options.onChanged.call(this, null);

		container.find('.pp-slider-button').bind('mousedown',startSlide);

		$(document).mousemove( lambda e: moving(e) )
		$(document).mouseup( lambda e: dropCallback(e) )

		if options.value:
			w = container.find('.pp-slider-scale').width()-container.find('.pp-slider-button').width()
			container.find('.pp-slider-button').css(
				"left",
				w * options.value
			)
		

	def __init__(options):
		var opts = $.extend({}, $.fn.PPSlider.defaults, options);
		return this.each( lambda: new PPSliderClass($(this), opts) )
	$.fn.PPSlider = __init__

	$.fn.PPSlider.defaults = {
		'width': 300
	};

__setup_slider_class( jQuery )

__sid = 0

class TabMenuWrapper:
	## provides a workaround for bootstrap failing to update the active page when a tab is clicked
	def __init__(self, manager):
		self.manager = manager
		self.root = document.createElement('div')
		self.root.setAttribute('class', 'tabbable tabs-left')
		self.tabs = document.createElement('ul')
		self.tabs.setAttribute('class', 'nav nav-tabs')
		self.root.appendChild( self.tabs )
		#container.appendChild( menu )

		self.pages_container = document.createElement('div')
		self.pages_container.id = '_' + manager.newid()  ## scroll bars will show on this div
		self.pages_container.setAttribute('class', 'tab-content')
		self.root.appendChild( self.pages_container )

		## setting the tab page container to 100% width and height breaks twitter-bootstrap
		#self.pages_container.style.width = '100%'
		#self.pages_container.style.height = '100%'
		## for some reason, bootstrap appears to do something "funky" on the tab-content div,
		## `scrollTop` can be read on the source tab-content div, but not written to the clone.

		## this cheat will not work either, scrollTop on the clone is readonly and zero ##
		#def onscroll(evt):
		#	print(this.scrollTop)
		#	if this._clone:
		#		print(this._clone)
		#		this._clone.scrollTop = this.scrollTop
		#self.pages_container.onscroll = onscroll

		## workaround to disable scrollbars
		self.pages_container.style.overflow = 'hidden'


		self._tab_pages = []


	def add_tab(self, tabname):

		tab = document.createElement('li')
		taba = document.createElement('a')
		#taba.setAttribute('href', '#'+tabid)  ## not required
		taba.setAttribute('data-toggle', 'tab')

		tab.appendChild( taba )
		self.tabs.appendChild( tab )
		taba.appendChild( document.createTextNode(tabname) )


		page = document.createElement('div')
		a = 'tab-pane'
		if len(self._tab_pages)==0: a += ' active'
		page.setAttribute('class', a)

		#page.setAttribute('id', self.manager.newid() )  ## required to sync scrollbars

		self.pages_container.appendChild( page )
		self._tab_pages.append( page )

		## TODO force page to be full size, or sync scroll bars
		page.style.width = '100%'  ## this fails to force the window to resize
		page.style.height = '100%'

		_tab_pages = self._tab_pages
		def clicktab():
			for other in _tab_pages:
				other.setAttribute('class', 'tab-pane')
			this._tab_page.setAttribute('class', 'tab-pane active')

		taba._tab_page = page
		taba.onclick = clicktab

		return page



def create_slider(value, onchange=None, width=200):
	slider = document.createElement('input')

	## the native slider looks different on each platform,
	## and it is not clickable, because the camera controls preventDefault?
	## however, if focused the keyboard arrow keys, can still change the slider values.
	## to be safe, instead of using a native slider, we use the custom jquery/css slider.
	##slider.setAttribute('type', 'range')  ## do not use native slider
	#slider.setAttribute('min', 0)
	#slider.setAttribute('max', 100)
	#slider.setAttribute('step', 1)
	#slider.setAttribute('value', 100)

	slider.setAttribute('type', 'hidden')
	#$("#"+id).PPSlider( width=300, onInput=onchange, value=value )

	div = document.createElement('div')  ## a parent container is required
	div.appendChild( slider )
	$( slider ).PPSlider( width=width, onInput=onchange, value=value )

	slider.onclick = lambda : slider.focus()

	return div

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

def create_checkbox( checked, onchange=None ):
	## no special hacks required for checkboxes ##
	c = document.createElement('input')
	c.setAttribute('type', 'checkbox')
	if checked: c.setAttribute('checked', 'true')
	if onchange: c.onchange = onchange
	return c

def create_number_input(value, step=1, onchange=None):
	input = document.createElement('input')
	input.setAttribute('type', 'number')
	input.setAttribute('step', step)
	input.value = value
	input.style.width = 64
	input.style.height = 32
	input.onclick = lambda : this.focus()
	if onchange: input.onchange = onchange
	return input

def create_float_input(value, step=0.01, onchange=None):
	input = document.createElement('input')
	input.setAttribute('type', 'number')
	input.setAttribute('step', step)
	input.value = value
	input.style.width = 64
	input.style.height = 32
	input.onclick = lambda : this.focus()
	if onchange: input.onchange = onchange
	return input


def create_dropdown_button( name, options ):
	div = document.createElement('div')
	div.setAttribute('class', 'btn-group')

	b = document.createElement('button')
	b.setAttribute('class', 'btn dropdown-toggle')
	b.setAttribute('data-toggle', 'dropdown')
	caret = document.createElement('span')
	caret.setAttribute('class', 'caret')
	b.appendChild( document.createTextNode(name))
	b.appendChild(caret)

	## the darkstrap css fails to properly expand the options,
	## TODO - fix darkstrap or convert this to a 3D dropdown.
	ul = document.createElement('ul')
	ul.setAttribute('class', 'dropdown-menu')
	for opt in options:
		li = document.createElement('li')
		a = document.createElement('a')
		a.appendChild( document.createTextNode(opt) )
		li.appendChild( a )
		ul.appendChild( li )

	div.appendChild(b)
	div.appendChild(ul)
	return div


CLICKABLES = []
class SelectManager:
	def __init__(self, camera):
		self.camera = camera
		document.addEventListener('mouseup', self.on_mouse_up.bind(self), false)

	def on_mouse_up(self, evt):
		x = ( event.clientX / window.innerWidth ) * 2 - 1;
		y = - ( event.clientY / window.innerHeight ) * 2 + 1;
		vector = new THREE.Vector3( x, y, 0.5 );
		projector = new THREE.Projector();
		projector.unprojectVector( vector, self.camera );
		raycaster = new THREE.Raycaster( self.camera.position, vector.sub( self.camera.position ).normalize() );
		intersects = raycaster.intersectObjects( CLICKABLES );
		#if intersects.length > 0:
		#	ob = intersects[0].object
		for inter in intersects:
			ob = inter.object
			print(ob)
			if hasattr(ob, 'onclick'):
				ob.onclick( inter )



class Window3D:
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
		self.collasped = False

		## shadow_images is required because every frame the entire dom is cloned to be rendered under webgl layer,
		## image data is lazy loaded, so even if the image is shown on the top interactive layer and cloned,
		## it still takes time before the clone will lazy load the image data,
		## below shadow_images holds a mapping of url and image, these must be inserted into the cloned dom each update.
		self.shadow_images = {}
		self.clone_videos = {}
		self._video_textures = []  ## list of : {texture, video, context}
		self.clone_iframes = {}    ## this will not work, iframes are not lazy in the same way as images and videos.

		self.dropdown = None
		self._scrollbars = {}

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

	def newid(self):
		self._sid += 1
		return self._sid

	def create_tab_menu(self):
		return TabMenuWrapper( self )


	def create_iframe( self, url, element ):
		## this currently only renders on the top layer transparent layer,
		## to make iframes visible the top layer needs to become semi-transparent or opaque.
		## `element` is the DOM element that will have its opacity adjusted on mouse enter/leave
		iframe = document.createElement('iframe')
		iframe.setAttribute('src', url)
		iframe.style.width = '100%'
		iframe.style.height = '100%'
		iframe.style.border = 0
		self._sid += 1
		id = '__fid'+self._sid
		iframe.setAttribute('id', id)

		def f1(evt):
			print('mouse enter')
			element.style.opacity = 0.8
		def f2(evt):
			print('mouse leave')
			element.style.opacity = 0.2
		iframe.onmouseenter = f1
		iframe.onmouseleave = f2

		return iframe

	def create_video( self, mp4=None, ogv=None ):
		self._sid += 1
		id = '__vid'+self._sid
		v = document.createElement('video')
		v.setAttribute('id', id)
		#v.setAttribute('autoplay', 'true')  ## this must not be set, otherwise the clone will also play
		#v.setAttribute('style', "color: rgba(255, 255, 0, 1)")  ## this will not work
		#v.setAttribute('style', "opacity: 2")  ## this will not work either

		## for some reason play/pause can not be forced on the clone,
		## this might have something to do with the clone always being reparented.
		#def onclick_not_working(evt):
		#	vclone = self.clone_videos[ id ]
		#	print(vclone)
		#	if vclone.paused:
		#		print('playing...')
		#		vclone.play()
		#	else:
		#		vclone.pause()
		#		print('pause!')

		def onclick(evt):
			print('video clicked')
			if v.paused:
				print('playing...')
				v.play()
			else:
				v.pause()
				print('pause!')

		v.onclick = onclick.bind(self)

		def onmetaload(evt):
			print('video metadata loaded...')

			image = document.createElement( 'canvas' );
			image.width = v.videoWidth;
			image.height = v.videoHeight;

			imageContext = image.getContext( '2d' );
			imageContext.fillStyle = '#000000';
			imageContext.fillRect( 0, 0, v.videoWidth, v.videoHeight );

			texture = new THREE.Texture( image );
			texture.minFilter = THREE.LinearFilter;
			texture.magFilter = THREE.LinearFilter;

			material = new THREE.MeshBasicMaterial( map=texture, overdraw=true )
			#plane = new THREE.PlaneGeometry( v.videoWidth, v.videoHeight, 4, 4 );
			plane = new THREE.PlaneGeometry( 1, 1, 4, 4 );
			mesh = new THREE.Mesh( plane, material );
			H = v.videoHeight
			X = v.offsetLeft / 2
			Y = ((self.element.clientHeight-H) / 2) - v.offsetTop
			#mesh.position.x = v.offsetLeft  ## TODO
			mesh.position.y = Y
			mesh.position.z = 1
			mesh.scale.x = v.videoWidth
			mesh.scale.y = v.videoHeight

			self.root.add( mesh )


			self._video_textures.append( {'texture':texture, 'video':v, 'context':imageContext, 'image':image} )


		v.addEventListener('loadedmetadata', onmetaload.bind(self), false)

		if mp4:
			s = document.createElement('source')
			s.setAttribute('src', mp4)
			s.setAttribute('type', 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"')
			v.appendChild( s )
		if ogv:
			s = document.createElement('source')
			s.setAttribute('src', ogv)
			s.setAttribute('type', 'video/ogg; codecs="theora, vorbis"')
			v.appendChild( s )

		return v


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
		#global sel, g
		#g = e
		sel = document.createElement('select')
		sel.setAttribute('multiple', 'multiple')
		self._sid += 1
		id = '_sid'+self._sid
		sel.setAttribute('id', id)
		self._scrollbars[ id ] = 0


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
		H = 12 * options.length
		if H < 100: H = 100
		sel.style.height = int(H * 0.95)
		X = e.offsetLeft / 2
		Y = ((self.element.clientHeight-H) / 2) - (e.offsetHeight + e.offsetTop)

		## create dropdown css object and add it to self.object,
		## this makes it part of the interactive scene,
		## it is also needs its own shadow clone to be updated.
		self.dropdown = new THREE.CSS3DObject( sel )
		self.object.add( self.dropdown )
		self.dropdown_clone = new THREE.CSS3DObject(sel.cloneNode())
		self.shadow.add( self.dropdown_clone )

		self.dropdown.position.x = X
		self.dropdown.position.y = Y
		self.dropdown.position.z += 20
		self.dropdown_clone.position.copy( self.dropdown.position )
		self.dropdown_clone.position.z -= 1

		sel.focus()  # required?

		## this is used to capture a click on the dropdown popup, and copy selectedIndex
		## from the clone to the source, and if the source has an onchange callback, call it.
		def onclick(evt):
			#sel.focus()  ## this triggers a bug that offsets the interactive layer
			print(evt.toElement.getAttribute('index'))
			e.selectedIndex = sel.selectedIndex = int(evt.toElement.getAttribute('index'))
			## setting `selectedIndex` on the source e will not trigger its `onchange` callback to fire,
			## so call onchange directly.  Note that the event `evt` from the clone is passed the source
			## as the first argument. end-user code inside e.onchange should not modify elements referenced in the event.
			## note that the calling context is set to the source by `e.onchange(evt)` so it is safe to use `this`
			## inside of onchange.
			if e.onchange:
				e.onchange( evt )
		sel.onclick = onclick

		def onscroll(evt):  ## this hack is required to capture the scroll position
			self.dropdown_clone.element.scrollTop = sel.scrollTop
		sel.onscroll = onscroll.bind(self)

		geo = new THREE.BoxGeometry( 1.1, H*1.1, 3 );
		mat = new THREE.MeshBasicMaterial( {'color': 0x00ffff, 'transparent':true, 'opacity':0.18, 'blending':THREE.AdditiveBlending } );
		self._ddmesh1 = m = new THREE.Mesh( geo, mat );
		self.root.add( m );
		m.castShadow = true;
		m.position.x = X
		m.position.y = Y
		m.position.y += 10
		m.position.z = 1
		m.scale.x = e.clientWidth

		geo = new THREE.BoxGeometry( 1.07, H, 3 );
		mat = new THREE.MeshBasicMaterial( {'color': 0xffffff, 'transparent':true, 'opacity':0.48, 'blending':THREE.SubtractiveBlending } );
		self._ddmesh2 = m = new THREE.Mesh( geo, mat );
		self.root.add( m );
		m.castShadow = true;
		m.position.x = X
		m.position.y = Y
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

	def hide_windowframe(self):
		self.mask.visible = False
		self.shaded_border.visible = False
		self.glowing_border.visible = False

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
		CLICKABLES.append( m )
		def expand(inter):
			self.expand()
		m.onclick = expand.bind(self)

		geo = new THREE.BoxGeometry( 0.9, 0.1, 20 );
		mat = new THREE.MeshPhongMaterial( color=0xffff00, transparent=True, opacity=0.84 );
		self.footer = m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.y -= 0.6
		m.position.z -= 5
		m.castShadow = true;
		CLICKABLES.append( m )

		def clickfooter(inter):
			self.active = True
			if self.collasped:
				self.expand()
		m.onclick = clickfooter.bind(self)

		geo = new THREE.BoxGeometry( 0.2, 0.1, 10 );
		mat = new THREE.MeshPhongMaterial( {'color': 0xffff00 } );
		self.minimize_object = m = new THREE.Mesh( geo, mat );
		r.add( m );
		m.position.y += 0.8
		m.position.x += 0.45
		m.position.z -= 2
		m.castShadow = true;
		CLICKABLES.append( m )
		def collaspe(inter):
			self.collaspe()
		m.onclick = collaspe.bind(self)

	def collaspe(self):
		self.collasped = True
		self.active = False
		self.object.rotation.x = -Math.PI / 2
		self.object.position.y = 0

	def expand(self):
		self.collasped = False
		self.active = True
		self.object.rotation.x = 0

	def spin90(self):
		self.object.rotation.y += Math.PI / 2

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

		## this is just to display content, cloneNode(true) ensures deep copy
		self.shadow.element = self.element.cloneNode(true)

		## sync scrollbars of any div with an id,
		## note: this will not work with tab-content div's.
		a = self.element.getElementsByTagName('DIV')
		b = self.shadow.element.getElementsByTagName('DIV')
		c = {}
		for d in b:
			if not d.id: continue
			c[ d.id ] = d

		for d in a:
			if not d.id: continue
			clone = c[ d.id ]
			#d._clone = clone ## no help for tab-content
			if d.scrollTop:
				clone.scrollTop = d.scrollTop

		################################################

		a = self.element.getElementsByTagName('SELECT')
		b = self.shadow.element.getElementsByTagName('SELECT')
		c = {}
		for sel in b:
			c[ sel.getAttribute('id') ] = sel

		for sel in a:
			id = sel.getAttribute('id')
			clone = c[ id ]
			clone.selectedIndex = sel.selectedIndex
			if sel.scrollTop:  ## select `multiple` type boxes. (note: self.dropdown is not updated here)
				clone.scrollTop = sel.scrollTop


		a = self.element.getElementsByTagName('TEXTAREA')
		b = self.shadow.element.getElementsByTagName('TEXTAREA')
		c = {}
		for sel in b:
			c[ sel.getAttribute('id') ] = sel

		for sel in a:
			c[ sel.getAttribute('id') ].value = sel.value


		## do not load iframes in the clone ##
		iframes = self.shadow.element.getElementsByTagName('IFRAME')
		for iframe in iframes:
			iframe.src = None

		## insert lazy loading iframes into shadow dom ##
		## it appears that this will not work, because when an iframe is reparented,
		## it triggers a reload of the iframe, there might be a way to cheat around this,
		## (possible workaround: block dom clone update until iframe has fully loaded)
		## but it would be better to have a different solution anyways that only single
		## renders the iframe - workaround: on mouse enter/leave adjust opacity of top css3d layer.
		if False:
			iframes = self.shadow.element.getElementsByTagName('IFRAME')
			for frame in iframes:
				#if frame.src in self.clone_iframes:
				#	lazy = self.clone_iframes[ frame.src ]
				#	frame.parentNode.replaceChild(lazy, frame)
				if frame.getAttribute('srcHACK') in self.clone_iframes:
					#lazy = self.clone_iframes[ frame.getAttribute('srcHACK') ]
					#frame.parentNode.replaceChild(lazy, frame)
					pass
				else:
					#self.clone_iframes[ frame.src ] = frame
					iframe = document.createElement('iframe')
					#iframe.setAttribute('src', frame.src)
					#iframe.setAttribute('src', frame.getAttribute('srcHACK'))
					#iframe.src = 'file://'+frame.getAttribute('srcHACK')
					iframe.setAttribute('src','http://localhost:8000/')
					iframe.style.width = '100%'
					iframe.style.height = '100%'
					iframe.style.zIndex = 100
					#self.clone_iframes[ frame.src ] = iframe
					self.clone_iframes[ frame.getAttribute('srcHACK') ] = iframe
					print('new iframe---')
					print(iframe)




		## insert lazy loading images into shadow dom ##
		images = self.shadow.element.getElementsByTagName('IMG')
		for img in images:
			if img.src in self.shadow_images:
				lazy = self.shadow_images[ img.src ]
				img.parentNode.replaceChild(lazy, img)
			else:
				self.shadow_images[ img.src ] = img

		## this is still required because when the video lazy loads it sets
		## the proper size for the clone.
		videos = self.shadow.element.getElementsByTagName('VIDEO')
		for vid in videos:
			id = vid.getAttribute('id')
			if id in self.clone_videos:
				lazy = self.clone_videos[ id ]
				vid.parentNode.replaceChild(lazy, vid)
			else:
				#vid.setAttribute('autoplay', 'true')  ## no help
				#vid.play()                            ## no help
				self.clone_videos[ id ] = vid

		for d in self._video_textures:
			video = d['video']
			if video.readyState == video.HAVE_ENOUGH_DATA:
				d['context'].drawImage( video, 0, 0 )
				d['texture'].needsUpdate = True

# Pixi.js wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

class Texture:
	def __init__(self, baseTexture=None, crop=None, fromImage=None, crossOrigin=False, fromFrame=None, fromCanvas=None):
		with javascript:
			if baseTexture:
				self[...] = new( PIXI.Texture(baseTexture[...], crop) )
			elif fromCanvas:
				self[...] = PIXI.Texture.fromCanvas( fromCanvas )
			elif fromFrame:
				self[...] = PIXI.Texture.fromFrame( fromFrame )
			elif fromImage:
				self[...] = PIXI.Texture.fromImage( fromImage, crossOrigin )

	def setFrame(self, rect):
		with javascript:
			self[...].setFrame( rect[...] )


class _Renderer:
	@property
	def view(self):
		with javascript:
			return self[...].view

	def render(self, stage):
		with javascript:
			self[...].render( stage[...] )

	def resize(self, w, h):
		with javascript:
			self[...].resize( w, h )

class WebGLRenderer( _Renderer ):
	def __init__(self, width=800, height=600, view=None, transparent=False, antialias=False):
		with javascript:
			self[...] = new( PIXI.WebGLRenderer(width, height, view, transparent, antialias) )

class CanvasRenderer( _Renderer ):
	def __init__(self, width=800, height=600, view=None, transparent=False, antialias=False):
		with javascript:
			self[...] = new( PIXI.CanvasRenderer(width, height, view, transparent, antialias) )

@pythonjs.init_callbacks
@pythonjs.property_callbacks
class Point:
	def __init__(self, x=0, y=0, object=None):
		with javascript:
			if object:
				self[...] = object
			else:
				self[...] = new( PIXI.Point(x,y) )

	@returns( float )
	@property
	def x(self):
		with javascript: return self[...].x
	@x.setter
	def x(self, value):
		with javascript: self[...].x = value

	@returns( float )
	@property
	def y(self):
		with javascript: return self[...].y
	@y.setter
	def y(self, value):
		with javascript: self[...].y = value

	def clone(self):
		return Point(x=self.x, y=self.y)


@pythonjs.property_callbacks
class DisplayObject:
	def on_pressed_callback(self, data):
		self._on_pressed_callback( self, data )

	def set_pressed_callback(self, js_callback=None, callback=None, touch=True):
		if js_callback:
			callback = js_callback
		else:
			self._on_pressed_callback = callback
			callback = self.on_pressed_callback
		with javascript:
			self[...].mousedown = callback
			if touch:
				self[...].touchstart = callback

	def on_released_callback(self, data):
		self._on_released_callback( self, data )

	def set_released_callback(self, js_callback=None, callback=None, touch=True, outside=True):
		if js_callback:
			callback = js_callback
		else:
			self._on_released_callback = callback
			callback = self.on_released_callback
		with javascript:
			self[...].mouseup = callback
			if touch:
				self[...].touchend = callback
			if outside:
				self[...].mouseupoutside = callback

	def on_drag_callback(self, data):
		self._on_drag_callback( self, data )

	def set_drag_callback(self, js_callback=None, callback=None, touch=True):
		if js_callback:
			callback = js_callback
		else:
			self._on_drag_callback = callback
			callback = self.on_drag_callback
		with javascript:
			self[...].mousemove = callback
			if touch:
				self[...].touchmove = callback

	@cached_property
	def position(self):
		with javascript: ptr = self[...].position
		return Point( object=ptr )

	@cached_property
	def scale(self):
		with javascript: ptr = self[...].scale
		return Point( object=ptr )

	@cached_property
	def pivot(self):
		with javascript: ptr = self[...].pivot
		return Point( object=ptr )


	@returns( float )
	@property
	def rotation(self):
		with javascript: return self[...].rotation
	@rotation.setter
	def rotation(self, value):
		with javascript: self[...].rotation = value

	@returns( float )
	@property
	def alpha(self):
		with javascript: return self[...].alpha
	@alpha.setter
	def alpha(self, value):
		with javascript: self[...].alpha = value

	@returns( bool )
	@property
	def visible(self):
		with javascript: return self[...].visible
	@visible.setter
	def visible(self, value):
		with javascript: self[...].visible = value

	@property
	def hitArea(self):
		with javascript: return self[...].hitArea
	@hitArea.setter
	def hitArea(self, value):
		with javascript: self[...].hitArea = value

	@returns( bool )
	@property
	def buttonMode(self):
		with javascript: return self[...].buttonMode
	@buttonMode.setter
	def buttonMode(self, value):
		with javascript: self[...].buttonMode = value

	@returns( bool )
	@property
	def renderable(self):
		with javascript: return self[...].renderable
	@renderable.setter
	def renderable(self, value):
		with javascript: self[...].renderable = value


	@property
	def parent(self):  ## read only
		with javascript: return self[...].parent

	@property
	def stage(self):  ## read only
		with javascript: return self[...].stage

	@property
	def worldAlpha(self):  ## read only
		with javascript: return self[...].worldAlpha


	def setInteractive(self, value):
		with javascript:
			if value:
				self[...].interactive = True
			else:
				self[...].interactive = False

	@returns( bool )
	@property
	def interactive(self):
		with javascript: return self[...].interactive
	@interactive.setter
	def interactive(self, value):
		with javascript: self[...].interactive = value

	@property
	def mask(self):
		with javascript: return self[...].mask
	@mask.setter
	def mask(self, value):
		with javascript: self[...].mask = value

	def addFilter(self, graphics):
		with javascript: return self[...].addFilter( graphics )

	def removeFilter(self):  ## private
		with javascript: return self[...].removeFilter()

	def updateTransform(self):  ## private
		with javascript: return self[...].updateTransform()

class DisplayObjectContainer( DisplayObject ):


	@property
	def children(self):
		with javascript: ptr = self[...].children
		return list( js_object=ptr )

	def addChild(self, child):
		with javascript:
			self[...].addChild( child[...] )

	def addChildAt(self, child, index=0):
		with javascript:
			self[...].addChildAt( child[...], index )

	def getChildAt(self, index=0):
		with javascript:
			return self[...].getChildAt( index )

	def removeChild(self, child):
		with javascript:
			self[...].removeChild( child[...] )


class Stage( DisplayObjectContainer ):
	def __init__(self, backgroundColor=0, interactive=False ):
		with javascript:
			self[...] = new( PIXI.Stage(backgroundColor, interactive) )
			self[...][...] = self ## this[...] points to self

	def setBackgroundColor(self, color):
		with javascript:
			self[...].setBackgroundColor( color )

	def getMousePosition(self):
		with javascript:
			return self[...].getMousePosition()

@pythonjs.init_callbacks
@pythonjs.property_callbacks
class Sprite( DisplayObjectContainer ):
	def __init__(self, texture=None, image=None, blendMode='NORMAL', position_x=0.0, position_y=0.0, anchor_x=0.0, anchor_y=0.0, interactive=False, on_drag=None, on_pressed=None, on_released=None, parent=None):

		if image:
			texture = Texture( fromImage=image )

		with javascript:
			## texture can be low level PIXI.Texture or high level PythonJS Texture
			if isinstance( texture, Texture ):
				texture = texture[...]

			sprite = new( PIXI.Sprite(texture) )
			self[...] = sprite
			sprite[...] = self  ## this[...] points to self - the wrapper
			sprite.position.x = position_x
			sprite.position.y = position_y
			sprite.anchor.x = anchor_x
			sprite.anchor.y = anchor_y
			sprite.interactive = interactive

			if blendMode == 'NORMAL':
				sprite.blendMode = PIXI.blendModes.NORMAL
			elif blendMode == 'SCREEN':
				sprite.blendMode = PIXI.blendModes.SCREEN
			else:
				print 'ERROR: unknown blend mode type for Sprite:' + blendMode

			if image:
				sprite._image_url = image


		if on_drag:
			self.set_drag_callback( on_drag )
		if on_pressed:
			self.set_pressed_callback( on_pressed )
		if on_released:
			self.set_released_callback( on_released )
		if parent:
			parent.addChild( self )

	@returns( float )
	@property
	def width(self):
		with javascript: return self[...].width
	@width.setter
	def width(self, value):
		with javascript: self[...].width = value

	@returns( float )
	@property
	def height(self):
		with javascript: return self[...].height
	@height.setter
	def height(self, value):
		with javascript: self[...].height = value

	def setTexture(self, texture):
		if isinstance( texture, Texture ): texture = texture[...]
		with javascript: self[...].setTexture( texture )

	@cached_property
	def anchor(self):
		with javascript: ptr = self[...].anchor
		return Point( object=ptr )


class MovieClip( Sprite ):
	def __init__(self, textures=None, animationSpeed=1.0, loop=True, onComplete=None):
		with javascript: arr = []
		for tex in textures:
			if isinstance(tex, Texture):
				arr.push( tex[...] )
			else:
				arr.push( tex )

		with javascript:
			self[...] = new( PIXI.MovieClip( arr ) )
			self[...][...] = self
			self[...].animationSpeed = animationSpeed
			self[...].loop = loop
			self[...].onComplete = onComplete

	@property
	def currentFrame(self):
		with javascript: return self[...].currentFrame

	@property
	def playing(self):
		with javascript: return self[...].playing

	def play(self):
		with javascript: return self[...].play()

	def stop(self):
		with javascript: return self[...].stop()

	def gotoAndPlay(self, frame):
		with javascript: return self[...].gotoAndPlay( frame )

	def gotoAndStop(self, frame):
		with javascript: return self[...].gotoAndStop( frame )

@pythonjs.init_callbacks
@pythonjs.property_callbacks
class Text( Sprite ):
	def __init__(self, text, font='Arial', size=20, bold=False, fill='black', align='left', stroke='blue', strokeThickness=0, wordWrap=False, wordWrapWidth=100, interactive=False, on_drag=None, on_pressed=None, on_released=None, parent=None ):
		self._text = text
		self._font = font
		self._size = size
		self._bold = bold
		self._fill = fill
		self._align = align
		self._stroke = stroke
		self._strokeThickness = strokeThickness
		self._wordWrap = wordWrap
		self._wordWrapWidth = wordWrapWidth
		style = self._get_style()
		with javascript:
			self[...] = new( PIXI.Text( text, style ) )
			self[...][...] = self
			self[...].interactive = interactive

		if on_drag:
			self.set_drag_callback( on_drag )
		if on_pressed:
			self.set_pressed_callback( on_pressed )
		if on_released:
			self.set_released_callback( on_released )
		if parent:
			parent.addChild( self )

	def _get_style(self):
		font = self._font
		size = self._size
		bold = self._bold
		fill = self._fill
		align = self._align
		stroke = self._stroke
		strokeThickness = self._strokeThickness
		wordWrap = self._wordWrap
		wordWrapWidth = self._wordWrapWidth
		if bold:
			font = 'bold ' + size + 'pt ' + font
		else:
			font = size + 'pt ' + font
		with javascript:
			return {font:font, fill:fill, align:align, stroke:stroke, strokeThickness:strokeThickness, wordWrap:wordWrap, wordWrapWidth:wordWrapWidth}

	def setStyle(self, font='Arial', size=20, bold=False, fill='black', align='left', stroke='blue', strokeThickness=0, wordWrap=False, wordWrapWidth=100):
		self._text = text
		self._font = font
		self._size = size
		self._bold = bold
		self._fill = fill
		self._align = align
		self._stroke = stroke
		self._strokeThickness = strokeThickness
		self._wordWrap = wordWrap
		self._wordWrapWidth = wordWrapWidth
		style = self._get_style()
		with javascript:
			self[...].setStyle( style )

	def setText(self, text):
		self._text = text
		print 'setting new text:', text
		with javascript:
			self[...].setText( text )

	@returns( str )
	@property
	def text(self):
		return self._text
	@text.setter
	def text(self, txt):
		self.setText(txt)

	@returns( bool )
	@property
	def bold(self):
		return self._bold
	@bold.setter
	def bold(self, v):
		self._bold = v
		style = self._get_style()
		with javascript:
			self[...].setStyle( style )

	@returns( float )
	@property
	def size(self):
		return self._size
	@size.setter
	def size(self, v):
		self._size = v
		style = self._get_style()
		with javascript:
			self[...].setStyle( style )


	def destroy(self, destroyTexture=False):
		with javascript:
			return self[...].destroy( destroyTexture )

	def updateText(self):  ## private
		with javascript:
			self[...].updateText()

	def updateTexture(self):  ## private
		with javascript:
			self[...].updateTexture()

	def determineFontHeight(self):  ## private
		with javascript:
			return self[...].determineFontHeight()

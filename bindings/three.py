# THREE.js wrapper for PythonScript
# by Brett Hartshorn - copyright 2013
# License: "New" BSD

class _ObjectBase:
	def add(self, child):
		ob = self._object
		JS('ob.add(child)')

class _PerspectiveCamera( _ObjectBase ):


class _Scene:
	def __init__(self):
		self._scene = JS('new THREE.Scene()')

	def add(self, child):
		scene = self._scene
		JS('scene.add(child)')


class _Renderer:
	def setSize(self, width, height):
		renderer = self._renderer
		JS('renderer.setSize( width, height )')

	def setClearColor(self, red=1.0, green=1.0, blue=1.0, alpha=1.0):
		renderer = self._renderer
		JS('renderer.setClearColor( {r:red, g:green, b:blue}, alpha)')


class _CSS3DRenderer( _Renderer ):
	def __init__(self):
		self._renderer = JS('new THREE.CSS3DRenderer()')

	def getDomElement(self):
		renderer = self._renderer
		return JS('renderer.domElement')

class _WebGLRenderer( _Renderer ):
	def __init__(self):
		self._renderer = JS('new THREE.WebGLRenderer()')


class _ImageUtils:
	def loadTexture( url ):
		return JS('THREE.ImageUtils.loadTexture(url)')

	def loadTextureCube( urls ):
		## TODO THREE.CubeRefractionMapping()
		JS('var _mapping = new THREE.CubeReflectionMapping()')
		return JS('THREE.ImageUtils.loadTextureCube(urls, _mapping)')

class _Three:
	def __init__(self):
		self.ImageUtils = _ImageUtils()

	def Scene(self):
		return _Scene()

	def CSS3DRenderer(self):
		return _CSS3DRenderer()

	def WebGLRenderer(self):
		return _WebGLRenderer()



Three = _Three()
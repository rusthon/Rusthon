# THREE.js wrapper for PythonScript
# by Brett Hartshorn - copyright 2013
# License: "New" BSD

class _Scene:
	def __init__(self):
		self._scene = JS('new THREE.Scene()')

class _CSS3DRenderer:
	def __init__(self):
		self._renderer = JS('new THREE.CSS3DRenderer()')

	def setSize(self, width, height):
		renderer = self._renderer
		JS('renderer.setSize( width, height )')

	def getDomElement(self):
		renderer = self._renderer
		return JS('renderer.domElement')


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


Three = _Three()
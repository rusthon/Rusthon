# THREE.js wrapper for PythonScript
# by Brett Hartshorn - copyright 2013
# License: PSFLv2 - http://www.python.org/psf/license/


class _Vector3:
	def __init__(self, jsobject=None):
		self._vec = jsobject

class _ObjectBase:
	def add(self, child):
		ob = self._object
		JS('ob.add(child)')

class _Camera( _ObjectBase ):

	def updateProjectionMatrix(self):
		ob = self._object
		JS('ob.updateProjectionMatrix()')

class _OrthographicCamera( _Camera ):
	def __init__(self, left, right, top, bottom, near, far):
		self._object = JS('new THREE.OrthographicCamera(left, right, top, bottom, near, far)')

class _PerspectiveCamera( _Camera ):
	def __init__(self, fov, aspect, near, far):
		self._object = JS('new THREE.PerspectiveCamera(fov, aspect, near, far)')

	def setLens(self, focalLength, frameSize):
		'''Uses Focal Length (in mm) to estimate and set FOV
		* 35mm (fullframe) camera is used if frame size is not specified;
		* Formula based on http://www.bobatkins.com/photography/technical/field_of_view.html
		'''
		ob = self._object
		JS('ob.setLens(focalLength, frameSize)')

	def setViewOffset(self, fullWidth, fullHeight, x, y, width, height):
		'''
		Sets an offset in a larger frustum. This is useful for multi-window or
		multi-monitor/multi-machine setups.
		'''
		ob = self._object
		JS('ob.setViewOffset(fullWidth, fullHeight, x, y, width, height)')


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

	def PerspectiveCamera(self, fov, aspect, near, far):
		return _PerspectiveCamera(fov, aspect, near, far)

	def OrthographicCamera(left, right, top, bottom, near, far):
		return _OrthographicCamera(left, right, top, bottom, near, far)

Three = _Three()
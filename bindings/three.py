# THREE.js wrapper for PythonScript
# by Brett Hartshorn - copyright 2013
# License: PSFLv2 - http://www.python.org/psf/license/

class Vector3:
	def __init__(self, x=0, y=0, z=0 ):
		self._vec = JS('new THREE.Vector3(x,y,z)')

	@property
	def x(self):
		vec = self._vec
		return JS('vec.x')
	@x.setter
	def x(self, value):
		vec = self._vec
		JS('vec.x=value')

	@property
	def y(self):
		vec = self._vec
		return JS('vec.y')
	@y.setter
	def y(self, value):
		vec = self._vec
		JS('vec.y=value')

	@property
	def z(self):
		vec = self._vec
		return JS('vec.z')
	@z.setter
	def z(self, value):
		vec = self._vec
		JS('vec.z=value')

	def setComponent(self, index, value):
		vec = self._vec
		JS('vec.setComponent(index,value)')
	def getComponent(self, index):
		vec = self._vec
		return JS('vec.getComponent(index)')

	def set(self, x,y,z):
		vec = self._vec
		JS('vec.set(x,y,z)')
	def setX(self, x):
		vec = self._vec
		JS('vec.setX(x)')
	def setY(self, y):
		vec = self._vec
		JS('vec.setY(y)')
	def setZ(self, z):
		vec = self._vec
		JS('vec.setZ(z)')

	def copy(self, other):
		assert isinstance(other, Vector3)
		self.set( other.x, other.y, other.z )
		return self

	def add(self, other):
		assert isinstance(other, Vector3)
		#self.x += other.x ## TODO fix inplace property assignment
		self.set( self.x+other.x, self.y+other.y, self.z+other.z )
		return self

	def addScalar(self, s):
		self.set( self.x+s, self.y+s, self.z+s )
		return self

	def addVectors(self, a,b):
		var( a=Vector3, b=Vector3 )
		self.set( a.x+b.x, a.y+b.y, a.z+b.z )
		return self


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
		"""Uses Focal Length (in mm) to estimate and set FOV
		* 35mm (fullframe) camera is used if frame size is not specified;
		* Formula based on http://www.bobatkins.com/photography/technical/field_of_view.html
		"""
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
		self.Vector3 = Vector3

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
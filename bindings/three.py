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

	def __add__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			assert isinstance(other, Vector3)
			return Vector3( self.x+other.x, self.y+other.y, self.z+other.z )
		else:
			return Vector3( self.x+other, self.y+other, self.z+other )

	def __iadd__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			self.add( other )
		else:
			self.addScalar( other )

	def addScalar(self, s):
		self.set( self.x+s, self.y+s, self.z+s )
		return self

	def addVectors(self, a,b):
		var( a=Vector3, b=Vector3 )
		self.set( a.x+b.x, a.y+b.y, a.z+b.z )
		return self

	def sub(self, other):
		assert isinstance(other, Vector3)
		self.set( self.x-other.x, self.y-other.y, self.z-other.z )
		return self

	def __sub__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			assert isinstance(other, Vector3)
			return Vector3( self.x-other.x, self.y-other.y, self.z-other.z )
		else:
			return Vector3( self.x-other, self.y-other, self.z-other )

	def __isub__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			self.sub( other )
		else:
			self.set( self.x-other, self.y-other, self.z-other )

	def subVectors(self, a,b):
		var( a=Vector3, b=Vector3 )
		self.set( a.x-b.x, a.y-b.y, a.z-b.z )
		return self

	def multiply(self, other):
		assert isinstance(other, Vector3)
		self.set( self.x*other.x, self.y*other.y, self.z*other.z )
		return self

	def __mul__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			assert isinstance(other, Vector3)
			return Vector3( self.x*other.x, self.y*other.y, self.z*other.z )
		else:
			return Vector3( self.x*other, self.y*other, self.z*other )

	def __imul__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			self.multiply( other )
		else:
			self.multiplyScalar( other )

	def multiplyScalar(self, s):
		self.set( self.x*s, self.y*s, self.z*s )
		return self

	def multiplyVectors(self, a,b):
		var( a=Vector3, b=Vector3 )
		self.set( a.x*b.x, a.y*b.y, a.z*b.z )
		return self

	def applyMatrix3(self, m):
		vec = self._vec
		JS('vec.applyMatrix3(m)')
		return self

	def applyMatrix4(self, m):
		vec = self._vec
		JS('vec.applyMatrix4(m)')
		return self

	def applyProjection(self, m):
		vec = self._vec
		JS('vec.applyProjection(m)')
		return self

	def applyQuaternion(self, q):
		vec = self._vec
		JS('vec.applyQuaternion(q)')
		return self

	def transformDirection(self, m):
		vec = self._vec
		JS('vec.transformDirection(m)')
		return self

	def divide(self, other):
		assert isinstance(other, Vector3)
		self.set( self.x/other.x, self.y/other.y, self.z/other.z )
		return self

	def divideScalar(self, s):
		vec = self._vec
		JS('vec.divideScalar(s)')  ## takes care of divide by zero
		return self

	def __div__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			assert isinstance(other, Vector3)
			return Vector3( self.x/other.x, self.y/other.y, self.z/other.z )
		else:
			return Vector3( self.x/other, self.y/other, self.z/other )

	def __idiv__(self, other):
		if JS("{}.toString.call(other) === '[object Object]'"):
			self.divide( other )
		else:
			self.divideScalar( other )

	def min(self, s):
		vec = self._vec
		JS('vec.min(s)')
		return self
	def max(self, s):
		vec = self._vec
		JS('vec.max(s)')
		return self
	def clamp(self, s):
		vec = self._vec
		JS('vec.clamp(s)')
		return self
	def negate(self):
		vec = self._vec
		JS('vec.negate()')
		return self

	def dot(self, v):
		vec = self._vec
		return JS('vec.dot(v)')
	def lengthSq(self):
		vec = self._vec
		return JS('vec.lengthSq()')
	def length(self):
		vec = self._vec
		return JS('vec.length()')
	def lengthManhattan(self):
		vec = self._vec
		return JS('vec.lengthManhattan()')

	def normalize(self):
		vec = self._vec
		JS('vec.normalize()')
		return self

	def setLength(self, l):
		vec = self._vec
		JS('vec.setLength(l)')
		return self

	def lerp(self, v, alpha):
		vec = self._vec
		JS('vec.lerp(v, alpha)')
		return self

	def cross(self, v):  ## cross product
		vec = self._vec
		JS('vec.cross(v)')
		return self

	def crossVectors(self, a,b):
		vec = self._vec
		JS('vec.crossVectors(a,b)')
		return self

	def __ixor__(self, other):  ## ^=
		self.cross(other)

	def angleTo(self, v):
		vec = self._vec
		return JS('vec.angleTo(v)')

	def distanceTo(self, v):
		vec = self._vec
		return JS('vec.distanceTo(v)')

	def distanceToSquared(self, v):
		vec = self._vec
		return JS('vec.distanceToSquared(v)')

	def getPositionFromMatrix(self, m):
		vec = self._vec
		JS('vec.getPositionFromMatrix(m)')
		return self

	def getScaleFromMatrix(self, m):
		vec = self._vec
		JS('vec.getScaleFromMatrix(m)')
		return self

	def getColumnFromMatrix(self, i, m):
		vec = self._vec
		JS('vec.getColumnFromMatrix(i,m)')
		return self

	def equals(self, v):
		vec = self._vec
		return JS('vec.equals(v)')

	def fromArray(self, a):
		vec = self._vec
		JS('vec.fromArray(a)')
		return self

	def toArray(self):
		vec = self._vec
		return JS('vec.toArray()')

	def clone(self):
		return Vector3( self.x, self.y, self.z )


class _ObjectBase:
	def add(self, child):
		ob = self._object
		JS('ob.add(child)')

class _Camera( _ObjectBase ):

	def updateProjectionMatrix(self):
		ob = self._object
		JS('ob.updateProjectionMatrix()')

class OrthographicCamera( _Camera ):
	def __init__(self, left, right, top, bottom, near, far):
		self._object = JS('new THREE.OrthographicCamera(left, right, top, bottom, near, far)')

class PerspectiveCamera( _Camera ):
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


class Scene:
	def __init__(self):
		self._scene = JS('new THREE.Scene()')

	def add(self, child):
		scene = self._scene
		JS('scene.add(child)')

	def updateMatrixWorld(self):
		scene = self._scene
		JS('scene.updateMatrixWorld()')


class _Renderer:
	def setSize(self, width, height):
		renderer = self._renderer
		JS('renderer.setSize( width, height )')

	def setClearColor(self, red=1.0, green=1.0, blue=1.0, alpha=1.0):
		renderer = self._renderer
		JS('renderer.setClearColor( {r:red, g:green, b:blue}, alpha)')

	def getDomElement(self):
		renderer = self._renderer
		return JS('renderer.domElement')

	def render(self, scn, cam):
		renderer = self._renderer
		return JS('renderer.render(scn, cam)')

class CSS3DRenderer( _Renderer ):
	def __init__(self):
		self._renderer = JS('new THREE.CSS3DRenderer()')


class WebGLRenderer( _Renderer ):
	def __init__(self):
		self._renderer = JS('new THREE.WebGLRenderer()')

	def getContext(self):
		renderer = self._renderer
		return JS('renderer.getContext()')


class _ImageUtils:
	def loadTexture( url ):
		return JS('THREE.ImageUtils.loadTexture(url)')

	def loadTextureCube( urls ):
		## TODO THREE.CubeRefractionMapping()
		JS('var _mapping = new THREE.CubeReflectionMapping()')
		return JS('THREE.ImageUtils.loadTextureCube(urls, _mapping)')

ImageUtils = _ImageUtils()


# THREE.js wrapper for PythonScript
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

class Color:
	def __init__(self, red=1.0, green=1.0, blue=1.0, object=None ):
		if object:
			self[...] = object
		else:
			with javascript: self[...] = new( THREE.Color() )
			self.setRGB(red=red, green=green, blue=blue)

	def setRGB(self, red=1.0, green=1.0, blue=1.0):
		with javascript: self[...].setRGB(red, green, blue)

	@property
	def r(self):
		with javascript: return self[...].r
	@property
	def g(self):
		with javascript: return self[...].g
	@property
	def b(self):
		with javascript: return self[...].b

	def clone(self):
		return Color( red=self.r, green=self.g, blue=self.b )

class Quaternion:
	def __init__(self, object=None ):
		if object:
			self[...] = object
		else:
			with javascript: self[...] = new(THREE.Quaternion())

	@property
	def w(self):
		with javascript: return self[...].w
	@w.setter
	def w(self, value):
		with javascript: self[...].w = value

	@property
	def x(self):
		with javascript: return self[...].x
	@x.setter
	def x(self, value):
		with javascript: self[...].x = value

	@property
	def y(self):
		with javascript: return self[...].y
	@y.setter
	def y(self, value):
		with javascript: self[...].y = value

	@property
	def z(self):
		with javascript: return self[...].z
	@z.setter
	def z(self, value):
		with javascript: self[...].z = value

class Vector3:
	def __init__(self, x=0, y=0, z=0, object=None ):
		if object:
			self[...] = object
		else:
			with javascript: self[...] = new(THREE.Vector3(x,y,z))

	@property
	def x(self):
		with javascript: return self[...].x
	@x.setter
	def x(self, value):
		with javascript: self[...].x = value

	@property
	def y(self):
		with javascript: return self[...].y
	@y.setter
	def y(self, value):
		with javascript: self[...].y = value

	@property
	def z(self):
		with javascript: return self[...].z
	@z.setter
	def z(self, value):
		with javascript: self[...].z = value

	def setComponent(self, index, value):
		self[...].setComponent(index,value)

	def getComponent(self, index):
		self[...].getComponent(index)

	def set(self, x,y,z):
		self[...].set(x,y,z)
	def setX(self, x):
		self[...].setX(x)
	def setY(self, y):
		self[...].setY(y)
	def setZ(self, z):
		self[...].setZ(z)

	def copy(self, other):
		assert isinstance(other, Vector3)
		self.set( other.x, other.y, other.z )
		return self

	def add(self, other):
		assert isinstance(other, Vector3)
		self.set( self.x+other.x, self.y+other.y, self.z+other.z )
		return self

	def __add__(self, other):
		#if JS("{}.toString.call(other) === '[object Object]'"):
		if instanceof(other, Object):
			assert isinstance(other, Vector3)
			return Vector3( self.x+other.x, self.y+other.y, self.z+other.z )
		else:
			return Vector3( self.x+other, self.y+other, self.z+other )

	def __iadd__(self, other):
		if instanceof(other, Object):
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
		if instanceof(other, Object):
			assert isinstance(other, Vector3)
			return Vector3( self.x-other.x, self.y-other.y, self.z-other.z )
		else:
			return Vector3( self.x-other, self.y-other, self.z-other )

	def __isub__(self, other):
		if instanceof(other, Object):
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
		if instanceof(other, Object):
			assert isinstance(other, Vector3)
			return Vector3( self.x*other.x, self.y*other.y, self.z*other.z )
		else:
			return Vector3( self.x*other, self.y*other, self.z*other )

	def __imul__(self, other):
		if instanceof(other, Object):
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
		self[...].applyMatrix3(m[...])
		return self

	def applyMatrix4(self, m):
		self[...].applyMatrix4(m[...])
		return self

	def applyProjection(self, m):
		self[...].applyProjection(m[...])
		return self

	def applyQuaternion(self, q):
		self[...].applyQuaternion(q[...])
		return self

	def transformDirection(self, m):
		self[...].transformDirection(m[...])
		return self

	def divide(self, other):
		assert isinstance(other, Vector3)
		self.set( self.x/other.x, self.y/other.y, self.z/other.z )
		return self

	def divideScalar(self, s):
		self[...].divideScalar(s)  ## takes care of divide by zero
		return self

	def __div__(self, other):
		if instanceof(other, Object):
			assert isinstance(other, Vector3)
			return Vector3( self.x/other.x, self.y/other.y, self.z/other.z )
		else:
			return Vector3( self.x/other, self.y/other, self.z/other )

	def __idiv__(self, other):
		if instanceof(other, Object):
			self.divide( other )
		else:
			self.divideScalar( other )

	def min(self, s):
		self[...].min(s)
		return self
	def max(self, s):
		self[...].max(s)
		return self
	def clamp(self, s):
		self[...].clamp(s)
		return self
	def negate(self):
		self[...].negate()
		return self

	def dot(self, v):
		return self[...].dot(v[...])
	def lengthSq(self):
		return self[...].lengthSq()
	def length(self):
		return self[...].length()
	def lengthManhattan(self):
		return self[...].lengthManhattan()

	def normalize(self):
		self[...].normalize()
		return self

	def setLength(self, l):
		self[...].setLength(l)
		return self

	def lerp(self, v, alpha):
		self[...].lerp(v[...], alpha)
		return self

	def cross(self, v):  ## cross product
		self[...].cross(v[...])
		return self

	def crossVectors(self, a,b):
		self[...].crossVectors(a[...],b[...])
		return self

	def __ixor__(self, other):  ## ^=
		self.cross(other)

	def angleTo(self, v):
		return self[...].angleTo(v[...])

	def distanceTo(self, v):
		return self[...].distanceTo(v[...])

	def distanceToSquared(self, v):
		return self[...].distanceToSquared(v[...])

	def getPositionFromMatrix(self, m):
		self[...].getPositionFromMatrix(m[...])
		return self

	def getScaleFromMatrix(self, m):
		self[...].getScaleFromMatrix(m[...])
		return self

	def getColumnFromMatrix(self, i, m):
		self[...].getColumnFromMatrix(i,m[...])
		return self

	def equals(self, v):
		return self[...].equals(v[...])

	def fromArray(self, a):
		self[...].fromArray(a)
		return self

	def toArray(self):
		return self[...].toArray()

	def clone(self):
		return Vector3( self.x, self.y, self.z )


class _ObjectBase:
	def add(self, child):
		with javascript:
			self[...].add( child[...] )

class _Camera( _ObjectBase ):

	def updateProjectionMatrix(self):
		with javascript:
			self[...].updateProjectionMatrix()

class OrthographicCamera( _Camera ):
	def __init__(self, left, right, top, bottom, near, far):
		#self._object = JS('new THREE.OrthographicCamera(left, right, top, bottom, near, far)')
		with javascript:
			self[...] = new( THREE.OrthographicCamera(left, right, top, bottom, near, far) )

class PerspectiveCamera( _Camera ):
	def __init__(self, fov, aspect, near, far):
		with javascript:
			self[...] = new( THREE.PerspectiveCamera(fov, aspect, near, far) )

	def setLens(self, focalLength, frameSize):
		"""Uses Focal Length (in mm) to estimate and set FOV
		* 35mm (fullframe) camera is used if frame size is not specified;
		* Formula based on http://www.bobatkins.com/photography/technical/field_of_view.html
		"""
		self[...].setLens(focalLength, frameSize)

	def setViewOffset(self, fullWidth, fullHeight, x, y, width, height):
		'''
		Sets an offset in a larger frustum. This is useful for multi-window or
		multi-monitor/multi-machine setups.
		'''
		self[...].setViewOffset(fullWidth, fullHeight, x, y, width, height)

	@property
	def position(self):
		vec = self[...].position
		return Vector3( object=vec )



class Scene:
	def __init__(self):
		with javascript:
			self[...] = new( THREE.Scene() )

	def add(self, child):
		with javascript:
			self[...].add( child[...] )

	def updateMatrixWorld(self):
		with javascript:
			self[...].updateMatrixWorld()


class _Renderer:
	def setSize(self, width, height):
		with javascript: self[...].setSize( width, height )

	def setClearColor(self, red=1.0, green=1.0, blue=1.0, alpha=1.0):
		clr = Color( red=red, green=green, blue=blue )
		with javascript:
			self[...].setClearColor( clr[...], alpha)

	@property
	def domElement(self):
		return self[...].domElement

	def render(self, scn, cam):
		with javascript:
			self[...].render( scn[...], cam[...] )


class CanvasRenderer( _Renderer ):
	def __init__(self):
		with javascript:
			self[...] = new( THREE.CanvasRenderer() )


class CSS3DRenderer( _Renderer ):
	def __init__(self):
		with javascript:
			self[...] = new( THREE.CSS3DRenderer() )


class WebGLRenderer( _Renderer ):
	def __init__(self):
		with javascript:
			self[...] = new( THREE.WebGLRenderer() )

	def getContext(self):
		return self[...].getContext()


class _ImageUtils:
	def loadTexture( url ):
		with javascript:
			return THREE.ImageUtils.loadTexture(url)

	def loadTextureCube( urls ):
		## TODO THREE.CubeRefractionMapping()
		JS('var _mapping = new THREE.CubeReflectionMapping()')
		return JS('THREE.ImageUtils.loadTextureCube(urls, _mapping)')

ImageUtils = _ImageUtils()

class _Material:
	def __setattr__(self, name, value):
		print '__setattr__', name, value
		with javascript:
			self[...][ name ] = value

	def setValues(self, params):
		with javascript:
			self[...].setValues( params[...] )


class MeshBasicMaterial( _Material ):
	def __init__(self, color=None, wireframe=False):
		if not color: color = Color()
		else: #elif isinstance(color, dict):
			color = Color(red=color['red'], green=color['green'], blue=color['blue'])

		with javascript:
			self[...] = new( THREE.MeshBasicMaterial({color:color[...], wireframe:wireframe}) )

	@property
	def color(self):
		return Color( object=self[...].color )


class CubeGeometry:
	def __init__(self, width, height, length):
		with javascript:
			self[...] = new( THREE.CubeGeometry(width, height, length) )


class Mesh:
	def __init__(self, geometry, material):
		self.geometry = geometry
		self.material = material  ## the compile time type system can not know what type this is
		with javascript:
			self[...] = new( THREE.Mesh(geometry[...], material[...]))

	@property
	def position(self):
		vec = self[...].position
		return Vector3( object=vec )

	@property
	def rotation(self):
		vec = self[...].rotation
		return Vector3( object=vec )

	@property
	def scale(self):
		vec = self[...].scale
		return Vector3( object=vec )

	@property
	def quaternion(self):
		return Quaternion( object=self[...].quaternion )
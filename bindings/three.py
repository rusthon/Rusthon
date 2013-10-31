# THREE.js wrapper for PythonJS
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

	def getHex(self):
		with javascript:
			return self[...].getHex()

	def setHex(self, hex):
		with javascript:
			self[...].setHex(hex)

	def getHexString(self):
		with javascript:
			return self[...].getHexString()

	def getHSL(self):
		with javascript:
			return self[...].getHSL()

	def setHSL(self, hex):
		with javascript:
			self[...].setHSL(hex)


	def setStyle(self, style):
		with javascript:
			self[...].setStyle(style)

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


########################## helpers ############################
def rgb_to_hex( red=1.0, green=1.0, blue=1.0, as_string=False ):
	clr = Color( red=red, green=green, blue=blue )
	if as_string:
		return clr.getHexString()
	else:
		return clr.getHex()

def rgb_to_hsl( red=1.0, green=1.0, blue=1.0 ):
	clr = Color( red=red, green=green, blue=blue )
	return clr.getHSL()



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
			with javascript:
				self[...] = new(THREE.Vector3(x,y,z))

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

class Euler:
	def __init__(self, x=0, y=0, z=0, object=None ):
		if object:
			self[...] = object
		else:
			with javascript:
				self[...] = new(THREE.Euler(x,y,z))

	def set(self, x,y,z):
		self[...].set(x,y,z)

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

	def setFromRotationMatrix( m, order=None ):
		#assert isinstance(m, Matrix3x3)
		with javascript:
			self[...].setFromRotationMatrix(m[...], order)

	def setFromQuaternion(self, quat, order=None, update=True ):
		with javascript:
			self[...].setFromQuaternion( quat[...], order, update)

	def reorder(self):
		## warning: discards revolution information
		with javascript:
			self[...].reorder()

	def equals(self, other):
		with javascript:
			return self[...].equals( other[...] )

	def clone(self):
		return Euler( x=self.x, y=self.y, z=self.z )


class Face3:
	def __init__(self, a, b, c, normal=None, color=None, materialIndex=None):
		if normal: normal = normal[...]
		if color: color = color[...]
		with javascript:
			self[...] = new( THREE.Face3(a,b,c, normal, color, materialIndex))

	@property
	def normal(self):
		vec = self[...].normal
		return Vector3( object=vec )

	@property
	def vertexNormals(self):
		return self[...].vertexNormals  ## TODO wrap array in list

	@property
	def color(self):
		vec = self[...].position
		return Vector3( object=vec )

	@property
	def vertexColors(self):
		return self[...].vertexColors  ## TODO wrap array in list

	@property
	def centroid(self):
		vec = self[...].centroid
		return Vector3( object=vec )


class Object3D:
	def __init__(self, pointer=None):
		with javascript:
			if pointer:
				self[...] = pointer
			else:
				self[...] = new( THREE.Object3D() )

	@property
	def parent(self):
		with javascript: ptr = self[...].parent
		if ptr:
			## TODO check what type parent is and return the correct subclass
			## not just Object3D.
			return Object3D( pointer=ptr )

	@property
	def up(self):
		vec = self[...].up
		return Vector3( object=vec )

	@property
	def position(self):
		vec = self[...].position
		return Vector3( object=vec )

	@property
	def rotation(self):
		vec = self[...].rotation
		return Euler( object=vec )

	@property
	def scale(self):
		vec = self[...].scale
		return Vector3( object=vec )

	@property
	def quaternion(self):
		return Quaternion( object=self[...].quaternion )

	def setRotationFromAxisAngle(self, axis, angle):
		with javascript:
			self[...].setRotationFromAxisAngle(axis[...], angle)

	def setRotationFromEuler(self, euler):
		with javascript:
			self[...].setRotationFromEuler( euler[...] )

	def setRotationFromMatrix(self, m):
		with javascript:
			self[...].setRotationFromMatrix(m[...])

	def setRotationFromQuaternion(self, quat):
		with javascript:
			self[...].setRotationFromQuaternion( quat[...] )

	def rotateX(self, angle):	# rotate in local space
		with javascript:
			self[...].rotateX( angle )
	def rotateY(self, angle):
		with javascript:
			self[...].rotateY( angle )
	def rotateZ(self, angle):
		with javascript:
			self[...].rotateZ( angle )

	def translateX(self, distance):		# translate in local space
		with javascript:
			self[...].translateX( distance )
	def translateY(self, distance):
		with javascript:
			self[...].translateY( distance )
	def translateZ(self, distance):
		with javascript:
			self[...].translateZ( distance )

	def localToWorld(self, vec):
		with javascript:
			v = self[...].localToWorld( vec[...] )
		return Vector3( object=v )

	def worldToLocal(self, vec):
		with javascript:
			v = self[...].worldToLocal( vec[...] )
		return Vector3( object=v )

	def lookAt(self, vec):
		assert not self.parent  ## this only works for objects without a parent
		with javascript:
			self[...].lookAt( vec[...] )

	def add(self, child):
		with javascript:
			self[...].add( child[...] )

	def remove(self, child):
		with javascript:
			self[...].remove( child[...] )

	def traverse(self, jsfunc):  ## TODO support pythonJS functions
		with javascript:
			self[...].traverse( jsfunc )

	def getObjectById(self, ID, recursive=True ):  ## this returns unwrapped THREE.Object3D
		with javascript:
			return self[...].getObjectById( ID, recursive )

	def getChildByName(self, name, recursive=True ):  ## this returns unwrapped THREE.Object3D
		with javascript:
			return self[...].getChildByName( name, recursive )

	def getDescendants(self):
		with javascript:
			return self[...].getDescendants()

	def updateMatrix(self):
		with javascript:
			self[...].updateMatrix()

	def updateMatrixWorld(self):
		with javascript:
			self[...].updateMatrixWorld()


	def clone(self, other, recursive=True):
		with javascript:
			self[...].clone( other, recursive )



class _Camera( Object3D ):

	def updateProjectionMatrix(self):
		with javascript:
			self[...].updateProjectionMatrix()

class OrthographicCamera( _Camera ):
	def __init__(self, left, right, top, bottom, near, far):
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





class Scene:
	def __init__(self):
		with javascript:
			self[...] = new( THREE.Scene() )

	def add(self, child):
		with javascript:
			self[...].add( child[...] )

	def remove(self, child):
		print 'Scene.remove', child
		with javascript:
			self[...].remove( child[...] )

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
	def __init__(self, antialias=False ):
		## note: antialias may not work depending on hardware and/or browser support,
		## for example: Chrome 27 fails, while on the same machine FireFox 20 works.

		with javascript:
			self[...] = new( THREE.WebGLRenderer( {antialias:antialias}) )

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

class AmbientLight( Object3D ):
	def __init__(self, color=None, intensity=1.0 ):
		if color:
			hx = rgb_to_hex(
				red=color['red'] * intensity, 
				green=color['green'] * intensity, 
				blue=color['blue'] * intensity
			)
		else:
			hx = rgb_to_hex(red=intensity, green=intensity, blue=intensity )

		with javascript:
			self[...] = new( THREE.AmbientLight( hx ) )


class DirectionalLight( Object3D ):
	## TODO shadow map stuff
	def __init__(self, color=None, intensity=1.0 ):
		if color:
			hx = rgb_to_hex( red=color['red'], green=color['green'], blue=color['blue'] )
		else:
			hx = rgb_to_hex( red=1, green=1, blue=1 )

		with javascript:
			self[...] = new( THREE.DirectionalLight( hx, intensity ) )


class PointLight( Object3D ):
	def __init__(self, color=None, intensity=1.0, distance=0 ):
		if color:
			hx = rgb_to_hex( red=color['red'], green=color['green'], blue=color['blue'] )
		else:
			hx = rgb_to_hex( red=1, green=1, blue=1 )

		with javascript:
			self[...] = new( THREE.PointLight( hx, intensity, distance ) )

class SpotLight( Object3D ):
	## TODO shadow map stuff
	def __init__(self, color=None, intensity=1.0, distance=0, angle=1.0472, exponent=10 ):
		if color:
			hx = rgb_to_hex( red=color['red'], green=color['green'], blue=color['blue'] )
		else:
			hx = rgb_to_hex( red=1, green=1, blue=1 )

		with javascript:
			self[...] = new( THREE.SpotLight( hx, intensity, distance, angle, exponent ) )

class HemisphereLight( Object3D ):
	def __init__(self, sky_color=None, ground_color=None, intensity=1.0):
		if sky_color:
			shx = rgb_to_hex( red=sky_color['red'], green=sky_color['green'], blue=sky_color['blue'] )
		else:
			shx = rgb_to_hex( red=1, green=1, blue=1 )
		if ground_color:
			ghx = rgb_to_hex( red=ground_color['red'], green=ground_color['green'], blue=ground_color['blue'] )
		else:
			ghx = rgb_to_hex( red=1, green=1, blue=1 )

		with javascript:
			self[...] = new( THREE.HemisphereLight( shx, ghx, intensity ) )

class AreaLight( Object3D ):
	def __init__(self, color=None, intensity=1.0 ):
		if color:
			hx = rgb_to_hex( red=color['red'], green=color['green'], blue=color['blue'] )
		else:
			hx = rgb_to_hex( red=1, green=1, blue=1 )

		with javascript:
			self[...] = new( THREE.AreaLight( hx, intensity ) )


class _Material:
	_color_props = []

	def __init__(self, **kwargs):
		params = kwargs  ## no need to copy
		keys = kwargs.keys()
		for name in self._color_props:  ## subclasses can redefine this
			if name in keys:
				color = kwargs[ name ]
				color = Color(red=color['red'], green=color['green'], blue=color['blue'])
				params[ name ] = color[...]

		self._reset_material( params )  ## subclasses need to implement this

	def __getattr__(self, name):
		with javascript:
			return self[...][ name ]

	def __setattr__(self, name, value):
		with javascript:
			self[...][ name ] = value

	def setValues(self, **params):
		with javascript:
			self[...].setValues( params[...] )


class MeshBasicMaterial( _Material ):
	_color_props = ['color']

	def _reset_material(self, params):
		with javascript:
			## the three.js API takes an javascript-object as params to configure the material
			self[...] = new( THREE.MeshBasicMaterial( params[...] ) )

	@property
	def color(self):
		return Color( object=self[...].color )


class MeshLambertMaterial( _Material ):
	_color_props = ['color', 'ambient', 'emissive']

	def _reset_material(self, params):
		with javascript:
			self[...] = new( THREE.MeshLambertMaterial( params[...] ) )

	@property
	def color(self):
		return Color( object=self[...].color )
	@property
	def ambient(self):
		return Color( object=self[...].ambient )
	@property
	def emissive(self):
		return Color( object=self[...].emissive )


class MeshPhongMaterial( _Material ):
	_color_props = ['color', 'ambient', 'emissive', 'specular']

	def _reset_material(self, params):
		with javascript:
			self[...] = new( THREE.MeshPhongMaterial( params[...] ) )

	@property
	def color(self):
		return Color( object=self[...].color )
	@property
	def ambient(self):
		return Color( object=self[...].ambient )
	@property
	def emissive(self):
		return Color( object=self[...].emissive )
	@property
	def specular(self):
		return Color( object=self[...].specular )


class MeshNormalMaterial( _Material ):
	def _reset_material(self, params):
		with javascript:
			self[...] = new( THREE.MeshNormalMaterial( params[...] ) )


class MeshDepthMaterial( _Material ):
	def _reset_material(self, params):
		with javascript:
			self[...] = new( THREE.MeshDepthMaterial( params[...] ) )


class ShaderMaterial( _Material ):
	def _reset_material(self, params):
		with javascript:
			self[...] = new( THREE.ShaderMaterial( params[...] ) )



class _Geometry:
	def __getattr__(self, name):
		with javascript:
			return self[...][ name ]

	def __setattr__(self, name, value):
		with javascript:
			self[...][ name ] = value

class CircleGeometry( _Geometry ):
	def __init__(self, radius=50, segments=8, thetaStart=0, thetaEnd=None ):
		with javascript:
			self[...] = new( THREE.CircleGeometry(radius, segments, thetaStart, thetaEnd) )

class CubeGeometry( _Geometry ):
	def __init__(self, width, height, length):
		with javascript:
			self[...] = new( THREE.CubeGeometry(width, height, length) )

class CylinderGeometry( _Geometry ):
	def __init__(self, radiusTop=20, radiusBottom=20, height=100, radialSegments=8, heightSegments=1, openEnded=False):
		with javascript:
			self[...] = new( THREE.CylinderGeometry(radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded) )


class ExtrudeGeometry( _Geometry ):
	def __init__(self, shapes, options ):
		with javascript:
			self[...] = new( THREE.ExtrudeGeometry( shapes[...], options[...] ) )

	def addShape(self, shape, options ):
		with javascript:
			self[...].addShape( shape[...], options[...] )

class TextGeometry( ExtrudeGeometry ):
	def __init__(self, text, size=100, curveSegments=4, font='helvetiker', weight='normal', style='normal', height=50, bevelThickness=10, bevelSize=8, bevelEnabled=False ):
		assert weight in ('normal','bold')
		assert style in ('normal', 'italics')
		params = {
			'size':size,			## FontUtils.generateShapes
			'curveSegments':curveSegments,
			'font'  : font,
			'weight': weight,
			'style' : style,
			'height': height,		## ExtrudeGeometry.call
			'bevelThickness' : bevelThickness, 
			'bevelSize'      : bevelSize,
			'bevelEnabled'   : bevelEnabled
		}
		with javascript:
			self[...] = new( THREE.TextGeometry( text, params[...] ) )

class LatheGeometry( _Geometry ):
	def __init__(self, points, segments, phiStart, phiLength):
		## TODO convert points and segments from lists to JSArray
		with javascript:
			self[...] = new( THREE.LatheGeometry(points, segments, phiStart, phiLength))

class PolyhedronGeometry( _Geometry ):
	def __init__(self, vertices, faces, radius=1.0, detail=0 ):
		with javascript:
			self[...] = new( THREE.PolyhedronGeometry( vertices, faces, radius, detail ) )

class IcosahedronGeometry( PolyhedronGeometry ):
	def __init__(self, radius=1.0, detail=0 ):
		with javascript:
			self[...] = new( THREE.IcosahedronGeometry( radius, detail ) )

class OctahedronGeometry( PolyhedronGeometry ):
	def __init__(self, radius=1.0, detail=0 ):
		with javascript:
			self[...] = new( THREE.OctahedronGeometry( radius, detail ) )



class Mesh( Object3D ):
	def __init__(self, geometry, material):
		self.geometry = geometry
		self.material = material  ## the compile time type system can not know what type this is
		with javascript:
			self[...] = new( THREE.Mesh(geometry[...], material[...]))

class _Controls:
	def update(self):
		clock = self.clock
		with javascript:
			delta = clock.getDelta()
			self[...].update( delta )

class FlyControls( _Controls ):
	def __init__(self, ob, movementSpeed=1000, autoForward=False, dragToLook=False ):
		with javascript:
			self[...] = new( THREE.FlyControls(ob[...]) )
			self[...].movementSpeed = movementSpeed
			self[...].autoForward = autoForward
			self[...].dragToLook = dragToLook
			clock = new( THREE.Clock() )
		self.clock = clock


class OrbitControls( _Controls ):
	def __init__(self, ob):
		with javascript:
			self[...] = new( THREE.OrbitControls(ob[...]) )
			clock = new( THREE.Clock() )
		self.clock = clock

class TrackballControls( _Controls ):
	def __init__(self, ob, rotateSpeed=1.0, zoomSpeed=1.2, panSpeed=0.8, noZoom=False, noPan=False, staticMoving=True, dynamicDampingFactor=0.3):
		with javascript:
			self[...] = new( THREE.TrackballControls(ob[...]) )
			self[...].rotateSpeed = rotateSpeed
			self[...].zoomSpeed = zoomSpeed
			self[...].panSpeed = panSpeed
			self[...].noZoom = noZoom
			self[...].noPan = noPan
			self[...].staticMoving = staticMoving
			self[...].dynamicDampingFactor = dynamicDampingFactor
			clock = new( THREE.Clock() )
		self.clock = clock

# Physijs wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

def Physijs_initialize( worker='/libs/physijs/physijs_worker.js', ammo='/libs/ammo/ammo.js'):
	with javascript:
		Physijs.scripts.worker = worker
		Physijs.scripts.ammo = ammo


def PhysijsMaterial( material, friction=0.8, restitution=0.2):  ## TODO should this be wrapped in its own class?
	print 'converting material to physijs material', material
	with javascript:
		return Physijs.createMaterial( material[...], friction, restitution )

class _Eventable:
	def addEventListener(self, name, callback):
		with javascript:
			self[...].addEventListener( name, callback )

class PointConstraint:
	def __init__(self, object1, object2, position=None):
		'''
		if position is not given it defaults to object2.
		'''
		with javascript:
			self[...] = new( Physijs.PointConstraint(object1[...], object2[...], position[...]) )


class HingeConstraint:
	def __init__(self, object1, object2, position=None, axis=None):
		'''
		if axis is not given it defaults to position, and position becomes object2.
		in other words, if you want to define position you must also provide the axis.
		'''
		with javascript:
			self[...] = new( Physijs.PointConstraint(object1[...], object2[...], position[...], axis[...]) )

	def setLimits(self, low, high, bias_factor, relaxation_factor=0.0):
		'''
			* low = minimum angle in radians
			* high = maximum angle in radians
			* bias_factor = applied as a factor to constraint error
			* relaxation_factor = controls bounce (0.0 == no bounce)
		'''
		with javascript:
			self[...].setLimits( low, high, bias_factor, relaxation_factor )

	def enableAngularMotor(self, velocity, acceleration):
		with javascript:
			self[...].enableAngularMotor( velocity, acceleration )

	def disableAngularMotor(self):
		with javascript:
			self[...].disableMotor()  ## is this right Chandler?


class SliderConstraint:
	def __init__(self, object1, object2, position=None, axis=None):
		'''
		if axis is not given it defaults to position, and position becomes object2.
		in other words, if you want to define position you must also provide the axis.
		'''
		with javascript:
			self[...] = new( Physijs.SliderConstraint(object1[...], object2[...], position[...], axis[...]) )


	def setLimits(self, lin_low, lin_high, ang_low, ang_high ):
		with javascript:
			self[...].setLimits( lin_low, lin_high, ang_low, ang_high )

	def setRestitution(self, linear, angular):
		with javascript:
			self[...].setRestitution( linear, angular )

	def enableLinearMotor(self, velocity, acceleration):
		with javascript:
			self[...].enableLinearMotor( velocity, acceleration )

	def disableLinearMotor(self):
		with javascript:
			self[...].disableLinearMotor()

	def enableAngularMotor(self, velocity, acceleration):
		with javascript:
			self[...].enableAngularMotor( velocity, acceleration )

	def disableAngularMotor(self):
		with javascript:
			self[...].disableAngularMotor()


class ConeTwistConstraint:
	def __init__(self, object1, object2, position=None):
		if position is None:  ## cone requires position
			raise TypeError

		with javascript:
			self[...] = new( Physijs.SliderConstraint(object1[...], object2[...], position[...]) )

	def setLimit(self, x=0, y=0, z=0):
		with javascript:
			self[...].setLimit( x,y,z )

	def enableMotor(self):
		with javascript:
			self[...].enableMotor()

	def disableMotor(self):
		with javascript:
			self[...].disableMotor()

	def setMaxMotorImpulse(self, impulse ):
		with javascript:
			self[...].setMaxMotorImpulse( impulse )

	def setMotorTarget(self, target):
		with javascript:
			self[...].setMotorTarget( target[...] )


class DOFConstraint:
	def __init__(self, object1, object2, position=None):
		with javascript:
			self[...] = new( Physijs.DOFConstraint(object1[...], object2[...], position[...]) )

	def setLinearLowerLimit(self,  x=0, y=0, z=0 ):
		with javascript:
			self[...].setLinearLowerLimit( {x:x, y:y, z:z} )

	def setLinearUpperLimit(self,  x=0, y=0, z=0 ):
		with javascript:
			self[...].setLinearUpperLimit( {x:x, y:y, z:z} )

	def setAngularLowerLimit(self,  x=0, y=0, z=0 ):
		with javascript:
			self[...].setAngularLowerLimit( {x:x, y:y, z:z} )

	def setAngularUpperLimit(self,  x=0, y=0, z=0 ):
		with javascript:
			self[...].setAngularUpperLimit( {x:x, y:y, z:z} )


	def enableAngularMotor(self, which):  ## what type is "which"?
		with javascript:
			self[...].enableAngularMotor( which )

	def disableAngularMotor(self, which):  ## what type is "which"?
		with javascript:
			self[...].disableAngularMotor( which )

	def configureAngularMotor(self, which, low, high, velocity, max_force):
		with javascript:
			self[...].configureAngularMotor( which, low, high, velocity, max_force )


class PhysijsScene( _Eventable ):
	def __init__(self, time_step=0.016666666666666666, rate_limit=True ):
		with javascript:
			self[...] = new( Physijs.Scene({fixedTimeStep:time_step, rateLimit:rate_limit}) )

	def addConstraint(self, cns, show_marker=False):
		with javascript:
			self[...].addConstraint( cns[...], show_marker )

	def removeConstraint(self, cns):
		with javascript:
			self[...].removeConstraint( cns[...] )

	def add(self, ob):
		'phyisjs-SCENE.add', ob
		with javascript:
			self[...].add( ob[...] )

	def remove(self, ob):
		with javascript:
			self[...].remove( ob[...] )

	def setFixedTimeStep(self, t):
		with javascript:
			self[...].setFixedTimeStep( t )

	def setGravity(self, x=0, y=0, z=0):
		with javascript:
			self[...].setGravity( {x:x, y:y, z:z} )

	def simulate(self, time_step=None, max_substeps=1):
		with javascript:
			self[...].simulate( time_step, max_substeps )

class PhysijsMesh:
	def __init__(self, geo, material, mass=1.0, friction=0.8, restitution=0.2 ):
		mat = PhysijsMaterial( material, friction=friction, restitution=restitution )
		print 'Physijs.mat', mat
		self.material = mat  ## note this is unwrapped
		with javascript:
			self[...] = new( Physijs.Mesh(geo[...], mat, mass) )

	def applyCentralImpulse(self, x=0, y=0, z=0):
		with javascript:
			self[...].applyCentralImpulse( {x:x, y:y, z:z} )

	def applyImpulse(self, x=0, y=0, z=0, offset_x=0, offset_y=0, offset_z=0):
		with javascript:
			self[...].applyImpulse( {x:x, y:y, z:z}, {x:offset_x, y:offset_y, z:offset_z} )

	def applyCentralForce(self, x=0, y=0, z=0):
		with javascript:
			self[...].applyCentralForce( {x:x, y:y, z:z} )

	def applyForce(self, x=0, y=0, z=0, offset_x=0, offset_y=0, offset_z=0):
		with javascript:
			self[...].applyForce( {x:x, y:y, z:z}, {x:offset_x, y:offset_y, z:offset_z} )


	def getAngularVelocity(self):
		with javascript:
			return self[...].getAngularVelocity()  ## TODO, wrap this in a Vector3

	def setAngularVelocity(self, x=0, y=0, z=0):
		with javascript:
			self[...].setAngularVelocity( {x:x, y:y, z:z} )


	def getLinearVelocity(self):
		with javascript:
			return self[...].getLinearVelocity()  ## TODO, wrap this in a Vector3

	def setLinearVelocity(self, x=0, y=0, z=0):
		with javascript:
			self[...].setLinearVelocity( {x:x, y:y, z:z} )

	def setAngularFactor(self, x=0, y=0, z=0):
		with javascript:
			self[...].setAngularFactor( {x:x, y:y, z:z} )

	def setLinearFactor(self, x=0, y=0, z=0):
		with javascript:
			self[...].setLinearFactor( {x:x, y:y, z:z} )

	## slightly different API - TODO test if this works
	def setLinearDamping(self, x=0, y=0, z=0):
		with javascript:
			self[...].setDamping( {x:x, y:y, z:z}, None )
	## slightly different API - TODO test if this works
	def setAngularDamping(self, x=0, y=0, z=0):
		with javascript:
			self[...].setDamping( None, {x:x, y:y, z:z} )


	def setCcdMotionThreshold(self, threshold):
		with javascript:
			self[...].setCcdMotionThreshold( threshold )

	def setCcdSweptSphereRadius(self, radius):
		with javascript:
			self[...].setCcdSweptSphereRadius( radius )


class PhysijsPlaneMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass=1.0, friction=0.8, restitution=0.2 ):
		mat = PhysijsMaterial( material, friction=friction, restitution=restitution )
		print 'Physijs.mat', mat
		self.material = mat  ## note this is unwrapped

		with javascript:
			self[...] = new( Physijs.PlaneMesh(geo[...], mat, mass) )

class PhysijsHeightfieldMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass=1.0, friction=0.8, restitution=0.2, xdiv=16, ydiv=16 ):
		mat = PhysijsMaterial( material, friction=friction, restitution=restitution )
		print 'Physijs.mat', mat
		self.material = mat  ## note this is unwrapped

		with javascript:
			self[...] = new( Physijs.HeightfieldMesh(geo[...], mat, mass, xdiv, ydiv) )


class PhysijsBoxMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass=1.0, friction=0.8, restitution=0.2 ):
		mat = PhysijsMaterial( material, friction=friction, restitution=restitution )
		print 'Physijs.mat', mat
		self.material = mat  ## note this is unwrapped
		with javascript:
			self[...] = new( Physijs.BoxMesh(geo[...], mat, mass) )


class PhysijsSphereMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass=1.0, friction=0.8, restitution=0.2 ):
		with javascript:
			self[...] = new( Physijs.SphereMesh(geo[...], material[...], mass) )


class PhysijsCylinderMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass ):
		with javascript:
			self[...] = new( Physijs.CylinderMesh(geo[...], material[...], mass) )

class PhysijsCapsuleMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass ):
		with javascript:
			self[...] = new( Physijs.CapsuleMesh(geo[...], material[...], mass) )

class PhysijsConeMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass ):
		with javascript:
			self[...] = new( Physijs.ConeMesh(geo[...], material[...], mass) )

class PhysijsConcaveMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass ):
		with javascript:
			self[...] = new( Physijs.ConcaveMesh(geo[...], material[...], mass) )


class PhysijsConvexMesh( PhysijsMesh ):
	def __init__(self, geo, material, mass ):
		with javascript:
			self[...] = new( Physijs.ConvexMesh(geo[...], material[...], mass) )


class Vehicle:
	def __init__(self, mesh, tuning ):
		with javascript:
			self[...] = new( Physijs.Vehicle(mesh[...], tuning) )

	def addWheel(self, geo, material, connection_point, direction, axle, rest_length, radius, is_front, tuning):
		with javascript:
			self[...].addWheel(
				geo[...], 
				material[...], 
				connection_point[...], 
				direction[...], 
				axle[...], 
				rest_length, 
				radius, 
				is_front, 
				tuning
			)


	def setSteering(self, amount, wheel):
		with javascript:
			self[...].setSteering( amount, wheel[...] )

	def setBrake(self, amount, wheel):
		with javascript:
			self[...].setBrake( amount, wheel[...] )

	def applyEngineForce(self, amount, wheel):
		with javascript:
			self[...].applyEngineForce( amount, wheel[...] )


## TODO Physijs.VehicleTuning
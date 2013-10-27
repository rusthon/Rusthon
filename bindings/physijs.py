# Physijs wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

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


class PhysijsScene:
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
		with javascript:
			self[...].add( ob )

	def remove(self, ob):
		with javascript:
			self[...].remove( ob )

	def setFixedTimeStep(self, t):
		with javascript:
			self[...].setFixedTimeStep( t )

	def setGravity(self, g):
		with javascript:
			self[...].setGravity( g )

	def simulate(self, time_step, max_substeps):
		with javascript:
			self[...].simulate( time_step, max_substeps )

class PhysijsMesh:
	def __init__(self, geo, material, mass ):
		with javascript:
			self[...] = new( Physijs.Mesh(geo[...], material[...], mass) )

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



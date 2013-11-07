# Tween.js wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

class _TweenManagerSingleton:
	'''
	Outside code should only call the update method.
	Notes:
		. This class only wraps the raw tween js objects,
		not the Tween pythonjs instances.
		. The Tween class below on start calls start_tween
		here because the Tween.js API will not check if
		a tween is already playing.
	'''
	def __init__(self):
		self.reset()
		self.paused = False

	def reset(self):
		self._tweens = []  ## raw tween js objects
		with javascript: arr = TWEEN.getAll()
		self._tweens.js_object = arr

	@property
	def raw_tweens(self):
		return self._tweens

	def update(self):
		if not self.paused:
			with javascript:
				TWEEN.update()

TweenManager = _TweenManagerSingleton()

@pythonjs.init_callbacks
@pythonjs.property_callbacks
class Tween:
	'''
	This wrapper class for TWEEN.Tween is slightly different that the Tween.js API,
	time is given in seconds, the callbacks: on_start, on_complete, and on_update
	will pass as the first argument this high level wrapper self, and source,
	note that source is not the raw javascript object.  A Tween can be initialized
	without a source, and then later set_source can be called.  It is safe to set
	a target before setting a source as well, using set_target.

	A helper method retarget, is provided that can change the target of this Tween 
	while keeping your callbacks intact.  You only call retarget when this Tween is 
	currently active.  This solves a problem of the Tween.js API where dynamically
	setting the target inplace only works if the values are greater than the state
	of the current source or greater than the previous target.

	Notes:
		on_start_js, on_update_js, on_complete_js
		these should only be used if you know what you are doing.

		the tween.js API will not allow changing the tween duration time
		after tween.to has been called.  Can we call tween.to multiple times?

	'''
	def __init__(self, source=None, on_start=None, on_update=None, seconds=1.0, delay=0, repeat=0, yoyo=False, on_complete=None, on_start_js=None, on_update_js=None, on_complete_js=None ):
		self.source = source
		self.source_is_raw = False
		self.on_start = on_start
		self.on_update = on_update
		self.on_complete = on_complete
		self._on_start_js = on_start_js
		self._on_update_js = on_update_js
		self._on_complete_js = on_complete_js
		self._seconds = seconds
		self._seconds_remaining = seconds
		self.active = True
		self.started = False

		self.target = None
		self.target_is_raw = False
		self.target_armed = False

		self._delay = delay
		self._repeat = repeat
		self._yoyo = yoyo

		if source:
			self.set_source( source )

	def set_source(self, source=None, source_js=None, clone=False):
		'''
		Sometimes we need to create the Tween without a source, and then later set the source,
		for example: this helps with integration with GoogleBlockly where we need to create the
		Tween instance first with a target and later set a source.
		Use source_js to pass a raw javascript object to use as source, only use this if you
		know what your doing.
		'''

		self._clone = clone

		if source:
			self.source = source
			source = source[...]  ## unwrap
		elif source_js:
			self.source = source_js
			self.source_is_raw = True
			source = source_js
		else:
			raise TypeError

		print '--tween set_source', source

		on_start_method = self._on_start
		on_update_method = self._on_update
		on_complete_method = self._on_complete

		on_start_js = self._on_start_js
		on_update_js = self._on_update_js
		on_complete_js = self._on_complete_js

		if self.source_restart:
			for key in self.source_restart:
				value = self.source_restart
				source[key] = value
		elif self._clone:  ## the low-level javascript object needs a clone method
			source = source.clone()
			self.source_restart = source


		with javascript:
			tween = new( TWEEN.Tween( source ) )
			if on_start_js:
				tween.onStart( on_start_js )
			else:
				tween.onStart( lambda : on_start_method([this]) )

			if on_update_js:
				tween.onUpdate( on_update_js )
			else:
				tween.onUpdate( lambda delta: on_update_method([this, delta],{}) )

			if on_complete_js:
				tween.onComplete( on_complete_js )
			else:
				tween.onComplete( lambda : on_complete_method([this]) )

			self[...] = tween

		if self.target and not self.target_armed and self._seconds:
			if self.target_is_raw:
				self.to( target_js=self.target, seconds=self._seconds )
			else:
				self.to( target=self.target, seconds=self._seconds )


	def set_target(self, target=None, target_js=None ):
		if target:
			self.target = target
		elif target_js:
			self.target = target_js
			self.target_is_raw = True
		else:
			raise TypeError

		if self.target_armed:  ## redirect target
			if self.target_is_raw:
				self.to( target_js=self.target, seconds=self._seconds )
			else:
				self.to( target=self.target, seconds=self._seconds )


	def set_seconds(self, seconds=1.0):
		self._seconds = seconds
		self._seconds_remaining = seconds
		if self.started and self.target:
			if self.target_is_raw:
				self.to( target_js=self.target, seconds=seconds)
			else:
				self.to( target=self.target, seconds=seconds)

	@returns( float )
	@property
	def seconds(self):
		return self._seconds
	@seconds.setter
	def seconds(self, v):
		self.set_seconds( v )



	#############################################
	def _on_start(self, jsob):
		print '-on-start', jsob
		self.started = True
		if self.on_start:
			self.on_start( self, self.source )

	def _on_update(self, jsob, delta):
		print '-on-update', jsob, delta
		if Number.isNaN(delta):
			TweenManager.paused = True
			raise TypeError

		self._seconds_remaining = self._seconds - (self._seconds * delta)

		if self.sync_object:
			with javascript:
				for key in jsob:
					value = jsob[key]
					print 'jsob:', key, value
					with python:
						setattr( self.sync_object, key, value, property=True )

		if self.on_update:
			self.on_update( self, self.source, delta )

	def _on_complete(self, jsob):
		print '-on-complete', jsob
		self.active = False
		self.target_armed = False  ## need this so the tween can be restarted
		if self.on_complete:
			self.on_complete( self, self.source )

	#############################################

	def to(self, target=None, target_js=None, seconds=1.0):
		print 'TWEEN.TO', target, target_js, seconds
		if seconds is None:
			raise TypeError
		self._seconds = seconds
		self._seconds_remaining = seconds
		if target:
			self.target = target
			target = target[...]
		elif target_js:
			self.target = target_js
			self.target_is_raw = True
			target = target_js
		else:
			raise TypeError

		self.target_armed = True
		with javascript:
			self[...].to( target, seconds*1000 )

	def start(self):
		print '--starting tweeen'
		## set these in case they were set from __init__
		if self._yoyo: self.set_yoyo( self._yoyo )
		if self._delay: self.set_delay( self._delay )
		if self._repeat: self.set_repeat( self._repeat )

		if self.target and not self.target_armed:
			if self.target_is_raw:
				self.to( target_js=self.target, seconds=self._seconds )
			else:
				self.to( target=self.target, seconds=self._seconds )

		with javascript:
			self[...].start()

	def stop(self):
		## it is safe to call stop multiple times,
		## it will only be removed once from TWEEN._tweens
		self.active = False
		with javascript:
			self[...].stop()

	def set_delay(self, seconds):
		self._delay = seconds
		with javascript:
			self[...].delay( seconds*1000 )

	@returns( float )
	@property
	def delay(self):
		return self._delay
	@delay.setter
	def delay(self, v):
		self.set_delay( v )

	def set_repeat(self, amount):
		self._repeat = amount
		with javascript:
			self[...].repeat( amount )


	@returns( int )
	@property
	def repeat(self):
		return self._repeat
	@repeat.setter
	def repeat(self, v):
		self.set_repeat( v )


	def set_yoyo(self, yoyo):
		self._yoyo = yoyo
		with javascript:
			self[...].yoyo( yoyo )

	@returns( bool )
	@property
	def yoyo(self):
		return self._yoyo
	@yoyo.setter
	def yoyo(self, v):
		self.set_yoyo( v )


	## TODO test these
	def set_easing(self, easing ):
		with javascript:
			self[...].easing( easing )

	def set_interpolation(self, interp):
		with javascript:
			self[...].interpolation( interp )

	def chain(self, chain):
		'''
		The Tween API allows for multiple tweens to be chained,
		they all get started at the same time when this tween
		has finished.
		'''
		with javascript:
			self[...].chain( chain )



	############# retarget helper #############
	def retarget(self, target):
		assert self._seconds_remaining
		assert self.active

		on_complete = self.on_complete ## get this so that when we call stop below, this will not get triggered
		self.on_complete = None
		ob = self.source
		started = self.started
		on_start_method = self._on_start
		on_update_method = self._on_update
		on_complete_method = self._on_complete

		with javascript:
			self[...].stop()
			tween = new( TWEEN.Tween( ob[...] ) )
			if not started: tween.onStart( lambda : on_start_method([this]) )
			tween.onUpdate( lambda delta: on_update_method([this, delta]) )
			tween.onComplete( lambda : on_complete_method([this]) )
			self[...] = tween

		self.on_complete = on_complete
		self.to( target, self._seconds_remaining )
		self.start()

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

class Tween:
	'''
	This wrapper class for TWEEN.Tween is slightly different that the Tween.js API,
	time is given in seconds, and the callbacks: on_start, on_complete, and on_update
	will pass as the first argument this high level wrapper self, and source,
	note that source is not the raw javascript object.  Otherwise the API is the same.

	A helper method retarget, is provided that can change the target of this Tween 
	while keeping your callbacks intact.  You only call retarget when this Tween is 
	currently active.  This solves a problem of the Tween.js API where dynamically
	setting the target inplace only works if the values are greater than the state
	of the current source or greater than the previous target.

	Note:
		on_start_js, on_update_js, on_complete_js
		these should only be used if you know what you are doing.

	'''
	def __init__(self, ob, on_start=None, on_update=None, on_complete=None, on_start_js=None, on_update_js=None, on_complete_js=None ):
		print 'tween.init', ob, ob[...]
		self.source = ob
		self.on_start = on_start
		self.on_update = on_update
		self.on_complete = on_complete
		self.seconds = None
		self.seconds_remaining = None
		self.active = True
		self.started = False

		on_start_method = self._on_start
		on_update_method = self._on_update
		on_complete_method = self._on_complete

		with javascript:
			tween = new( TWEEN.Tween( ob[...] ) )
			if on_start_js:
				tween.onStart( on_start_js )
			else:
				tween.onStart( lambda : on_start_method([this]) )

			if on_update_js:
				tween.onUpdate( on_update_js )
			else:
				tween.onUpdate( lambda delta: on_update_method([this, delta]) )

			if on_complete_js:
				tween.onComplete( on_complete_js )
			else:
				tween.onComplete( lambda : on_complete_method([this]) )

			##print 'tween._valuesStart', tween._valuesStart  ## this variable is really private
			self[...] = tween

	#############################################
	def _on_start(self, jsob):
		print '-on-start', jsob
		self.started = True
		if self.on_start:
			self.on_start( self, self.source )

	def _on_update(self, jsob, delta):
		print '-on-update', jsob, delta
		self.seconds_remaining = self.seconds - (self.seconds * delta)
		if self.on_update:
			self.on_update( self, self.source, delta )

	def _on_complete(self, jsob):
		print '-on-complete', jsob
		self.active = False
		if self.on_complete:
			self.on_complete( self, self.source )

	#############################################

	def to(self, vec, seconds=1.0):
		self.seconds = seconds
		self.seconds_remaining = seconds
		print '--tween.to', vec, vec[...]
		with javascript:
			self[...].to( vec[...], seconds*1000 )

	def start(self):
		print '--starting tweeen'
		with javascript:
			self[...].start()

	def stop(self):
		## it is safe to call stop multiple times,
		## it will only be removed once from TWEEN._tweens
		self.active = False
		with javascript:
			self[...].stop()

	def delay(self, seconds):
		with javascript:
			self[...].delay( seconds*1000 )

	def repeat(self, amount):
		with javascript:
			self[...].repeat( amount )

	def yoyo(self, yoyo):
		with javascript:
			self[...].yoyo( yoyo )

	def easing(self, easing ):
		with javascript:
			self[...].easing( easing )

	def interpolation(self, interp):
		with javascript:
			self[...].interpolation( interp )

	def chain(self, chain):
		with javascript:
			self[...].chain( chain )



	############# retarget helper #############
	def retarget(self, target):
		assert self.seconds_remaining
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
		self.to( target, self.seconds_remaining )
		self.start()

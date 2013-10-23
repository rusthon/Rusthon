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

	def reset(self):
		self._tweens = []  ## raw tween js objects
		with javascript: arr = TWEEN.getAll()
		self._tweens.js_object = arr

	@property
	def raw_tweens(self):
		return self._tweens

	def start_tween(self, raw_tween):
		if raw_tween in self._tweens:
			pass
		else:
			raw_tween.start()

	def update(self):
		with javascript:
			TWEEN.update()

TweenManager = _TweenManagerSingleton()

class Tween:
	def __init__(self, flatob, on_start=None, on_update=None, on_complete=None ):
		with javascript:
			tween = new( TWEEN.Tween(flatob) )
			if on_start: tween.onStart( on_start )
			if on_update: tween.onUpdate( on_update )
			if on_complete: tween.onComplete( on_complete )
			self[...] = tween

	def to(self, vec, seconds=1.0):
		with javascript:
			self[...].to( vec[...], seconds*1000 )

	def start(self, force=False):
		if force:
			with javascript:
				self[...].start()
		else:
			TweenManager.start_tween( self[...] )





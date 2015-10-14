
class __WorkerPool__:
	def create_webworker(self, cpuid):
		## this is lazy because if the blob is created when the js is first executed,
		## then it will pick all functions of `window` but they will be `undefined`
		## if their definition comes after the construction of this singleton.
		print 'creating blob'

		## having the worker report back the current time to the main thread allows
		## some gauge of its CPU load, this can be average over time, and the user
		## could call something like `worker.how_busy()` which is some relative value.

		header = [
			'setInterval(',
			'	function(){',
			'		self.postMessage({time_update:(new Date()).getTime()});',
			'	}, 100',
			');',
			## TODO other builtins prototype hacks. see above.
			'Array.prototype.append = function(a) {this.push(a);};',
		]

		## this is something extra stuff injected from NW.js
		## that should not be inserted into the webworker.
		nwjs_skip = ('Buffer', 'AppView', 'WebView')
		for name in dir(window):
			if name in nwjs_skip:
				continue
			ob = window[name]
			if ob is undefined:
				print 'WARNING: object in toplevel namespace window is undefined ->' + name
			elif typeof(ob) == 'function':
				## should actually check function code for `[ native code ]` and skip those.

				header.append( 'var ' + name + '=' + ob.toString() + ';\n' )
				for subname in dir(ob.prototype):
					sob = ob.prototype[subname]
					header.append(name + '.prototype.' +subname + '=' + sob.toString() + ';\n' )
			#elif typeof(ob) == 'object':
			#	header.append( 'var ' + name + '=' + ob.toString() + ';\n' )

		xlibs = []
		for name in self.extras:
			if '.' in name:
				print 'import webworker submodule: ' + name
				mod = name.split('.')[0]
				xname = name.split('.')[1]
				ob = eval(name)
				if typeof(ob) == 'object':  ## copy objects with static methods
					print 'import object: ' + xname
					header.append( name + '= {' )
					for sname in Object.keys(ob):
						subob = ob[sname]
						ok = True
						try:
							tmp = eval("("+subob+")")
						except:
							ok = False
						if ok:
							print 'import->: ' + sname
							header.append( '"'+sname + '":(' + ob[sname] +')' )
							header.append(',\n')
					header.pop()
					header.append('};\n')

				#if mod not in xlibs:
				#	print 'new module: '+mod
				#	header.append('var ' + mod + '= {};' )
				#	xlibs.append(mod)
			else:
				print 'import webworker module: ' + name
				header.append( 'var ' + name + '= {};\n' )
				modulemain = window[name]

				for xname in dir(modulemain):
					ob = modulemain[xname]
					if typeof(ob) == 'function':
						print 'import class: ' + xname
						header.append( name + '.' + xname + '=' + ob.toString() + ';\n' )
						if ob.prototype: ## copy methods
							#for method_name in dir(ob.prototype):
							for method_name in Object.keys(ob.prototype):
								if method_name == 'constructor': continue
								ok = True
								try:
									## getting some properties can throw deprecation errors
									sub = ob.prototype[method_name]
								except:
									ok = False

								if ok and typeof(sub) == 'function':
									print 'import method: ' + method_name
									header.append(name + '.' + xname + '.prototype.' + method_name + '=' + sub.toString() + ';' )
									#header.append(name + '.' + xname + '.' + method_name + '=' + ob.toString() + ';' )

		## Web Worker ##
		header.extend( self.source )
		blob = new(Blob(header, type='application/javascript'))
		url = URL.createObjectURL(blob)
		ww = new(Worker(url))
		#self.thread = ww  ## temp, TODO multiple threads
		#self.thread.onmessage = self.update.bind(this)

		ww._cpuid = cpuid
		ww._last_time_update = 0
		ww._stream_callbacks = {}
		ww._stream_triggers  = {}
		ww._get_callback  = None  ## this should actually be a stack of callbacks, right now it assumes its synced
		ww._call_callback = None  ## this should actually be a stack of callbacks.
		ww._callmeth_callback = None  ## TODO also should be a stack

		## if worker has not sent a time update in awhile ##
		ww.busy     = lambda : ww._last_time_update - (new(Date())).getTime() < 200
		ww.how_busy = lambda : 100.0 / (ww._last_time_update - (new(Date())).getTime())

		@bind(ww.spawn_class)
		def _spawn_class(cfg):
			sid = cfg['spawn']
			print '_spawn_class:' + ww._cpuid + '|' + sid
			ww._stream_callbacks[sid] = []
			ww._stream_triggers[sid]  = []
			ww.postMessage(cfg)


		def onmessage_update(evt):
			if self._binrecv:
				#print 'got binary....'
				id    = self._binrecv['id']
				btype = self._binrecv['type']
				self._binrecv = None
				msg = None
				switch btype:
					case "Float32Array":
						msg = new Float32Array(evt.data)
					case "Float64Array":
						msg = new Float64Array(evt.data)
					case "Int32Array":
						msg = new Int32Array(evt.data)

				if id in ww._stream_callbacks:  ## channels
					callbacks = ww._stream_callbacks[id]
					if len(callbacks):
						cb = callbacks.pop()
						cb( msg )
					else:
						ww._stream_triggers[id].push( msg )
				else:
					raise WebWorkerError('invalid id:' + id)

			elif evt.data.time_update:  ## the worker uses setInterval to report the time, see `worker.busy()`
				ww._last_time_update = evt.data.time_update
			elif evt.data.debug:
				console.warn( ww._cpuid + '|' + evt.data.debug)
			else:
				ww._last_time_update = (new(Date())).getTime()

				msg = evt.data.message
				## restore object class if `proto` was given (user static return type)
				if evt.data.proto: msg.__proto__ = eval(evt.data.proto + '.prototype')


				if evt.data.GET:
					ww._get_callback( msg )
				elif evt.data.CALL:
					ww._call_callback( msg )
				elif evt.data.CALLMETH:
					ww._callmeth_callback( msg )
				else:
					id = evt.data.id
					if evt.data.bin:
						self._binrecv = {'id':id, 'type':evt.data.bin}
					elif id in ww._stream_callbacks:  ## channels
						callbacks = ww._stream_callbacks[id]
						if len(callbacks):
							cb = callbacks.pop()
							cb( msg )
						else:
							ww._stream_triggers[id].push( msg )
					else:
						raise WebWorkerError('invalid id:' + id)


		ww.onmessage = onmessage_update
		return ww

	def __init__(self, src, extras):
		## note:  src is an array
		## note: thread-ids = `cpu-id:spawned-id`
		self.source = src
		self.extras = extras
		## each worker in this pool runs on its own CPU core
		## how to get number of CPU cores in JS?
		self.pool = {}
		self.num_spawned = 1  ## must be 1, not zero


	def spawn(self, cfg, options):
		cpu = 0
		autoscale = True
		if options is not undefined:
			print 'using CPU:'+options.cpu
			cpu = options.cpu
			autoscale = False

		id = str(cpu) + '|' + str(self.num_spawned)
		cfg['spawn']     = self.num_spawned
		self.num_spawned += 1

		if cpu in self.pool:
			## this thread could be busy, spawn into it anyways.
			print 'reusing cpu already in pool'
			self.pool[cpu].spawn_class(cfg)
		elif autoscale:
			print 'spawn auto scale up'
			## first check if any of the other threads are not busy
			readythread = None
			cpu = len(self.pool.keys())
			for cid in self.pool.keys():
				thread = self.pool[ cid ]
				if not thread.busy():
					print 'reusing thread is not busy:' + cid
					readythread = thread
					cpu = cid
					break

			if not readythread:
				assert cpu not in self.pool.keys()
				readythread = self.create_webworker(cpu)
				self.pool[cpu] = readythread

			readythread.spawn_class(cfg)
		else:
			## user defined CPU ##
			print 'spawn user defined cpu:' + cpu
			assert cpu not in self.pool.keys()
			readythread = self.create_webworker(cpu)
			self.pool[cpu] = readythread
			self.pool[cpu].spawn_class(cfg)

		return id

	def send(self, id=None, message=None):
		tid, sid = id.split('|')
		if tid not in self.pool:
			raise RuntimeError('send: invalid cpu id')

		if __is_typed_array(message):  ## transferable buffers (no copy, moves data into worker)
			bspec = {'send_binary':sid}
			if instanceof(message, Float32Array):
				bspec['type'] = 'Float32Array'
			elif instanceof(message, Float64Array):
				bspec['type'] = 'Float64Array'
			elif instanceof( ob, Int32Array ):
				bspec['type'] = 'Int32Array'
			elif instanceof( ob, Int16Array ):
				bspec['type'] = 'Int16Array'
			elif instanceof( ob, Uint16Array ):
				bspec['type'] = 'Uint16Array'
			elif instanceof( ob, Uint32Array ):
				bspec['type'] = 'Uint32Array'

			self.pool[tid].postMessage(bspec)  ## object header
			self.pool[tid].postMessage(message.buffer, [message.buffer])  ## binary body

		else:
			try:
				self.pool[tid].postMessage({'send':sid, 'message':message})

			except:
				print 'DataCloneError: can not send data to webworker'
				print message
				raise RuntimeError('DataCloneError: can not send data to webworker')

	def recv(self, id, callback):

		if id is undefined:
			raise WebWorkerError("undefined id")

		tid, sid = id.split('|')
		if tid not in self.pool:
			raise RuntimeError('send: invalid cpu id')

		ww = self.pool[ tid ]
		if sid in ww._stream_triggers and ww._stream_triggers[sid].length:
			callback( ww._stream_triggers[sid].pop() )
		elif sid in ww._stream_callbacks:
			ww._stream_callbacks[sid].insert(0, callback)
		else:
			raise WebWorkerError('webworker.recv - invaid id: '+id)


	def get(self, id, attr, callback):
		tid, sid = id.split('|')
		if tid not in self.pool:
			raise RuntimeError('get: invalid cpu id')
		ww = self.pool[ tid ]
		ww._get_callback = callback
		ww.postMessage(
			id  = sid,
			get = attr
		)

	def call(self, func, args, callback):
		#self._call = callback
		#self.thread.postMessage({'call':func, 'args':args})
		## which CPU do we select? default to `0`, have extra option for CPU?
		raise RuntimeError('TODO call plain function in webworker')

	def callmeth(self, id, func, args, callback):
		tid, sid = id.split('|')
		if tid not in self.pool:
			raise RuntimeError('callmeth: invalid cpu id')
		ww = self.pool[ tid ]
		ww._callmeth_callback = callback
		ww.postMessage(
			id       = sid,
			callmeth = func,
			args     = args
		)

	def select(self, id):
		tid, sid = id.split('|')
		if tid not in self.pool:
			raise RuntimeError('select: invalid cpu id')
		if sid not in self.pool[ tid ]._stream_triggers:
			raise RuntimeError('select: invalid worker id')
		return self.pool[ tid ]._stream_triggers[ sid ]

__cp__ = require('child_process')

class Popen:
	def __init__(self, executeable=None, args=[], stdin='ignore', stdout='ignore', stderr='ignore', cwd=None, env=None, detached=False, callback=None, error_callback=None, returns_binary=False):
		if stdin is None: stdin = 'pipe'
		elif stdin == -1: stdin = 'pipe'
		self._echo_stdout = False
		self._echo_stderr = False
		if stdout is None:
			stdout = 'pipe'
			self._echo_stdout = True
		if stderr is None:
			stderr = process.stderr
			self._echo_stderr = True

		with javascript:
			if env is None: env = process.env
			options = {
				'cwd': cwd,
				'stdio' : [stdin, stdout, stderr],
				'env' : env,
				'detached' : detached
			}
			proc = __cp__.spawn( executeable, args, options )
			self[...] = proc
			#print 'proc.stdio', proc.stdio ## this is in the new API?

		self.stdin = proc.stdin
		self.stdout = proc.stdout
		self.stderr = proc.stderr
		if self.stderr:
			self.stderr.setEncoding('utf8')  ## assume that errors are always text

		self.stdout_callback = callback
		self.stderr_callback = error_callback
		self._returns_binary = returns_binary
		self._stdout_buff = []
		self._stderr_buff = []

		if self._echo_stdout or self.stdout_callback:
			if self.stdout_callback:
				self._hookup_stdout( echo=False )
			else:
				self._hookup_stdout( echo=True )

		if self._echo_stderr:
			self._hookup_stderr()

	def _read_stdout(self, data):
		if self._echo_stdout:
			print data
		self._stdout_buff.append( data )

	def _read_stderr(self, data):
		if self._echo_stderr:
			print data
		self._stderr_buff.append( data )

	def _end_stdout(self):
		if len( self._stdout_buff ) == 1:
			data = self._stdout_buff[0]
		elif not self._returns_binary:
			data = ''.join( self._stdout_buff )
		else:
			print 'TODO'
		if self.stdout_callback:
			self.stdout_callback( data )
		else:
			print 'WARNING: no stdout callback assigned'

	def _end_stderr(self):
		data = ''.join( self._stderr_buffer )
		if self.stderr_callback:
			self.stderr_callback( data )

	def _hookup_stdout(self, echo=False):
		self._stdout_buff = []
		self._echo_stdout = echo
		if self.stdout:
			if not self._returns_binary: self.stdout.setEncoding( 'utf8' )
			self.stdout.on('data', self._read_stdout )
			self.stdout.on('end', self._end_stdout )
		else:
			print 'WARNING: tried to hookup stdout, but it is null'

	def _hookup_stderr(self):
		self._stderr_buff = []
		self.stderr.on('data', self._read_stderr )
		self.stderr.on('end', self._end_stderr )


	def communicate(self, data, encoding='utf8', returns_binary=False, callback=None, error_callback=None):
		## TODO fix me
		def flushed(): print 'write data flushed'
		print 'communicate->', data
		self.stdin.write( data, encoding, flushed )
		self.stdout_callback = callback
		self.stderr_callback = error_callback
		self._returns_binary = returns_binary
		self._hookup_stdout( echo=True )
		self._hookup_stderr()
		return [ self.stdout, self.stderr ]



class _fake_subprocess:
	def __init__(self):
		self.PIPE = -1 ## in python this is -1, nodejs has "pipe"
		self.Popen = Popen
		

	def call(self, executeable=None, args=[], callback=None, stdin='ignore', stdout=None, stderr='ignore', cwd=None, env=None):
		print 'subprocess.call'
		print executeable
		p = Popen( executeable=executeable, args=args, callback=callback, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd, env=env )
		return p


subprocess = _fake_subprocess()

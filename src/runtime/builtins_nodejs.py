
## file IO ##
class file:
	#TODO, support multiple read/writes.  Currently this just reads all data,
	#and writes all data.

	def __init__(self, path, flags):
		self.path = path

		if flags == 'rb':
			self.flags = 'r'
			self.binary = True
		elif flags == 'wb':
			self.flags = 'w'
			self.binary = True
		else:
			self.flags = flags
			self.binary = False

		self.flags = flags

	def read(self, binary=False):
		_fs = require('fs')
		path = self.path
		if binary or self.binary:
			return _fs.readFileSync( path, encoding=None )
		else:
			return _fs.readFileSync( path, {'encoding':'utf8'} )

	def write(self, data, binary=False):
		_fs = require('fs')
		path = self.path
		if binary or self.binary:
			binary = binary or self.binary
			if binary == 'base64':  ## TODO: fixme, something bad in this if test
				#print('write base64 data')
				buff = new(Buffer(data, 'base64'))
				_fs.writeFileSync( path, buff, {'encoding':None})

			else:
				#print('write binary data')
				#print(binary)
				_fs.writeFileSync( path, data, {'encoding':None})
		else:
			#print('write utf8 data')
			_fs.writeFileSync( path, data, {'encoding':'utf8'} )

	def close(self):
		pass

def __open__( path, mode):  ## this can not be named `open` because it replaces `window.open`
	if mode is undefined:
		mode = 'r'
	return file( path, mode )



_fs = require('fs')
_path = require('path')


class _fake_path:
	def __init__(self):
		self.sep = _path.sep

	def join(self, a, b):
		return _path.join( a, b )

	def normpath(self, path):
		return _path.normalize( path )

	def dirname(self, path):
		return _path.dirname( path )

	def basename(self, path):
		return _path.basename( path )

	def split(self, path):
		a = self.dirname(path)
		b = self.basename(path)
		return [a,b]

	def exists(self, path):  ## this is new - missing in Node v0.6.19
		return _fs.existsSync(path)

	def abspath(self, path):
		return _path.resolve( path )

	def expanduser(self, path):
		## assume that path starts with "~/"
		return self.join( process.env.HOME, path[2:] )

	def isdir(self, path):
		if self.exists( path ):
			stat = _fs.statSync( path )
			if stat:
				return stat.isDirectory()
			else:
				return False
		return False

	def isfile(self, path):
		if self.exists( path ):
			stat = _fs.statSync( path )
			if stat:
				return stat.isFile()
			else:
				return False
		return False

class _fake_os:
	def __init__(self):
		self.environ = process.env
		self.path = _fake_path()

	def abort(self):
		process.abort()

	def chrdir(self, path):
		process.chdir( path )

	def getcwd(self):
		return process.cwd()

	def getpid(self):
		return process.pid

	def listdir(self, path):
		return _fs.readdirSync(path)

	def mkdir(self, path):
		_fs.mkdirSync( path )

	def stat(self, path):
		return _fs.statSync( path )

os = _fake_os()


class _fake_sys:
	def __init__(self):
		if process.platform=='win32':  ## not available on mswindows
			self.stdin = None
			self.stdout = None
			self.stderr = None
		else:
			self.stdin = process.stdin
			self.stdout = process.stdout
			self.stderr = process.stderr
		self.argv = process.argv

	def exit(self):
		process.exit()

sys = _fake_sys()

__cp__ = require('child_process')

class Popen:
	def __init__(self, executeable=None, args=[], stdin='ignore', stdout='ignore', stderr='ignore', cwd=None, env=None, detached=False, callback=None, error_callback=None, returns_binary=False):
		if stdin is None: stdin = 'pipe'
		elif stdin == -1: stdin = 'pipe'
		self._echo_stdout = False
		self._echo_stderr = False

		self.stdout_callback = callback
		self.stderr_callback = error_callback
		self._returns_binary = returns_binary
		self._stdout_buff = []
		self._stderr_buff = []

		if callback and stdout=='ignore':
			stdout = None

		if stdout is None:
			stdout = 'pipe'
			self._echo_stdout = True

		if stderr is None:
			stderr = process.stderr
			self._echo_stderr = True

		if env is None: env = process.env
		options = {
			'cwd': cwd,
			'stdio' : [stdin, stdout, stderr],
			'env' : env,
			'detached' : detached
		}
		proc = __cp__.spawn( executeable, args, options )
		self.__proc = proc
		#print 'proc.stdio', proc.stdio ## this is in the new API?

		self.stdin = proc.stdin
		self.stdout = proc.stdout
		self.stderr = proc.stderr
		if self.stderr:
			self.stderr.setEncoding('utf8')  ## assume that errors are always text


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
			self.stdout.on('data', self._read_stdout.bind(self) )
			self.stdout.on('end', self._end_stdout.bind(self) )
		else:
			print 'WARNING: tried to hookup stdout, but it is null'

	def _hookup_stderr(self):
		self._stderr_buff = []
		self.stderr.on('data', self._read_stderr.bind(self) )
		self.stderr.on('end', self._end_stderr.bind(self) )


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
		#self.Popen = Popen  ## this requires the user call `new subprocess.Popen`
		
	def Popen(self, executeable=None, args=[], callback=None, stdin='ignore', stdout='ignore', stderr='ignore', cwd=None, env=None):
		p = Popen( executeable=executeable, args=args, callback=callback, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd, env=env )
		return p

	def call(self, executeable=None, args=[], callback=None, stdin='ignore', stdout=None, stderr='ignore', cwd=None, env=None):
		p = Popen( executeable=executeable, args=args, callback=callback, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd, env=env )
		return p


subprocess = _fake_subprocess()


__os__ = require('os')

tempfile = {
	'gettempdir' : lambda : __os__.tmpdir()
}
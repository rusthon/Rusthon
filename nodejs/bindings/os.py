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
			with javascript:
				stat = _fs.statSync( path )
				if stat:
					return stat.isDirectory()
				else:
					return False
		return False

	def isfile(self, path):
		if self.exists( path ):
			with javascript:
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

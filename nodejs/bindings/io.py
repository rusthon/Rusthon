_fs = require('fs')


class file:
	'''
	TODO, support multiple read/writes.  Currently this just reads all data,
	and writes all data.
	'''
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
		#self.fd = _fs.openSync( path, flags )
		#self.stat = _fs.statSync( path )
		#print 'stat', self.stat
		#print 'self.path:', self.path

	def read(self, binary=False):
		path = self.path
		with javascript:
			if binary or self.binary:
				return _fs.readFileSync( path )
			else:
				return _fs.readFileSync( path, {'encoding':'utf8'} )

	def write(self, data, binary=False):
		path = self.path
		with javascript:
			if binary or self.binary:
				_fs.writeFileSync( path, data )
			else:
				_fs.writeFileSync( path, data, {'encoding':'utf8'} )

	def close(self):
		pass

def open( path, mode=None):
	return file( path, mode )

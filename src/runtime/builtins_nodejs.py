
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

def __open__( path, mode=None):  ## this can not be named `open` because it replaces `window.open`
	return file( path, mode )


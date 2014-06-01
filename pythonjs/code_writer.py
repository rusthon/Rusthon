import sys

if sys.version_info.major == 3:
	import io
	StringIO = io.StringIO
else:
	from StringIO import StringIO
	
class Writer(object):

	def __init__(self):
		self.level = 0
		self.buffer = list()
		self.output = StringIO()
		self.functions = []

	def is_at_global_level(self):
		return self.level == 0

	def push(self):
		self.level += 1

	def pull(self):
		self.level -= 1

	def append(self, code):
		self.buffer.append(code)

	def write(self, code):
		for content in self.buffer:
			self._write(content)
		self.buffer = list()
		self._write(code)

	def _write(self, code):
		indentation = self.level * 4 * ' '
		s = '%s%s\n' % (indentation, code)
		self.output.write(s)

	def getvalue(self):
		s = self.output.getvalue()
		self.output = StringIO()
		return s
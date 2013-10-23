# PythonJS binding for Ace Editor http://ace.c9.io/
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

class AceEditor:
	def __init__(self, div_id='editor', mode='python', theme=None):
		with javascript: self[...] = ace.edit( div_id )
		if mode: self.setMode( mode )
		if theme: self.setTheme( theme )

	def setMode(self, mode):
		with javascript:
			self[...].getSession().setMode( 'ace/mode/'+mode )

	def setTheme(self, name='monokai'):
		with javascript:
			self[...].setTheme( 'ace/theme/'+name)

	def setValue(self, txt):
		with javascript:
			self[...].setValue( txt )

	def getValue(self):
		with javascript:
			return self[...].getValue()

	def setFontSize(self, size):
		with javascript:
			self[...].setFontSize( size )



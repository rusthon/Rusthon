"""@javaScript decorator in JS mode"""
def main():
	if PYTHON == 'PYTHONJS':
		@javascript
		def dummy(): return ""
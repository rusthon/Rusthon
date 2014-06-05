_os = require('os')

with javascript:
	tempfile = {
		'gettempdir' : lambda : _os.tmpdir()
	}


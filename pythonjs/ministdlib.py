# Python to PythonJS Mini Standard Library
# by Brett Hartshorn - copyright 2013
# You may destribute this file using the "New BSD" or MIT license

LUA = {
	'time': {
		'time' : 'time = function() return os.time() end',
		'clock' : 'clock = function() return os.time() end'
	}
}


DART = {
	'time': {
		'time' : 'time() { return new DateTime.now().millisecondsSinceEpoch / 1000.0; }'
	}
}

JS = {
	'time': {
		'time': 'function time() { return new Date().getTime() / 1000.0; }',
		'clock': 'function clock() { return new Date().getTime() / 1000.0; }'
	},
	'random': {
		'random': 'var random = Math.random'
	},
	'bisect' : {
		'bisect' : '/*bisect from fake bisect module*/'  ## bisect is a builtin
	},
	'math' : {
		'sin' : 'var sin = Math.sin',
		'cos' : 'var cos = Math.cos',
		'sqrt': 'var sqrt = Math.sqrt'
	},
	'os.path' : {
		'dirname' : "function dirname(s) { return s.slice(0, s.lastIndexOf('/')+1)}; var os = {'path':{'dirname':dirname}}"
	}
}
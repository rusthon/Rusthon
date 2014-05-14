# Python to PythonJS Mini Standard Library
# by Brett Hartshorn - copyright 2013
# You may destribute this file using the "New BSD" or MIT license

REQUIRES = 1

LUA = {
	'time': {
		## requires socket module, install for luajit on ubuntu - `sudo-apt get install lua-socket`
		## for lua interpreter on ubuntu - `sudo apt-get install liblua5.1-socket`
		REQUIRES : ['socket'],
		'time' : 'time = function() return socket.gettime() end',
		'clock' : 'clock = function() return socket.gettime() end'
	},
	'math': {
		'sin' : 'sin = function(a) return math.sin(a[1]) end',
		'cos' : 'cos = function(a) return math.cos(a[1]) end',
		'sqrt' : 'sqrt = function(a) return math.sqrt(a[1]) end',
	}
}


DART = {
	'time': {
		'time' : 'time() { return new DateTime.now().millisecondsSinceEpoch / 1000.0; }',
		'clock' : 'clock() { return new DateTime.now().millisecondsSinceEpoch / 1000.0; }'
	},
	'math': {
		'sin' : 'sin = math.sin',
		'cos' : 'cos = math.cos',
		'sqrt' : 'sqrt = math.sqrt',
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
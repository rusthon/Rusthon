(function () {
	self.console = {
		log: function () {}
	};
	self.prompt = function () {
		return 'Input not supported in demo';
	};
	
	importScripts('empythoned.js');

	// https://github.com/kripken/emscripten/wiki/Filesystem-API
	FS.createLazyFile(".", "python_to_pythonjs.py", "./python_to_pythonjs.py",
		true,false
	);
	FS.createLazyFile(".", "pythonjs.py", "./pythonjs.py",
		true,false
	);
	FS.createLazyFile(".", "ministdlib.py", "./ministdlib.py",
		true,false
	);


	Python.initialize(null, function(chr) {
		if (chr !== null) 
			postMessage(String.fromCharCode(chr));
	});

	var on_message = function (e) {
		if (Python.isFinished(e.data)) {
			var result = Python.eval(e.data);
			if (result !== null && result !== undefined) {
				postMessage('\n--------------------------\nResult: ' + result);
			}
		} else {
			postMessage('\nCommand not finished.\n');
		}
	};

	addEventListener('message', on_message, false);

	postMessage('Empythoned Ready\n');
})();

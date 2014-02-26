(function () {
	self.console = {
		log: function () {}
	};
	self.prompt = function () {
		return 'Input not supported in demo';
	};
	var ready = false;
	
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

	var buffer = [];
	var on_stderr = function(chr) {
		if (chr == null || chr == 0 || chr == 10) {
			postMessage( {'error':buffer.join('')} );
			buffer.length = 0;
		} else {
			buffer.push( String.fromCharCode(chr) );
		}
	}

	Python.initialize(
		null,         // stdin
		null,         // stdout
		on_stderr     // stderr
	);

	var res = Python.eval('from python_to_pythonjs import main as to_pythonjs');
	var res = Python.eval('from pythonjs import main as to_javascript');
	var res = Python.eval('def translate_to_javascript(src): return to_javascript(to_pythonjs(src))');

	ready = true;

	var on_message = function (e) {
		if (ready != true) throw Error('Empythoned not ready');
		// e.data is written to a file to avoid any problems with escaping string quotes
		// note: emscripten 1.0 api
		FS.createDataFile( "/sandbox", "temp", e.data, true, true );
		var result = Python.eval('translate_to_javascript(open("/sandbox/temp","r").read())');
		if (result !== null && result !== undefined) {
			postMessage( {'code':result} ); // javascript to eval
		}
		//FS.deleteFile( "/sandbox/temp" );
	};

	addEventListener('message', on_message, false);

})();

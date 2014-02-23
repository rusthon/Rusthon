// PythonJS Translator Bridge for Node-Webkit
// by Brett Hartshorn - copyright 2014
// License: "New BSD"

_cp = require('child_process');
_fs = require('fs');


s = '';
on_stderr = function( data ) {
	document.write('ERROR:'+data);
}

translate = function( options ) {
	console.log('translating...')
	//console.log( options )
	var os_name = require('os').type();
	var args = ['pythonjs/translator.py'];
	var use_stdin = true;
	if (options.file) {
		args.push( options.file );
		use_stdin = false;
	}
	if (options.vis) {
		args.push('--visjs');
	}

	if (os_name == 'Windows_NT') {
		var proc = _cp.spawn(
			'external/python/python.exe', 
			args, 
			{stdio:['pipe', 'pipe', 'pipe']}
		);
	} else {
		var proc = _cp.spawn(
			'python', 
			args, 
			{stdio:['pipe', 'pipe', 'pipe']}
		);		
	}
	proc.stdout.setEncoding('utf8');
	proc.stderr.setEncoding('utf8');
	var buff = [];
	proc.stderr.on('data', on_stderr);
	proc.stdout.on('data', function (data){ buff.push(data); console.log('read...') });

	if (options.callback) {
		proc.stdout.on(
			'end', 
			function(){
				if (options.callback_args) {
					options.callback(''.join(buff), options.callback_args);
				} else {
					options.callback(''.join(buff));
				}
			}
		);

	} else {
		proc.stdout.on(
			'end', 
			function(){s=''.join(buff); eval(s)}
		);
	}

	if (use_stdin) {
		var data = options.data;
		//var lines = data.split('\n');
		//console.log(lines);
		//for (var i=0; i<lines.length; i++) {
		//	console.log(lines[i]);
		//}

		proc.stdin.write( data, 'utf8' );
		proc.stdin.end();
	}
}

translate( {file:'nodejs/bindings/io.py'} );
translate( {file:'nodejs/bindings/os.py'} );
translate( {file:'nodejs/bindings/sys.py'} );
translate( {file:'nodejs/bindings/tempfile.py'} );

var translate_python_scripts = function() {
	var scripts = document.getElementsByTagName('script');
	for (var i=0; i<scripts.length; i++) {
		var script = scripts[i];
		if (script.getAttribute('type')=='text/python') {
			if (script.getAttribute('src')) {
				var code = _fs.readFileSync( 'pypubjs/'+script.getAttribute('src'), {encoding:'utf8'} );
				translate( {data:code} );
			} else {
				translate( {data:script.firstChild.nodeValue} );
			}
		}
	}
}

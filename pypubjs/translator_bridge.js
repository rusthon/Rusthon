// PythonJS Translator Bridge for Node-Webkit
// by Brett Hartshorn - copyright 2014
// License: "New BSD"

_cp = require('child_process');
_fs = require('fs');


s = '';
on_stderr = function( data ) {
	document.write('ERROR:'+data);
}


function _translate_empythoned( options ) {
	// TODO optimize this so that a new Empythoned is not spawned each time!
	var translate_worker = new Worker( '../pythonjs/empythoned-translator-webworker.js' );

	function __on_message( output ) {
		if (output.data.error) {
			console.log('TRANSLATION ERROR!')
			console.log( output.data.error )
		} else {
			console.log('---------------translation ok------------------')
			var code = output.data.code;
			code = code.substring(1, code.length-1);
			code = code.split('\\n').join('\n');
			code = code.split("\\'").join("\'");
			var lines = code.split('\n');
			for (var i=0; i<lines.length; i++) console.log( (i+1) +'.' + lines[i] );

			if (options.callback) {
				if (options.callback_args) {
					options.callback(code, options.callback_args);
				} else {
					options.callback(code);
				}

			} else {
				eval( code );
			}
		}
	}

	translate_worker.addEventListener('message', __on_message)



	if (options.file) {
		var code = _fs.readFileSync( options.file, {encoding:'utf8'} );
	} else {
		var code = options.data;
	}
	console.log( code );
	translate_worker.postMessage( code );
}


function _translate_subprocess( options ) {
	console.log('translating...')
	//console.log( options )
	
	var args = ['pythonjs/translator.py'];
	var use_stdin = true;
	if (options.file) {
		args.push( options.file );
		use_stdin = false;
	}
	if (options.vis) {
		args.push('--visjs');
	}

	var proc = _cp.spawn(
		'python', 
		args, 
		{stdio:['pipe', 'pipe', 'pipe']}
	);		
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

var os_name = require('os').type();

if (os_name == 'Windows_NT') {
	var translate = _translate_empythoned;
} else {
	var translate = _translate_subprocess;
}

translate( {file:'nodejs/bindings/io.py'} );
translate( {file:'nodejs/bindings/os.py'} );
translate( {file:'nodejs/bindings/sys.py'} );
translate( {file:'nodejs/bindings/tempfile.py'} );
translate( {file:'nodejs/bindings/subprocess.py'} );

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

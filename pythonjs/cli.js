#!/usr/bin/env node


if (process.argv.length <= 2) {
	console.log('python-js input.py output.js [--dart, --coffee, --lua, --visjs]')
	console.log('(the default output is javascript)')
} else {
	var fs = require('fs')
	var pythonjs = require('./python-js')
	var input = fs.readFileSync( process.argv[2], {'encoding':'utf8'} )

	if (process.argv.indexOf('--dart') != -1) {
		var output = pythonjs.translator.to_dart( input )
	} else if (process.argv.indexOf('--coffee') != -1) {
		var output = pythonjs.translator.to_coffee( input )
	} else if (process.argv.indexOf('--lua') != -1) {
		var output = pythonjs.translator.to_lua( input )
	} else if (process.argv.indexOf('--visjs') != -1) {
		var output = pythonjs.translator.to_visjs( input )
	} else {
		var output = pythonjs.translator.to_javascript( input )

	}

	if (process.argv.length >= 4) {
		fs.writeFileSync( process.argv[3], output, {'encoding':'utf8'} )
	} else {
		console.log(output)
	}

}
#!/usr/bin/env python
import sys, subprocess
cmd = ['./pythonjs/translator.py', '--rust'] + sys.argv[1:]

output = None
for arg in sys.argv[1:]:
	if arg.startswith('output='):
		output = arg

if output:
	cmd.append( output )
	subprocess.check_call( cmd )

else:  ## run program after translation
	import json, tempfile
	cmd.append( '--stdout' )
	dump = subprocess.check_call( cmd )
	build = json.loads( dump )
	tempdir = tempfile.gettempdir()
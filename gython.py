#!/usr/bin/env python
import sys, subprocess
cmd = ['./pythonjs/translator.py', '--go'] + sys.argv[1:]
subprocess.check_call( cmd )
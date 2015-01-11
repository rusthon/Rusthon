#!/usr/bin/env python
import sys, subprocess
import pythonjs
import pythonjs.python_to_pythonjs
import pythonjs.pythonjs_to_cpp


def main(script, module_path=None):
	a = pythonjs.python_to_pythonjs.main(script, cpp=True, module_path=module_path)
	build = pythonjs.pythonjs_to_cpp.main( a )
	#print(build.keys())
	#print(build['main'])
	tmpfile = '/tmp/rusthon-build.cpp'
	open(tmpfile, 'wb').write( build['main'] )
	open('header.h', 'wb').write( build['header.c'] )
	open('header.hpp', 'wb').write( build['header.cpp'] )

	print('translation written to: %s' %tmpfile)
	subprocess.check_call(['g++', tmpfile, '-o', '/tmp/rusthon-bin', '-pthread', '-std=c++11',   ] )
	subprocess.check_call(['/tmp/rusthon-bin'])


if __name__ == '__main__':
	path = sys.argv[-1]
	assert path.endswith('.py')
	main( open(path,'rb').read() )
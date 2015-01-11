#!/usr/bin/env python
import sys, subprocess
import pythonjs
import pythonjs.python_to_pythonjs
import pythonjs.pythonjs_to_cpp

def convert_to_markdown_project(path):
	files = []
	if os.path.isfile(path):
		files.append( path )
		assert path.endswith('.rs')

	elif os.path.isdir(path):
		for name in os.listdir(path):
			if name.endswith( ('.rs', '.py', '.s') ):
				files.append(os.path.join(path,name))

			#elif os.path.isdir( os.path.join(path,name)): TODO

	project = []
	for file in files:
		print 'reading: ', file

		data = open(file, 'rb').read()
		header = [
			'#' + os.path.split(file)[-1],
			'* file: ' + file,
			'* md5sum   : %s' %md5.new(data).hexdigest(),
			'* changed  : %s' %os.stat(file).st_mtime,
			'',
		]
		lang = ''
		if file.endswith('.rs'):
			lang = 'rust'
		elif file.endswith('.py'):
			lang = 'python'
		elif file.endswith('.s'):
			lang = 'asm'

		impls = []
		pub_funcs = []
		pri_funcs = []
		pub_structs = []
		pri_structs = []
		pub_enums = []
		pri_enums = []

		code = []
		code.append('\n```%s' %lang)  ## begin fence
		fence = True
		comment_block = False
		for line in data.splitlines():

			if line.strip().startswith('//') or (lang != 'rust' and line.startswith('#')):
				if fence:
					code.append('```\n')  ## end fence
					fence = False
				if line.startswith('#'):
					line = line[1:]
				code.append('>'+line)

			elif line.strip().startswith('/*'):
				if fence:
					code.append('```\n')  ## end fence
					fence = False

				if '*/' in line:
					code.append('>*%s*' %line.replace('/*', '').replace('*/','').strip() )
				else:
					comment_block = True

			elif '*/' in line:
				assert comment_block
				comment_block = False
				a = line.replace('*/', '').strip()
				if a:
					code.append('>'+a)
			elif comment_block:
				code.append('>'+line)
			else:
				if not fence:
					code.append('\n```%s' %lang)  ## begin fence
					fence = True

				if lang=='rust':
					a = line ##.strip()
					if a.startswith('pub fn '):
						pub_funcs.append( a.split('pub fn ')[-1].split('(')[0] )
					elif a.startswith('fn '):
						pub_funcs.append( a.split('fn ')[-1].split('(')[0] )
					elif a.startswith('pub struct '):
						pub_structs.append( a.split('pub struct ')[-1].split('{')[0] )
					elif a.startswith('struct '):
						pri_structs.append( a.split('struct ')[-1].split('{')[0] )
					elif a.startswith('pub enum '):
						pub_enums.append( a.split('pub enum ')[-1].split('{')[0] )
					elif a.startswith('enum '):
						pri_enums.append( a.split('enum ')[-1].split('{')[0] )
					elif a.startswith('impl '):
						impls.append( a.split('impl ')[-1].split('{')[0] )

				code.append( line )
		if fence:
			code.append('```')

		if impls:
			header.append('###implementations:')
			for a in impls:
				header.append('* '+a)
			header.append('')

		if pub_funcs:
			header.append('###public functions:')
			for a in pub_funcs:
				header.append('* '+a)
			header.append('')
		if pub_structs:
			header.append('###public structs:')
			for a in pub_structs:
				header.append('* '+a)
			header.append('')

		if pub_enums:
			header.append('###public enums:')
			for a in pub_enums:
				header.append('* '+a)
			header.append('')

		if pri_funcs:
			header.append('###private functions:')
			for a in pri_funcs:
				header.append('* '+a)
			header.append('')
		if pri_structs:
			header.append('###private structs:')
			for a in pri_structs:
				header.append('* '+a)
			header.append('')

		if pri_enums:
			header.append('###private enums:')
			for a in pri_enums:
				header.append('* '+a)
			header.append('')

		code.append('___')

		md = '\n'.join(header+code)
		project.append(md)

	return '\n'.join(project)


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
#!/usr/bin/env python
import os, sys, subprocess
import pythonjs
import pythonjs.pythonjs
import pythonjs.python_to_pythonjs
import pythonjs.pythonjs_to_cpp

def compile_js( script, module_path ):
	fastjs = True
	directjs = False     ## compatible with pythonjs-minimal.js
	directloops = False  ## allows for looping over strings, arrays, hmtlElements, etc. if true outputs cleaner code.
	result = {}

	pyjs = pythonjs.python_to_pythonjs.main(
		script, 
		module_path=module_path,
		fast_javascript = fastjs,
		pure_javascript = directjs
	)

	if isinstance(pyjs, dict):  ## split apart by webworkers
		for jsfile in a:
			result[ jsfile ] = pythonjs.pythonjs.main(
				a[jsfile], 
				webworker=jsfile != 'main',
				requirejs=False, 
				insert_runtime=False,
				fast_javascript = fastjs,
				fast_loops      = directloops
			)

	else:
		print( pyjs )

		code = pythonjs.pythonjs.main(
			pyjs, 
			requirejs=False, 
			insert_runtime=False,
			fast_javascript = fastjs,
			fast_loops      = directloops
		)
		if isinstance(code, dict):
			result.update( code )
		else:
			result['main'] = code

	return result

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

def new_module():
	return {
		'markdown': '',
		'python'  : [],
		'rusthon' : [],
		'rust'    : [],
		'c'       : [],
		'c++'     : [],
	}

def import_md( url, modules=None ):
	if modules is None: modules = new_module()
	doc = []
	code = []
	lang = False
	in_code = False

	data = open(url, 'rb').read()
	for line in data.splitlines():
		if line.strip().startswith('```'):
			if in_code:
				if lang:
					p, n = os.path.split(url)
					mod = {'path':p, 'name':n, 'code':'\n'.join(code) }
					modules[ lang ].append( mod )
				in_code = False
				code = []
			else:
				in_code = True
			lang = line.strip().split('```')[-1]
		elif in_code:
			code.append(line)
		else:
			doc.append(line)

	modules['markdown'] += '\n'.join(doc)
	return modules


def build( modules, module_path ):
	output = {'executeable':None, 'rust':[], 'c':[], 'c++':[], 'go':[], 'javascript':[], 'python':[]}
	python_main = {'name':'main.py', 'script':[]}

	if modules['python']:
		for mod in modules['python']:
			if 'name' in mod:
				name = mod['name']
				if name.endswith('.md'):
					python_main['script'].append( mod['code'] )
				else:
					output['python'].append( {'name':name, 'script':mod['code']} )
			else:
				python_main['script'].append( mod['code'] )

	if modules['rusthon']:
		for mod in modules['rusthon']:
			script = mod['code']
			header = script.splitlines()[0]
			backend = 'c++'  ## default to c++ backend
			if header.startswith('#'):
				backend = header[1:].strip() or 'c++'


			if backend == 'c++':
				pyjs = pythonjs.python_to_pythonjs.main(script, cpp=True, module_path=module_path)
				pak = pythonjs.pythonjs_to_cpp.main( pyjs )   ## pak contains: c_header and cpp_header
				modules['c++'].append( {'code':pak['main']})  ## gets compiled below

			elif backend == 'rust':
				pyjs = pythonjs.python_to_pythonjs.main(script, rust=True, module_path=module_path)
				rustcode = pythonjs.pythonjs_to_rust.main( pyjs )
				modules['rust'].append( {'code':rustcode})  ## gets compiled below

			elif backend == 'go':
				pyjs = pythonjs.python_to_pythonjs.main(script, go=True, module_path=module_path)
				gocode = pythonjs.pythonjs_to_go.main( pyjs )
				modules['go'].append( {'code':gocode})  ## gets compiled below

			elif backend == 'javascript':
				js = compile_js( mod['code'], module_path )
				for name in js:
					output['javascript'].append( {'name':name, 'script':js[name]} )

	link = []

	if modules['rust']:
		source = []
		for mod in modules['rust']:
			source.append( mod['code'] )

		tmpfile = '/tmp/rusthon-build.rs'
		data = '\n'.join(source)

		open(tmpfile, 'wb').write( data )
		if modules['c++']:
			libname = 'rusthon-lib%s' %len(output['rust'])
			link.append(libname)
			subprocess.check_call(['rustc', '--crate-name', 'rusthon', '--crate-type', 'staticlib' ,'-o', '/tmp/'+libname,  tmpfile] )
			output['rust'].append( {'source':data, 'staticlib':libname, 'name':'lib'+libname+'.a'} )

		else:
			subprocess.check_call(['rustc', '--crate-name', 'rusthon', '-o', '/tmp/rusthon-bin',  tmpfile] )
			output['rust'].append( {'source':data, 'binary':'/tmp/rusthon-bin', 'name':'rusthon-bin'} )
			output['executeable'] = '/tmp/rusthon-bin'

	if modules['c']:
		libname = 'rusthon-clib%s' %len(output['c'])
		link.append(libname)
		source = []
		for mod in modules['c']:
			source.append( mod['code'] )

		tmpfile = '/tmp/rusthon-build.c'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )
		cmd = ['gcc', '-c', tmpfile, '-o', '/tmp/'+libname+'.o' ]
		subprocess.check_call( cmd )
		cmd = ['ar', 'rcs', '/tmp/lib'+libname+'.a', '/tmp/'+libname+'.o']
		subprocess.check_call( cmd )
		output['c'].append({'source':data, 'staticlib':libname+'.a'})


	if modules['c++']:
		source = []
		for mod in modules['c++']:
			source.append( mod['code'] )

		tmpfile = '/tmp/rusthon-build.cpp'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )
		cmd = ['g++']
		if link:
			cmd.append('-static')
			cmd.append( tmpfile )
			cmd.append('-L/tmp/.')
			for libname in link:
				cmd.append('-l'+libname)
		cmd.extend(
			[tmpfile, '-o', '/tmp/rusthon-bin', '-pthread', '-std=c++11' ]
		)
		subprocess.check_call( cmd )
		output['c++'].append( {'source':data, 'binary':'/tmp/rusthon-bin', 'name':'rusthon-bin'} )
		output['executeable'] = '/tmp/rusthon-bin'

	if python_main['script']:
		python_main['script'] = '\n'.join(python_main['script'])
		output['python'].append( python_main )

	return output

def save_tar( package, path='build.tar' ):
	import tarfile
	import StringIO
	tar = tarfile.TarFile(path,"w")
	exts = {'rust':'.rs', 'c++':'.cpp', 'javascript':'.js', 'python':'.py'}
	for lang in 'rust c++ go javascript python'.split():
		print(lang)
		for info in package[lang]:
			source = False
			s = StringIO.StringIO()
			if 'staticlib' in info:
				s.write(open(info['staticlib'],'rb').read())
				source = info['source']
			elif 'binary' in info:
				s.write(open(info['binary'],'rb').read())
				source = info['source']
			elif 'code' in info:
				s.write(info['code'])
			elif 'script' in info:
				s.write(info['script'])
			s.seek(0)
			ti = tarfile.TarInfo(name=info['name'])
			ti.size=len(s.buf)
			tar.addfile(tarinfo=ti, fileobj=s)

			if source:
				s = StringIO.StringIO()
				s.write(source)
				s.seek(0)
				ti = tarfile.TarInfo( name = info['name'] + exts[lang] )
				ti.size=len(s.buf)
				tar.addfile(tarinfo=ti, fileobj=s)


	tar.close()

if __name__ == '__main__':
	if len(sys.argv)==1:
		print('useage: ./rusthon.py myscript.py')
	else:
		modules = new_module()

		save = False
		paths = []
		scripts = []
		markdowns = []
		gen_md = False
		output_tar = 'rusthon-build.tar'

		for arg in sys.argv[1:]:
			if os.path.isdir(arg):
				paths.append(arg)
			elif arg.endswith('.py'):
				scripts.append(arg)
			elif arg.endswith('.md'):
				markdowns.append(arg)
			elif arg.endswith('.tar'):
				output_tar = arg
			elif arg == '--create-md':
				gen_md = True
			elif arg == '--tar':
				save = True

		base_path = None
		for path in scripts:
			script = open(path,'rb').read()
			modules['rusthon'].append( {'name':'main', 'code':script} )
			if base_path is None:
				base_path = os.path.split(path)[0]

		for path in markdowns:
			import_md( path, modules=modules )
			if base_path is None:
				base_path = os.path.split(path)[0]

		package = build(modules, base_path )
		if not save:
			subprocess.check_call( package['executeable'] )
		else:
			save_tar( package, output_tar )
			print('saved build to:')
			print(output_tar)



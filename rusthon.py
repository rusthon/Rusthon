#!/usr/bin/env python
import os, sys, subprocess
import pythonjs
import pythonjs.pythonjs
import pythonjs.python_to_pythonjs
import pythonjs.pythonjs_to_cpp
import pythonjs.pythonjs_to_verilog
import tempfile

def compile_js( script, module_path, directjs=False, directloops=False ):
	'''
	directjs = False     ## compatible with pythonjs-minimal.js
	directloops = False  ## allows for looping over strings, arrays, hmtlElements, etc. if true outputs cleaner code.
	'''
	fastjs = True  ## this is now the default, and complete python mode is deprecated
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
		'go'      : [],
		'html'    : [],
		'verilog' : [],
		'bash'    : [],
		'java'    : [],
		'nim'     : [],
		'javascript':[],
	}

def import_md( url, modules=None ):
	if modules is None: modules = new_module()
	doc = []
	code = []
	lang = False
	in_code = False
	index = 0
	prevline = None
	tag = None
	data = open(url, 'rb').read()

	for line in data.splitlines():
		# Start or end of a code block.
		if line.strip().startswith('```'):
			# End of a code block.
			if in_code:
				if lang:
					p, n = os.path.split(url)
					mod = {'path':p, 'markdown':url, 'code':'\n'.join(code), 'index':index, 'tag':tag }
					if tag and '.' in tag:
						ext = tag.split('.')[-1].lower()
						if ext in 'html js css py c h cpp hpp rust go'.split():
							mod['name'] = tag

					modules[ lang ].append( mod )
				in_code = False
				code = []
				index += 1
			# Start of a code block.
			else:
				in_code = True
				if prevline and prevline.strip().startswith('@'):
					tag = prevline.strip()[1:]
				else:
					tag = None

				lang = line.strip().split('```')[-1]
		# The middle of a code block.
		elif in_code:
			code.append(line)
		else:
			doc.append(line)

		prevline = line

	modules['markdown'] += '\n'.join(doc)
	return modules


def build( modules, module_path, datadirs=None ):
	output = {'executeables':[], 'rust':[], 'c':[], 'c++':[], 'go':[], 'javascript':[], 'python':[], 'html':[], 'verilog':[], 'datadirs':datadirs}
	python_main = {'name':'main.py', 'script':[]}
	go_main = {'name':'main.go', 'source':[]}
	tagged = {}

	java2rusthon = []

	if modules['nim']:
		nimbin = os.path.expanduser('~/Nim/bin/nim')
		if os.path.isfile(nimbin):
			mods_sorted_by_index = sorted(modules['nim'], key=lambda mod: mod.get('index'))
			for mod in mods_sorted_by_index:
				tmpfile = tempfile.gettempdir() + '/rusthon_build.nim'
				open(tmpfile, 'wb').write( mod['code'] )
				cmd = [nimbin, 'compile', '--app:staticlib', tmpfile]
				nim = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tempfile.gettempdir())
				nim.wait()
				if nim.returncode:
					raise SyntaxError(nim.stdout.read())
				else:
					raise RuntimeError('TODO')
		else:
			print('WARNING: can not find nim compiler')

	if modules['java']:
		mods_sorted_by_index = sorted(modules['java'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			j2py = subprocess.Popen(['j2py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			stdout,stderr  = j2py.communicate( mod['code'] )
			if stderr: raise RuntimeError(stderr)
			java2rusthon.append( stdout.replace('    ', '\t') )

	if modules['rusthon']:
		mods_sorted_by_index = sorted(modules['rusthon'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			script = mod['code']
			index = mod.get('index')
			header = script.splitlines()[0]
			backend = 'c++'  ## default to c++ backend
			if header.startswith('#backend:'):
				backend = header.split(':')[-1].strip()
				if backend not in 'c++ rust javascript go verilog'.split():
					raise SyntaxError('invalid backend: %s' %backend)

			if backend == 'myhdl':  ## TODO remove this
				vcode = compile_myhdl(script)
				modules['verilog'].append( {'code':vcode, 'index': index})  ## gets compiled below

			elif backend == 'verilog':
				vcode = pythonjs.pythonjs_to_verilog.main( script )
				modules['verilog'].append( {'code':vcode, 'index': index})  ## gets compiled below

			elif backend == 'c++':
				if java2rusthon:
					script = '\n'.join(java2rusthon) + '\n' + script
					java2rusthon = None

				pyjs = pythonjs.python_to_pythonjs.main(script, cpp=True, module_path=module_path)
				pak = pythonjs.pythonjs_to_cpp.main( pyjs )   ## pak contains: c_header and cpp_header
				modules['c++'].append( {'code':pak['main'], 'index': index})  ## gets compiled below

			elif backend == 'rust':
				pyjs = pythonjs.python_to_pythonjs.main(script, rust=True, module_path=module_path)
				rustcode = pythonjs.pythonjs_to_rust.main( pyjs )
				modules['rust'].append( {'code':rustcode, 'index': index})  ## gets compiled below

			elif backend == 'go':
				pyjs = pythonjs.python_to_pythonjs.main(script, go=True, module_path=module_path)
				gocode = pythonjs.pythonjs_to_go.main( pyjs )
				#modules['go'].append( {'code':gocode})  ## gets compiled below
				go_main['source'].append( gocode )

			elif backend == 'javascript':
				js = compile_js( mod['code'], module_path )
				for name in js:
					output['javascript'].append( {'name':name, 'script':js[name], 'index': index} )

				if len(js.keys())==1 and mod['tag']:
					tagged[ mod['tag'] ] = js['main']

	if modules['python']:
		mods_sorted_by_index = sorted(modules['python'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			if 'name' in mod:
				name = mod['name']
				if name.endswith('.md'):
					python_main['script'].append( mod['code'] )
				else:
					output['python'].append( {'name':name, 'script':mod['code']} )
			else:
				python_main['script'].append( mod['code'] )

	if modules['html']:
		mods_sorted_by_index = sorted(modules['html'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			html = []
			for line in mod['code'].splitlines():
				## `~/some/path/myscript.js` special syntax to copy javascript directly into the output html, good for testing locally.
				if line.strip().startswith('<script ') and line.strip().endswith('</script>') and 'src="~/' in line:
					url = line.split('src="')[-1].split('"')[0]
					url = os.path.expanduser( url )
					if os.path.isfile(url):
						html.append('<script type="text/javascript">')
						html.append( open(url, 'rb').read() )
						html.append('</script>')
					else:
						print('WARNING: could not find file: %s' %url)
						html.append( line )
				else:
					html.append( line )

			html = '\n'.join(html)

			for tagname in tagged:
				tag = '<@%s>' %tagname
				js  = tagged[tagname]
				if tag in html:
					html = html.replace(tag, '<script type="text/javascript">\n%s</script>' %js)
			mod['code'] = html
			output['html'].append( mod )

	if modules['verilog']:
		source = []
		mods_sorted_by_index = sorted(modules['verilog'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			source.append( mod['code'] )
		source = '\n'.join(source)

		mod = {}
		output['verilog'].append(mod)

		if os.path.isfile('/usr/bin/iverilog') or os.path.isfile('/usr/local/bin/iverilog'):
			mod['source'] = source
			mod['binary'] = tempfile.gettempdir() + '/rusthon-sv-build.vvp'
			mod['name']   = 'main.vvp'
			output['executeables'].append( mod['binary'] )
			tmpfile = tempfile.gettempdir() + '/rusthon-verilog-build.sv'
			open(tmpfile, 'wb').write( source )
			## note: iverilog defaults to verilog mode, not systemverilog, `-g2005-sv` is required. '-g2012' also works.
			cmd = [
				'iverilog', 
				'-g2005-sv',
				'-o', 
				'rusthon-sv-build.vvp', 
				tmpfile
			]
			p = subprocess.Popen(cmd, cwd=tempfile.gettempdir(), stdout=subprocess.PIPE, stderr=subprocess.PIPE )
			p.wait()
			if p.returncode != 0:
				srclines = source.splitlines()
				err = p.stderr.read()  ## ends with "I give up."
				errors = []
				for line in err.splitlines():
					if 'syntax error' in line:
						errors.append('- - - - - - - - - - - -')
						lineno = int( line.split(':')[-2] )
						e = [
							'Syntax Error - line: %s' %lineno,
						]
						if lineno-2 < len(srclines):
							e.append( srclines[lineno-2] )
						if lineno-1 < len(srclines):
							e.append( srclines[lineno-1] )
						if lineno < len(srclines):
							e.append( srclines[lineno] )

						errors.extend( e )
					else:
						errors.append(line)

				msg = [' '.join(cmd)]
				for i,line in enumerate(source.splitlines()):
					msg.append('%s:	%s' %(i+1, line))
				msg.extend(errors)
				raise RuntimeError('\n'.join(msg))


		else:
			print('WARNING: could not find iverilog')
			mod['code'] = source

	if modules['go']:
		for mod in modules['go']:
			if 'name' in mod:
				name = mod['name']
				if name.endswith('.md'):
					go_main['source'].append( mod['code'] )
				else:
					output['go'].append( mod )
			else:
				go_main['source'].append( mod['code'] )

	if go_main['source']:
		go_main['source'] = '\n'.join(go_main['source'])
		output['go'].insert( 0, go_main )

	if output['go']:
		source = [ mod['source'] for mod in output['go'] ]
		tmpfile = tempfile.gettempdir() + '/rusthon-go-build.go'
		open(tmpfile, 'wb').write( '\n'.join(source) )
		cmd = ['go', 'build', tmpfile]
		subprocess.check_call(['go', 'build', tmpfile], cwd=tempfile.gettempdir() )
		mod['binary'] = tempfile.gettempdir() + '/rusthon-go-build'
		output['executeables'].append(tempfile.gettempdir() + '/rusthon-go-build')

	link = []

	if modules['rust']:
		source = []
		mods_sorted_by_index = sorted(modules['rust'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			source.append( mod['code'] )

		tmpfile = tempfile.gettempdir() + '/rusthon-build.rs'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )

		if modules['c++']:
			libname = 'rusthon-lib%s' %len(output['rust'])
			link.append(libname)
			subprocess.check_call(['rustc', '--crate-name', 'rusthon', '--crate-type', 'staticlib' ,'-o', tempfile.gettempdir() + '/'+libname,  tmpfile] )
			output['rust'].append( {'source':data, 'staticlib':libname, 'name':'lib'+libname+'.a'} )

		else:
			subprocess.check_call(['rustc', '--crate-name', 'rusthon', '-o', tempfile.gettempdir() + '/rusthon-bin',  tmpfile] )
			output['rust'].append( {'source':data, 'binary':tempfile.gettempdir() + '/rusthon-bin', 'name':'rusthon-bin'} )
			output['executeables'].append(tempfile.gettempdir() + '/rusthon-bin')

	if modules['c']:
		libname = 'rusthon-clib%s' %len(output['c'])
		link.append(libname)
		source = []
		mods_sorted_by_index = sorted(modules['c'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			source.append( mod['code'] )

		tmpfile = tempfile.gettempdir() + '/rusthon-build.c'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )
		cmd = ['gcc', '-c', tmpfile, '-o', tempfile.gettempdir() + '/'+libname+'.o' ]
		subprocess.check_call( cmd )
		cmd = ['ar', 'rcs', tempfile.gettempdir() + '/lib'+libname+'.a', tempfile.gettempdir() + '/'+libname+'.o']
		subprocess.check_call( cmd )
		output['c'].append({'source':data, 'staticlib':libname+'.a'})


	if modules['c++']:
		source = []
		mods_sorted_by_index = sorted(modules['c++'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			source.append( mod['code'] )

		tmpfile = tempfile.gettempdir() + '/rusthon-c++-build.cpp'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )
		cmd = ['g++', '-O3', '-fprofile-generate', '-march=native', '-mtune=native']
		cmd.extend(
			[tmpfile, '-o', tempfile.gettempdir() + '/rusthon-c++-bin', '-pthread', '-std=c++11' ]
		)
		if link:
			cmd.append('-static')
			cmd.append('-L' + tempfile.gettempdir() + '/.')
			for libname in link:
				cmd.append('-l'+libname)
		subprocess.check_call( cmd )
		output['c++'].append( {'source':data, 'binary':tempfile.gettempdir() + '/rusthon-c++-bin', 'name':'rusthon-c++-bin'} )
		output['executeables'].append(tempfile.gettempdir() + '/rusthon-c++-bin')

	if python_main['script']:
		python_main['script'] = '\n'.join(python_main['script'])
		output['python'].append( python_main )

	return output

def save_tar( package, path='build.tar' ):
	import tarfile
	import StringIO
	tar = tarfile.TarFile(path,"w")

	if package['datadirs']:
		for datadir in package['datadirs']:
			for name in os.listdir(datadir):
				a = os.path.join(datadir,name)
				tar.add(a)  ## files and folders

	exts = {'rust':'.rs', 'c++':'.cpp', 'javascript':'.js', 'python':'.py', 'go':'.go', 'html': '.html', 'verilog':'.sv'}
	for lang in 'rust c++ go javascript python html verilog'.split():
		for info in package[lang]:
			name = 'untitled'
			if 'name' in info: name = info['name']

			source = False
			is_bin = False
			s = StringIO.StringIO()
			if 'staticlib' in info:
				s.write(open(info['staticlib'],'rb').read())
				source = info['source']
			elif 'binary' in info:
				s.write(open(info['binary'],'rb').read())
				source = info['source']
				is_bin = True
			elif 'code' in info:
				if lang=='verilog': print(info['code'])  ## just for testing.
				s.write(info['code'])
			elif 'script' in info:
				s.write(info['script'])
			s.seek(0)

			if not is_bin and not source and not name.endswith( exts[lang] ):
				name += exts[lang]

			ti = tarfile.TarInfo(name=name)
			ti.size=len(s.buf)
			if is_bin: ti.mode = 0777
			tar.addfile(tarinfo=ti, fileobj=s)

			if source:
				s = StringIO.StringIO()
				s.write(source)
				s.seek(0)
				ti = tarfile.TarInfo( name = name + '-source' + exts[lang] )
				ti.size=len(s.buf)
				tar.addfile(tarinfo=ti, fileobj=s)


	tar.close()

def main():
	if len(sys.argv)==1:
		print('usage: ./rusthon.py [python files] [markdown files] [tar file] [--run=]')
		return

	modules = new_module()

	save = False
	paths = []
	scripts = []
	markdowns = []
	gen_md = False
	output_tar = 'rusthon-build.tar'
	launch = []
	datadirs = []

	for arg in sys.argv[1:]:
		if os.path.isdir(arg):
			paths.append(arg)
		elif arg.startswith('--data='):
			datadirs.extend( arg.split('=')[-1].split(',') )
		elif arg.startswith('--run='):
			launch.extend( arg.split('=')[-1].split(',') )
			save = True
		elif arg.endswith('.py'):
			scripts.append(arg)
		elif arg.endswith('.md'):
			markdowns.append(arg)
		elif arg.endswith('.tar'):
			output_tar = arg
			save = True
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

	package = build(modules, base_path, datadirs=datadirs )

	if not save:
		for exe in package['executeables']:
			print('running: %s' %exe)
			subprocess.check_call( exe )

		if package['html']:
			import webbrowser
			for i,page in enumerate(package['html']):
				tmp = tempfile.gettempdir() + '/rusthon-webpage%s.html' %i
				open(tmp, 'wb').write( page['code'] )
				webbrowser.open(tmp)

	else:
		save_tar( package, output_tar )
		print('saved build to:')
		print(output_tar)

		if launch:
			tmpdir = tempfile.gettempdir()
			tmptar = os.path.join(tmpdir, 'temp.tar')
			open(tmptar, 'wb').write(
				open(output_tar, 'rb').read()
			)
			subprocess.check_call( ['tar', '-xvf', tmptar], cwd=tmpdir )

			for name in launch:
				if name.endswith('.py'):
					firstline = open(os.path.join(tmpdir, name), 'rb').readlines()[0]
					python = 'python'
					if firstline.startswith('#!'):
						if 'python3' in firstline:
							python = 'python3'
					subprocess.call( [python, name], cwd=tmpdir )

				elif name.endswith('.js'):
					subprocess.call( ['node', name],   cwd=tmpdir )

				else:
					subprocess.call( [name], cwd=tmpdir )



if __name__ == '__main__':
    main()


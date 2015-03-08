#!/usr/bin/env python
__version__ = '0.9.9'
import os, sys, subprocess, hashlib
#import pythonjs
#import pythonjs.pythonjs
#import pythonjs.python_to_pythonjs
#import pythonjs.pythonjs_to_cpp
#import pythonjs.pythonjs_to_verilog
#import pythonjs.typedpython as typedpython
import tempfile


def compile_js( script, module_path, main_name='main', directjs=False, directloops=False ):
	'''
	directjs = False     ## compatible with pythonjs-minimal.js
	directloops = False  ## allows for looping over strings, arrays, hmtlElements, etc. if true outputs cleaner code.
	'''
	fastjs = True  ## this is now the default, and complete python mode is deprecated
	result = {}

	pyjs = python_to_pythonjs(
		script,
		module_path=module_path,
		fast_javascript = fastjs,
		pure_javascript = directjs
	)

	if isinstance(pyjs, dict):  ## split apart by webworkers
		for jsfile in a:
			result[ jsfile ] = translate_to_javascript(
				a[jsfile],
				webworker=jsfile != 'main',
				requirejs=False,
				insert_runtime=False,
				fast_javascript = fastjs,
				fast_loops      = directloops
			)

	else:

		code = translate_to_javascript(
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

	if main_name != 'main':
		#assert main_name.endswith('.js')  ## allow tag names
		result[main_name] = result.pop('main')

	return result

def compile_java( javafiles ):
	assert 'JAVA_HOME' in os.environ
	tmpdir  = tempfile.gettempdir()
	cmd = ['javac']
	cmd.extend( javafiles )
	print(' '.join(cmd))
	subprocess.check_call(cmd, cwd=tmpdir)
	classfiles = [jfile.replace('.java', '.class') for jfile in javafiles]
	cmd = ['jar', 'cvf', 'mybuild.jar']
	cmd.extend( classfiles )
	print(' '.join(cmd))
	subprocess.check_call(cmd, cwd=tmpdir)
	jarfile = os.path.join(tmpdir,'mybuild.jar')
	assert os.path.isfile(jarfile)
	return {'class-files':classfiles, 'jar':jarfile}


def compile_giws_bindings( xml ):
	tmpdir  = tempfile.gettempdir()
	tmpfile = os.path.join(tmpdir, 'rusthon_giws.xml')
	open(tmpfile, 'wb').write(xml)
	cmd = [
		'giws',
		'--description-file='+tmpfile,
		'--output-dir='+tmpdir,
		#'--per-package',
		'--disable-return-size-array',
		#'--throws-exception-on-error', # requires GiwsException.hxx and GiwsException.cpp
	]
	#subprocess.check_call(cmd)
	proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	proc.wait()
	if proc.returncode:
		raise RuntimeError(proc.stderr.read())
	else:
		headers = []
		impls = []
		for line in proc.stdout.read().splitlines():
			if line.endswith(' generated ...'):  ## TODO something better
				name = line.split()[0]
				if name.endswith('.hxx'):
					headers.append( name )
				elif name.endswith('.cpp'):
					impls.append( name )

		code = []
		for header in headers:
			data = open(os.path.join(tmpdir,header), 'rb').read()
			code.append( data )

		for impl in impls:
			data = open(os.path.join(tmpdir,impl), 'rb').read()
			lines = ['/* %s */' %impl]
			includes = []  ## ignore these
			for line in data.splitlines():
				if line.startswith('#include'):
					includes.append(line)
				else:
					lines.append(line)
			code.append( '\n'.join(lines) )

		return '\n'.join(code)

def java_to_rusthon( input ):
	j2pybin = 'j2py'
	if os.path.isfile(os.path.expanduser('~/java2python/bin/j2py')):
		j2pybin = os.path.expanduser('~/java2python/bin/j2py')
	print('======== %s : translate to rusthon' %j2pybin)
	j2py = subprocess.Popen([j2pybin, '--rusthon'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	stdout,stderr  = j2py.communicate( input )
	if stderr: raise RuntimeError(stderr)
	if j2py.returncode: raise RuntimeError('j2py error!')
	print(stdout)
	print('---------------------------------')
	rcode = typedpython.transform_source(stdout.replace('    ', '\t'))
	print(rcode)
	print('---------------------------------')
	return rcode


def hack_nuitka(data):
	out = []
	for line in data.splitlines():
		if line.startswith('#include'):  ## do not include anything
			pass
		else:
			out.append(line)
	return '\n'.join(out)

def hack_nuitka_main(data, functions):
	out = []
	for line in data.splitlines():
		if line.startswith('#include'):  ## do not include anything
			pass
		elif line.startswith('static PyObject *impl_function_'):
			fname = line.split('impl_function_')[-1].split('(')[0]
			findex = fname.split('_')[0]
			fname  = fname.split('_')[1]
			cname  = line.split('static PyObject *')[-1].split('(')[0]
			func = {
				'name':fname,
				'cname': cname,
			}
			out.append(line)

		elif line.strip()=='#ifdef _NUITKA_WINMAIN_ENTRY_POINT':
			## cut away main ##
			break
		else:
			out.append(line)

	return '\n'.join(out)

def nuitka_compile(source, functions):
	'''
	not: all the headers can be removed, except `__helpers.hpp`,
	because that gets included from `calling.hpp` (part of the Nuitka public headers)
	'''
	tmp = tempfile.gettempdir()
	file = os.path.join(tmp,'nuitka_build.py')
	open(file, 'wb').write(source)
	subprocess.check_call(['nuitka', '--generate-c++-only', file], cwd=tmp)
	bdir = os.path.join(tmp, 'nuitka_build.build')
	assert os.path.isdir(bdir)
	constbin  = None
	helpers   = None
	headers   = ['#include "nuitka/prelude.hpp"']
	sources   = []

	for name in os.listdir(bdir):
		data = open(os.path.join(bdir,name), 'rb').read()
		if name == '__constants.bin':
			constbin = data
		elif name == '__helpers.hpp':
			helpers = data
		elif name.endswith('.hpp'):
			headers.append(data)
		elif name.endswith('.cpp'):
			if name.startswith('module.') and name.endswith('__main__.cpp'):
				data = hack_nuitka_main(data, functions)
			else:
				data = hack_nuitka( data )
			sources.append(data)
		else:
			raise RuntimeError('invalid file found in nuitka build: %s' %name)

	assert helpers
	return {
		'files':[
			{'name':'__helpers.hpp', 'data':helpers}
		],
		'main':'\n'.join(headers+sources)
	}

def convert_to_markdown_project(path, rust=False, python=False, asm=False, c=False, cpp=False, java=False, java2rusthon=False, giws=False, file_metadata=False):
	files = []
	exts = []
	if rust: exts.append('.rs')
	if python: exts.append('.py')
	if asm: exts.append('.s')
	if c:   exts.append('.c')
	if cpp: exts.append('.cpp')
	if java: exts.append('.java')
	exts = tuple(exts)

	if os.path.isfile(path):
		files.append( path )

	elif os.path.isdir(path):
		for name in os.listdir(path):
			if name.endswith( exts ):
				files.append(os.path.join(path,name))

	project = []
	for file in files:
		print('reading: ', file)

		data = open(file, 'rb').read()
		header = []
		if file_metadata:
			header.extend([
			'#' + os.path.split(file)[-1],
			'* file: ' + file,
			'* md5sum   : %s' %hashlib.md5(data).hexdigest(),
			'* changed  : %s' %os.stat(file).st_mtime,
			''
			])
		lang = ''
		if file.endswith('.rs'):
			lang = 'rust'
		elif file.endswith('.py'):
			lang = 'python'
		elif file.endswith('.s'):
			lang = 'asm'
		elif file.endswith('.c'):
			lang = 'c'
		elif file.endswith('.cpp'):
			lang = 'c++'
		elif file.endswith('.java'):
			if java2rusthon:
				## pre converts into rusthon in markdown, for hand editing ##
				lang = 'rusthon'
				data = java_to_rusthon(data)
			else:
				## this still trigers java2rusthon at final compile time ##
				lang = 'java'

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

			if False:
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
		'xml'     : [],
		'javascript':[],
	}

def import_md( url, modules=None, index_offset=0 ):
	assert modules is not None
	doc = []
	code = []
	lang = False
	in_code = False
	index = 0
	prevline = None
	tag = None
	fences = 0
	base_path, markdown_name = os.path.split(url)
	data = open(url, 'rb').read()

	for line in data.splitlines():
		# Start or end of a code block.
		if line.strip().startswith('```'):
			fences += 1
			# End of a code block.
			if in_code:
				if lang:
					p, n = os.path.split(url)
					mod = {'path':p, 'markdown':url, 'code':'\n'.join(code), 'index':index+index_offset, 'tag':tag }
					if tag and '.' in tag:
						ext = tag.split('.')[-1].lower()
						if ext in 'html js css py c h cpp hpp rust go java'.split():
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
			## import submarkdown file ##
			if line.startswith('* ') and '@import' in line and line.count('[')==1 and line.count(']')==1 and line.count('(')==1 and line.count(')')==1:
				submarkdown = line.split('(')[-1].split(')')[0].strip()
				subpath = os.path.join(base_path, submarkdown)
				if not os.path.isfile(subpath):
					raise RuntimeError('error: can not find markdown file: '+subpath)
				index += import_md( subpath, modules, index_offset=index )

			doc.append(line)

		prevline = line

	modules['markdown'] += '\n'.join(doc)
	if fences % 2:
		raise SyntaxError('invalid markdown - unclosed tripple back quote fence in: %s' %url)


	return index

def hack_nim_stdlib(code):
	'''
	already talked to the nim guys in irc, they dont know why these dl functions need to be stripped
	'''
	out = []
	for line in code.splitlines():
		if 'dlclose(' in line or 'dlopen(' in line or 'dlsym(' in line:
			pass
		else:
			out.append( line )
	return '\n'.join(out)

def hack_nim_code(code):
	'''
	this is required because nim outputs multiple c files that we merge into a single c file,
	some functions in stdlib_system.c are inlined into the main code here, and they must be removed.
	'''
	out = []
	skip_structs = ['TGenericSeq', 'NimStringDesc']
	skip_struct = False
	skip_inline = False

	for line in code.splitlines():
		if line.startswith('static N_INLINE('):
			#if 'nimFrame' in line or 'popFrame' in line or 'initStackBottomWith' in line: --deadCodeElim:on removes initStackBottomWith
			if 'nimFrame' in line or 'popFrame' in line:
				if line.strip().endswith(';'):
					continue
				elif line.strip().endswith('{'):
					skip_inline = True
				else:
					raise RuntimeError('error parsing nim c code')
			else:
				out.append(line)  ## TODO check these
		elif line.startswith('struct '):
			for s in skip_structs:
				if s in line:
					skip_struct = True
					break
			if skip_struct:
				continue
			else:
				out.append(line)
		elif skip_inline:
			if line=='}':
				skip_inline = False
			continue
		elif skip_struct:
			if line=='};':
				skip_struct = False
			continue
		else:
			out.append(line)

	return '\n'.join(out)


def gen_nim_wrappers(src, out):
	for line in src.splitlines():
		## check if line is a function that exports to C ##
		if line.startswith('proc ') and '{.' in line and '.}' in line and 'cdecl' in line and 'exportc' in line:
			funcname = line.split('proc ')[-1].strip().split('(')[0]
			restype  = line.split(':')[-1].split('{')[0].strip()
			if not restype or not restype.startswith('c'):
				raise RuntimeError('TODO: some other nim return type')
			if restype=='cstring':
				raise RuntimeError('TODO: nim function returns cstring')

			restype = restype[1:] ## strip `c` prefix
			args = line.split('(')[-1].split(')')[0]
			wargs = []
			for arg in args.split(','):
				name, type = arg.split(':')
				name = name.strip()
				type = type.strip()
				if not type=='cstring':  ## keep as cstring because we define that as `char*`
					type = type[1:] # strip the `c` prefix
				wargs.append( '%s:%s' %(name,type))

			wrap = [
				'	def %s(%s) ->%s:' %(funcname, ','.join(wargs), restype),
				'		pass'
			]
			out.extend(wrap)

def build( modules, module_path, datadirs=None ):
	output = {'executeables':[], 'rust':[], 'c':[], 'c++':[], 'go':[], 'javascript':[], 'java':[], 'xml':[], 'python':[], 'html':[], 'verilog':[], 'nim':[], 'lua':[], 'dart':[], 'datadirs':datadirs}
	python_main = {'name':'main.py', 'script':[]}
	go_main = {'name':'main.go', 'source':[]}
	tagged  = {}
	link    = []
	giws    = []   ## xml jni generator so c++ can call into java, blocks tagged with @gwis are compiled and linked with the final exe.
	java2rusthon = []
	nim_wrappers = []

	libdl = False ## provides: dlopen, dlclose, for dynamic libs. Nim needs this

	if modules['nim']:
		libdl = True
		nimbin = os.path.expanduser('~/Nim/bin/nim')
		niminclude = os.path.expanduser('~/Nim/lib')
		if os.path.isfile(nimbin):
			mods_sorted_by_index = sorted(modules['nim'], key=lambda mod: mod.get('index'))
			for mod in mods_sorted_by_index:

				if mod['tag']:  ## save standalone nim program, can be run with `rusthon.py my.md --run=myapp.nim`
					output['nim'].append(mod)

				else:  ## use nim to translate to C and build later as staticlib
					tmpfile = tempfile.gettempdir() + '/rusthon_build.nim'
					nimsrc = mod['code'].replace('\t', '  ')  ## nim will not accept tabs, replace with two spaces.
					gen_nim_wrappers( nimsrc, nim_wrappers )
					open(tmpfile, 'wb').write( nimsrc )
					#cmd = [nimbin, 'compile', '--noMain', '--app:staticlib', 'rusthon_build.nim']
					cmd = [
						nimbin,
						'compile',
						'--header',
						'--noMain',
						'--noLinking',
						'--compileOnly',
						'--genScript',   ## broken?
						'--app:staticlib', ## Araq says staticlib and noMain will not work together.
						'--deadCodeElim:on',
						'rusthon_build.nim',
					]
					print('-------- compile nim program -----------')
					print(' '.join(cmd))
					subprocess.check_call(cmd, cwd=tempfile.gettempdir())

					## staticlib broken in nim? missing dlopen
					#libname = 'rusthon_build.nim'
					#link.append(libname)
					#output['c'].append({'source':mod['code'], 'staticlib':libname+'.a'})

					## get source from nim cache ##
					nimcache = os.path.join(tempfile.gettempdir(), 'nimcache')
					nim_stdlib = hack_nim_stdlib(
						open(os.path.join(nimcache,'stdlib_system.c'), 'rb').read()
					)
					#nim_header = open(os.path.join(nimcache,'rusthon_build.h'), 'rb').read()
					nim_code   = hack_nim_code(
						open(os.path.join(nimcache,'rusthon_build.c'), 'rb').read()
					)

					## gets compiled below
					cfg = {
						'link-dirs' :[nimcache, niminclude],
						#'build-dirs':[nimcache],  ## not working
						'index'    : mod['index'],
						'code'     : '\n'.join([nim_stdlib, nim_code])
						#'code'     : header
					}
					modules['c'].append( cfg )
		else:
			print('WARNING: can not find nim compiler')

	if modules['java']:
		mods_sorted_by_index = sorted(modules['java'], key=lambda mod: mod.get('index'))
		javafiles = []
		tmpdir = tempfile.gettempdir()
		for mod in mods_sorted_by_index:
			if mod['tag']=='java2rusthon':
				rcode = java_to_rusthon( mod['code'] )
				java2rusthon.append( rcode )
			elif 'name' in mod:
				jpath = os.path.join(tmpdir, mod['name'])
				if '/' in mod['name']:
					jdir,jname = os.path.split(jpath)
					if not os.path.isdir(jdir):
						os.makedirs(jdir)
				open(jpath, 'wb').write(mod['code'])
				javafiles.append( jpath )
			else:
				raise SyntaxError('java code must have a tag header: `java2rusthon` or a file path')

		if javafiles:
			output['java'].append( compile_java( javafiles ) )


	if modules['xml']:
		mods_sorted_by_index = sorted(modules['xml'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			if mod['tag']=='gwis':
				giws.append(mod['code'])  ## hand written bindings should get saved in output tar.
				bindings = compile_giws_bindings(mod['code'])
				modules['c++'].append( {'code':bindings, 'index': mod['index']})  ## gets compiled below
			else:
				output['xml'].append(mod)

	js_merge  = []
	cpp_merge = []

	if modules['rusthon']:
		mods_sorted_by_index = sorted(modules['rusthon'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			script = mod['code']
			index = mod.get('index')
			header = script.splitlines()[0]
			backend = 'c++'  ## default to c++ backend
			if header.startswith('#backend:'):
				backend = header.split(':')[-1].strip()
				if backend not in 'c++ rust javascript go verilog dart lua'.split():
					raise SyntaxError('invalid backend: %s' %backend)


			if backend == 'verilog':
				vcode = translate_to_verilog( script )
				modules['verilog'].append( {'code':vcode, 'index': index})  ## gets compiled below

			elif backend == 'c++':
				cpp_merge.append(script)

			elif backend == 'rust':
				pyjs = python_to_pythonjs(script, rust=True, module_path=module_path)
				rustcode = translate_to_rust( pyjs )
				modules['rust'].append( {'code':rustcode, 'index': index})  ## gets compiled below

			elif backend == 'go':
				pyjs = python_to_pythonjs(script, go=True, module_path=module_path)
				gocode = translate_to_go( pyjs )
				#modules['go'].append( {'code':gocode})  ## gets compiled below
				go_main['source'].append( gocode )

			elif backend == 'javascript':
				if mod['tag']:  ## saves to external js file
					js = compile_js( mod['code'], module_path, main_name=mod['tag'] )
					mod['build'] = {'script':js[mod['tag']]}
					tagged[ mod['tag'] ] = js[mod['tag']]
					for name in js:
						output['javascript'].append( {'name':name, 'script':js[name], 'index': index} )
				else:
					js_merge.append(mod)

			elif backend == 'lua':
				pyjs = python_to_pythonjs(script, lua=True, module_path=module_path)
				luacode = translate_to_lua( pyjs )
				name = 'main.lua'
				if mod['tag']: name = mod['tag']
				if not name.endswith('.lua'): name += '.lua'
				output['lua'].append( {'name':name, 'script':luacode, 'index': index} )

			elif backend == 'dart':
				pyjs = python_to_pythonjs(script, dart=True, module_path=module_path)
				dartcode = translate_to_dart( pyjs )
				name = 'main.dart'
				if mod['tag']: name = mod['tag']
				if not name.endswith('.dart'): name += '.dart'
				output['dart'].append( {'name':name, 'script':dartcode, 'index': index} )

	if js_merge:
		tagname = None
		src = []
		for mod in js_merge:
			if mod['tag']:
				if tagname is not None:
					raise RuntimeError('TODO multiple tag insertions')
				tagname = mod['tag']
				src.append( mod['code'] )
			else:
				src.append(mod['code'])

			assert tagname
			js = compile_js( '\n'.join(src), module_path, main_name=tagname )
			tagged[ tagname ] = js[ tagname ]
			for name in js:
				output['javascript'].append( {'name':name, 'script':js[name], 'index': index} )

	nuitka = []
	nuitka_include_path = None  ## TODO option for this
	if modules['python']:
		mods_sorted_by_index = sorted(modules['python'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			if mod['tag']:
				name = mod['tag']
				if name == 'nuitka':
					nuitka.append(mod['code'])
				else:
					if not name.endswith('.py'):
						name += '.py'
					output['python'].append( {'name':name, 'script':mod['code']} )
			else:
				if len(output['python'])==0:
					python_main['script'].append( mod['code'] )
				else:
					output['python'][-1]['script'] += '\n' + mod['code']


	if cpp_merge:
		merge = []
		nuitka_funcs = []
		if java2rusthon:
			merge.extend(java2rusthon)
			java2rusthon = None
		if nim_wrappers:
			## inserts generated rusthon nim wrappers into script before translation ##
			nim_wrappers.insert(0,'# nim wrappers generated by rusthon #')
			nim_wrappers.insert(1, 'with extern(abi="C"):')
			merge.extend(nim_wrappers)
		if nuitka:
			npak = nuitka_compile('\n'.join(nuitka), nuitka_funcs)
			for h in npak['files']:
				modules['c++'].append(
					{'code':h['data'], 'tag':h['name'], 'index':0}
				)

		merge.extend(cpp_merge)
		script = '\n'.join(merge)
		pyjs = python_to_pythonjs(script, cpp=True, module_path=module_path)
		pak = translate_to_cpp( pyjs )   ## pak contains: c_header and cpp_header
		n = len(modules['c++']) + len(giws)
		cppcode = pak['main']
		if nuitka:
			cppcode = npak['main'] + '\n' + cppcode
		modules['c++'].append( {'code':cppcode, 'index':n+1})  ## gets compiled below



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
		mainmod = None
		mods_sorted_by_index = sorted(modules['verilog'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			source.append( mod['code'] )
			if 'name' in mod and mod['name']=='main':
				mainmod = mod
			elif mainmod is None:
				mainmod = mod

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
				if name=='main':
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


	if modules['rust']:
		source = []
		mainmod = None
		mods_sorted_by_index = sorted(modules['rust'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			source.append( mod['code'] )
			if 'name' in mod and mod['name']=='main':
				mainmod = mod
			elif mainmod is None:
				mainmod = mod

		tmpfile = tempfile.gettempdir() + '/rusthon-build.rs'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )

		pak = None
		if modules['c++']:
			libname = 'rusthon-lib%s' %len(output['rust'])
			link.append(libname)
			subprocess.check_call(['rustc', '--crate-name', 'rusthon', '--crate-type', 'staticlib' ,'-o', tempfile.gettempdir() + '/'+libname,  tmpfile] )
			pak = {'source':data, 'staticlib':libname, 'name':'lib'+libname+'.a'}

		else:
			subprocess.check_call(['rustc', '--crate-name', 'rusthon', '-o', tempfile.gettempdir() + '/rusthon-bin',  tmpfile] )
			pak = {'source':data, 'binary':tempfile.gettempdir() + '/rusthon-bin', 'name':'rusthon-bin'}
			output['executeables'].append(tempfile.gettempdir() + '/rusthon-bin')

		assert pak
		mainmod['build'] = pak
		output['rust'].append( pak )


	if modules['c']:
		source   = []
		cinclude = []
		cbuild   = []
		mods_sorted_by_index = sorted(modules['c'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			if 'link-dirs' in mod:
				cinclude.extend(mod['link-dirs'])
			if 'build-dirs' in mod:
				for bdir in mod['build-dirs']:
					for fname in os.listdir(bdir):
						if fname.endswith('.c'):
							cbuild.append(os.path.join(bdir,fname))

			if 'code' in mod and mod['code']:
				source.append( mod['code'] )
			else:
				## module must contain a build config
				raise RuntimeError('missing code')

		if source:
			libname = 'default-clib%s' %len(output['c'])
			link.append(libname)
			tmpfile = tempfile.gettempdir() + '/rusthon-build.c'
			data = '\n'.join(source)
			open(tmpfile, 'wb').write( data )
			cmd = ['gcc']
			for idir in cinclude:
				cmd.append('-I'+idir)

			cmd.extend(['-c', tmpfile])

			if cbuild:
				#gcc: fatal error: cannot specify -o with -c, -S or -E with multiple files
				#cmd.extend(cbuild)  ## extra c files `/some/path/*.c`
				raise RuntimeError('TODO fix building multiple .c files at once using gcc option -o')

			cmd.extend(['-o', tempfile.gettempdir() + '/'+libname+'.o' ])

			print('========== compiling C library =========')
			print(' '.join(cmd))
			subprocess.check_call( cmd )
			print('========== ar : staticlib ==========')
			cmd = ['ar', 'rcs', tempfile.gettempdir() + '/lib'+libname+'.a', tempfile.gettempdir() + '/'+libname+'.o']
			subprocess.check_call( cmd )
			output['c'].append({'source':data, 'staticlib':libname+'.a'})


	if modules['c++']:
		source = []
		mods_sorted_by_index = sorted(modules['c++'], key=lambda mod: mod.get('index'))
		mainmod = None
		for mod in mods_sorted_by_index:
			if 'tag' in mod and mod['tag'] and mod['tag'].endswith('.hpp'):
				## allows plain header files to be included in build directory ##
				open(
					os.path.join(tempfile.gettempdir(), mod['tag']), 'wb'
				).write( mod['code'] )
				output['c++'].append( mod )
			else:
				source.append( mod['code'] )
			if 'name' in mod and mod['name']=='main':
				mainmod = mod
			elif mainmod is None:
				mainmod = mod

		tmpfile = tempfile.gettempdir() + '/rusthon-c++-build.cpp'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )
		cmd = ['g++', '-O3', '-fprofile-generate', '-march=native', '-mtune=native', '-I'+tempfile.gettempdir()]

		if nuitka:
			if not nuitka_include_path:
				nuitka_include_path = '/usr/local/lib/python2.7/dist-packages/nuitka/build/include'
			cmd.append('-lpython')
			cmd.append('-I'+nuitka_include_path)
			cmd.append('-I/usr/include/python2.7')

		cmd.extend(
			[tmpfile, '-o', tempfile.gettempdir() + '/rusthon-c++-bin', '-pthread', '-std=c++11' ]
		)


		if link or giws:

			if libdl:
				cmd.append('-ldl')

			if giws:   ## link to the JVM if giws bindings were compiled ##
				cmd.append('-ljvm')

				os.environ['LD_LIBRARY_PATH']=''
				#for jrepath in 'include include/linux jre/lib/i386 jre/lib/i386/client/'.split():
				for jrepath in 'include include/linux'.split():
					cmd.append('-I%s/%s' %(os.environ['JAVA_HOME'], jrepath))
				for jrepath in 'jre/lib/amd64 jre/lib/amd64/server/'.split():
					cmd.append('-L%s/%s' %(os.environ['JAVA_HOME'], jrepath))
					os.environ['LD_LIBRARY_PATH'] += ':%s/%s'%(os.environ['JAVA_HOME'], jrepath)
				#raise RuntimeError(os.environ['LD_LIBRARY_PATH'])

			else:  ## TODO fix jvm with static c libs
				cmd.append('-static')

			if link:  ## c staticlibs or giws c++ wrappers ##
				cmd.append('-L' + tempfile.gettempdir() + '/.')
				for libname in link:
					cmd.append('-l'+libname)

		print('========== g++ : compile main ==========')
		print(' '.join(cmd))
		subprocess.check_call( cmd )
		mainmod['build'] = {'source':data, 'binary':tempfile.gettempdir() + '/rusthon-c++-bin', 'name':'rusthon-c++-bin'}
		output['c++'].append( mainmod['build'] )
		output['executeables'].append(tempfile.gettempdir() + '/rusthon-c++-bin')

	if python_main['script']:
		python_main['script'] = '\n'.join(python_main['script'])
		output['python'].append( python_main )

	return output

def get_first_build_from_package(package):
	for lang in 'rust c++ go javascript python html verilog java nim dart lua'.split():
		for pak in package[lang]:
			return pak

def save_tar( package, path='build.tar' ):
	import tarfile
	import StringIO
	tar = tarfile.TarFile(path,"w")

	if package['datadirs']:
		for datadir in package['datadirs']:
			if os.path.isdir(datadir):
				for name in os.listdir(datadir):
					a = os.path.join(datadir,name)
					tar.add(a)  ## files and folders
			elif os.path.isfile(datadir):
				tar.add(datadir)

	exts = {'rust':'.rs', 'c++':'.cpp', 'javascript':'.js', 'python':'.py', 'go':'.go', 'html': '.html', 'verilog':'.sv', 'nim':'.nim', 'java':'.java', 'dart':'.dart', 'lua':'.lua'}
	for lang in 'rust c++ go javascript python html verilog java nim dart lua'.split():
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
			if is_bin: ti.mode = 0o777
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
		print('usage: ./rusthon.py [python files] [markdown files] [tar file] [--anaconda] [--run=] [--data=]')
		print('		[tar file] is the optional name of the output tar that contains the build')
		print()
		print('		source files, transpiled source, and output binaries.')
		print()
		print('		--run is given a list of programs to run, "--run=a.py,b.py"')
		print('		a.py and b.py can be run this way by naming the code blocks in the markdown')
		print('		using the tag syntax "@a.py" on the line before the code block.')
		print()
		print('		--data is given a list of directories to include in the build dir and tarfile.')
		print()
		print('		--anaconda run scripts with Anaconda Python, must be installed to ~/anaconda')
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
	j2r = False
	anaconda = False

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
		elif arg.startswith('--output='):
			output_file = arg.split('=')[-1]
		elif arg == '--create-md':
			gen_md = True
		elif arg == '--tar':
			save = True
		elif arg == '--java2rusthon':
			gen_md = True
			j2r = True
		elif arg == '--anaconda':
			anaconda = True

	datadirs = [os.path.expanduser(dd) for dd in datadirs]

	if j2r:
		for path in paths:
			m = convert_to_markdown_project(path, java=True, java2rusthon=True)
			assert m
			raise RuntimeError(m)

	base_path = None
	singleout = None
	for path in scripts:
		script = open(path,'rb').read()
		if '--c++' in sys.argv:          script = '#backend:c++\n'+script
		elif '--javascript' in sys.argv: script = '#backend:javascript\n'+script
		elif '--rust' in sys.argv: script = '#backend:rust\n'+script
		elif '--go' in sys.argv:   script = '#backend:go\n'+script
		elif '--dart' in sys.argv: script = '#backend:dart\n'+script
		elif '--lua' in sys.argv:  script = '#backend:lua\n'+script
		elif '--verilog' in sys.argv: script = '#backend:verilog\n'+script
		fpath,fname = os.path.split(path)
		tag = fname.split('.')[0]
		singlemod = {'name':'main', 'tag':tag, 'code':script}
		modules['rusthon'].append( singlemod )
		if base_path is None:
			base_path = os.path.split(path)[0]
		if singleout is None and output_file:
			singleout = singlemod

	for path in markdowns:
		import_md( path, modules=modules )
		if base_path is None:
			base_path = os.path.split(path)[0]

	package = build(modules, base_path, datadirs=datadirs )
	if singleout:
		pak = get_first_build_from_package(package)
		if 'source' in pak:
			open(output_file, 'wb').write(pak['source'])
		elif 'code' in pak:
			open(output_file, 'wb').write(pak['code'])
		elif 'script' in pak:
			open(output_file, 'wb').write(pak['script'])
		else:
			raise RuntimeError(pak)
		print('saved output to: %s'%output_file)

	elif not save:
		tmpdir = tempfile.gettempdir()
		## copy jar files ##
		for p in datadirs:
			if p.endswith('.jar'):
				dpath,dname = os.path.split(p)
				open(os.path.join(tmpdir,dname),'wb').write(open(p,'rb').read())
		for exe in package['executeables']:
			print('running: %s' %exe)
			subprocess.check_call(
				exe,
				cwd=tmpdir ## jvm needs this to find the .class files
			)

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

					if anaconda:
						## assume that the user installed anaconda to the default location ##
						anabin = os.path.expanduser('~/anaconda/bin')
						if not os.path.isdir(anabin):
							raise RuntimeError('Anaconda Python not installed to default location: %s' %anabin)

						subprocess.call( [os.path.join(anabin,python), name], cwd=tmpdir )

					else:
						subprocess.call( [python, name], cwd=tmpdir )

				elif name.endswith('.js'):
					subprocess.call( ['node', name],   cwd=tmpdir )

				elif name.endswith('.nim'):
					subprocess.call( ['nim', 'compile', '--run', name],   cwd=tmpdir )

				elif name.endswith('.go'):
					subprocess.call( ['go', 'run', name],   cwd=tmpdir )

				elif name.endswith('.lua'):
					subprocess.call( ['luajit', name],   cwd=tmpdir )

				elif name.endswith('.dart'):
					dartbin = os.path.expanduser('~/dart-sdk/bin/dart')
					subprocess.call( [dartbin, name],   cwd=tmpdir )

				else:
					subprocess.call( [name], cwd=tmpdir )


def bootstrap_rusthon():
	localdir = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
	mods = new_module()
	import_md( os.path.join(localdir,'src/main.md'), modules=mods )
	src = []
	mods_sorted_by_index = sorted(mods['python'], key=lambda mod: mod.get('index'))
	for mod in mods_sorted_by_index:  ## this is simplified because rusthon's source is pure python
		src.append( mod['code'] )
	src = '\n'.join(src)
	if '--dump' in sys.argv: open('/tmp/bootstrap-rusthon.py', 'wb').write(src)
	exec(src, globals())

	if '--test' in sys.argv:
		test_typedpython()  ## runs some basic tests on the extended syntax

	if '--runtime' in sys.argv:
		print('creating new runtime: pythonjs.js')
		open('pythonjs.js', 'wb').write( generate_js_runtime() )
	if '--miniruntime' in sys.argv:
		print('creating new runtime: pythonjs-minimal.js')
		open('pythonjs-minimal.js', 'wb').write( generate_minimal_js_runtime() )


if __name__ == '__main__':
	bootstrap_rusthon()
	main()


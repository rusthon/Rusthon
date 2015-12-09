#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '0.9.9'
import os, sys, subprocess, hashlib, time
import tempfile
import webbrowser

## if installed as a symbolic link, this ensures things can still be bootstrapped from the `src` subfolder
RUSTHON_LIB_ROOT = os.path.dirname(unicode(os.path.realpath(__file__), sys.getfilesystemencoding()))


GO_EXE = None
if os.path.isfile('/usr/bin/go'):
	GO_EXE = '/usr/bin/go'
elif os.path.isfile('/usr/local/go/bin/go'):
	GO_EXE = '/usr/local/go/bin/go'
elif os.path.isfile(os.path.expanduser('~/go/bin/go')):
	GO_EXE = os.path.expanduser('~/go/bin/go')

nodewebkit_runnable = False
nodewebkit = os.path.expanduser('~/nwjs-v0.12.2-linux-x64/nw')
if os.path.isfile( nodewebkit ): nodewebkit_runnable = True
else:
	nodewebkit = os.path.expanduser('~/nwjs-v0.12.3-linux-x64/nw')
	if os.path.isfile( nodewebkit ): nodewebkit_runnable = True

if sys.platform=='darwin':
	nodewebkit = os.path.expanduser('~/nwjs-v0.12.3-osx-x64/nwjs.app/Contents/MacOS/nwjs')
	if os.path.isfile( nodewebkit ):
		nodewebkit_runnable = True


## special case for linux, just for debugging, look for google-chrome,
## if found then use it to launch tests, with the --disable-gpu-sandbox
## otherwise webgl may fail on some graphics cards, this is dangerous
## and can lockup the desktop, this was an issue on Fedora21 with intel graphics,
## but is no longer an issue in Fedora22.  Enable this at your own risk.
CHROME_EXE = None
#if os.path.isfile('/opt/google/chrome-unstable/google-chrome-unstable'):
#	CHROME_EXE = '/opt/google/chrome-unstable/google-chrome-unstable'
#elif os.path.isfile('/opt/google/chrome-beta/google-chrome-beta'):
#	CHROME_EXE = '/opt/google/chrome-beta/google-chrome-beta'
#elif os.path.isfile('/opt/google/chrome/google-chrome'):
#	CHROME_EXE = '/opt/google/chrome/google-chrome'

## on fedora nodejs command is `node`, but on others it can be `nodejs`
nodejs_exe = 'node'
if os.path.isfile('/usr/sbin/ax25-node'):
	if os.path.isfile('/usr/sbin/node'):
		if os.path.realpath('/usr/sbin/node') == '/usr/sbin/ax25-node':
			nodejs_exe = 'nodejs'

JS_WEBWORKER_HEADER = u'''
var __$UID$__ = 1;
var __construct__ = function(constructor, args) {
	function F() {
		return constructor.apply(this, args);
	}
	F.prototype = constructor.prototype;
	return new F();
};

var __instances__ = {};
var __bin__  = null;
self.onmessage = function (evt) {
	var id;
	if (__bin__) {
		var bmsg;
		if (__bin__.type=="Float32Array") {
			bmsg = new Float32Array(evt.data);
		} else if (__bin__.type=="Float64Array") {
			bmsg = new Float64Array(evt.data);
		} // TODO other types

		if (__bin__.send_binary) {
			id = __bin__.send_binary;
			var ob = __instances__[id];
			var re = ob.send(bmsg);
			if (re !== undefined) {
				if (ob.send.returns=="Float32Array") {
					self.postMessage({'id':id, 'bin':ob.send.returns});
					self.postMessage(re.buffer, [re.buffer]);
				} else {
					self.postMessage({'id':id, 'message':re, 'proto':ob.send.returns});
				}
			}
		}
		__bin__ = null;
		return;
	}
	var msg = evt.data;

	if (msg.send_binary) {
		// should assert here that __bin__ is null
		__bin__ = msg;
		return;
	}
	if (msg['spawn']) {
		id = msg.spawn;
		self.postMessage({debug:"SPAWN:"+id});
		if (__instances__[id] !== undefined) {
			self.postMessage({debug:"SPAWN ERROR - existing id:"+id});

		}
		//self.postMessage({debug:"SPAWN-CLASS:"+msg['new']});
		//self.postMessage({debug:"SPAWN-ARGS:"+msg['args']});
		__instances__[id] = __construct__(eval(msg['new']), msg.args );
		__instances__[id].__uid__ = id;
	}
	if (msg['send']) {
		id = msg.send;
		//self.postMessage({debug:"SEND:"+id});
		var ob = __instances__[id];
		var re = ob.send(msg.message);
		if (re !== undefined) {
			//self.postMessage({debug:"SEND-BACK:"+re});
			self.postMessage({'id':id, 'message':re, 'proto':ob.send.returns});
		} else {
			//self.postMessage({debug:"SEND-BACK-NONE:"});
		}
	}
	if (msg['call']) {
		self.postMessage({
			'CALL'   : 1, 
			'message': self[ msg.call ].apply(null,msg.args),
			'proto'  : self[ msg.call ].returns
		});
	}
	if (msg['callmeth']) {
		id = msg.id;
		//self.postMessage({debug:"CALLM:"+id});
		var ob = __instances__[id];
		if (typeof(ob) == "undefined") {
			self.postMessage({debug:"invalid spawn instance id:"+id});
			self.postMessage({debug:"instances:"+Object.keys(__instances__).length});
		} else {
			self.postMessage({
				'CALLMETH': 1, 
				'message' : ob[msg.callmeth].apply(ob,msg.args),
				'proto'   : ob[msg.callmeth].returns
			});

		}
	}

	if (msg['get']) {
		id = msg.id;
		//self.postMessage({debug:"GET:"+id});
		var ob = __instances__[id];
		self.postMessage({'GET':1, 'message':ob[msg.get]});
	}

}
'''

OPENSHIFT_PY = [
u'''#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
from base64 import b64decode
INDEX_HTML = b64decode("%s")
''',  ## header

u'''
def application(environ, start_response):

    ctype = 'text/plain'
    if environ['PATH_INFO'] == '/health':
        response_body = "1"
    elif environ['PATH_INFO'] == '/env':
        response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
        response_body = '\\n'.join(response_body)
    else:
        ctype = 'text/html'
        response_body = INDEX_HTML

    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    #
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
''']



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
		workers = []
		mainjs = None
		for jsfile in pyjs:
			js = translate_to_javascript(
				pyjs[jsfile],
				webworker=jsfile == 'worker.js',
				requirejs=False,
				insert_runtime=False,
				fast_javascript = fastjs,
				fast_loops      = directloops,
				runtime_checks  = '--release' not in sys.argv
			)
			result[ jsfile ] = js
			if jsfile == 'worker.js':
				workers.append(js)
			else:
				mainjs = jsfile

		src = [ 'var __workersrc__ = [' ]
		a = JS_WEBWORKER_HEADER.encode('utf-8') + workers[0]
		for line in a.strip().splitlines():
			src.append(	'"%s\\n",' % line.replace('"', '\\"'))
		src.append(']')
		src.append(result[mainjs])
		result[mainjs] = '\n'.join(src)

	else:

		code = translate_to_javascript(
			pyjs,
			as_module='--ES6-module' in sys.argv,
			requirejs=False,
			insert_runtime=False,
			fast_javascript = fastjs,
			fast_loops      = directloops,
			runtime_checks  = '--release' not in sys.argv
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




def new_module():
	return {
		'markdown': '',
		'coffee'  : [],
		'python'  : [],
		'rusthon' : [],
		'rust'    : [],
		'elm'     : [],
		'c'       : [],
		'c++'     : [],
		'c#'      : [],
		'go'      : [],
		'html'    : [],
		'verilog' : [],
		'bash'    : [],
		'java'    : [],
		'nim'     : [],
		'xml'     : [],
		'json'    : [],
		'bazel'   : [],
		'gyp'     : [],
		'rapydscript':[],
		'javascript':[],
	}

def import_md( url, modules=None, index_offset=0, force_tagname=None ):
	assert modules is not None
	doc = []
	code = []
	code_links = []
	code_idirs = []
	code_defines = []
	lang = False
	in_code = False
	index = 0
	prevline = None
	tag = force_tagname or None
	fences = 0
	base_path, markdown_name = os.path.split(url)
	#data = open(url, 'rb').read().decode('utf-8')
	import codecs
	data = codecs.open(url, 'r', 'utf-8').read()

	for line in data.splitlines():
		if line.startswith('* @link:'):
			code_links.append( os.path.expanduser(line.split(':')[-1]) )
		elif line.startswith('* @include:'):
			code_idirs.append( os.path.expanduser(line.split(':')[-1]) )
		elif line.startswith('* @define:'):
			code_defines.extend( line.split(':')[-1].strip().split() )
		# Start or end of a code block.
		elif line.strip().startswith('```'):
			fences += 1
			# End of a code block.
			if in_code:
				if lang:
					if lang=='python' and 'from rusthon import *' in code:
						rusthonpy = []
						for rln in open(__file__, 'rb').read().splitlines():
							if rln == 'if __name__ == "__main__":':
								break
							else:
								rusthonpy.append(rln)
						rusthonpy = '\n'.join(rusthonpy)
						utfheader = u'# -*- coding: utf-8 -*-\n'
						code.insert(0, utfheader + BOOTSTRAPED + '\n' + rusthonpy.decode('utf-8'))
						code.pop(code.index('from rusthon import *'))

					p, n = os.path.split(url)
					mod = {
						'path':p, 
						'markdown':url, 
						'code':'\n'.join(code), 
						'index':index+index_offset, 
						'tag':tag,
						'links':code_links,
						'include-dirs':code_idirs,
						'defines':code_defines,
					}
					if tag and '.' in tag:
						ext = tag.split('.')[-1].lower()
						#if ext in 'xml html js css py c cs h cpp hpp rust go java json'.split():
						mod['name'] = tag

					modules[ lang ].append( mod )
				in_code = False
				code = []
				code_links = []
				code_idirs = []
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
				#print 'importing submarkdown'
				#print subpath
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


def is_restricted_bash( line ):
	if '&&' in line:
		return False
	if "`" in line:
		return False
	if '"' in line:
		return False

	okcmds = [
		'./configure', 
		'make', 'cmake', 
		'scons', 'bazel', 
		'cd', 'mkdir', 'cp', #'pwd', 'ls',
		'npm', 'grunt', 'gyp', 'nw-gyp',
		'apt-get', 'yum',
		'pip', 'docker', 'rhc',
	]
	cmd = line.split()[0]
	if cmd == 'sudo': cmd = line.split()[1]

	if cmd in okcmds:
		return True
	else:
		return False

GITCACHE = os.path.expanduser('~/rusthon_cache')

def build( modules, module_path, datadirs=None ):
	if '--debug-build' in sys.argv:
		raise RuntimeError(modules)
	output = {'executeables':[], 'rust':[], 'c':[], 'c++':[], 'c#':[], 'go':[], 'javascript':[], 'java':[], 'xml':[], 'json':[], 'python':[], 'html':[], 'verilog':[], 'nim':[], 'lua':[], 'dart':[], 'datadirs':datadirs, 'datafiles':{}}
	python_main = {'name':'main.py', 'script':[]}
	go_main = {'name':'main.go', 'source':[]}
	tagged  = {}
	link    = []
	giws    = []   ## xml jni generator so c++ can call into java, blocks tagged with @gwis are compiled and linked with the final exe.
	java2rusthon = []
	nim_wrappers = []
	libdl = False ## provides: dlopen, dlclose, for dynamic libs. Nim needs this
	cached_json = {}
	gyp_builds  = {}

	if modules['bash']:
		for mod in modules['bash']:
			if 'tag' in mod and mod['tag']:
				tag = mod['tag']
				if tag.startswith('http://') or tag.startswith('https://'):
					if not tag.endswith('.git'):
						raise SyntaxError('only git repos links are allowed: '+tag)
					if not os.path.isdir(GITCACHE):
						print 'making new rusthon cache folder: ' + GITCACHE
						os.mkdir(GITCACHE)

					gitname = tag.split('/')[-1][:-4]
					projectdir = os.path.join(GITCACHE, gitname)

					rebuild = True
					if gitname not in os.listdir(GITCACHE):
						cmd = ['git', 'clone', tag]
						subprocess.check_call(cmd, cwd=GITCACHE)
					elif '--git-sync' in sys.argv:
						cmd = ['git', 'pull']
						subprocess.check_call(cmd, cwd=projectdir)
					else:
						rebuild = False

					if rebuild or '--force-rebuild-deps' in sys.argv:
						print 'rebuilding git repo: ' + tag
						## TODO restrict the bash syntax allowed here,
						## or build it in a sandbox or docker container.
						for line in mod['code'].splitlines():
							if not line.strip(): continue
							if not is_restricted_bash(line):
								raise SyntaxError('bash build script syntax is restricted:\n'+line)
							else:
								print '>>'+line
							subprocess.check_call( line.split(), cwd=projectdir )

				else:
					output['datafiles'][tag] = mod['code']


	if modules['gyp']:
		for mod in modules['gyp']:
			if 'tag' in mod and mod['tag']:
				if not mod['tag'] != 'binding.gyp':
					raise RuntimeError('nw-gyp requires the gyp file is named `binding.gyp`')

			output['datafiles']['binding.gyp'] = mod['code']

			gypcfg = json.loads( mod['code'].replace("'", '"') )
			#if len(gypcfg['targets']) > 1:
			#	continue
			for gtarget in gypcfg['targets']:
				for gsrc in gtarget['sources']:
					gyp_builds[ gsrc ] = {
						'gyp':mod['code'],
						'src': None
					}


	if modules['javascript']:
		for mod in modules['javascript']:
			if 'tag' in mod and mod['tag']:
				tagged[ mod['tag'] ] = mod['code']
				if '.' in mod['tag']:
					output['datafiles'][mod['tag']] = mod['code']

	if modules['json']:
		for mod in modules['json']:
			cached_json[ mod['name'] ] = mod['code']
			output['json'].append(mod)

	if modules['c#']:
		for mod in modules['c#']:
			output['c#'].append(mod)

	if modules['elm']:
		for mod in modules['elm']:
			tmpelm = tempfile.gettempdir() + '/MyApp.elm'
			tmpjs = tempfile.gettempdir() + '/elm-output.js'
			open(tmpelm, 'wb').write(mod['code'])
			subprocess.check_call(['elm-make', tmpelm, '--output', tmpjs])
			elmdata = open(tmpjs,'rb').read()
			output['datafiles'][mod['tag']] = elmdata
			tagged[ mod['tag'] ] = elmdata


	if modules['coffee']:
		for mod in modules['coffee']:
			tmpcoff = tempfile.gettempdir() + '/temp.coffee'
			tmpjs = tempfile.gettempdir() + '/coffee-output.js'
			open(tmpcoff, 'wb').write(mod['code'])
			subprocess.check_call(['coffee', '--compile', '--bare', '--output', tmpjs, tmpcoff])
			coffdata = open(tmpjs+'/temp.js','rb').read()
			output['datafiles'][mod['tag']] = coffdata
			tagged[ mod['tag'] ] = coffdata

	if modules['rapydscript']:
		for mod in modules['rapydscript']:
			tmprapyd = tempfile.gettempdir() + '/temp.rapyd'
			tmpjs = tempfile.gettempdir() + '/rapyd-output.js'
			open(tmprapyd, 'wb').write(mod['code'].encode('utf-8'))
			subprocess.check_call(['rapydscript', tmprapyd, '--bare', '--output', tmpjs])
			rapydata = open(tmpjs,'rb').read()
			output['datafiles'][mod['tag']] = rapydata
			tagged[ mod['tag'] ] = rapydata

	if modules['nim']:
		libdl = True
		## if compile_nim_lib is False then use old hack to compile nim source by extracting it and forcing into a single file.
		compile_nim_lib = True
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
					if compile_nim_lib:
						## lets nim compile the library
						#cmd = [nimbin, 'compile', '--app:staticLib', '--noMain', '--header']  ## staticlib has problems linking with dlopen,etc.
						cmd = [nimbin, 'compile', '--app:lib', '--noMain', '--header']
					else:
						cmd = [
							nimbin,
							'compile',
							'--header',
							'--noMain',
							'--noLinking',
							'--compileOnly',
							'--genScript',   ## broken?
							'--app:staticLib', ## Araq says staticlib and noMain will not work together.
							'--deadCodeElim:on',
						]
					if 'import threadpool' in nimsrc:
						cmd.append('--threads:on')
					cmd.append('rusthon_build.nim')

					print('-------- compile nim program -----------')
					print(' '.join(cmd))
					subprocess.check_call(cmd, cwd=tempfile.gettempdir())

					if compile_nim_lib:
						## staticlib broken in nim? missing dlopen
						libname = 'rusthon_build'
						link.append(libname)
						#output['c'].append({'source':mod['code'], 'staticlib':libname+'.a'})
						output['c'].append(
							{'source':mod['code'], 'dynamiclib':libname+'.so', 'name':'lib%s.so'%libname}

						)
					else:
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
							'dynamic'   : True,
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
	cpp_links = []
	cpp_idirs = []
	cpp_defines = []
	compile_mode = 'binary'
	exename = 'rusthon-test-bin'
	tagged_trans_src = {}


	if modules['rusthon']:
		mods_sorted_by_index = sorted(modules['rusthon'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			script = mod['code']
			index = mod.get('index')
			header = script.splitlines()[0]
			backend = 'c++'  ## default to c++ backend
			if header.startswith('#backend:'):
				backend = header.split(':')[-1].strip()
				if ' ' in backend:
					backend, compile_mode = backend.split(' ')
				if '\t' in backend:
					backend, compile_mode = backend.split('\t')

				if backend not in 'c++ rust javascript go verilog dart lua'.split():
					raise SyntaxError('invalid backend: %s' %backend)

				if compile_mode and compile_mode not in 'binary staticlib dynamiclib'.split():
					raise SyntaxError('invalid backend option <%s> (valid types: binary, staticlib, dynamiclib)' %backend)

			if backend == 'verilog':
				vcode = translate_to_verilog( script )
				modules['verilog'].append( {'code':vcode, 'index': index})  ## gets compiled below

			elif backend == 'c++':
				if mod['tag'] and mod['tag'] and '.' not in mod['tag']:
					exename = mod['tag']

				## user named output for external build tools that need .h,.hpp,.cpp, files output to hardcoded paths.
				if mod['tag'] and (mod['tag'].endswith('.h') or mod['tag'].endswith('.hpp') or mod['tag'].endswith('.cpp') or mod['tag'].endswith('.cc')):
					pyjs = python_to_pythonjs(script, cpp=True, module_path=module_path)
					use_try = True
					if '--no-except' in sys.argv:
						use_try = False
					elif mod['tag'] in gyp_builds.keys():  ## nw-gyp builds without c++ exceptions
						use_try = False

					pak = translate_to_cpp(
						pyjs, 
						cached_json_files=cached_json, 
						insert_runtime=mod['tag'] in gyp_builds.keys(),
						use_try = use_try
					)
					if '--debug-c++' in sys.argv:
						raise RuntimeError(pak)
					## pak contains: c_header and cpp_header
					output['datafiles'][ mod['tag'] ] = pak['main']  ## save to output c++ to tar

					if mod['tag'] in gyp_builds.keys():
						gyp_builds[ mod['tag'] ]['src'] = pak['main']

					if 'user-headers' in pak:
						for classtag in pak['user-headers'].keys():
							classheader = pak['user-headers'][ classtag ]
							headerfile  = classheader['file']
							if headerfile in output['datafiles']:
								output['datafiles'][ headerfile ] += '\n' + '\n'.join(classheader['source'])
							else:
								output['datafiles'][ headerfile ] = '\n'  + '\n'.join(classheader['source'])

				else:
					cpp_merge.append(script)

					if 'links' in mod:
						cpp_links.extend(mod['links'])
					if 'include-dirs' in mod:
						cpp_idirs.extend(mod['include-dirs'])
					if 'defines' in mod:
						cpp_defines.extend(mod['defines'])

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
				if mod['tag'] and mod['tag'].endswith('.js'):  ## saves to external js file
					js = compile_js( mod['code'], module_path, main_name=mod['tag'] )
					mod['build'] = {'script':js[mod['tag']]}
					tagged[ mod['tag'] ] = js[mod['tag']]
					tagged_trans_src[ mod['tag'] ] = mod['code']  ## so user can embed original source using <!tagname>
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
		taggroups = {}
		for mod in js_merge:
			tagname = mod['tag']
			if tagname not in taggroups:
				taggroups[tagname] = []

			src = taggroups[tagname]
			src.append( mod['code'] )
		for tagname in taggroups.keys():
			groupsrc = '\n'.join( taggroups[tagname] )
			js = compile_js( groupsrc, module_path, main_name=tagname )
			tagged[ tagname ]           = js[ tagname ]
			tagged_trans_src[ tagname ] = groupsrc

			for name in js:
				output['javascript'].append( {'name':name, 'script':js[name], 'index': index} )


	cpyembed = []
	nuitka = []
	nuitka_include_path = None  ## TODO option for this
	nuitka_module_name  = 'unnamed_nuitka_module'
	if modules['python']:
		mods_sorted_by_index = sorted(modules['python'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			if mod['tag']:
				name = mod['tag']
				if name == 'nuitka' or name.startswith('nuitka:'):
					if ':' in name:
						nuitka_module_name = name.split(':')[-1]
					if not len(nuitka):
						## __file__ is undefined when CPython is embedded
						#cpyembed.append('sys.path.append(os.path.dirname(__file__))')
						#cpyembed.append('print sys.argv')  ## also undefined
						cpyembed.append('import sys')
						cpyembed.append('sys.path.append("./")')
						cpyembed.append('from %s import *'%nuitka_module_name)

					nuitka.append(mod['code'])

				elif name == 'embed' or name == 'embed:cpython':
					cpyembed.append(mod['code'])
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
			#npak = nuitka_compile_integrated('\n'.join(nuitka), nuitka_funcs)
			#for h in npak['files']:
			#	modules['c++'].append(
			#		{'code':h['data'], 'tag':h['name'], 'index':0}
			#	)
			nsrc = '\n'.join(nuitka)
			output['c++'].append(
				{
					'staticlib'   : nuitka_compile( nsrc, nuitka_module_name ),
					'source-name' : 'my_nuitka_module.py',
					'name'        : 'my_nuitka_module.so',
					'source'      : nsrc,
				}
			)

		merge.extend(cpp_merge)
		script = '\n'.join(merge)
		pyjs = python_to_pythonjs(script, cpp=True, module_path=module_path)
		pak = translate_to_cpp( pyjs, cached_json_files=cached_json )   ## pak contains: c_header and cpp_header
		n = len(modules['c++']) + len(giws)
		cppcode = pak['main']
		#if nuitka:
		#	cppcode = npak['main'] + '\n' + cppcode
		if cpyembed:
			inlinepy = ('\n'.join(cpyembed)).replace('\n', '\\n').replace('"', '\\"')
			staticstr = 'const char* __python_main_script__ = "%s";\n' %inlinepy
			cppcode = staticstr + cppcode
		modules['c++'].append(
			{'code':cppcode, 'index':n+1, 'links':cpp_links, 'include-dirs':cpp_idirs, 'defines':cpp_defines}
		)  ## gets compiled below



	## HTML ##
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
						html.append( open(url, 'rb').read().decode('utf-8') )
						html.append('</script>')
					elif 'git="' in line:
						giturl = line.split('git="')[-1].split('"')[0]
						print 'downloading library-> ' + giturl
						cmd = ['git', 'clone', giturl]
						subprocess.check_call(cmd, cwd=os.environ['HOME'])
						assert os.path.isfile(url)
						html.append('<script type="text/javascript">')
						html.append( open(url, 'rb').read().decode('utf-8') )
						html.append('</script>')
					elif 'source="' in line:
						srcurl = line.split('source="')[-1].split('"')[0]
						print 'downloading javascript-> ' + srcurl
						import urllib
						srcdata = urllib.urlopen(srcurl).read()
						srcpath = os.path.split(url)[0]
						if not os.path.isdir(srcpath):
							os.makedirs(srcpath)
						open(url, 'wb').write(srcdata)
						assert os.path.isfile(url)
						html.append('<script type="text/javascript">')
						html.append( open(url, 'rb').read().decode('utf-8') )
						html.append('</script>')

					else:
						print('ERROR: could not find file to inline: %s' %url)
						html.append( line )
				elif line.strip().startswith('<link ') and ('href="~/' in line or "href='~/" in line):
					zipurl = None
					if 'zip="' in line:
						zipurl = line.split('zip="')[-1].split('"')[0]

					if 'href="' in line:
						url = line.split('href="')[-1].split('"')[0]
					else:
						url = line.split("href='")[-1].split("'")[0]

					url = os.path.expanduser( url )
					if os.path.isfile(url):
						html.append('<style>')
						html.append( open(url, 'rb').read() )
						html.append('</style>')
					elif zipurl:
						import urllib
						print 'downloading css library->' + zipurl
						zipdata = urllib.urlopen(zipurl).read()
						open('/tmp/csslib.zip', 'wb').write( zipdata )
						subprocess.check_call(['unzip', '/tmp/csslib.zip'], cwd=os.environ['HOME'])
						html.append('<style>')
						html.append( open(url, 'rb').read() )
						html.append('</style>')

					else:
						print('ERROR: could not find css file to inline: %s' %url)
						html.append( line )

				else:
					html.append( line )

			html = unicode('\n'.join(html))

			for tagname in tagged:
				tag = u'<@%s>' %tagname
				js  = tagged[tagname]
				if tag in html:
					## TODO fix this ugly mess
					try:
						## javascript with unicode
						xxx = u'<script type="text/javascript" id="%s_transpiled">\n%s</script>' %(tagname, js)
					except UnicodeDecodeError:
						## rusthon translated to js
						xxx = u'<script type="text/javascript" id="%s_transpiled">\n%s</script>' %(tagname, js.decode('utf-8'))
					html = html.replace(tag, xxx)

				if tagname in tagged_trans_src.keys():
					stag = u'<!%s>' %tagname
					py  = tagged_trans_src[tagname]
					if stag in html:
						## TODO fix this ugly mess
						try:
							xxx = u'<script type="text/rusthon" id="%s">\n%s</script>' %(tagname, py)
						except UnicodeDecodeError:
							xxx = u'<script type="text/rusthon" id="%s">\n%s</script>' %(tagname, py.decode('utf-8'))
						html = html.replace(stag, xxx)


			mod['code'] = html
			output['html'].append( mod )
			## inlines js app into openshift default style python server ##
			if '--openshift-python' in sys.argv:
				import base64
				bcoded = base64.b64encode(mod['code'].encode('utf-8'))
				wsgi = [ OPENSHIFT_PY[0]%bcoded, OPENSHIFT_PY[1] ]
				output['datafiles']['wsgi.py'] = '\n'.join(wsgi).encode('utf-8')

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
		if GO_EXE:
			cmd = [GO_EXE, 'build', tmpfile]
			subprocess.check_call([GO_EXE, 'build', tmpfile], cwd=tempfile.gettempdir() )
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
		dynamiclib = False
		source   = []
		cinclude = []
		cbuild   = []
		mods_sorted_by_index = sorted(modules['c'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			if 'dynamic' in mod and mod['dynamic']:
				dynamiclib = True
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
			data = '\n'.join(source)
			cpak = {'source':data}
			output['c'].append(cpak)

			libname = 'default-clib%s' %len(output['c'])  ## TODO user named
			link.append(libname)
			dynamic_path = tempfile.gettempdir() + '/lib'+libname+'.so'
			static_path = tempfile.gettempdir() + '/lib'+libname+'.a'
			object_path = tempfile.gettempdir() + '/'+libname+'.o'


			tmpfile = tempfile.gettempdir() + '/rusthon-build.c'
			open(tmpfile, 'wb').write( data )

			cmd = ['gcc']
			for idir in cinclude:
				cmd.append('-I'+idir)
			cmd.extend(['-c', tmpfile])


			if dynamiclib:
				cmd.extend(
					[
						'-fPIC',
						'-O3',
						'-fomit-frame-pointer',
						'-Wall', '-Wno-unused',
						'-o', object_path
					]
				)
				subprocess.check_call(cmd)

				cmd = [
					'gcc',
					'-shared',
					'-Wl,-soname,lib%s.so' %libname,
					#'-Wl,-rpath,/tmp',
					'-Wl,--export-dynamic',
					'-pthread', '-o', dynamic_path,
					object_path
				]
				subprocess.check_call(cmd)
				cpak['dynamiclib'] = dynamic_path
				cpak['name']       = 'lib%s.so' %libname

			else:

				if cbuild:
					#gcc: fatal error: cannot specify -o with -c, -S or -E with multiple files
					#cmd.extend(cbuild)  ## extra c files `/some/path/*.c`
					raise RuntimeError('TODO fix building multiple .c files at once using gcc option -o')

				cmd.extend(['-o', object_path ])

				print('========== compiling C static library =========')
				print(' '.join(cmd))
				subprocess.check_call( cmd )
				print('========== ar : staticlib ==========')
				cmd = ['ar', 'rcs', static_path, object_path]
				subprocess.check_call( cmd )
				cpak['staticlib'] = libname+'.a'
				cpak['name']      = libname+'.a'


	if modules['c++']:
		links = []
		idirs = []
		source = []
		defines = []
		mods_sorted_by_index = sorted(modules['c++'], key=lambda mod: mod.get('index'))
		mainmod = None
		builddir = tempfile.gettempdir()
		#compile_mode = 'binary'
		for mod in mods_sorted_by_index:
			if 'tag' in mod and mod['tag'] and ( mod['tag'].endswith('.hpp') or mod['tag'].endswith('.hpp') ):
				## allows plain header files to be included in build directory ##
				open(
					os.path.join(builddir, mod['tag']), 'wb'
				).write( mod['code'] )
				output['c++'].append( mod )
			else:
				source.append( mod['code'] )

			if 'name' in mod and mod['name']=='main':
				mainmod = mod
			elif mainmod is None:
				mainmod = mod
			if 'links' in mod:
				links.extend(mod['links'])
			if 'include-dirs' in mod:
				idirs.extend(mod['include-dirs'])
			if 'defines' in mod:
				defines.extend(mod['defines'])

			#if 'compile-mode' in mod:
			#	compile_mode = mod['compile-mode']

			if 'tag' in mod and mod['tag'] and '.' not in mod['tag']:
				exename = mod['tag']

		tmpfile = builddir + '/rusthon-c++-build.cpp'
		data = '\n'.join(source)
		open(tmpfile, 'wb').write( data )
		cmd = ['g++']

		if compile_mode=='binary':
			cmd.extend(['-O3', '-fprofile-generate', '-march=native', '-mtune=native', '-I'+tempfile.gettempdir()])

		cmd.append('-Wl,-rpath,/usr/local/lib/')  ## extra user installed dynamic libs
		cmd.append('-Wl,-rpath,./')  ## can not load dynamic libs from same directory without this
		cmd.append(tmpfile)

		if '/' in exename and not os.path.isdir( os.path.join(builddir,os.path.split(exename)[0]) ):
			os.makedirs(os.path.join(builddir,os.path.split(exename)[0]))

		if compile_mode == 'binary':
			cmd.extend(['-o', os.path.join(builddir,exename)])
		elif compile_mode == 'dynamiclib':
			cmd.extend(
				['-shared', '-fPIC']
			)
			exename += '.so'
			cmd.extend(['-o', os.path.join(builddir,exename)])

		cmd.extend(
			['-pthread', '-std=c++11' ]
		)

		for D in defines:
			cmd.append('-D%s' %D)

		if nuitka:
			## note: linking happens after the object-bin above is created `-o ruston-c++-bin`,
			## fixes the error: undefined reference to `_PyThreadState_Current', etc.
			#if not nuitka_include_path:
			#	nuitka_include_path = '/usr/local/lib/python2.7/dist-packages/nuitka/build/include'
			#cmd.append('-I'+nuitka_include_path)
			cmd.append('-I/usr/include/python2.7')
			cmd.append('-lpython2.7')

		if idirs:
			for idir in idirs:
				cmd.append('-I'+idir)

		if links:
			for lib in links:
				cmd.append('-l'+lib)

		## always link to libdl, external libraries may require dl_open, etc.
		cmd.append('-ldl')


		if link or giws:

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

			#else:  ## TODO fix jvm with static c libs
			#	cmd.append('-static')

			if link:  ## c staticlibs or giws c++ wrappers ##
				cmd.append('-L' + tempfile.gettempdir() + '/.')
				for libname in link:
					cmd.append('-l'+libname)

		print('========== g++ : compile main ==========')
		print(' '.join(cmd))
		subprocess.check_call( cmd )
		mainmod['build'] = {
			'source':data, 
			'binary':tempfile.gettempdir() + '/' + exename, 
			'name':exename
		}
		if compile_mode == 'binary':
			output['c++'].append( mainmod['build'] )
			output['executeables'].append(tempfile.gettempdir() + '/' + exename)
		else:
			output['datafiles'][ exename ] = open(tempfile.gettempdir() + '/' + exename, 'rb').read()

	if python_main['script']:
		python_main['script'] = '\n'.join(python_main['script'])
		output['python'].append( python_main )

	if modules['bazel']:
		# http://bazel.io/docs/build-ref.html#workspaces
		## a WORKSPACE file is required, even if empty.
		tmpdir = tempfile.gettempdir()
		open(tmpdir+'/WORKSPACE', 'wb')

		for filename in output['datafiles'].keys():
			open(tmpdir+'/'+filename, 'wb').write(output['datafiles'][filename])

		bazelbuilds = []
		mods_sorted_by_index = sorted(modules['bazel'], key=lambda mod: mod.get('index'))
		for mod in mods_sorted_by_index:
			bazelconfig = mod['code']
			open(tmpdir+'/BUILD', 'wb').write(bazelconfig)
			for chk in bazelconfig.split(','):
				chk = chk.strip()
				words = chk.split()
				if chk.endswith('"') and 'name' in words and '=' in words:
					chk = chk.split()
					bazelbuilds.append(chk[-1][1:-1])


		assert len(bazelbuilds)==1
		buildname = bazelbuilds[0]
		#subprocess.check_call(['bazel', 'build', ':'+buildname], cwd=tmpdir)
		subprocess.check_call(['bazel', 'run', ':'+buildname], cwd=tmpdir)

	if gyp_builds:
		tmpdir = tempfile.gettempdir()
		for gname in gyp_builds.keys():
			gbuild = gyp_builds[gname]
			if gbuild['src']:
				open(tmpdir+'/binding.gyp', 'wb').write(gbuild['gyp'])
				open(tmpdir+'/'+gname, 'wb').write( gbuild['src'] )
				subprocess.check_call(['nw-gyp', 'configure', '--target=0.12.3'], cwd=tmpdir)
				subprocess.check_call(['nw-gyp', 'build'], cwd=tmpdir)

				node_module = open(tmpdir+'/build/Release/binding.node', 'rb').read()
				output['datafiles']['binding.node'] = node_module


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

	if package['datafiles']:
		for fpath in package['datafiles']:
			fdata = package['datafiles'][fpath]
			s = StringIO.StringIO()
			s.write( fdata )
			s.seek(0)
			ti = tarfile.TarInfo(name=fpath)
			ti.size=len(s.buf)
			tar.addfile(tarinfo=ti, fileobj=s)

	exts = {'rust':'.rs', 'c++':'.cpp', 'c#':'.cs', 'javascript':'.js', 'json':'.json', 'python':'.py', 'go':'.go', 'html': '.html', 'verilog':'.sv', 'nim':'.nim', 'java':'.java', 'dart':'.dart', 'lua':'.lua'}
	for lang in 'rust c c++ c# go javascript json python xml html verilog java nim dart lua'.split():
		for info in package[lang]:
			name = 'untitled'
			if 'name' in info and info['name']:
				name = info['name']

			source = False
			is_bin = False
			s = StringIO.StringIO()
			if 'dynamiclib' in info:
				s.write(open(info['dynamiclib'],'rb').read())
				if 'source' in info:
					source = info['source']
			elif 'staticlib' in info:
				s.write(open(info['staticlib'],'rb').read())
				if 'source' in info:
					source = info['source']
			elif 'binary' in info:
				s.write(open(info['binary'],'rb').read())
				source = info['source']
				is_bin = True
			elif 'code' in info:
				if lang=='verilog': print(info['code'])  ## just for testing.
				s.write(info['code'].encode('utf-8'))
			elif 'script' in info:
				s.write(info['script'])
			s.seek(0)

			if not is_bin and not source and not name.endswith( exts[lang] ) and '.' not in name:
				name += exts[lang]

			ti = tarfile.TarInfo(name=name)
			ti.size=len(s.buf)
			if is_bin:
				ti.mode = 0o777
			try:
				tar.addfile(tarinfo=ti, fileobj=s)
			except UnicodeEncodeError as err:
				s.seek(0)
				print s.getvalue()
				raise err

			if source:
				s = StringIO.StringIO()
				s.write(source)
				s.seek(0)
				if 'source-name' in info:
					ti = tarfile.TarInfo( name = info['source-name'] )
				else:
					ti = tarfile.TarInfo( name = name + '-source' + exts[lang] )
				ti.size=len(s.buf)
				tar.addfile(tarinfo=ti, fileobj=s)

	tar.close()


## this hack to force the devtools window to show first will not work because a body onload will execute
## at the same time and the js debugger will also reload,
## but because the debugger is in another process, it will the first debug events.
NW_DEVTOOLS_HACK = '''
<html>
<script>
require('nw.gui').Window.get().showDevTools();
setTimeout(function (){
		//require('nw.gui').Window.get().reloadDev();
		require('nw.gui').Window.get().reload();
	},
	3000
);
</script>
<body>opening devtools window....</body>
</html>
'''

NW_STARTUP_HACK = '''
exports.myinit = function() {
	require('nw.gui').Window.get().showDevTools();
}

'''

def main():
	if len(sys.argv)==1 or '--help' in sys.argv:
		print('usage: ./rusthon.py [python files] [markdown files] [tar file] [--release] [--run=] [--data=]')
		print('		[tar file] is the optional name of the output tar that contains the build')
		print
		print('		source files, transpiled source, and output binaries.')
		print
		print('		--release generates optimized output without extra runtime checks')
		print
		print('		--run is given a list of programs to run, "--run=a.py,b.py"')
		print('		a.py and b.py can be run this way by naming the code blocks in the markdown')
		print('		using the tag syntax "@a.py" on the line before the code block.')
		print
		print('		--data is given a list of directories to include in the build dir and tarfile.')
		print
		print('		--obfuscate produces random names for unicode functions and variables.')
		print
		print('		--literate-unicode enables unicode variables names to be output for the javascript backend.')
		print
		print('		--convert2python=MYOUTPUT strips away static type annotations, to run your script in regular Python.')
		print
		print('		--anaconda run scripts with Anaconda Python, must be installed to ~/anaconda')
		print
		print('		--transparent linux and NW.js only (forces window transparency and disables GPU acceleration)')
		print
		print('		--debug-inter print intermediate translation code and then exit.')
		print
		print('		note: when using regular python files (.py) as input instead of markdown (.md)')
		print('		you can use these extra options to set which backend is used by the transpiler:')
		for backend in '--c++ --javascript --go --rust'.split():
			print('		'+backend)
		return

	modules = new_module()

	save = False
	paths = []
	scripts = []
	markdowns = []
	gen_md = False
	output_tar  = 'rusthon-build.tar'
	output_dir  = None
	output_file = None
	launch = []
	datadirs = []
	j2r = False
	anaconda = False
	convert2py = False

	for arg in sys.argv[1:]:
		if os.path.isdir(arg):
			paths.append(arg)
		elif arg.startswith('--data='):
			datadirs.extend( arg.split('=')[-1].split(',') )
		elif arg.startswith('--run='):
			launch.extend( arg.split('=')[-1].split(',') )
			save = True
		elif arg.startswith('--output='):
			output_file = arg.split('=')[-1]
		elif arg.startswith('--output-dir='):
			output_dir = arg.split('=')[-1]
			if output_dir.startswith('~'):
				output_dir = os.path.expanduser(output_dir)
		elif arg.startswith('--convert2python='):
			convert2py = arg.split('=')[-1]

		elif arg.endswith('.py'):
			scripts.append(arg)
		elif arg.endswith('.md'):
			markdowns.append(arg)
		elif arg.endswith('.tar'):
			output_tar = arg
			save = True
		elif arg =='--generate-markdown':
			gen_md = True
		elif arg == '--tar':
			save = True
		elif arg == '--java2rusthon':
			j2r = True
		elif arg == '--anaconda':
			anaconda = True

	datadirs = [os.path.expanduser(dd) for dd in datadirs]

	if j2r:
		for path in paths:
			m = convert_to_markdown_project(path, java=True, java2rusthon=True)
			raise RuntimeError('TODO: %s'%m)

	if gen_md:
		for path in paths:
			mds = convert_to_markdown_project(path)
			if not output_file:
				raise RuntimeError('%s \n ERROR: no output file given `--output=myproject.md`'%mds)
			elif os.path.isdir(output_file):
				## write as multiple markdowns into directory
				for m in mds:
					if m['name'].count('.')==1:
						mname = m['name'].split('.')[0] + '.md'
					else:
						mname = m['name'] + '.md'
					mpath = os.path.join(output_file, mname)
					print('writing-> %s'%mpath)
					open(mpath, 'wb').write(m['markdown'])
			else:
				if not output_file.endswith('.md'):
					output_file += '.md'
				md = '\n'.join([m['markdown'] for m in mds])
				open(output_file, 'wb').write(md)
			sys.exit()


	if convert2py:
		## strips away rusthon type annotations ##
		if not len(scripts):
			raise RuntimeError('the option --convert2python=myoutput requires an input script')
		if len(scripts)!=1:
			raise RuntimeError('the option --convert2python=myoutput requires a single input script')
		a = typedpython.transform_source(
			open(scripts[0],'rb').read(), 
			strip=True
		)
		open(convert2py, 'wb').write(a)
		sys.exit()

	base_path = None
	singleout = None
	for path in scripts:
		## note: .decode('utf-8') is not required here,
		## should also check the strip to ensure the user has not
		## used unicode strings starting with the `u` prefix,
		## because that will break the translator, because it
		## promotes those strings to unicode objects in the AST (which is written in Python2)
		script = open(path,'rb').read()
		if '--c++' in sys.argv:          script = '#backend:c++\n'+script
		elif '--javascript' in sys.argv: script = '#backend:javascript\n'+script
		elif '--rust' in sys.argv: script = '#backend:rust\n'+script
		elif '--go' in sys.argv:   script = '#backend:go\n'+script
		elif '--dart' in sys.argv: raise RuntimeError('dart backend removed')
		elif '--lua' in sys.argv:  raise RuntimeError('lua backend removed')
		elif '--verilog' in sys.argv: script = '#backend:verilog\n'+script
		else: script = '#backend:javascript\n'+script

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
		## copy jar and other extra libraries files files ##
		for p in datadirs:
			## saves jar and other files like dynamic libraries,
			## needed to do quick testing.
			if '.' in p:
				dpath,dname = os.path.split(p)
				open(os.path.join(tmpdir,dname),'wb').write(open(p,'rb').read())

		for exe in package['executeables']:
			print('running: %s' %exe)
			subprocess.check_call(
				exe,
				cwd=tmpdir ## jvm needs this to find the .class files
			)

		if package['html']:
			for i,page in enumerate(package['html']):
				tname = 'rusthon-webpage%s.html' %i

				if 'name' in page and page['name']:
					tname = page['name']

				tmp = tempfile.gettempdir() + '/' + tname
				if sys.platform=='darwin':  ## force /tmp directory on OSX, makes debugging the output simpler
					tmp = '/tmp/' + tname

				## note in Chrome UTF-8 javascript will fail with this error: 
				## `Unexpected token ILLEGAL` with unicode variables
				## the file must be written as UTF-16.
				## http://stackoverflow.com/questions/22543354/how-well-is-node-js-support-for-unicode
				#open(tmp, 'wb').write( page['code'].encode('utf-8') )
				open(tmp, 'wb').write( page['code'].encode('utf-16') )

				if i<len(package['html'])-1:  ## only launch the last html file.
					pass
				elif sys.platform=='darwin' and not nodewebkit_runnable:  ## hack for OSX
					subprocess.call(['open', tmp])
				elif nodewebkit_runnable:
					## nodewebkit looks for `package.json` in the folder it is given ##
					nwcfg = '{"name":"test", "main":"%s", ' %os.path.split(tmp)[1]
					if '--frameless' in sys.argv:
						nwcfg += '"window":{"width":1200, "height":680, "toolbar":false, "frame":false}}'
					elif '--desktop' in sys.argv:
						## note as_desktop is broken in new NW.js
						## https://github.com/nwjs/nw.js/issues/2833
						nwcfg += '"window":{"width":1200, "height":680, "toolbar":false, "as_desktop":true, "frame":false}}'
					else:
						nwcfg += '"window":{"width":1200, "height":680, "toolbar":false}}'

					open(os.path.join(tmpdir,"package.json"),'wb').write(nwcfg)
					nwcmd = [nodewebkit]
					if '--v8-natives' in sys.argv:
						nwcmd.append('--allow-natives-syntax')
					if sys.platform=='linux2' and '--transparent' in sys.argv:
						nwcmd.extend(['--enable-transparent-visuals', '--disable-gpu'])
					nwcmd.append(tmpdir)
					subprocess.Popen(nwcmd, cwd=tmpdir)
				else:
					webbrowser.open(tmp)

		elif package['javascript']:
			tmpdir = tempfile.gettempdir()
			for pak in package['javascript']:
				fname = pak['name']
				if fname is None:
					fname = 'rusthon-temp.js'
				elif not fname.endswith('.js'):
					fname += '.js'

				fpath = os.path.join(tmpdir, fname)
				open(fpath, 'wb').write( pak['script'] )
				#xxx = pak['script'].decode('utf-8')
				#open(fpath, 'wb').write( xxx.encode('utf-16') )  ## TODO fix nodejs unicode
				#codecs.open(fpath, 'w', 'utf-8').write( pak['script'] )  ## TODO fix nodejs unicode
				if '--v8-natives' in sys.argv:
					subprocess.check_call([nodejs_exe, '--allow-natives-syntax', fpath])
				else:
					subprocess.check_call([nodejs_exe, fpath])

	else:
		save_tar( package, output_tar )
		print('saved build to:')
		print(output_tar)

		if launch:
			tmpdir = output_dir or tempfile.gettempdir()
			tmptar = os.path.join(tmpdir, 'temp.tar')
			open(tmptar, 'wb').write(
				open(output_tar, 'rb').read()
			)
			subprocess.check_call( ['tar', '-xvf', tmptar], cwd=tmpdir )

			run = subprocess.call

			for name in launch:
				if name==launch[-1]:
					run = subprocess.check_call
				else:
					run = subprocess.Popen

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

						run( [os.path.join(anabin,python), name], cwd=tmpdir )

					else:
						run( [python, name], cwd=tmpdir )

				elif name.endswith('.js'):
					run( ['node', name],   cwd=tmpdir, env={'NODE_PATH':'/usr/lib/node_modules/'} )

				elif name.endswith('.nim'):
					run( ['nim', 'compile', '--run', name],   cwd=tmpdir )

				elif name.endswith('.go'):
					run( ['go', 'run', name],   cwd=tmpdir )

				elif name.endswith('.lua'):
					run( ['luajit', name],   cwd=tmpdir )

				elif name.endswith('.dart'):
					dartbin = os.path.expanduser('~/dart-sdk/bin/dart')
					run( [dartbin, name],   cwd=tmpdir )

				elif name.endswith('.html'):
					if sys.platform=='darwin':
						subprocess.call(['open', tmpdir+'/'+name])
					elif nodewebkit_runnable:
						raise RuntimeError('todo nodewebkitxx')
						subprocess.call([nodewebkit, tmp], cwd=tmpdir)
					else:
						webbrowser.open(tmpdir+'/'+name)

				else:
					print 'running: %s' %name
					run( [os.path.join(tmpdir,name)], cwd=tmpdir )

BOOTSTRAPED = None
class rusthon(object):
	@classmethod
	def translate( cls, code, mode='markdown' ):
		if mode=='javascript':
			js = compile_js( code, '/tmp', main_name='main' )
			return js['main']

		elif mode=='c++':
			pyjs = python_to_pythonjs(code, cpp=True)
			pak = translate_to_cpp(
				pyjs, 
				insert_runtime=False
			)
			## pak contains: c_header and cpp_header
			return pak['main']

		elif mode=='go':
			pyjs = python_to_pythonjs(code, go=True)
			return translate_to_go( pyjs )

		elif mode=='rust':
			pyjs = python_to_pythonjs(code, rust=True)
			return translate_to_rust( pyjs )

		else:
			#modules = new_module()
			#import_md( path, modules=modules )
			base_path = None
			package = build(modules, base_path )
			raise RuntimeError(package)
			return 

def bootstrap_rusthon():
	global BOOTSTRAPED
	localdir = os.path.dirname(unicode(os.path.realpath(__file__), sys.getfilesystemencoding()))
	#raise RuntimeError(localdir)
	mods = new_module()
	import_md( os.path.join(localdir,'src/main.md'), modules=mods )
	src = []
	mods_sorted_by_index = sorted(mods['python'], key=lambda mod: mod.get('index'))
	for mod in mods_sorted_by_index:  ## this is simplified because rusthon's source is pure python
		src.append( mod['code'] )
	src = '\n'.join(src)
	BOOTSTRAPED = src

	if '--dump' in sys.argv: open('/tmp/bootstrap-rusthon.py', 'wb').write(src.encode('utf-8'))
	exec(src, globals())

	if '--test' in sys.argv:
		test_typedpython()  ## runs some basic tests on the extended syntax

	if '--runtime' in sys.argv:
		print('creating new runtime: pythonjs.js')
		jsruntime = generate_js_runtime()
		if os.path.isdir('./pythonjs'):
			print 'saving runtime to pythonjs/pythonjs.js'
			open('pythonjs/pythonjs.js', 'wb').write( jsruntime )
		return jsruntime


#MAIN#
if __name__ == "__main__":
	bootstrap_rusthon()
	main()


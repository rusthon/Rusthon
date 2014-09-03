#!/usr/bin/env python3

"""
Without argument: run all the regression tests.

About the tests:

   * They are stored as python file in the subdirectories.
   * The firstline must be an explanation about the test.
   * Errors(must be True)  defines an Error that must be corrected
   * Warning(must be True) defines something that should be corrected
     once corrected, must be redefined as an Error

"""

import os, sys, re, tempfile, subprocess, json
import wsgiref, wsgiref.simple_server

sys.path.append('../pythonjs')
import typedpython

if 'NODE_PATH' not in os.environ:
    os.environ['NODE_PATH'] = '/usr/local/lib/node_modules/'

tmpname = os.path.join(tempfile.gettempdir(), "xxx_regtest")

print("Temporary files are stored into '%s...'" % tmpname)
print()

show_details = len(sys.argv) > 1

# List of valid filenames in the parameters
argv = [os.path.abspath(name)
        for name in sys.argv[1:]
        if os.path.exists(name)
        ]


__sandbox = {
    'mycollection' : range(10)
}
__clients = {}  ## keeps track of iterator indices

def httpd_reply( env, start_response ):

    path = env['PATH_INFO']
    host = env['HTTP_HOST']
    client = env['REMOTE_ADDR']
    arg = env['QUERY_STRING']

    if client not in __clients:
        __clients[ client ] = {}

    length = 0
    if 'CONTENT_LENGTH' in env: length = int(env['CONTENT_LENGTH'])
    data = env['wsgi.input'].read( length ).decode('utf-8')
    #print('http_reply ->', path, host, client, arg, data)

    msg = json.loads( data )
    res = ''

    if 'call' in msg:
        assert 'args' in msg
        if msg['call'] == 'concat':
            res = ''.join( msg['args'] )
        elif msg['call'] == 'add':
            res = msg['args'][0] + msg['args'][1]
        else:
            raise NotImplementedError( msg )

    elif 'iter' in msg:
        name = msg['iter']
        assert name in __sandbox
        if name not in __clients[ client ]:
            __clients[ client ][name] = 0
        index = __clients[ client ][name]
        iterable = __sandbox[name]
        if index == len(iterable):
            index = 0
            res = '__STOP_ITERATION__'
        else:
            res = iterable[ index ]
            index += 1
        __clients[ client ][name] = index

    elif 'set' in msg:
        __sandbox[ msg['set'] ] = msg['value']

    elif 'get' in msg:
        res = __sandbox[ msg['get'] ]

    else:
        raise NotImplementedError( msg )

    start_response( '200 OK', [] )
    return [ json.dumps(res).encode('utf-8') ]

httpd = wsgiref.simple_server.make_server( 'localhost', 8080, httpd_reply )
import threading
thread_id = threading._start_new_thread( httpd.serve_forever, ())


def runnable(command):
    ## this fails with lua5.1 "lua -v"
    #"""Returns True is the standard out of the command display something"""
    #f = os.popen(command, "r")
    #output = f.read()
    #f.close()
    #return output != ''
    try:
        subprocess.check_call( command.split() )
        return True
    except OSError:
        return False

def run_pypy_test_on(filename):
    """PyPy"""
    write("%s.py" % tmpname, patch_python(filename, python='PYPY'))
    return run_command("%s %s.py %s" % (pypy_exe, tmpname, display_errors))

def run_old_pypy_test_on(filename):
    """PyPy 1.9"""
    write("%s.py" % tmpname, patch_python(filename, python='PYPY'))
    return run_command("%s %s.py %s" % (old_pypy_exe, tmpname, display_errors))


old_pypy_runnable = pypy_runnable = False
old_pypy_exe = pypy_exe = None
if os.path.isfile( os.path.expanduser('~/pypy-2.3.1-linux64/bin/pypy') ):
    pypy_runnable = True
    pypy_exe = os.path.expanduser('~/pypy-2.3.1-linux64/bin/pypy')
    run_pypy_test_on.__doc__ = 'PyPy 2.3.1'
elif os.path.isfile( os.path.expanduser('~/pypy-2.2-linux64/bin/pypy') ):
    pypy_runnable = True
    pypy_exe = os.path.expanduser('~/pypy-2.2-linux64/bin/pypy')
    run_pypy_test_on.__doc__ = 'PyPy 2.2'
elif runnable( 'pypy --help' ):
    pypy_runnable = True
    pypy_exe = 'pypy'

if os.path.isfile( os.path.expanduser('~/pypy-1.9/bin/pypy') ) and '--old-pypy' in sys.argv:
    old_pypy_runnable = True
    old_pypy_exe = os.path.expanduser('~/pypy-1.9/bin/pypy')

webclgl = []
if os.path.isdir( os.path.expanduser('~/webclgl') ):
    #webclgl.append( open( os.path.expanduser('~/webclgl/WebCLGL_2.0.Min.class.js'), 'rb').read().decode('utf-8') )
    webclgl.append( open( os.path.expanduser('~/webclgl/WebCLGLUtils.class.js'), 'rb').read().decode('utf-8') )
    webclgl.append( open( os.path.expanduser('~/webclgl/WebCLGLBuffer.class.js'), 'rb').read().decode('utf-8') )
    webclgl.append( open( os.path.expanduser('~/webclgl/WebCLGLKernel.class.js'), 'rb').read().decode('utf-8') )
    webclgl.append( open( os.path.expanduser('~/webclgl/WebCLGL.class.js'), 'rb').read().decode('utf-8') )

## rhino is not run by default because it simply freezes up on maximum callstack errors
rhino_runnable = '--rhino' in sys.argv and runnable("rhino -e 'quit()'")

node_runnable = runnable("node --help")

## sudo npm install nodewebkit -g
## nodewebkit npm package is broken? https://github.com/shama/nodewebkit/issues/31
#nodewebkit = '/usr/local/lib/node_modules/nodewebkit/bin/nodewebkit'

## download https://github.com/rogerwang/node-webkit/releases/tag/nw-v0.9.2
## and extract to your home directory.
nodewebkit_runnable = False


nodewebkit = os.path.expanduser('~/node-webkit-v0.10.0-rc1-linux-x64/nw')
if os.path.isfile( nodewebkit ): nodewebkit_runnable = True
else:
    nodewebkit = os.path.expanduser('~/node-webkit-v0.9.2-linux-x64/nw')
    if os.path.isfile( nodewebkit ): nodewebkit_runnable = True
    else:
        nodewebkit = os.path.expanduser('~/node-webkit-v0.9.1-linux-x64/nw')
        if os.path.isfile( nodewebkit ): nodewebkit_runnable = True
        else:
            nodewebkit = os.path.expanduser('~/node-webkit-v0.8.4-linux-x64/nw')
            if os.path.isfile( nodewebkit ): nodewebkit_runnable = True

if not show_details or '--no-nodewebkit' in sys.argv:
    nodewebkit_runnable = False

#dart2js = os.path.expanduser( '~/dart-sdk-1.0/dart-sdk/bin/dart2js')  ## TODO support dart-sdk-1.3+
dart2js = os.path.expanduser( '~/dart-sdk/bin/dart2js') # tested with dart 1.3
dart2js_runnable = runnable( dart2js + ' -h' ) and '--dart2js' in sys.argv

dart_exe = os.path.expanduser( '~/dart-sdk/bin/dart')
dart_runnable = os.path.isfile( dart_exe )

coffee_runnable = runnable( "coffee -v" ) and '--coffee' in sys.argv
lua_runnable = runnable( "lua -v" ) and '--lua' in sys.argv
luajit_runnable = runnable( "luajit -v" ) and '--luajit' in sys.argv

lua2js = os.path.abspath( '../external/lua.js/lua2js' )
luajs_runnable = os.path.isfile( lua2js ) and '--lua2js' in sys.argv

go_runnable = runnable( 'go version')
gopherjs_runnable = runnable( 'gopherjs')

assert rhino_runnable or node_runnable

if show_details:
    display_errors = ""
else:
    display_errors = "2>/dev/null"

def files():
    """returns all the filenames of the regression tests.
    this also needs to copy all the original python files to /tmp
    because `from xxx import *` syntax will trigger the translator
    to read files from the same directory and insert them.
    """
    tests = []
    html_tests = []
    benchmarks = []
    mods = []
    for dirpath, dirnames, filenames in os.walk('.'):
        if dirpath == '.':
            continue
        for filename in filenames:
            a = dirpath + os.path.sep + filename
            if filename.endswith(".py"):
                if 'bench' in dirpath:
                    benchmarks.append( a )
                else:
                    tests.append( a )
            elif 'html' in dirpath:
                if filename.endswith(".html"):
                    html_tests.append( a )
                elif filename.endswith('.py'):  ## these are modules
                    mods.append( filename )

    tmpdir = tempfile.gettempdir()
    for mod in mods+tests:
        data = open(mod,'rb').read()
        name = os.path.split(mod)[-1]
        open(os.path.join(tmpdir, name), 'wb').write( data )

    tests.extend( html_tests )
    tests.extend( benchmarks )
    return tests

def read(filename):
    """Returns the file content as a string"""
    f = open(filename)
    content = f.read()
    f.close()
    return content

def write(filename, content):
    """Write the content into the file"""
    f = open(filename, "w")
    f.write(content)
    f.close()

def run_command(command, returns_stdout_stderr=False, nodewebkit_workaround=False):
    """Returns the number of problems"""
    if os.path.isfile("%s.errors" % tmpname):
        os.unlink("%s.errors" % tmpname)
    f = os.popen(command + " 2>%s.errors" % tmpname,  'r')

    killed = False
    try:
        stdout = f.read().strip()
    except KeyboardInterrupt:
        stdout = f.read().strip()
        killed = True

    f.close()


    stderr = read("%s.errors" % tmpname)


    if nodewebkit_workaround:
        stdout = stderr
        stderr = ''
        a = []
        for line in stdout.splitlines():
            if 'INFO:CONSOLE' in line:
                line = line.replace('\\n', '\n')
                line = line.replace('\\u003C', '<')
                start = line.index('"')
                end = line.rindex('"')
                a.append( line[start+1:end] )
        stdout = '\n'.join(a)


    if stderr:
        if show_details:
            print('TEST ERROR!')
            print(stderr)

    if killed:
        print(stdout)
        sys.exit()

    if returns_stdout_stderr:
        return stdout, stderr

    #########################

    if show_details and stdout:
        print(stdout)

    unknown = []
    for line in stdout.splitlines():
        if _benchmark:
            if line.startswith('#'):
                _benchmark.append( line )
            else:
                #exe = command.split()[0]
                _benchmark.append( _test_description + ' ' + line )
        else:
            unknown.append(line)
    errors = '\n'.join(unknown) + stderr
            
    d = {}
    x = errors.count("Error fail")
    if x:
        d['Error'] = x
    x = errors.count("Warning fail")
    if x:
        d['Warning'] = x
    if len(d) == 0 and errors != '':
        if '.py", line' in errors:
            d["Syntax Error Python"] = 1
        else:
            d["?"] = 1
    
    return d

_benchmark = None
def start_benchmark( name ):
    print('starting benchmark:', name)
    global _benchmark
    _benchmark = [
        'font=Helvetica',
        'fontsz=12',
        '=color_per_datum',
        'yformat=%g',
        'ylabel=seconds'
    ]

def end_benchmark( name ):
    print('ending benchmark:', name)
    global _benchmark
    path = '/tmp/%s.perf' %name
    f = open( path, 'wb' )
    data = '\n'.join( _benchmark )
    f.write( data.encode('utf-8') )
    f.close()
    os.system( './bargraph.pl -eps %s > /tmp/%s.eps' %(path,name))
    _benchmark = None

def patch_assert(filename):
    """Patch the regression tests to add information into asserts"""
    out = []
    for i, line in enumerate(read(filename).split('\n')):
        out.append(re.sub("(TestError|TestWarning)\((.*)\)",
                          r'\1("%s",%d,\2,u"""\2""")' % (filename, i),
                          line)
                   )
    return '\n'.join(out)
        

_patch_header = """# -*- coding: utf-8 -*-
def TestError(file, line, result, test):
    if result == False:
        print(file + ":" + str(line) + " Error fail " + test)
def TestWarning(file, line, result, test):
    if result == False:
        print(file + ":" + str(line) + " Warning fail " + test)
"""

_patch_header_go = """# -*- coding: utf-8 -*-
def TestError(file:string, line:int, result:bool, test:string):
    if result == False:
        print(file + ":" + str(line) + " Error fail " + test)
"""


_python_only_extra_header = """
try:
    import threading
    threading.start_webworker = lambda f,a: threading._start_new_thread(f,a)
    threading.start_new_thread = threading._start_new_thread
except ImportError:
    pass

class __faker__(object):
    def __enter__(self, *args): pass
    def __exit__(self, *args): pass
    def __call__(self, *args, **kw):
        return lambda f: f
    def vectorize(self, f):
        return f
    def main(self, f):
        return f
    def object(self, f):
        return f
    def method(self, f):
        return f

webworker = __faker__()
glsl = __faker__()
gpu = __faker__()
returns = __faker__()
typedef = __faker__()
vec2 = None
mat4 = None

def int16(a): return int(a)

try:
    import numpy
except ImportError:
    try:
        import numpypy as numpy
    except ImportError:
        pass

from math import isnan as isNaN


"""

def patch_python(filename, dart=False, python='PYTHONJS', backend=None):
    """Rewrite the Python code"""
    code = patch_assert(filename)

    ## a main function can not be simply injected like this for dart,
    ## because dart has special rules about what can be created outside
    ## of the main function at the module level.
    #if dart:
    #    out = []
    #    main_inserted = False
    #    for line in code.splitlines():
    #        if line.startswith('TestError') or line.startswith('TestWarning'):
    #            if not main_inserted:
    #                out.append('def main():')
    #                main_inserted = True
    #            out.append( '\t'+line )
    #        else:
    #            out.append( line )
    #    code = '\n'.join( out )
    a = [
        'PYTHON="%s"'%python, 
        'BACKEND="%s"'%backend, 
    ]
    if backend == 'GO':
        a.append(_patch_header_go)
    else:
        a.append(_patch_header)

    if python != 'PYTHONJS':
        code = typedpython.transform_source( code, strip=True )
        a.append( _python_only_extra_header )

    a.append( code )

    if not dart and python != 'PYTHONJS':
        a.append( 'main()' )

    return '\n'.join( a )

def run_python_test_on(filename):
    """Python2"""
    write("%s.py" % tmpname, patch_python(filename, python='PYTHON2'))
    return run_command("python %s.py %s" % (tmpname, display_errors))

def run_python3_test_on(filename):
    """Python3"""
    write("%s.py" % tmpname, patch_python(filename, python='PYTHON3'))
    return run_command("python3 %s.py %s" % (tmpname, display_errors))



def translate_js(filename, javascript=False, dart=False, coffee=False, lua=False, luajs=False, go=False, gopherjs=False, multioutput=False, requirejs=True):
    global tmpname
    tmpname = os.path.join(
        tempfile.gettempdir(), 
        #'test-%s-js=%s-dart=%s-lua=%s' %(filename.split('/')[-1], javascript, dart, lua)
        'regtest-%s'%filename.split('/')[-1]
    )

    output_name = "%s.py" % tmpname
    if javascript:
        content = 'pythonjs.configure(javascript=True)\n' + patch_python(filename, backend='JAVASCRIPT')
    elif dart:
        source = [
            'pythonjs.configure(dart=True)',
            open('../pythonjs/runtime/dart_builtins.py', 'rb').read().decode('utf-8'),
            patch_python(filename, dart=True, backend='DART')
        ]
        content = '\n'.join( source )
    elif coffee:
        source = [
            'pythonjs.configure(coffee=True)',
            patch_python(filename, backend='COFFEE')
        ]
        content = '\n'.join( source )
    elif lua or luajs:
        source = [
            'pythonjs.configure(lua=True)',
            read('../pythonjs/runtime/lua_builtins.py'),
            patch_python(filename, backend='LUA')
        ]
        content = '\n'.join( source )

    elif go or gopherjs:
        content = patch_python(filename, backend='GO')

    else:
        content = patch_python(filename)

    code = '\n'.join(
        [
            '# -*- coding: utf-8 -*-',
            'pythonjs.configure(runtime_exceptions=False)',
            content
        ]
    )
    write(output_name, code)
    cmd = [
        os.path.join("..", "pythonjs", "translator.py"),
        output_name,
        '--debug'
    ]
    if dart:
        cmd.append( '--dart' )
    elif coffee:
        cmd.append( '--coffee')
    elif lua:
        cmd.append( '--lua')
    elif luajs:
        cmd.append( '--luajs')
    elif go:
        cmd.append( '--go' )
    elif gopherjs:
        cmd.append( '--gopherjs' )

    if not requirejs:
        cmd.append( '--no-wrapper' )

    stdout, stderr = run_command(' '.join(cmd), returns_stdout_stderr=True)
    if stderr:
        return ''
    else:

        #jsheader = 'if (typeof(process) != "undefined") { var requirejs = require("requirejs"); }'
        jsheader = ''

        if multioutput or (stdout.startswith("{") and stdout.endswith("}")):
            d = json.loads( stdout )
            stdout = d.pop('main')
            #builtins = read(os.path.join("../pythonjs", "pythonjs.js"))
            for jsfile in d:
                if not jsfile.startswith('/'):
                    stdout = stdout.replace('"%s"' %jsfile, '"/tmp/%s"' %jsfile)
                write(
                    os.path.join('/tmp', jsfile), 
                    '\n'.join( [jsheader, d[jsfile]] ) 
                )

        if dart:

            if os.path.isfile('/tmp/dart2js-output.js'):
                os.unlink('/tmp/dart2js-output.js')

            dart_input = '/tmp/dart2js-input.dart'
            open( dart_input, 'wb').write( stdout.encode('utf-8') )

            cmd = [
                dart2js,
                '-o', '/tmp/dart2js-output.js',
                dart_input
            ]
            if show_details:
                subprocess.call( cmd )
            else:
                sout, serr = run_command(' '.join(cmd), returns_stdout_stderr=True)

            if os.path.isfile('/tmp/dart2js-output.js'):
                return open('/tmp/dart2js-output.js', 'rb').read().decode('utf-8')
            else:
                return ''

        elif coffee:

            coffee_input = '/tmp/coffee-input.coffee'
            open( coffee_input, 'wb').write( stdout.encode('utf-8') )

            cmd = [
                'coffee',
                '--print', # print js to stdout
                coffee_input
            ]
            #subprocess.call( cmd )
            sout, serr = run_command(' '.join(cmd), returns_stdout_stderr=True)
            if serr:
                return ''
            elif sout:
                builtins = read(os.path.join("../pythonjs", "pythonjs.js"))
                open('/tmp/coffee-output.js', 'wb').write( (builtins+'\n'+sout).encode('utf-8') )
                return sout
            else:
                return ''

        elif luajs:
            lua2js_input = '/tmp/lua2js-input.lua'
            lua2js_output = '/tmp/lua2js-output.js'
            open( lua2js_input, 'wb').write( stdout.encode('utf-8') )

            cmd = [
                lua2js,
                lua2js_input,
                lua2js_output
            ]
            try:
                subprocess.check_call( cmd )
            except subprocess.CalledProcessError:
                return ''
            return open( lua2js_output, 'rb' ).read().decode('utf-8')

        else:
            return '\n'.join( [jsheader, stdout] )

def run_if_no_error(function):
    """Run the function if the JS code is not empty"""
    global js
    if js:
        return function(js)
    else:
        return {'Translation error':1}

def run_pythonjs_test_on(dummy_filename):
    """JS PythonJS tests"""
    return run_if_no_error(run_js_rhino)

def run_pythonjsjs_test_on(filename):
    """JSJS PythonJS with javascript tests"""
    return run_pythonjs_test_on(filename)

def run_js_rhino(content):
    """Run Javascript using Rhino"""
    builtins = read(os.path.join("../pythonjs", "pythonjs.js"))
    # Patch in order to run Rhino
    builtins = builtins.replace('Object.create(null)', '{}', 1)
    # Add the program to test
    content = builtins + content
    # Remove documentation strings from JavaScript (Rhino don't like)
    content = re.sub('^ *".*" *$', '', content)
    # Add the console for Rhino
    content = '''
console = { log: print } ;
process = { title:"", version:"" } ;
''' + content
    write("%s.js" % tmpname, content)
    return run_command("rhino -O -1 %s.js" % tmpname)

def run_pythonjs_test_on_node(dummy_filename):
    """PythonJS (normal)"""
    return run_if_no_error(run_js_node)

def run_pythonjsjs_test_on_node(filename):
    """PythonJS (fast backend)"""
    return run_pythonjs_test_on_node(filename)

def run_js_node(content):
    """Run Javascript using Node"""
    #builtins = read(os.path.join("../pythonjs", "pythonjs.js"))
    write("/tmp/mymodule.js", content)
    lines = [
        "var requirejs = require('requirejs')",
        "var module = requirejs('mymodule')",
        "module.main()"
    ]
    write("%s.js" % tmpname, '\n'.join(lines))
    return run_command("node %s.js" % tmpname)


def run_pythonjs_test_on_nodewebkit(dummy_filename):
    """PythonJS (normal) - NodeWebkit"""
    return run_if_no_error(run_js_nodewebkit)

def run_pythonjsjs_test_on_nodewebkit(filename):
    """PythonJS (fast backend) - NodeWebkit"""
    return run_pythonjs_test_on_nodewebkit(filename)

def run_js_nodewebkit(content):
    """Run Javascript using NodeWebkit"""

    ## there is likely a bug in requirejs and/or nodewebkit that prevents WebWorkers from working,
    ## `workerjs` for node also seems like its incompatible with nodewebkit and requirejs,
    ## as a quick workaround simply strip away the wrapper function from the javascript.
    code = '\n'.join( content.strip().splitlines()[1:-2] )


    write("/tmp/package.json", '{"name":"test", "main":"test.html"}')
    #write("/tmp/mymodule.js", content)
    lines = [
        "var __nw = require('nw.gui')",
        "var requirejs = require('requirejs')",
        #"var module = requirejs('mymodule')",
        #"module.main()",
        code,
        "main()",
        "__nw.App.quit()"
    ]

    html = ['<html>']
    if webclgl:
        for data in webclgl:
            html.append('<script>')
            html.append( data )
            html.append('</script>')

    html.append('<script>')
    html.extend( lines )
    html.append('</script>')

    html.append('</html>')
    write("/tmp/test.html", '\n'.join(html))

    #write("%s.js" % tmpname, '\n'.join(lines))
    #return run_command("node %s.js" % tmpname)
    return run_command("%s /tmp" %nodewebkit, nodewebkit_workaround=True)



def run_pythonjs_dart_test_on_node(dummy_filename):
    """PythonJS (Dart backend - dart2js)"""
    return run_if_no_error(run_dart2js_node)

def run_dart2js_node(content):
    """Run Dart2js using Node"""
    write("%s.js" % tmpname, content)
    return run_command("node %s.js" % tmpname)

def run_pythonjs_dart_test_on_dart(dummy_filename):
    """PythonJS (Dart backend - Dart VM)"""
    return run_if_no_error(run_dart)

def run_dart(content):
    """Run Dart2js using Node"""
    #write("%s.js" % tmpname, content)
    return run_command("%s %s" % (dart_exe, "/tmp/dart2js-input.dart"))


def run_pythonjs_coffee_test_on_node(dummy_filename):
    """PythonJS (CoffeeScript)"""
    return run_if_no_error(run_coffee_node)

def run_coffee_node(content):
    """Run CoffeeScript using Node"""
    #builtins = read(os.path.join("../pythonjs", "pythonjs.js"))
    write("%s.js" % tmpname, content)
    return run_command("node %s.js" % tmpname)


def run_pythonjs_lua_test_on_lua(dummy_filename):
    """PythonJS (Lua) on Lua"""
    return run_if_no_error(run_lua_lua)

def run_lua_lua(content):
    """Run Lua using Lua"""
    write("%s.lua" % tmpname, content)
    return run_command("lua %s.lua" % tmpname)


def run_pythonjs_lua_test_on_luajit(dummy_filename):
    """PythonJS (LuaJIT backend)"""
    return run_if_no_error(run_lua_luajit)

def run_lua_luajit(content):
    """Run Lua using LuaJIT"""
    write("%s.lua" % tmpname, content)
    return run_command("luajit %s.lua" % tmpname)

def run_pythonjs_luajs_test_on_node(dummy_filename):
    """PythonJS (Lua.js)"""
    return run_if_no_error(run_luajs_node)

def run_luajs_node(content):
    """Run Lua.js using Node"""
    builtins = read(os.path.join("../external/lua.js", "lua.js"))
    write("%s.js" % tmpname, builtins + '\n' + content)
    return run_command("node %s.js" % tmpname)


def run_pythonjs_go_test(dummy_filename):
    """PythonJS (Go backend)"""
    return run_if_no_error(run_go)

def run_go(content):
    """compile and run go program"""
    write("%s.go" % tmpname, content)
    errors = run_command("go build -o /tmp/regtest-go %s.go" % tmpname)
    if errors:
        return errors
    else:
        return run_command( '/tmp/regtest-go' )


def run_pythonjs_gopherjs_test(dummy_filename):
    """PythonJS (Gopherjs)"""
    return run_if_no_error(run_gopherjs_node)

def run_gopherjs_node(content):
    """Run Gopherjs using Node"""
    write("%s.js" % tmpname, content)
    return run_command("node %s.js" % tmpname)

def run_html_test( filename, sum_errors ):
    lines = open(filename, 'rb').read().decode('utf-8').splitlines()
    filename = os.path.split(filename)[-1]
    doc = []; script = None
    for line in lines:
        if line.strip().startswith('<link') and 'stylesheet' in line and '~/' in line:
            doc.append('<style>')
            css = line.split('href=')[-1].split()[0][1:-1]
            print('css', css)
            assert css.startswith('~/')
            assert css.endswith('.css')
            assert os.path.isfile( os.path.expanduser(css) )
            doc.append( open(os.path.expanduser(css), 'rb').read().decode('utf-8') )
            doc.append('</style>')
        elif line.strip().startswith('<script'):
            if 'type="text/python"' in line:
                doc.append( '<script type="text/javascript">')
                script = list()
            elif 'src=' in line and '~/' in line:  ## external javascripts installed in users home folder
                x = line.split('src="')[-1].split('"')[0]
                if os.path.isfile(os.path.expanduser(x)):

                    doc.append( '<script type="text/javascript">' )
                    doc.append( open(os.path.expanduser(x), 'rb').read().decode('utf-8') )
                    doc.append( '</script>')
            else:
                doc.append( line )

        elif line.strip() == '</script>':
            if script:
                open('/tmp/%s.js'%filename, 'wb').write( ('\n'.join(script)).encode('utf-8') )
                js = translate_js( '/tmp/%s.js'%filename, requirejs=False )  ## inserts TestError and others
                doc.append( js )
            doc.append( line )
            script = None

        elif isinstance( script, list ):
            script.append( line )

        else:
            doc.append( line )

    html = '\n'.join(doc)
    open('/tmp/%s.html'%filename, 'wb').write( html.encode('utf-8') )
    if '--nodewebkit' in sys.argv:
        ## nodewebkit can bypass all cross origin browser-side security
        cfg = '{"name":"test", "main":"%s.html", "window":{"width":1200, "height":700}}' %filename
        write("/tmp/package.json", cfg)
        run_command("%s /tmp" %nodewebkit, nodewebkit_workaround=True)

    else:
        ## chrome-extension that won't force you to close your browser windows when deving: `Allow-Control-Allow-Origin:*`
        ## this still fails with iframes that do not allow cross origin.
        cmd = [
            'google-chrome', 
            '--app=file:///tmp/%s.html'%filename,
            '--allow-file-access-from-files',  ## only takes affect if chrome is closed
            '--allow-file-access',             ## only takes affect if chrome is closed
            '--disable-web-security'           ## only takes affect if chrome is closed
        ]
        ## non-blocking, TODO check for chrome extension that allows output of console.log to stdout
        subprocess.check_call(cmd)


table_header = "%-12.12s %-28.28s"
table_cell   = '%-6.6s'

def run_test_on(filename):
    """run one test and returns the number of errors"""
    if not show_details:
        f = open(filename)
        comment = f.readline().strip(" \n\"'")
        f.close()
        print(table_header % (filename[2:-3], comment), end='')
    sum_errors = {}

    if filename.endswith('.html'):
        run_html_test( filename, sum_errors )
        return sum_errors

    def display(function):
        global _test_description
        _test_description = function.__doc__
        if show_details:
            print('\n<%s>\n' % function.__doc__)

        errors = function(filename)
        if errors:
            if not show_details:
                print(table_cell % ''.join('%s%d' % (k[0], v)
                                            for k, v in errors.items()),
                      end='')
        else:
            if not show_details:
                print(table_cell % 'OK', end='')
        sys.stdout.flush()

        for k, v in errors.items():
            sum_errors[k] = sum_errors.get(k, 0) + v

        if show_details:
            print('-'*77)

    if 'requirejs' not in filename and not filename.startswith('./go/'):
        display(run_python_test_on)
        display(run_python3_test_on)
        if pypy_runnable:
            display(run_pypy_test_on)
        if old_pypy_runnable:
            display(run_old_pypy_test_on)

    global js
    if not filename.startswith('./go/'):
        js = translate_js(
            filename, 
            javascript=False, 
            multioutput=filename.startswith('./threads/' or filename.startswith('./bench/webworker'))
        )
        if rhino_runnable:
            display(run_pythonjs_test_on)
        if node_runnable:
            display(run_pythonjs_test_on_node)

        if nodewebkit_runnable:
            display(run_pythonjs_test_on_nodewebkit)


    if '--no-javascript-mode' not in sys.argv and not filename.startswith('./go/'):
        js = translate_js(filename, javascript=True, multioutput=filename.startswith('./threads/' or filename.startswith('./bench/webworker')))
        if rhino_runnable:
            display(run_pythonjsjs_test_on)
        if node_runnable:
            display(run_pythonjsjs_test_on_node)

        if nodewebkit_runnable:
            display(run_pythonjsjs_test_on_nodewebkit)


    if 'requirejs' not in filename:

        if dart_runnable:
            js = translate_js(filename, javascript=False, dart=True)
            display(run_pythonjs_dart_test_on_dart)

        if dart2js_runnable and node_runnable:
            js = translate_js(filename, javascript=False, dart=True)
            display(run_pythonjs_dart_test_on_node)

        if coffee_runnable and node_runnable:
            js = translate_js(filename, javascript=False, dart=False, coffee=True)
            display(run_pythonjs_coffee_test_on_node)

        if luajs_runnable and node_runnable:
            js = translate_js(filename, luajs=True)
            display(run_pythonjs_luajs_test_on_node)

        if lua_runnable:
            js = translate_js(filename, lua=True)
            display(run_pythonjs_lua_test_on_lua)

        if luajit_runnable:
            js = translate_js(filename, lua=True)
            display(run_pythonjs_lua_test_on_luajit)

        if go_runnable:
            js = translate_js(filename, go=True)
            display(run_pythonjs_go_test)

        if gopherjs_runnable:
            js = translate_js(filename, gopherjs=True)
            display(run_pythonjs_gopherjs_test)

    print()
    return sum_errors

def run():
    """Run all the tests or the selected ones"""

    if not show_details:
        headers =  ["Py-\nthon2", "Py-\nthon3"]
        if pypy_runnable:
            headers.append("PyPy\n")

        if old_pypy_runnable:
            headers.append("PyPy\n1.9")

        if rhino_runnable:
            headers.append("JS\nRhino")
        if node_runnable:
            headers.append("JS\nNode")

        if nodewebkit_runnable:
            headers.append("JS\nWebkit")

        if rhino_runnable:
            headers.append("JSJS\nRhino")

        if node_runnable:
            headers.append("JSJS\nNode")

        if nodewebkit_runnable:
            headers.append("JSJS\nWebkit")

        if dart_runnable:
            headers.append("Dart\nDart")

        if node_runnable:

            if dart2js_runnable:
                headers.append("Dart\nNode")
            if coffee_runnable:
                headers.append("Coffe\nNode")

            if luajs_runnable:
                headers.append("LuaJS\nNode")

        if lua_runnable:
            headers.append("Lua\nLua")

        if luajit_runnable:
            headers.append("Lua\nJIT")
        
        if go_runnable:
            headers.append("Go\n-")


        print(table_header % ("", "Regtest run on")
              + ''.join(table_cell % i.split('\n')[0]
                        for i in headers)
              )
        print(table_header % ("", "")
              + ''.join(table_cell % i.split('\n')[1]
                        for i in headers
                        )
              )
    errors = []
    total_errors = {}
    for filename in files():
        if filename.startswith('./bench/'):
            start_benchmark( os.path.split(filename)[-1] )

        if show_details:
            if os.path.abspath(filename) not in argv:
                continue
            print('*'*77)
            print(filename)
        sum_errors = run_test_on(filename)
        if sum_errors:
            errors.append(filename)
            for k, v in sum_errors.items():
                total_errors[k] = total_errors.get(k, 0) + v

        if filename.startswith('./bench/'):
            end_benchmark( os.path.split(filename)[-1] )


    print()
    if errors:
        nr_errors = 0
        if not show_details:
            print("To see details about errors, run the commands:")
            for i in errors:
                print('\t%s %s' % (sys.argv[0], i))
            print("\nSummary of errors:")
            for k, v in total_errors.items():
                print('\t%d %s' % (v, k))
                if k in ('Error', 'Translation error'):
                    nr_errors += v
        if nr_errors == 0:
            print("\nRegression tests run fine but with warnings")
        sys.exit(nr_errors)
    else:
        print("Regression tests run fine")
        sys.exit(0)
run()

#!/usr/bin/env python
import os, sys, traceback, json

from python_to_pythonjs import main as python_to_pythonjs
from pythonjs import main as pythonjs_to_javascript
from pythonjs_to_dart import main as pythonjs_to_dart
from pythonjs_to_coffee import main as pythonjs_to_coffee
from pythonjs_to_lua import main as pythonjs_to_lua
from pythonjs_to_luajs import main as pythonjs_to_luajs

cmdhelp = """\
usage: translator.py [--dart|--coffee|--lua] file.py
       translator.py --visjs file.py\
"""

def main(script, module_path=None):
    if '--visjs' in sys.argv:
        import python_to_visjs
        return python_to_visjs.main( script )
    else:
        code = ''
        if '--dart' in sys.argv:
            a = python_to_pythonjs(script, dart=True, module_path=module_path)
            code = pythonjs_to_dart( a )
        elif '--coffee' in sys.argv:
            a = python_to_pythonjs(script, coffee=True, module_path=module_path)
            code = pythonjs_to_coffee( a )
        elif '--lua' in sys.argv:
            a = python_to_pythonjs(script, lua=True, module_path=module_path)
            try: code = pythonjs_to_lua( a )
            except SyntaxError:
                err = traceback.format_exc()
                lineno = 0
                for line in err.splitlines():
                    if "<unknown>" in line:
                        lineno = int(line.split()[-1])

                b = a.splitlines()[ lineno ]
                sys.stderr.write( '\n'.join([err,b]) )
                
        elif '--luajs' in sys.argv:  ## converts back to javascript
            a = python_to_pythonjs(script, lua=True, module_path=module_path)
            code = pythonjs_to_luajs( a )
        else:
            a = python_to_pythonjs(script, module_path=module_path)
            if isinstance(a, dict):
                res = {}
                for jsfile in a:
                    res[ jsfile ] = pythonjs_to_javascript( a[jsfile], webworker=jsfile != 'main' )
                return res
            else:
                ## requirejs module is on by default, this wraps the code in a `define` function
                ## and returns `__module__`
                ## if --no-wrapper is used, then the raw javascript is returned.
                code = pythonjs_to_javascript( a, requirejs='--no-wrapper' not in sys.argv )

        return code

def command():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(cmdhelp)
        return

    mpath = None
    scripts = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.endswith('.py') or arg.endswith('.html'):
                scripts.append( arg )
                if mpath is None:
                    mpath = os.path.split(arg)[0]

    if len(scripts):
        a = []
        for script in scripts:
            a.append( open(script, 'rb').read() )
        data = '\n'.join( a )
    else:
        data = sys.stdin.read()

    js = main(data, module_path=mpath)
    if isinstance(js, dict):
        print( json.dumps(js) )
    else:
        print(js)


if __name__ == '__main__':
    command()

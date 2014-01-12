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

import os
import re
import sys
import tempfile

tmpname = os.path.join(tempfile.gettempdir(), "xxx_regtest")

print("Temporary files are stored into '%s...'" % tmpname)
print()

show_details = len(sys.argv) > 1

# List of valid filenames in the parameters
argv = [os.path.abspath(name)
        for name in sys.argv[1:]
        if os.path.exists(name)
        ]

if show_details:
    display_errors = ""
else:
    display_errors = "2>/dev/null"

def files():
    """All the filenames of the regression tests"""
    for dirpath, dirnames, filenames in os.walk('.'):
        if dirpath == '.':
            continue
        for filename in filenames:
            if filename.endswith(".py"):
                yield dirpath + os.path.sep + filename

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

def run_command(command, returns_stdout_stderr=False):
    """Returns the number of problems"""
    f = os.popen(command + " 2>%s.errors" % tmpname,  'r')
    stdout = f.read().strip()
    f.close()

    stderr = read("%s.errors" % tmpname)
    if stderr:
        if show_details:
            print(stderr)
    if returns_stdout_stderr:
        return stdout, stderr
    if stdout:
        if show_details:
            print(stdout)

    errors = stdout + stderr
            
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

def patch_assert(filename):
    """Patch the regression tests to add information into asserts"""
    out = []
    for i, line in enumerate(read(filename).split('\n')):
        out.append(re.sub("(Error|Warning)\((.*)\)",
                          r'\1("%s",%d,\2,"\2")' % (filename, i),
                          line)
                   )
    return '\n'.join(out)
        
def patch_python(filename):
    """Rewrite the Python code"""
    return ("""# -*- coding: utf-8 -*-
def Error(file, line, result, test):
    if not result:
        print(file + ":" + str(line) + " Error fail " + test)
def Warning(file, line, result, test):
    if not result:
        print(file + ":" + str(line) + " Warning fail " + test)
"""
            +  patch_assert(filename))

def run_python_test_on(filename):
    """Python tests"""
    write("%s.py" % tmpname, patch_python(filename))
    return run_command("python %s.py %s" % (tmpname, display_errors))

def run_python3_test_on(filename):
    """Python3 tests"""
    write("%s.py" % tmpname, patch_python(filename))
    return run_command("python3 %s.py %s" % (tmpname, display_errors))

def run_pythonjs_test(filename):
    """run tests"""
    stdout, stderr = run_command(os.path.join("..", "pythonjs",
                                              "translator.py")
                                 + ' ' + filename,
                                 returns_stdout_stderr=True)
    if stderr:
        return {'Translation error':1}
    else:
        return run_js(stdout)

def run_pythonjs_test_on(filename):
    """JS PythonJS tests"""
    write("%s.py" % tmpname, patch_python(filename))
    return run_pythonjs_test("%s.py" % tmpname)

def run_pythonjsjs_test_on(filename):
    """JSJS PythonJS with javascript tests"""
    write("%s.py" % tmpname,
          'pythonjs.configure(javascript=True)\n'
          + patch_python(filename))
    return run_pythonjs_test("%s.py" % tmpname)

def run_js(content):
    """Run Javascript using Rhino"""
    builtins = read(os.path.join("..", "pythonjs.js"))
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

table_header = "%-20.20s %-30.30s"
table_cell   = '%-8.8s'

def run_test_on(filename):
    """run one test and returns the number of errors"""
    if not show_details:
        f = open(filename)
        comment = f.readline().strip(" \n\"'")
        f.close()
        print(table_header % (filename[2:-3], comment), end='')
    sum_errors = {}
    def display(function):
        if show_details:
            print('-'*77,'\nRunning %s\n\n' % function.__doc__)
        errors = function(filename)
        if errors:
            if not show_details:
                #print(table_cell % function.__doc__.split(' ')[0], end='')
                print(table_cell % ''.join('%s%d' % (k[0], v)
                                            for k, v in errors.items()),
                      end='')
        else:
            if not show_details:
                print(table_cell % 'OK', end='')

        for k, v in errors.items():
            sum_errors[k] = sum_errors.get(k, 0) + v
        
    display(run_python_test_on)
    display(run_python3_test_on)
    display(run_pythonjs_test_on)
    display(run_pythonjsjs_test_on)
    print()
    return sum_errors

def run():
    """Run all the tests or the selected ones"""

    if not show_details:
        print(table_header % ("", "Regtest run on")
              + ''.join(table_cell % i
                        for i in ("Python", "Python3", "PyJS", "PyJSJS")
                        )
              )
    errors = []
    total_errors = {}
    for filename in files():
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

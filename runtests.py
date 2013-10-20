#!/usr/bin/env python
import os
from difflib import Differ

from envoy import run

from pythonscript.pythonscript import main as pythonjs


ROOT = os.path.join(os.path.dirname(__file__), 'unittests')

with open('pythonscript.js') as f:
    PYTHONJS = f.read()

MOCK = """
// MOCK START
window = {};
HTMLDocument = HTMLElement = function() {};
// MOCK END
"""


if __name__ == '__main__':
    for test in os.listdir(ROOT):
        if test.endswith('.py'):
            filepath = os.path.join(ROOT, test)
            with open(filepath) as f:
                script = f.read()
            exec_script = test + 'exec.js'
            exec_script = os.path.join('/tmp', exec_script)
            with open(exec_script, 'w') as f:
                f.write(MOCK)
                f.write(PYTHONJS)
                f.write(pythonjs(script))
            r = run('nodejs %s' % exec_script)
            if r.status_code != 0:
                print(r.std_err)
                print('%s ERROR :(' % test)
            else:
                expected = os.path.join(ROOT, test + '.expected')
                with open(expected) as f:
                    expected = f.read()
                if expected == r.std_out:
                    print('%s PASS :)' % test)
                else:
                    compare = Differ().compare
                    diff = compare(expected.split('\n'), r.std_out.split('\n'))
                    for line in diff:
                        print(line)
                    print('%s FAILED :(' % test)

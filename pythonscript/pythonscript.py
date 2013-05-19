#!/usr/bin/env python
import sys

from StringIO import StringIO

from python_to_pythonjs import PythonToPythonJS
from pythonjs import JSGenerator
from ast import parse


def main():
    input = parse(sys.stdin.read())
    tree = parse(input)
    stdout = sys.stdout
    s = StringIO()
    sys.stdout = s
    PythonToPythonJS().visit(tree)
    tree = parse(s.getvalue())
    sys.stdout = stdout
    print JSGenerator().visit(tree)


if __name__ == '__main__':
    main()

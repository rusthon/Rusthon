#!/usr/bin/env python
import sys
from ast import parse

from pythonjs import JSGenerator
from python_to_pythonjs import PythonToPythonJS


def main():
    input = parse(sys.stdin.read())
    pythonscript = PythonToPythonJS().visit(input)
    jsgenerator = JSGenerator()
    print jsgenerator.visit(pythonscript)


if __name__ == '__main__':
    main()

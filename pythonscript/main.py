import sys
from ast import parse

from pythonjs import JSGenerator
from pythonscript_transformer import PythonScriptTransformer


def main():
    input = parse(sys.stdin.read())
    pythonscript = PythonScriptTransformer().visit(input)
    jsgenerator = JSGenerator()
    print jsgenerator.visit(pythonscript)


if __name__ == '__main__':
    main()

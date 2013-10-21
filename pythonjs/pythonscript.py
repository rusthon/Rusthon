#!/usr/bin/env python
import sys

from python_to_pythonjs import main as python_to_pythonjs
from pythonjs import main as pythonjs


def main(script):
    return pythonjs(python_to_pythonjs(script))


def command():
    print(main(sys.stdin.read()))


if __name__ == '__main__':
    command()

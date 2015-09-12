"""replace"""
from runtime import *

def main():
	a = 'abc'
	b = a.replace('a', 'A')
	assert( b == 'Abc')

	a = 'aaa'
	b = a.replace('a', 'A')
	assert( b == 'AAA')

main()
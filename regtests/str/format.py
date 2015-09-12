"""string.format"""
from runtime import *

def main():
	a = '{x}{y}'.format( x='A', y='B')
	assert(a == 'AB')

main()
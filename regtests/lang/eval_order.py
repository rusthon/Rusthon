from runtime import *
'''
evaluation order
'''
# https://github.com/PythonJS/PythonJS/issues/131

def main():
	a = False and (False or True)
	assert( a==False )
main()

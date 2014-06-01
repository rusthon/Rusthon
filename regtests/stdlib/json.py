'''stdlib json'''
import json

def main():
	x = ['a', 'b']
	s = json.dumps( x )
	y = json.loads( s )
	TestError( len(y)==2 )
	TestError( y[0]=='a' )
	TestError( y[1]=='b' )

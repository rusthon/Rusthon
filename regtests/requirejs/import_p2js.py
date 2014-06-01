'''load p2.js physics library'''
# sudo npm install -g p2
import p2

def main():
	v1 = p2.vec2.create()
	v2 = p2.vec2.fromValues(10,20)
	TestError( len(v1)==2 )
	TestError( v2[0]==10 )
	TestError( v2[1]==20 )


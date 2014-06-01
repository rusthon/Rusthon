'''load three.js library'''
# sudo npm install -g three
import three

def main():
	v1 = new( three.Vector3(1,2,3) )
	TestError( len(v1)==3 )
	TestError( v1.x==1 )
	TestError( v1.y==2 )
	TestError( v1.z==3 )



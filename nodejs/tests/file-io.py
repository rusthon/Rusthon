from nodejs.io import *
from nodejs.sys import *
from nodejs.os import *

path = sys.argv[ len(sys.argv)-1 ]
f = open( path, 'rb' )
print f.read()
print 'read file:', path
print 'file-io test complete'


print 'printing files in tmp'
for name in os.listdir( '/tmp' ):
	print name

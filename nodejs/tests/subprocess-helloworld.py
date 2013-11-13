from nodejs.subprocess import *

print 'testing subprocess.call'
subprocess.call( 'ls', ['-lh'] )
print 'test complete.'


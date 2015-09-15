import os, subprocess
os.chdir( os.path.split(__file__)[0] )
subprocess.check_call(['python', 'test-c++.py'])
subprocess.check_call(['python', 'test-go.py'])
subprocess.check_call(['python', 'test-javascript.py'])
subprocess.check_call(['python', 'test-markdowns.py'])

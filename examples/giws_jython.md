Jython Hello World
------------------
You need to download jython-standalone.jar from 
http://www.jython.org/downloads.html
tested with jython-standalone-2.7-b3.jar, rename to jython.jar and build with this command:

@test.sh
```bash
./rusthon.py ./examples/giws_jython.md --data=~/Downloads/jython.jar
```

Gwis Wrapper
-------
Gwis generates JNI wrappers so the Java object can be used from C++.
https://github.com/opencollab/giws
The XML below wraps the PythonInterpreter from Jython.

@gwis
```xml
<package name="org.python.util">
	<object name="PythonInterpreter">
		<method name="exec" returnType="void">
		<param type="String" name="s" />
		</method>
	</object>
</package>
```


Rusthon
------------

```rusthon
import jvm
jvm.load( 'jython.jar' )
jvm.namespace('org.python.util')

def main():
	interp = jvm( PythonInterpreter() )
	script = "print 'hello world'"
	interp.__exec__(cstr(script))

```
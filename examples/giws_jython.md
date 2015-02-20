
Jython Gwis Wrapper
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
You need to download jython-standalone.jar and place it in the build directory.
http://www.jython.org/downloads.html
tested with jython-standalone-2.7-b3.jar

```rusthon
import jvm
jvm.load( 'jython.jar' )
jvm.namespace('org.python.util')

def main():
	interp = jvm( PythonInterpreter() )
	script = "print 'hello world'"
	interp.__exec__(cstr(script))

```
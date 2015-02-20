
Jython Gwis Wrapper
-------
Gwis generates JNI wrappers so the Java object can be used from C++.
https://github.com/opencollab/giws
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
#jvm.load( 'jython-standalone-2.7-b3.jar' )
jvm.load( 'jython.jar' )
jvm.namespace('org.python.util')

def main():
	interp = jvm( PythonInterpreter() )
	script = "print 'hello world'"
	interp.__exec__(cstr(script))

```
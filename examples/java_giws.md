Java
-----
@mymodule/MyJavaClass.java
```java
package mymodule;

public class MyJavaClass{
	public MyJavaClass(){
	}
	public double bar(double a, double b){
		return a*b;
	}
}
```

Gwis Wrapper
-------
Gwis generates JNI wrappers so the Java object can be used from C++.
https://github.com/opencollab/giws
@gwis
```xml
<package name="mymodule">
  <object name="MyComplexClass">
        <method name="bar" returnType="double">
          <param type="double" name="a" />
          <param type="double" name="b" />
        </method>
  </object>
</package>
```


Rusthon
------------
```rusthon
import jvm
using_namespace('mymodule')


def foo( ob: MyJavaClass ):
	print ob.bar( 10.0, 100.0 )

def main():
	vm = jvm.create()
	ob  = new( MyJavaClass(vm) )
	foo( ob )

```
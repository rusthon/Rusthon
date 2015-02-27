Nim
-------
simple Nim function that adds two integers together and returns the result

```nim
proc nim_sum( a:cint, b:cint ): cint {.cdecl, exportc.} =
	result = a+b

```


Java
-------
simple Java class

@mymod/Point.java
```java
package mymod;
public class Point{
	public int x;
	public int y;
	public Point(){this.x=0; this.y=0; }
	public void set(int x, int y){
		this.x = x;
		this.y = y;
	}
	public int getx(){
		return this.x;
	}
	public int gety(){
		return this.y;
	}
	public void scale(int s){
		this.x *= s;
		this.y *= s;
	}

}
```

Gwis Wrapper
-------
wrapper for the above Java class

@gwis
```xml
<package name="mymod">
	<object name="Point">
		<method name="set" returnType="void">
		<param type="int" name="x" />
		<param type="int" name="y" />
		</method>
		<method name="getx" returnType="int">
		</method>
		<method name="gety" returnType="int">
		</method>
		<method name="scale" returnType="void">
		<param type="int" name="s" />
		</method>
	</object>
</package>
```


Rusthon
------------
`PointSubclass` subclasses from the Java class `Point`, __init__ is used to call the Java method `set`
because Gwis is missing support for constructors.
The result of nim function `nim_sum` is passed to the Java method `scale`.

```rusthon
#backend:c++

import nim
import jvm
jvm.namespace('mymod')

@jvm
class PointSubclass( Point ):
	def __init__(self, x:int, y:int):
		self.set(x,y)

	def show(self):
		print self.getx()
		print self.gety()


def main():
	nim.main()
	p1 = jvm( PointSubclass(1,2) )
	p2 = jvm( PointSubclass(10,20) )
	p1.show()
	p2.show()
	## test calling nim function and passing the result to JVM ##
	p2.scale( nim_sum(100, 1000) )
	p2.show()
```

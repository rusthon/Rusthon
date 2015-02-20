Java Subclass Hello World
------------------

@test.sh
```bash
./rusthon.py ./examples/giws_subclass.md
```

Java
-------
@mymod/A.java
```java
package mymod;
public class A{
	public A(){}
	public void foo(){
		System.out.println("A.foo from java.");
	}
}
```
@mymod/B.java
```java
package mymod;
public class B extends A{
	public B(){}
	public void bar(){
		System.out.println("B.bar from java.");
	}
}
```


Gwis Wrapper
-------

@gwis
```xml
<package name="mymod">
	<object name="A">
		<method name="foo" returnType="void">
		</method>
	</object>
	<object name="B" extends="A">
		<method name="bar" returnType="void">
		</method>
	</object>
</package>
```


Rusthon
------------

```rusthon
import jvm
jvm.namespace('mymod')

def main():
	a = jvm( A() )
	b = jvm( B() )
	a.foo()
	b.bar()

```
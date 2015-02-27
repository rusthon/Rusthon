Java Subclass Hello World
------------------

@test.sh
```bash
./rusthon.py ./examples/giws_subclass.md
```

Java
-------
note: only public classes can be wrapped by Giws.

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

Java Class B
-------
subclasses from `A` and adds the member `y` an integer.

@mymod/B.java
```java
package mymod;
public class B extends A{
	public int y;
	public B(){ this.y=420; }
	public void bar(int i){
		System.out.println("B.bar from java.");
		this.y = i;
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
		<param type="int" name="i" />
		</method>
	</object>
</package>
```


Rusthon
------------

```rusthon
import jvm
jvm.namespace('mymod')

@jvm
class C(B):
	def __init__(self, x:int):
		self.x = x

	def get_y(self) ->int:
		inline('''
		auto env = getCurrentEnv();
		auto fid = env->GetFieldID(this->instanceClass, "y", "I");
		return env->GetIntField(this->instance, fid);
		''')

	def hey(self):
		print('hey from rusthon')

```

main entry point
-----

```rusthon
def main():
	a = jvm( A() )
	b = jvm( B() )
	a.foo()
	b.bar( 10 )

```
A rusthon class that subclasses from a java class can have constructor args, below `C` is constructed with 999.
The attribute `x` can be used directly on `c` because it is attached to the c++ class instance

```rusthon
	c = jvm( C(999) )
	print c.x  # prints 999
	c.hey()

```
Below `y` can not be used directly because its attached to the java object.
The workaround `get_y` defined above works because it uses the JNI api directly.

```rusthon
	#print c.y       ## this fails
	print c.get_y()  ## prints 420

```

the subclass can use methods defined on java parent class and up to the base class.

```rusthon
	c.foo()
	c.bar( 100 )     ## sets y to 100
	print c.get_y()  ## prints 100

	## TODO java-only classes ##
	if isinstance(c, C):
		print 'c is class C'

```
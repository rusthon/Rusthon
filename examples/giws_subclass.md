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

def main():
	a = jvm( A() )
	b = jvm( B() )
	a.foo()
	b.bar( 10 )

	print 'testing c...'

	## a rusthon class that subclasses from a java class can have constructor args ##
	c = jvm( C(999) )
	print c.x  ## x can be used directly, prints 999

	## y can not be used directly because its attached to the java object ##
	#print c.y
	## this works because JNI code is inlined above in get_y
	print c.get_y()  ## prints 420

	## the subclass can use methods defined from java. ##
	c.foo()
	c.bar( 100 )     ## sets y to 100
	print c.get_y()  ## prints 100

	## testing subclass method ##
	c.hey()

	## TODO java-only classes ##
	if isinstance(c, C):
		print 'c is class C'

```
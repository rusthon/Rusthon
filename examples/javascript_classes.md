JavaScript Backend - Classes
-------

Nested classes can be used to emulate Python style modules, and create namespaces.

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_classes.md
```

See Also
--------
* [javascript_webworkers_classes.md](javascript_webworkers_classes.md)
* [threejs_catmullclark.md](threejs_catmullclark.md)


html
----


@index.html
```html
<html>
<head>

<@myscript>

</head>
<body>
see the javascript console for test results
</body>
</html>
```

Example
--------

@myscript
```rusthon
#backend:javascript
from runtime import *

class Root:
	def root(self):
		return 'hi from root'

class Nested:
	class SubClass(Root):
		def foo(self):
			print 'calling Nested.Subclass.foo'
			print Nested
			print Nested.SubClass
			print 'Nested.Subclass: foo OK'
			return new(Nested.SubClass())

	def foobar(self, x):
		print x

		class SubNested:
			def submeth(self, x,y):
				print x+y

		snest = SubNested()
		snest.submeth('testing sub', 'NESTED')
		return snest

def test():
	nest = Nested()
	snest = nest.foobar('testing nexted class')
	print snest
	snest.submeth('called from outer scope','subnested')

	scls = new Nested.SubClass()
	scls2 = scls.foo()

	print 'TESTING META STUFF'
	print scls.__class__
	print scls.__class__.__name__
	print 'testing isinstance'
	print isinstance(scls, Nested.SubClass)
	print isinstance(scls, scls.__class__)

	class SubSubClass(Nested.SubClass):
		def bar(self):
			print 'SubSubClass.bar OK'

	print 'testing issubclass'
	print issubclass(SubSubClass, Nested.SubClass)
	print issubclass(Nested.SubClass, Root)
	print issubclass(SubSubClass, Root)
	print 'testing SubSubClass...'
	ssc = SubSubClass()
	ssc.foo()
	ssc.bar()


test()

```
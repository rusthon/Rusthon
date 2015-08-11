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
	MyClassVar = 1
	MyOb = {'x':1, 'y':2 }
	## TODO clean up list comps, here it leaks temp vars into the global namespace
	SomeList = [a for a in ('hello', 'world')]

	@staticmethod
	def somefunc(v): return v*2

	## any function without `self` as the first argument becomes a staticmethod ##
	def otherfunc(v): return v*3

	def root(self):
		return 'hi from root'

	@property
	def myprop(self):
		return 100

	## same as `@property`, just shorter and more clear
	@getter
	def otherprop(self):
		return 200

class Nested:
	class SubClass(Root):
		class XXX:
			def bar(self):
				print 'XXX'

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

@debugger
def test():
	assert Root.MyClassVar == 1
	assert len(Root.SomeList) == 2
	for item in Root.SomeList:
		print item

	for key in Root.MyOb:
		print key
		print Root.MyOb[key]

	assert Root.somefunc(2) == 4
	assert Root.otherfunc(2) == 6

	r = Root()
	assert r.myprop == 100
	assert r.otherprop == 200

	nest = Nested()
	snest = nest.foobar('testing nexted class')
	print snest
	snest.submeth('called from outer scope','subnested')

	scls = new Nested.SubClass()
	scls2 = scls.foo()

	xx = new Nested.SubClass.XXX()
	xx.bar()

	print 'TESTING META STUFF'
	print scls.__class__
	print scls.__class__.__name__
	print 'testing isinstance'
	assert isinstance(scls, Nested.SubClass)
	assert isinstance(scls, scls.__class__)
	assert isinstance(scls, Root)
	assert isinstance(scls, Nested) is False

	class SubSubClass(Nested.SubClass):
		def bar(self):
			print 'SubSubClass.bar OK'

	print 'testing issubclass'
	assert issubclass(SubSubClass, Nested.SubClass)
	assert issubclass(Nested.SubClass, Root)
	assert issubclass(SubSubClass, Root)
	assert issubclass(Root, Nested) is False

	print 'testing SubSubClass...'
	ssc = SubSubClass()
	ssc.foo()
	ssc.bar()


test()

```
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

note the special HTML syntax `<!myscript>` embeds the original source in your html as
`<script type="text/rusthon" id="myscript">SOURCE</script>`

@index.html
```html
<html>
<head>
<script src="~/ace-builds/src-min/ace.js" git="https://github.com/ajaxorg/ace-builds.git"></script>
<script src="~/ace-builds/src-min/theme-monokai.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/worker-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/mode-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/mode-python.js" type="text/javascript"></script>

<!myscript>
<@myscript>

</head>
<body onload="test()">
</body>
</html>
```

Example
--------

Note the extra syntax `->` is used below, any class that defines a method named `__right_arrow__` can use this special operator.


@myscript
```rusthon
#backend:javascript
from runtime import *

class Root:
	def __right_arrow__(self, a, b):
		print a+b
		return a+b

	MyClassVar = 1
	MyOb = {'x':1, 'y':2 }
	## TODO clean up list comps, here it leaks temp vars into the global namespace
	SomeList = [a for a in ('hello', 'world')]

	## note: this is valid python, but will not work in Rusthon
	#OtherClassVar = MyClassVar + 10
	## class-level variables that refer to another must prefix the class name
	OtherClassVar = Root.MyClassVar + 10

	@staticmethod
	def somefunc(v): return v*2

	## any function without `self` as the first argument becomes a staticmethod ##
	def otherfunc(v): return v*3

	def root(self):
		return 'hi from root'

	@property
	def myprop(self):
		return 100
	@myprop.setter
	def f(self, v):
		self._myprop = v

	## same as `@property`, just shorter and more clear
	@getter
	def otherprop(self):
		return 200
	@setter
	def otherprop(self, v):
		print 'calling setter on `otherprop`:' + v
		self.hidden = v

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

def show_source_code():
	document.body->(
		document->('div')->(id='PY_CODE', style="position:absolute;height:100%;width:50%;top:0;left:0"),
		document->('div')->(id='JS_CODE', style="position:absolute;height:100%;width:50%;top:0;right:0"),
	)
	editor = ace.edit('PY_CODE')
	editor.setValue(document->('#myscript').firstChild.nodeValue)
	editor.setTheme("ace/theme/monokai")
	editor.getSession().setMode("ace/mode/python")
	editor.gotoLine( editor.session.getLength()-1 )

	editor = ace.edit('JS_CODE')
	editor.setValue(document->('#myscript_transpiled').firstChild.nodeValue)
	editor.setTheme("ace/theme/monokai")
	editor.getSession().setMode("ace/mode/javascript")
	editor.gotoLine( editor.session.getLength()-1 )


@debugger
def test():
	show_source_code()

	assert Root.MyClassVar == 1
	assert Root.OtherClassVar == 11
	assert len(Root.SomeList) == 2
	for item in Root.SomeList:
		print item

	for key in Root.MyOb:
		print key
		print Root.MyOb[key]

	assert Root.somefunc(2) == 4
	assert Root.otherfunc(2) == 6

	r = Root()
	assert r->(1,2) == 3

	assert r.myprop == 100
	r.myprop = 'OK'
	assert r._myprop == 'OK'

	print r.otherprop
	assert r.otherprop == 200
	r.otherprop = 'OK'
	assert r.hidden == 'OK'


	nest = Nested()
	snest = nest.foobar('testing nexted class')
	print snest
	snest.submeth('called from outer scope','subnested')

	scls = new Nested.SubClass()
	assert scls->(100,100) == 200
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


```
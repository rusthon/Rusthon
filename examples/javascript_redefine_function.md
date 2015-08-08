Redefinable JavaScript Functions
--------------------------------

By default when you transpile your application to JavaScript 
special code will be inserted into your functions to that checks
for uncaught errors and makes all functions redefinable at runtime.

The command line option `--release` generates regular JavaScript functions,
which can not be redefined at runtime in an easy and clear way, 
check out what a pain it can be normally:
* http://stackoverflow.com/questions/9941736/why-javascript-doesnt-let-a-function-redefine-itself-from-within-itself
* http://stackoverflow.com/questions/2136522/can-you-alter-a-javascript-function-after-declaring-it
* http://stackoverflow.com/questions/3227222/javascript-function-redefinition

Redefinable functions are helpful with custom debuggers and other advanced use cases.
For your app release, if you want to keep some of your functions redefinable at runtime,
use the `@redef` decorator on the function, and it will be kept as redefinable
even when you build your project with `--release` option.

Functions marked with `@redef` can call the special method `redefine` passing a string
of code or function object.  If you pass a string it will be [evaluated](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval)
in the scope of the function itself (and this way can capture variables in its outer scope if it is a nested function).
If you pass a function object it is directly set as the new function.

The runtime overhead of using `@redef` is minimal: one indirect call and two if-checks.

@myapp
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

@redef
def bar():
	show('bar original')

	def F(x,y):
		show('bar changed')
		show( x+y )

	bar.redefine(F)
	show('only shows once')

def redefine_bar():
	code = document.getElementById('CODE').value
	print code
	bar.redefine(code)

class A:
	@redef
	def foo(self):
		show('foo method')

def main():
	bar()
	bar(1,1)
	bar(2,2)

	a = A()
	a.foo()
	def newfoo():
		show('new foo method OK')
	a.foo.redefine(newfoo)
	a.foo()


```

@index.html
```html
<html>
<head>
</head>
<body onload="main()">
<pre id="CONTAINER">
</pre>
<@myapp>
<input type="text" id="CODE" value="function f(){show('hello world')}"/>
<input type="button" onclick="redefine_bar();bar()"/>
</body>
</html>
```
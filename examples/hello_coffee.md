CoffeeScript
------------

http://coffeescript.org/


@mycoffee.js
```coffee

elvis = 1
alert "I knew it!" if elvis?

square = (x) -> x * x

```

PythonJS
---------

@mypython.js
```rusthon
#backend:javascript

def main():
	alert( square(420) )

main()

```

HTML
-----

The output of both transpilers is inserted into the final html

@index.html
```html
<html>
<body>
<@mycoffee.js>
<@mypython.js>
</body>
</html>
```
Syntax for importing external markdowns into one for building together.

* [@import mylib/mylib_A](mylib/mylib_A.md)
* [@import mylib/mylib_B](mylib/mylib_B.md)


```rusthon

def main():
	a = A()
	a.foo()
	b = B()
	b.bar()

```
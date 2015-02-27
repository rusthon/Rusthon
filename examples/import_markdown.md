Syntax for importing external markdowns into one for building together.

* [@import mylibs/mylib_A](mylibs/mylib_A.md)
* [@import mylibs/mylib_B](mylibs/mylib_B.md)


```rusthon

def main():
	a = A()
	a.foo()
	b = B()
	b.bar()

```
Java Frontend
--------------
https://github.com/rusthon/java2python

@install-script.sh
```bash
wget http://www.antlr3.org/download/antlr-3.1.3.tar.gz
tar xfz antlr-3.1.3.tar.gz
cd antlr-3.1.3/runtime/Python/
sudo python setup.py install
```

```java

public class HelloWorld {
    public static void test() {
        System.out.println("Hello, World test");
    }

    public static void foo(String msg) {
        System.out.println(msg);
    }

}
```

Rusthon
---------------------------

```rusthon
#backend:c++

def main():
	inline('HelloWorld::test()')
	s = 'hello from rusthon'
	inline('HelloWorld::foo(s)')

```
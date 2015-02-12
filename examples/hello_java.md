Java Frontend
--------------
Requires:
* https://github.com/rusthon/java2python
* Antlr 3.1.3 for Python2

@install-script.sh
```bash
cd
git clone https://github.com/rusthon/java2python.git
cd java2python
sudo python setup.py install
cd
wget http://www.antlr3.org/download/antlr-3.1.3.tar.gz
tar xfz antlr-3.1.3.tar.gz
cd antlr-3.1.3/runtime/Python/
sudo python setup.py install
```

Java
-----
Some hand written Java source code, auto converted to Rusthon's syntax,
and merged with below.
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
The above Java code is converted to Rusthon, and merged with this code.
```rusthon
#backend:c++

def main():
	HelloWorld.test()
	HelloWorld.foo("hi java")

```
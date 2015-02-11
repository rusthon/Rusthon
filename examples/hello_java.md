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

    public static void main(String[] args) {
        System.out.println("Hello, World");
    }

}
```

Rusthon
---------------------------

```rusthon
#backend:c++

def main():
	args = []string('x', 'y')
	HelloWorld.main( args )
	print('hello from rusthon')

```
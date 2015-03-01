Numba
--------
Numba is the replacement for Numpy that JIT's your code to LLVM.
Even on Linux, it is not so simple installing the correct version of LLVM and building Numba from source.
The best way to run this example is first get Anaconda Python from Continuum and install it to the default location. Get Anaconda [here](https://store.continuum.io/).

You can then tell Rusthon to use Anaconda's Python using the `--anaconda` command line switch.
This command compiles and runs this markdown file:
```bash
./rusthon.py ./examples/numba.md --run=test.py --anaconda
```

Anaconda is how Python should be packaged.  Standard Python ships with TKinter as its GUI toolkit, so that you can make the most ugly interfaces anyone has ever seen since the 80's, take a look at [this](http://tktable.sourceforge.net/tile/screenshots/demo-alt-unix.png)

Anaconda ships with a modern GUI toolkit using [Qt](http://qt-project.org/).


Simple Numba Example
--------------------

Below this simple hello world is broken apart into three code blocks,
only the first is tagged with `@test.py`, the blocks that follow are merged with it.
This allows you to write documentation in markdown, instead of python comments `#blabla`,
or doc strings.

While python comments and doc strings are still helpful, I think it is much more clear to
write high level documentation in markdown in the same file with the code, where it gets
version controlled with the source, and not lost in some wiki elsewhere.


Imports
---------
* numpy
* numba

@test.py
```python
from numpy import arange
from numba import jit
```

The jit decorator tells Numba to compile this function.
The argument types will be inferred by Numba when function is called.

```python
@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result
```

main entry point

```python
def main():
    a = arange(9).reshape(3,3)
    print(sum2d(a))

if __name__=='__main__':
    main()

```
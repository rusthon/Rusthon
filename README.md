[![Build Status](https://travis-ci.org/rusthon/Rusthon.svg)](https://travis-ci.org/rusthon/Rusthon)

Easily mix multiple languages, frontends, backends, compilers, and transpilers inside markdown files.
Markdown is the container format for your multi-language application that can contain: server backend logic and config files,
and frontend javascript with html and css, all in a single markdown file.
Rusthon compiles the markdown into tar files for release, or runs it for testing.

The integrated Python transpiler targets multiple backend languages, like: JavaScript and C++.
The JavaScript backend implements most of the dynamic and some builtin functions of Python.
The C++ backend is less dynamic and uses an extended static type syntax based on Go, Rust and C++.
The other backends are experimental.

* [highlevel overview](http://rusthon-lang.blogspot.com/2015/06/rusthon-overview.html)
* [multiple markdown syntax](https://github.com/rusthon/Rusthon/wiki/Multiple-Markdowns)

Installing
----------

* [Debian Package](https://github.com/rusthon/Rusthon/releases/download/0.9.9s/rusthon_0.9.6_all.deb)
* Fedora package comming soon

If you want to stay in sync with the git-repo, use the `install-dev.sh` script instead of the Debian or Fedora package. note: `install-dev.sh` just creates a symbolic link `transpile` that points to the current location of `rusthon.py`.


```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon
sudo ./install-dev.sh
```


Using `transpile`
-----------------
To see all the command line options run `transpile --help`

```bash
cd myproject
transpile mymarkdown.md
```

Above will compile everything in mymarkdown.md:
* if the markdown contains an html page, it will be opened with NW.js or your system default web browser.
* if the markdown contains a javascript file, it will be run with nodejs
* otherwise, if the markdown contains: C++, Rust, or Go code, it will be compiled, and the exe is run.


Getting Started Javascript
-----------------

Transpile from Python to Javascript, with specialized syntax for static types, and using [WebWorkers](https://github.com/rusthon/Rusthon/wiki/WebWorker-Syntax) and other extensions to the Python language like [mini-macros](https://github.com/rusthon/Rusthon/wiki/Macro-Functions)

Mini-macros help you make your code more readable, and hide ugly APIs like HTML DOM.
note: you can use unicode for macro names.
```python
with 𝕄 as "_=document.createElement(%s); _.setAttribute('id',%s); %s.appendChild(_)":
    𝕄( 'div', 'someid1', document.body )
    𝕄( 'img', 'someid2', document.body )

```

You can also use the `->` right arrow syntax as a shortcut on DOM elements for appending, setting attributes,
and creating text nodes.  You can also define `__right_arrow__` on your own classes to customize what `->` will do,
for more info see: [here](https://github.com/rusthon/Rusthon/wiki/JavaScript-DOM-Syntax)

The example above could be rewritten as:
```c++
with 𝕄 as "document.createElement(%s)":
    document.body->(
        𝕄('div')->(id='someid1'),
        𝕄('img')->(id='someid2')
    )

```

You can also do the same thing as above using pure python syntax.
```python
a = document.createElement('div')
a.setAttribute('id', 'someid1')
b = document.createElement('img')
b.setAttribute('id', 'someid2')
document.body.appendChild(a)
document.body.appendChild(b)
```

* [javascript example](https://github.com/rusthon/Rusthon/blob/master/examples/javascript_syntax.md)
* [javascript backend wiki](https://github.com/rusthon/Rusthon/wiki/JavaScript-Backend)
* [javascript backend doc](https://github.com/rusthon/Rusthon/blob/master/doc/pythonjs.md)
* [javascript literate unicode](https://github.com/rusthon/Rusthon/wiki/JavaScript-Unicode-Literate-Output)


Extra JavaScript Frontends
--------------------
CoffeeScript and Rapydscript are great languages to use to avoid the pains of writing JavaScript by hand.
They can be directly included in the markdown files, and will get compiled to javascript.

To use these frontends install them on your system, they will be used as subprocesses
to output the final javascript.
* [coffee script](https://github.com/rusthon/Rusthon/blob/master/examples/hello_coffee.md)
* [rapydscript](https://github.com/rusthon/Rusthon/blob/master/examples/hello_rapydscript.md)

JavaScript Regression Test Results
-----------------------------------
* [classes](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-class.md)
* [calling](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-calling.md)
* [dict](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-dict.md)
* [lang](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-lang.md)
* [list](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-list.md)
* [loop](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-loop.md)
* [set](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-set.md)
* [str](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-js-str.md)


C++/Rust/Go Backends
--------------------

The C++11 backend is the most mature of the native compiled backends.
All the backends are regression tested, and the tests results are here:

* [c++ regression test results](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-c%2B%2B.md)
* [go regression test results](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-go.md)
* [rust regression test results](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-rust.md)


C++ Backend Docs
-----------
note: this and other backends are still a work in progress.

* [typed backend extra syntax](https://github.com/rusthon/Rusthon/blob/master/doc/syntax.md)
* [vectors](https://github.com/rusthon/Rusthon/wiki/Lists-and-Arrays)
* [concurrency](https://github.com/rusthon/Rusthon/wiki/concurrency)
* [cpython integration](https://github.com/rusthon/Rusthon/wiki/CPython-Integration)
* [arrays and generics](https://github.com/rusthon/Rusthon/wiki/Array-Generics)
* [java frontend](https://github.com/rusthon/Rusthon/wiki/Java-Frontend)
* [memory and reference counting](https://github.com/rusthon/Rusthon/blob/master/doc/memory.md)
* [weak references](https://github.com/rusthon/Rusthon/wiki/Weak-References)
* [nim integration](https://github.com/rusthon/Rusthon/wiki/Nim-Integration)


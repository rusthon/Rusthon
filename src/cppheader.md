C++ Header
----------

notes: new in c++11: algorithm, functional, thread, and chrono.
includes typedefs for the standard types, like `f32`.

```python

CPP_HEADER = """
#include <cmath>
#include <memory>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <algorithm>
#include <functional>
#include <thread>
#include <chrono>

typedef long   i64;
typedef int    i32;
typedef double f64;
typedef float  f32;
typedef const char*  cstring;

template<class T>
std::shared_ptr<T> pointer(T* ob) {return std::make_shared<T>(ob);}

template<class T>
std::shared_ptr<T> pointer(T& ob) {return std::make_shared<T>(&ob);}

template<class T>
std::shared_ptr<T> pointer(std::shared_ptr<T> ob) {return ob;}


"""

```
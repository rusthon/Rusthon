C++ Header
----------

notes: new in c++11: algorithm, functional, thread, and chrono.
includes typedefs for the standard types, like `f32`.

```python

CPP_HEADER = """
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
std::shared_ptr<T> __shared__(T* ob) {return std::make_shared<T>(ob);}

template<class T>
std::shared_ptr<T> __shared__(T& ob) {return std::make_shared<T>(&ob);}

template<class T>
std::shared_ptr<T> __shared__(std::shared_ptr<T> ob) {return ob;}

std::shared_ptr<std::string> __shared__(std::string ob) {
	return std::make_shared<std::string>(ob);
}


template<class T>
T* __pointer__(T* ob) {return ob;}

template<class T>
T* __pointer__(T& ob) {return &ob;}

template<class T>
T* __pointer__(std::shared_ptr<T> ob) {return ob.get();}


"""

```
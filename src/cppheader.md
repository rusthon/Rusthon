C++ Header
----------

notes: new in c++11: algorithm, functional, thread, and chrono.
includes typedefs for the standard types, like `f32`.

note: OSX requires cmath, because std::pow and std::round is used in the builtins.

```python

CPP_HEADER = """
#include <memory>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <algorithm>
#include <functional>
#include <thread>
#include <chrono>
#include <cmath>

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

std::shared_ptr<std::runtime_error> __shared__(std::runtime_error ob) {
	return std::make_shared<std::runtime_error>(ob);
}


template<class T>
T* __pointer__(T* ob) {return ob;}

template<class T>
T* __pointer__(T& ob) {return &ob;}

template<class T>
T* __pointer__(T ob) {return &ob;}  // compiler optimizes away the copy?

std::string* __pointer__(std::string ob) {
	return &ob;
}

template<class T>
T* __pointer__(std::shared_ptr<T> ob) {return ob.get();}


"""

```
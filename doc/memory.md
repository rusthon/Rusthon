The Rust and C++ backends use reference counting for arrays, maps, and objects.
This limits you to non cyclic data structures.

An object `T` in C++ is `std::shared_ptr<T>`.
An array of objects is
```cpp
std::shared_ptr<
	std::vector<
		std::shared_ptr<T>
		>
	>
```

rusthon
----------
```python

class A:
	def __init__(self, id:int ):
		self.id = id

def test_pass_array( arr:[]int ):
	arr.append( 3 )

def test_pass_array_of_objects( arr:[]A, id:int ):
	a = A( id )
	arr.append( a )

def main():
	a = []int(x for x in range(3))
	TestError( len(a)==3 )
	TestError( a[0]==0 )
	TestError( a[1]==1 )
	TestError( a[2]==2 )
	test_pass_array( a )
	TestError( len(a)==4 )
	TestError( a[3]==3 )
	b = []A( A(x) for x in (1,2,3,4))
	TestError( len(b)==4 )
	test_pass_array_of_objects( b, 5 )
```

c++
------
```cpp
class A {
  public:
	int  id;
	void __init__(int id);
	A() {}
};
void A::__init__(int id) {
	this->id = id;
}

void test_pass_array(std::shared_ptr<std::vector<int>> arr) {
	arr->push_back(3);
}

void test_pass_array_of_objects(std::shared_ptr<std::vector< std::shared_ptr<A> >> arr, int id) {
	A  _ref_a = A{};_ref_a.__init__(id);
	std::shared_ptr<A> a = std::make_shared<A>(_ref_a);
	arr->push_back(a);
}

int main() {
	std::vector<int> _comp_a;
	for (int x=0; x<3; x++) {
		_comp_a.push_back(x);
	}
	auto a = std::make_shared<std::vector<int>>(_comp_a);
	TestError(std::string("./rust/list_comp.py"), 18, ( a->size() ) == 3, std::string(" len(a)==3 "));
	TestError(std::string("./rust/list_comp.py"), 19, ( (*a)[0] ) == 0, std::string(" a[0]==0 "));
	TestError(std::string("./rust/list_comp.py"), 20, ( (*a)[1] ) == 1, std::string(" a[1]==1 "));
	TestError(std::string("./rust/list_comp.py"), 21, ( (*a)[2] ) == 2, std::string(" a[2]==2 "));
	test_pass_array(a);
	TestError(std::string("./rust/list_comp.py"), 24, ( a->size() ) == 4, std::string(" len(a)==4 "));
	TestError(std::string("./rust/list_comp.py"), 25, ( (*a)[3] ) == 3, std::string(" a[3]==3 "));
	std::vector<std::shared_ptr<A>> _comp_b;
	for (auto &x: std::array<int, 4>{{1,2,3,4}}) {
		A  _ref__tmp_ = A{};_ref__tmp_.__init__(x);
		std::shared_ptr<A> _tmp_ = std::make_shared<A>(_ref__tmp_);
		_comp_b.push_back(_tmp_);
	}
	auto b = std::make_shared<std::vector< std::shared_ptr<A> >>(_comp_b);
	TestError(std::string("./rust/list_comp.py"), 34, ( b->size() ) == 4, std::string(" len(b)==4 "));
	test_pass_array_of_objects(b, 5);
	TestError(std::string("./rust/list_comp.py"), 36, ( b->size() ) == 5, std::string(" len(b)==5 "));
	return 0;
}

```

rust
------
```rust
struct A {
	__class__ : string,
	id : int,
}
impl A {
	fn __init__(&mut self, id:int) {
		self.id = id;
	}
	/*		constructor		*/
	fn new( id:int ) -> A {
		let mut __ref__ = A{__class__:"A",id:0};
		__ref__.__init__(id);
		return __ref__; 
	}
}

fn test_pass_array(  arr : Rc<RefCell<Vec<int>>> ) {
	arr.borrow_mut().push( 3 );
}

fn test_pass_array_of_objects(   arr : Rc<RefCell<Vec<Rc<RefCell<A>>>>>, id:int) {
	let a : Rc<RefCell<A>> = Rc::new(RefCell::new( A::new(id) ));
	arr.borrow_mut().push( a.clone() );
}

fn main() {
	let mut _comp_a : Vec<int> = Vec::new();
	for x in range(0u,3u) {
		_comp_a.push(x as int);
	}
	let a : Rc<RefCell< Vec<int> >> = Rc::new(RefCell::new(_comp_a));
	TestError("./rust/list_comp.py".to_string(), 18, ( a.borrow().len() ) == 3, " len(a)==3 ".to_string());
	TestError("./rust/list_comp.py".to_string(), 19, ( a.borrow_mut()[0] ) == 0, " a[0]==0 ".to_string());
	TestError("./rust/list_comp.py".to_string(), 20, ( a.borrow_mut()[1] ) == 1, " a[1]==1 ".to_string());
	TestError("./rust/list_comp.py".to_string(), 21, ( a.borrow_mut()[2] ) == 2, " a[2]==2 ".to_string());
	test_pass_array(a.clone());
	TestError("./rust/list_comp.py".to_string(), 24, ( a.borrow().len() ) == 4, " len(a)==4 ".to_string());
	TestError("./rust/list_comp.py".to_string(), 25, ( a.borrow_mut()[3] ) == 3, " a[3]==3 ".to_string());
	let mut _comp_b : Vec< Rc<RefCell<A>> > = Vec::new();
	for &x in vec!(1, 2, 3, 4).iter() {
		_comp_b.push(Rc::new(RefCell::new( A::new(x) )));
	}
	let b : Rc<RefCell< Vec<Rc<RefCell<A>>> >> = Rc::new(RefCell::new(_comp_b));
	TestError("./rust/list_comp.py".to_string(), 34, ( b.borrow().len() ) == 4, " len(b)==4 ".to_string());
	test_pass_array_of_objects(b.clone(), 5);
	TestError("./rust/list_comp.py".to_string(), 36, ( b.borrow().len() ) == 5, " len(b)==5 ".to_string());
}

```


TODO
----
  . weak ref syntax to break cycles
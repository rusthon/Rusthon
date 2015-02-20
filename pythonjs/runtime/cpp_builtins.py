# Cppthon builtins
# by Brett Hartshorn - copyright 2014
# License: "New BSD"


inline("""

typedef double f64;
typedef float  f32;

const char* cstr( std::string s ) { return s.c_str(); }

template<typename T, typename ...Args>
std::unique_ptr<T> _make_unique( Args&& ...args )
{
    return std::unique_ptr<T>( new T( std::forward<Args>(args)... ) );
}

double __double__(int a) { return (double)a; }

int sum(std::shared_ptr<std::vector<int>> arr) {
	int s = 0;
	std::for_each(arr->begin(),arr->end(),[&](int n){s += n;});
	return s;
}
double sumd(std::shared_ptr<std::vector<double>> arr) {
	double s = 0.0;
	std::for_each(arr->begin(),arr->end(),[&](double n){s += n;});
	return s;
}
float sumf(std::shared_ptr<std::vector<float>> arr) {
	float s = 0.0;
	std::for_each(arr->begin(),arr->end(),[&](float n){s += n;});
	return s;
}


std::string str( const std::string s ) {
	return s;
}
std::string str( int s ) {
	return std::to_string(s);
}

std::ofstream* __open__(const std::string name) {
	std::ofstream *f;
	f = new std::ofstream;
	f->open( name.c_str(), std::ofstream::in | std::ofstream::binary );
	return f;
}

// a pointer version is also required for `range` because it could be called inside
// a `with pointers:` block, in this special case return a copy and let the caller
// take the pointer.
std::vector<int> __range1__( int n ) {
	std::vector<int> vec(n);
	for (int i=0; i<n; i++) {
		vec[i] = i;
	}
	return vec;
}


std::shared_ptr<std::vector<int>> range1( int n ) {
	std::vector<int> vec(n);
	for (int i=0; i<n; i++) {
		vec[i] = i;
	}
	return std::make_shared<std::vector<int>>(vec);
}

std::shared_ptr<std::vector<int>> range2( int start, int end ) {
	std::vector<int> vec(end-start);
	int index = 0;
	for (int i=start; i<end; i++) {
		vec[index] = i;
		index ++;
	}
	return std::make_shared<std::vector<int>>(vec);
}

int ord( std::string s) {
	int r = (int)s.c_str()[0];
	return r;
}

double __float__( std::string s ) {
	return std::stod( s );
}

double round( double n, int places ) {
	auto p = std::pow(10, places);
	return std::round(n * p) / p;
}

std::string chr( int c ) {
	//return std::to_string( static_cast<char>(c) );  // as a oneliner it fails?
	auto s = static_cast<char>(c);
	return std::string( &s );
}

""")

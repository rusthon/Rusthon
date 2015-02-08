# Cppthon builtins
# by Brett Hartshorn - copyright 2014
# License: "New BSD"


inline("""

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

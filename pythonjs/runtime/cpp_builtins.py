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

std::ofstream& __open__(const std::string name) {
	std::ofstream f;
	f.open( name.c_str(), std::ofstream::in | std::ofstream::binary );
	return f;
}

""")

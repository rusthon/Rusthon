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


""")

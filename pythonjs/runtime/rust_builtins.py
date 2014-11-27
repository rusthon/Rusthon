# Rusthon builtins
# by Brett Hartshorn - copyright 2014
# License: "New BSD"


inline("""

/* Rusthon builtins */

type string = &'static str;
//type string = String;
type __type__int = Vec<int>;

//fn range1<'caller>( lifetime : &'caller int, x : int ) -> &'caller Vec<uint> {
fn range1( x : int ) -> Vec<int> {
	let mut arr: Vec<int> = Vec::with_capacity(x as uint);
	for i in range(0u, x as uint) {
		arr.push(i as int);
	}
	return arr;
}

/*
	this hack fails to overload the `+` operator on static strings: `&'static str`,
	https://github.com/rust-lang/rust/issues/13721
	error: cannot provide an extension implementation where both trait and type are not defined in this crate
	impl Add<string, string> for string {
		fn add(&self, other: &string) -> string {
			self.to_string() + other.to_string()
		}
	}
*/

""")

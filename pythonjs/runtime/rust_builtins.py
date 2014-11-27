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
	for i in range(0u, x as uint) { arr.push(i as int); }
	return arr;
}

fn range2( start:int, end:int ) -> Vec<int> {
	let mut arr: Vec<int> = Vec::with_capacity( (end-start) as uint);
	for i in range(start as uint, end as uint) { arr.push(i as int); }
	return arr;
}


""")

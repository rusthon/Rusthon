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

fn ord( s:String ) -> int {
	return s.into_bytes()[0] as int;
}

fn __float__( s:String ) -> f32 {
	return std::str::FromStr::from_str( s.as_slice() ).unwrap();
}

fn __int__( n:String ) -> int {
	return from_str::<int>( n.as_slice() ).unwrap();
}

fn round( n:f32, places:int ) -> f32 {
	let p = (10i).pow( places as uint ) as f32;
	return (n*p) / p;
}

""")

# Rusthon builtins
# by Brett Hartshorn - copyright 2014
# License: "New BSD"


inline("""

/* Rusthon builtins */

type string = &'static str;
//type string = String;
type __type__int = Vec<int>;

fn range1( x : int ) -> Vec<uint> {
	let mut arr = vec![];
	for i in range(0u, x as uint) {
		arr[i]=i;
	}
	return arr
}

""")

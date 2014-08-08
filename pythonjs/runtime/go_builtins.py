# PythonJS Go builtins
# by Brett Hartshorn - copyright 2014
# License: "New BSD"

import strconv

inline("""

func str(v interface{}) string {
	switch v.(type) {
		case nil:
			return "None"
		case int:
			i,_ := v.(int)
			return strconv.Itoa(i)
		case float64:
			return "TODO float"
		case bool:
			b,_ := v.(bool)
			if b { return "True"  
			} else { return "False" }
		case string:
			s,_ := v.(string)
			return s
		default:
			return "TODO unknown type"

	}
}
""")

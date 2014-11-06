# PythonJS Go builtins
# by Brett Hartshorn - copyright 2014
# License: "New BSD"

import strconv

inline("""

type __object__ struct {
	__class__ string
}

type object interface{
	getclassname() string
}

func (self __object__) getclassname() string {
	return self.__class__
}



func ord(x string) int {
	r := []rune(x)
	return int(r[0])
}

func __test_if_true__(v interface{}) bool {
	switch v.(type) {
		case nil:
			return false
		case int:
			i,_ := v.(int)
			return i != 0
		case float64:
			i,_ := v.(int)
			return i != 0.0
		case bool:
			b,_ := v.(bool)
			return b
		case string:
			s,_ := v.(string)
			return s != ""
		default:
			return false

	}
}

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

func range1( x int ) *[]int {
	arr := make([]int, x)
	for i := 0; i < x; i++ {
		arr[i]=i
	}
	return &arr
}

func range2( start int, stop int ) *[]int {
	arr := make([]int, stop-start)
	for i := start; i < stop; i++ {
		arr[i]=i
	}
	return &arr
}

func range3( start int, stop int, step int ) *[]int {
	arr := make([]int, stop-start)
	for i := start; i < stop; i+=step {
		arr[i]=i
	}
	return &arr
}


""")



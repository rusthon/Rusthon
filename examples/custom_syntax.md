Custom Types Json
------------------

Custom syntax for Unreal Engine4 configures the C++ output to use these types
for vectors, strings, and shared references.

@unrealtypes.json
```json
{
	"vector"   : {
		"template": "TArray<%s>",
		"append"  : "Emplace",
		"len"     : "Num"
	},
	"string" : {
		"type": "FString",
		"new" : "TEXT(%s)"
	},
	"shared": "TSharedRef<%s>"
}
```

The code below inside the `with syntax` block uses the custom template above.
Instead of the default `std::vector` the vectors below will be constructed as `TArray`
from the UnrealEngine C++ API.

```rusthon
#backend:c++


with syntax('unrealtypes.json'):
	class A:
		def __init__(self, x:int, y:string):
			self.x = x
			self.y = y

	def foo( s:string, ob:A ) ->A:
		print s
		return ob

	def main():
		v1 = []int(1,2,3,4,5,6)
		v2 = []string( "hello", "world" )
		v1.append( 100 )
		v2.append( "xxx" )

		a = A()
		foo( v2[0], a )

```
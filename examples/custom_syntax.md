
```rusthon
#backend:c++

UNREAL_SYNTAX = {
	'list'   : {
		'template':'TArray',
		'append'  : 'Emplace',
		'len'     : 'Num',
	},
	'string' : 'FString',
	'shared': 'TSharedRef',

}

with syntax as UNREAL_SYNTAX:
	def main():
		v1 = []int32(1,2,3,4,5,6)
		v2 = []string( "hello", "world" )
		v1.append( 100 )
		v2.append( "xxx" )

```
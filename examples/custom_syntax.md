
```rusthon
#backend:c++

UNREAL_SYNTAX = {
	'list'   : {
		'template':'TArray<%s>',
		'append'  : 'Emplace',
		'len'     : 'Num',
	},
	'string' : {
		'type': 'FString',
		'new' : 'TEXT("%s")'
	},
	'shared': 'TSharedRef<%s>',

}

with syntax as UNREAL_SYNTAX:
	def foo( s:string ):
		print s

	def main():
		v1 = []int32(1,2,3,4,5,6)
		v2 = []string( "hello", "world" )
		v1.append( 100 )
		v2.append( "xxx" )
		foo( v2[0] )

```
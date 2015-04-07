
@unrealtypes.json
```json
{
	"vector"   : {
		"template": "TArray<%s>",
		"append"  : "Emplace",
		"len"     : "Num",
		"pop"     : "Pop"
	},
	"string" : {
		"type": "FString",
		"new" : "TEXT(%s)",
		"len" : "Len"
	},
	"shared" : {
		"template" : "TSharedRef<%s>",
		"type"     : "TSharedRef",
		"reset"    : "Reset"
	},
	"map"    : {
		"template" : "TMap<%s, %s>"
	}
}
```

* [FModuleManager](https://docs.unrealengine.com/latest/INT/API/Runtime/Core/Modules/FModuleManager/index.html)
* [Fname](https://docs.unrealengine.com/latest/INT/API/Runtime/Core/UObject/FName/index.html)


@fname.json
```json
{
	"string" : {
		"type": "FName",
		"new" : "FName(%s)",
		"len" : "Len"
	}
}
```

@Source/TestPlugin/Public/ITestPlugin.h


```rusthon
#backend:c++
inline('#pragma once')

import ModuleManager.h

class ITestPlugin( IModuleIterface ):
	@classmethod
	def Get() -> "ITestPlugin&":
		print 'get plugin...'
		with T as "FModuleManager::LoadModuleChecked<ITestPlugin>":
			with syntax('fname.json'):
				return T( "TestPlugin" )

	@classmethod
	def IsAvailable() -> bool:
		print 'check plugin...'
		with syntax('fname.json'):
			return FModuleManager::Get().IsModuleLoaded( "TestPlugin" )


```


@Source/TestPlugin/Private/TestPluginPrivatePCH.h
```
import ITestPlugin.h
```


@Source/TestPlugin/Private/TestPlugin.cpp
```
import TestPluginPrivatePCH.h

class FTestPlugin( ITestPlugin ):
	def StartupModule():
		print 'plugin startup'
		a = hello_rusthon()
		print a
	def ShutdownModule():
		print 'plugin exit'

`IMPLEMENT_MODULE( FTestPlugin, TestPlugin )`

```




Static Library
--------------

@mymodule.cpp
```
#backend:c++


with syntax('unrealtypes.json'):
	def hello_rusthon() -> string:
		print 'hello world'
		return 'OK'

```
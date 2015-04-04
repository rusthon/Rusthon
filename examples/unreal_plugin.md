
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

@Source/TestPlugin/Public/ITestPlugin.h
```rusthon
#pragma once

import ModuleManager.h

class ITestPlugin( IModuleIterface ):
	@classmethod
	def Get() -> ITestPlugin:
		return `FModuleManager::LoadModuleChecked< ITestPlugin >( "TestPlugin" )`
	@classmethod
	def IsAvailable() -> bool:
		return `FModuleManager::Get().IsModuleLoaded( "TestPlugin" )`

```


@Source/TestPlugin/Private/TestPluginPrivatePCH.h
```rusthon
import ITestPlugin.h
```


@Source/TestPlugin/Private/TestPlugin.cpp
```rusthon
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


```rusthon
#backend:c++


with syntax('unrealtypes.json'):
	def hello_rusthon() -> string:
		print 'hello world'
		return 'OK'

```
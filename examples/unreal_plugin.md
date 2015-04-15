UnrealEngine4 Plugin
--------------------

If have never made a plugin for Unreal, first read these docs:
* https://docs.unrealengine.com/latest/INT/Engine/Basics/DirectoryStructure/index.html
* https://docs.unrealengine.com/latest/INT/Programming/Plugins/index.html

compile and install this plugin with the command below.
note that `MyProject` is a project you have already created in Unreal,
the plugin source will be written to the `Plugins` folder in your project.

`./rusthon.py ./examples/unreal_plugin.md --run=install-plugin.py --output-dir=~/Documents/Unreal\ Projects/MyProject/`

you may need to edit the line to point to where you installed UE4Editor

@install-plugin.py
```python
import os, subprocess, json
projects = []
for file in os.listdir('.'):
	if file.endswith('.uproject'):
		projects.append(file)

if len(projects)==1:
	file = projects[0]
	print file
	cfg = json.loads(open(file,'rb').read())
	installed = False
	for mod in cfg['Modules']:
		if mod['Name'] == 'TestPlugin':
			installed = True
			break
	if not installed and False:
		print('installing plugin...')
		cfg['Modules'].append(
			{
				'Type':'Runtime', 
				'Name':'TestPlugin', 
				'LoadingPhase':'Default'
			}
		)
		open(file, 'wb').write(
			json.dumps(cfg)
		)
	else:
		print 'TestPlugin already installed'

	exe = os.path.expanduser('~/UnrealEngine/Engine/Binaries/Linux/UE4Editor')
	print exe
	subprocess.check_call([exe, os.path.abspath(file)])

```

uplugin
--------

plugin config file

@Plugins/TestPlugin/TestPlugin.uplugin
```json
{
	"FileVersion" : 3,
	"FriendlyName" : "Test Example Plugin",
	"Version" : 1,
	"VersionName" : "1.0",
	"CreatedBy" : "Epic Games, Inc.",
	"CreatedByURL" : "http://epicgames.com",
	"EngineVersion" : "4.2.0",
	"Description" : "An example of a minimal plugin.  This can be used as a starting point when creating your own plugin.",
	"Category" : "Examples",
	"EnabledByDefault" : true,
	"Modules" :
	[
		{
			"Name" : "TestPlugin",
			"Type" : "Developer",
			"LoadingPhase" : "PreDefault"
		}
	]
}
```


Unreal Types Template
---------------------

https://github.com/rusthon/Rusthon/wiki/Custom-Type-Templates

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

Main Header
-----------
unreal pre compiled header

@Plugins/TestPlugin/Source/TestPlugin/Private/TestPluginPrivatePCH.h
```rusthon
#backend:c++
#import ITestPlugin.h
from runtime import *

```

Public ITestPlugin.h
--------------------

Below `with T as "FModuleManager::LoadModuleChecked<ITestPlugin>"` defines a macro,
for more info see:
https://github.com/rusthon/Rusthon/wiki/Macro-Functions

@Plugins/TestPlugin/Source/TestPlugin/Public/ITestPlugin.h
```rusthon
#backend:c++
pragma('once')

import ModuleManager.h
with pointers:
	class ITestPlugin( IModuleInterface ):
		@classmethod
		def Get() -> ITestPlugin&:
			with T as "FModuleManager::LoadModuleChecked<ITestPlugin>":
				with syntax('fname.json'):
					return T( "TestPlugin" )

		@classmethod
		def IsAvailable() -> bool:
			with syntax('fname.json'):
				return FModuleManager::Get().IsModuleLoaded( "TestPlugin" )


```

Plugin Main
------------


@Plugins/TestPlugin/Source/TestPlugin/Private/TestPlugin.cpp
```rusthon
import TestPluginPrivatePCH.h
import ITestPlugin.h

class FTestPlugin( ITestPlugin ):
	@virtualoverride
	def StartupModule():
		print 'myplugin startup'
		#a = hello_rusthon()
		#print a

	@virtualoverride
	def ShutdownModule():
		print 'myplugin exit'

macro("IMPLEMENT_MODULE( FTestPlugin, TestPlugin )")


```


Shared Library
--------------


@3rdparty/mymodule
```rusthon
#backend:c++ dynamiclib

def hello_rusthon() -> int:
	print 'hello world'
	return 99

```

Unreal Build File
-----------------
Copyright 1998-2015 Epic Games, Inc. All Rights Reserved.

@Plugins/TestPlugin/Source/TestPlugin/TestPlugin.Build.cs
```c#
using UnrealBuildTool;
using System.IO;
 
public class TestPlugin : ModuleRules {
	public TestPlugin(TargetInfo Target) {
		PrivateIncludePaths.AddRange(new string[] { "TestPlugin/Private" });
		PublicIncludePaths.AddRange(new string[] { "TestPlugin/Public", "/usr/include/c++/4.9.2/" });
		PublicDependencyModuleNames.AddRange(new string[] { "Engine", "Core" });
	}
}
```

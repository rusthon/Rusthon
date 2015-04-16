UnrealEngine4 Plugin
--------------------

If you have never made a plugin for Unreal, first read these docs:
* [directory structure](https://docs.unrealengine.com/latest/INT/Engine/Basics/DirectoryStructure/index.html)
* [plugin basics](https://docs.unrealengine.com/latest/INT/Programming/Plugins/index.html)

The Unreal build system requires you name your header, source and classes correctly, using the Public/Private folders, 
and using the special PCH header file that imports everything.  
Having to keep in sync folder names, source files, and class names is a pain in the ass.
In the following example plugin, you can simply use "text-replace" on `TestPlugin` to `YourPlugin` in a text editor
to rename everything at once.


Testing
-------

To compile and install this plugin with the command below, the paths are hard coded for Linux,
and if you are using Fedora, you may need my fork of Unreal Editor to get the plugin to compile,
get it [here](https://github.com/rusthon/UnrealEngine).

note that `MyProject` is a project you have already created in Unreal Editor,
the plugin source will be written to the `Plugins` folder in your project.

`./rusthon.py ./examples/unreal_plugin.md --run=install-plugin.py --output-dir=~/Documents/Unreal\ Projects/MyProject/`


Installer Script
----------------

If your plugin requires building external libraries, you could add it here.
note: this script is triggered after compile by `--run=install-plugin.py` above.

TODO fix, how come this is not forcing Unreal to fully rebuild the plugin?


@install-plugin.py
```python
import os, subprocess, json

os.environ['LD_LIBRARY_PATH'] = os.path.abspath('./3rdparty')

UNREAL = os.path.expanduser('~/UnrealEngine/Engine/Binaries/Linux/UE4Editor')
UNREAL_BUILD = './Plugins/TestPlugin/Binaries/Linux/libUE4Editor-TestPlugin.so'

if os.path.isfile(UNREAL_BUILD):
	print('<test plugin installer - removing previous build>')
	os.unlink(UNREAL_BUILD)
	print('<unreal will rebuild plugin...>')

projects = []
for file in os.listdir('.'):
	if file.endswith('.uproject'):
		projects.append(file)

if len(projects)==1:
	subprocess.check_call([UNREAL, os.path.abspath(projects[0])])
else:
	print '<error loading your .uproject file, the output folder may not be an Unreal project>'

```

uplugin
--------

The Unreal build tool searches for `.uplugin` files in the project folder under `Plugins`.

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

This JSON file is used below to configure the transpiler to work transparently with Unreal standard types.

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
The Unreal build tool requires this pre-compiled header (PCH), it is a single header that includes any imports you need.
Here the Rusthon runtime and helper functions are imported with `from runtime import *`.
note: Rusthon will not include the runtime when you have defined an output file name ending with `.h` or `.cpp`,
that is why the runtime is imported here and gets automatically included in the rest of your plugin code by the Unreal build system.


@Plugins/TestPlugin/Source/TestPlugin/Private/TestPluginPrivatePCH.h
```rusthon
#backend:c++
from runtime import *
```

Public ITestPlugin.h
--------------------

`ITestPlugin` subclasses from IModuleInterface, see the Unreal docs on [FModuleManager](https://docs.unrealengine.com/latest/INT/API/Runtime/Core/Modules/FModuleManager/index.html)


note that syntax `with T as "X<Y>"` defines a mini-macro, for more info on macros see:
https://github.com/rusthon/Rusthon/wiki/Macro-Functions


@Plugins/TestPlugin/Source/TestPlugin/Public/ITestPlugin.h
```rusthon
#backend:c++
#pragma('once')
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
Main plugin code is here, this is a good place to write your GUI code using [Slate](https://docs.unrealengine.com/latest/INT/Programming/Slate/Overview/index.html)

This example calls an external function from a dynamic library created below, broken,
TODO fix calling shared libraries, for some reason calling `hello_rusthon()` segfaults at runtime.
`undefined symbol: hello_rusthon`


@Plugins/TestPlugin/Source/TestPlugin/Private/TestPlugin.cpp
```rusthon
import ITestPlugin.h

@extern
def hello_rusthon() -> int:
	pass

class FTestPlugin( ITestPlugin ):
	@virtualoverride
	def StartupModule():
		print 'HELLO MYPLUGIN'
		a = hello_rusthon()
		print a  ## should print 99
		print 'GOING TO QUIT UNREAL NOW'
		with Q as 'GetWorld()->Exec(GetWorld(), TEXT("%s"))':
			Q("quit")

	@virtualoverride
	def ShutdownModule():
		print 'MYPLUGIN EXIT'

macro("IMPLEMENT_MODULE( FTestPlugin, TestPlugin )")


```


Unreal Build File
-----------------

The Unreal C# build script.  If your not using Linux, change `libmymodule.so` below.


@Plugins/TestPlugin/Source/TestPlugin/TestPlugin.Build.cs
```c#
using UnrealBuildTool;
using System.IO;
 
public class TestPlugin : ModuleRules {
	public TestPlugin(TargetInfo Target) {
		PrivateIncludePaths.AddRange(new string[] { "TestPlugin/Private" });
		PublicIncludePaths.AddRange(new string[] { "TestPlugin/Public" });
		PublicDependencyModuleNames.AddRange(new string[] { "Engine", "Core" });

		var base_path = Path.GetFullPath(
			Path.Combine(
				Path.GetDirectoryName(
					RulesCompiler.GetModuleFilename(
						this.GetType().Name)), "../../../../3rdparty")
		);
		if (!Directory.Exists(base_path)) {
			Log.TraceError("can not find 3rdparty build folder");
			Log.TraceError(base_path);
		}
		PublicLibraryPaths.Add( base_path );
		PublicIncludePaths.Add( base_path );
		var path = Path.Combine(base_path, "libmymodule.so");
		PublicAdditionalLibraries.Add(path); // TODO FIXME
	}
}
```


Shared Library
--------------
Below the extra directive to the c++ backend `dynamiclib` will trigger Rusthon to use g++ to compile a shared library (.so) file,
this gets packged in the output tar, and saved to the output folder.  
The C# build script above includes this compiled library `libmymodule.so` so that it can be loaded when Unreal is run.


@3rdparty/libmymodule
```rusthon
#backend:c++ dynamiclib

def hello_rusthon() -> int:
	print 'hello world'
	return 99

```
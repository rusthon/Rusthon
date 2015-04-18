UnrealEngine4 CPython Plugin
--------------------

This example compiles a dynamic library that links in libpython2.7.so,
using Rusthon to make the glue code, you can run regular Python scripts,
and feed the data back into Unreal Engine.

For more info on getting started making Unreal plugins using Rusthon, see this example first:
https://github.com/rusthon/Rusthon/blob/master/examples/unreal_plugin.md

For more info on using CPython and embedding Python scripts inside Rusthon, see this example:
https://github.com/rusthon/Rusthon/blob/master/examples/cpython_embed.md


Testing
-------

To compile and install this plugin with the command below, the paths are hard coded for Linux,
and if you are using Fedora, you may need my fork of Unreal Editor to get the plugin to compile,
get it [here](https://github.com/rusthon/UnrealEngine).

note that `MyProject` is a project you have already created in Unreal Editor,
the plugin source will be written to the `Plugins` folder in your project.

`./rusthon.py ./examples/unreal_cpython.md --run=install-plugin.py --output-dir=~/Documents/Unreal\ Projects/MyProject/`


Installer Script
----------------


@install-plugin.py
```python
import os, subprocess, json

os.environ['LD_LIBRARY_PATH'] = os.path.abspath('./3rdparty')

UNREAL = os.path.expanduser('~/UnrealEngine/Engine/Binaries/Linux/UE4Editor')
UNREAL_BUILD = './Plugins/TestPlugin/Binaries/Linux/libUE4Editor-TestPlugin.so'
UNREAL_CACHE_DIR  = 'Intermediate/Build/Linux/x86_64-unknown-linux-gnu'
UNREAL_CACHE_FILE = UNREAL_CACHE_DIR +'/%s/Development/Plugins/Dynamic/TestPlugin/TestPlugin.cpp.o'

if os.path.isfile(UNREAL_BUILD):
	print('<test plugin installer - removing previous build>')
	os.unlink(UNREAL_BUILD)
if os.path.isdir(UNREAL_CACHE_DIR):
	for name in os.listdir(UNREAL_CACHE_DIR):
		cachepath = os.path.join(UNREAL_CACHE_DIR,name)
		if name.endswith('Editor') and os.path.isdir(cachepath):
			if os.path.isfile(UNREAL_CACHE_FILE % name):
				print('<test plugin installer - removing previous build cache>')
				os.unlink(UNREAL_CACHE_FILE % name)


projects = []
for file in os.listdir('.'):
	if file.endswith('.uproject'):
		projects.append(file)

if len(projects)==1:
	cmd = [UNREAL, os.path.abspath(projects[0])]
	print cmd
	subprocess.check_call(cmd)
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
This example calls an external function `hello_rusthon` from a dynamic library created below.


@Plugins/TestPlugin/Source/TestPlugin/Private/TestPlugin.cpp
```rusthon
import TestPluginPrivatePCH.h
import ITestPlugin.h

@extern
def hello_rusthon() -> int:
	pass

class FTestPlugin( ITestPlugin ):
	@virtualoverride
	def StartupModule():
		print 'HELLO MYPLUGIN XXXXX'
		a = hello_rusthon()
		print a  ## should print 100
		print 'GOING TO QUIT UNREAL NOW'
		## it takes too long for Unreal to start, so we just kill it here
		raise std::exception()

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

CPython Script
--------------

This is the embedded CPython script that is run when `cpython.initalize()` is called.
Funtions and classes defined here can be called by Rusthon C++ translated code.

@embed
```python

class A():
	def __init__(self):
		self.value = 100
	def pymethod(self):
		return self.value

```


Shared Library
--------------
This dynamiclib is linked to libpython2.7, below `cpython.initalize()` creates the global GIL state.
Inside `with gil:` CPython PyObjects can be used, `->` is syntatic sugar for using the CPython CAPI,
for more info see the [wiki page](https://github.com/rusthon/Rusthon/wiki/CPython-Integration)

notes:
* the extra directive to c++ backend `dynamiclib` this makes Rusthon compile a shared library (.so) file.
* C# build script above includes this compiled library `libmymodule.so` so that it can be loaded when Unreal is run.


* @link:python2.7
* @include:/usr/include/python2.7
@3rdparty/libmymodule
```rusthon
#backend:c++ dynamiclib
import cpython


def hello_rusthon() -> int:
	print 'initalize CPython'
	state = cpython.initalize()
	result = 0
	with gil:
		a = cpython.A()
		print 'addr of a:', a
		print a->value as int
		result = a->pymethod() as int
	return result

```
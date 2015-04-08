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
			"Type" : "Developer"
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

class ITestPlugin( IModuleIterface ):
	@classmethod
	def Get() -> ITestPlugin&:
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


@Plugins/TestPlugin/Source/TestPlugin/Private/TestPluginPrivatePCH.h
```rusthon
import ITestPlugin.h
```


@Plugins/TestPlugin/Source/TestPlugin/Private/TestPlugin.cpp
```rusthon
import TestPluginPrivatePCH.h

class FTestPlugin( ITestPlugin ):
	@classmethod
	def StartupModule():
		print 'myplugin startup'
		#a = hello_rusthon()
		#print a
	@classmethod
	def ShutdownModule():
		print 'myplugin exit'

macro("IMPLEMENT_MODULE( FTestPlugin, TestPlugin )")


```


Static Library
--------------
TODO link this with the build script.

@3rdparty/mymodule.cpp
```rusthon
#backend:c++

with syntax('unrealtypes.json'):
	def hello_rusthon() -> string:
		print 'hello world'
		return 'OK'

```

Unreal Build File
-----------------
Copyright 1998-2015 Epic Games, Inc. All Rights Reserved.

@Plugins/TestPlugin/Source/TestPlugin/TestPlugin.Build.cs
```c#

using System;
using System.IO;
using System.Text.RegularExpressions;

namespace UnrealBuildTool.Rules
{
	public class TestPlugin : ModuleRules
	{
		public TestPlugin(TargetInfo target)
		{
			/** Setup an external C++ module */
			//LoadLibrary(target, "3rdparty", "3rdparty", "mymodule");
			/** Setup files in this plugin locally */
			SetupLocal(target);
		}


		/** Setup an external Rust module */
		private void SetupLibExtern(TargetInfo target) {
		}

		/** Perform all the normal module setup for plugin local c++ files. */
		private void SetupLocal(TargetInfo target) {
			PublicIncludePaths.AddRange(new string[] {"Developer/TestPlugin/Public" });
			PrivateIncludePaths.AddRange(new string[] {"Developer/TestPlugin/Private" });
			PublicDependencyModuleNames.AddRange(new string[] {"Core"});
			PrivateDependencyModuleNames.AddRange(new string[] {});
			DynamicallyLoadedModuleNames.AddRange(new string[] {});
		}

		/**
		 * Helper to setup an arbitrary library in the given library folder
		 * @param include_path Relative include path, eg. 3rdparty/mylib/include
		 * @param build_path Relative build path, eg. 3rdparty/mylib/build
		 * @param library_name Short library name, eg. mylib. Automatically expands to libmylib.a, mylib.lib, etc.
		 */
		private void LoadLibrary(TargetInfo target, string include_path, string build_path, string library_name) {

			// Add the include path
			var full_include_path = Path.Combine(PluginPath, include_path);
			if (!Directory.Exists(full_include_path)) {
				Fail("Invalid include path: " + full_include_path);
			}
			else {
				PublicIncludePaths.Add(full_include_path);
				Trace("Added include path: {0}", full_include_path);
			}

			// Get the build path
			var full_build_path = Path.Combine(PluginPath, build_path);
			if (!Directory.Exists(full_build_path)) {
				Fail("Invalid build path: " + full_build_path + " (Did you build the 3rdparty module already?)");
			}

			// Look at all the files in the build path; we need to smartly locate
			// the static library based on the current platform. For dynamic libraries
			// this is more difficult, but for static libraries, it's just .lib or .a
			string [] fileEntries = Directory.GetFiles(full_build_path);
			var pattern = ".*" + library_name + ".*\\.";
			if ((target.Platform == UnrealTargetPlatform.Win64) || (target.Platform == UnrealTargetPlatform.Win32)) {
				pattern += "lib";
			}
			else {
				pattern += "a";
			}
			Regex r = new Regex(pattern, RegexOptions.IgnoreCase);
			string full_library_path = null;
			foreach (var file in fileEntries) {
				if (r.Match(file).Success) {
					full_library_path = Path.Combine(full_build_path, file);
					break;
				}
			}
			if (full_library_path == null) {
				Fail("Unable to locate any build libraries in: " + full_build_path);
			}

			// Found a library; add it to the dependencies list
			PublicAdditionalLibraries.Add(full_library_path);
			Trace("Added static library: {0}", full_library_path);
		}

		/**
		 * Print out a build message
		 * Why error? Well, the UE masks all other errors. *shrug*
		 */
		private void Trace(string msg) {
			Log.TraceError(Plugin + ": " + msg);
		}

		/** Trace helper */
		private void Trace(string format, params object[] args) {
			Trace(string.Format(format, args));
		}

		/** Raise an error */
		private void Fail(string message) {
			Trace(message);
			throw new Exception(message);
		}

		/** Get the absolute root to the plugin folder */
		private string PluginPath {
			get {
				return Path.GetFullPath(Path.Combine(Path.GetDirectoryName(RulesCompiler.GetModuleFilename(this.GetType().Name)), "../.."));
			}
		}

		/** Get the name of this plugin's folder */
		private string Plugin {
			get {
				return new DirectoryInfo(PluginPath).Name;
			}
		}
	}
}
```

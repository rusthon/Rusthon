# PythonJS Low Level Runtime
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

__NULL_OBJECT__ = Object.create( null )
__WEBWORKER__ = False
__NODEJS__ = False
__BROWSER__ = False

## note browser and nodejs can both be true in the case of NodeWebkit
if typeof(process) != 'undefined':  ## TODO check if this is true inside a nodejs webworker
	__NODEJS__ = True
if typeof(window) != 'undefined':
	__BROWSER__ = True
if typeof(importScripts) == 'function':
	__WEBWORKER__ = True

if not __NODEJS__ and not __WEBWORKER__:
	if typeof(HTMLDocument) == 'undefined':  ## fix for older IE
		HTMLDocument = Document

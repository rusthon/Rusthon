JavaScript Backend - Static Types
-------

Type errors most often happen when interfacing with external libraries, not the code you have written yourself.
This example using Three.js shows you how to type arguments as class types from external javascript libraries.


To run this example, run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/threejs_static_types.md
```

Example
--------

In the function below `setup_camera`, the argument `c` is typed as `THREE.PerspectiveCamera`, if the function is called with `undefined`
it will throw and error with this message:
```
Uncaught TypeError: in function `setup_camera`, 
argument `c` must be of type `THREE.PerspectiveCamera`,
instead got->undefined
```
This error message makes it easy for you to understand what went wrong in the function.

The untyped version of the same function `setup_camera_untyped`, called with `undefined`, 
prints an error message which offers little help in fixing the problem.
```
Uncaught TypeError: Cannot read property `position` of undefined
```
By default, above is all you get from the javascript debug console in Chrome,
the variable name and function the error happened in is not printed!
To find out the variable and function name you have to click on the error, 
and it will take you to that line number in the source code, wasting your time.


@myscript
```rusthon
#backend:javascript
from runtime import *

Meshes = []
ren = None
scn = None
cam = None

def add_mesh( scn:THREE.Scene, mesh:THREE.Mesh ):
	scn.add( mesh )
	Meshes.append( mesh )

def setup_camera( c:THREE.PerspectiveCamera ):
	c.position.z = 60
	c.position.x = 5

def setup_camera_untyped( c ):
	c.position.z = 60
	c.position.x = 5


def main():
	global ren, scn, cam

	div = document.createElement( 'div' )
	document.body.appendChild(div)
	print(div)

	width = 640; height = 320
	scn = new( THREE.Scene() )
	print(scn)
	cam = new( THREE.PerspectiveCamera( 45, width/height, 0.01, 10000) )
	setup_camera( cam )

	## throws a readable error message
	#setup_camera( undefined )

	## throws a confusing error message
	#setup_camera_untyped( undefined )

	ren = new( THREE.WebGLRenderer() )
	print(ren)
	ren.setSize( width, height )

	div.appendChild( ren.domElement )

	light = new( THREE.PointLight() )
	light.position.set( 0, 100, 90 )
	scn.add( light )
	print(light)

	radius = 4; segments = 32
	geo = new( THREE.CircleGeometry( radius, segments ) )
	mat = new( THREE.MeshBasicMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = -30

	add_mesh( scn, mesh )

	## this fails properly and is caught
	try:
		add_mesh( scn, 1 )
	except TypeError:
		print 'caught TypeError OK'

	radiusTop=3; radiusBottom=6; height=10
	geo = new( THREE.CylinderGeometry( radiusTop, radiusBottom, height ) )
	mat = new( THREE.MeshPhongMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = -15
	add_mesh( scn, mesh )

	radius=4.0; detail=1
	geo = new( THREE.IcosahedronGeometry( radius, detail ) )
	mat = new( THREE.MeshPhongMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = 0
	add_mesh( scn, mesh )

	geo = new( THREE.OctahedronGeometry( radius, detail ) )
	mat = new( THREE.MeshPhongMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = 15
	add_mesh( scn, mesh )

	print('OK')
	animate()

def animate():
	requestAnimationFrame( animate )
	for m in Meshes:
		m.rotation.x = m.rotation.x + 0.01
		m.rotation.y = m.rotation.y + 0.02
		x = m.quaternion.x
		y = m.quaternion.y
		z = m.quaternion.z
		m.material.color.setRGB( x,y,z )

	ren.render( scn, cam )

main()

```


html
--------

```html
<html>
<head>
<script src="~/three.js/build/three.min.js"></script>

</head>
<body>
<@myscript>
</body>
</html>
```
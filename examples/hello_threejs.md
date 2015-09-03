html
----
To run this example run these commands in your shell:
```
cd
git clone https://github.com/mrdoob/three.js.git
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/hello_threejs.md
```
This will compile, and then open a web-browser, clicking "click me" will start the threejs scene, and you should see some 3D objects rotating.

Rusthon allows you to assemble html files, inserting static javascripts, and output from Rusthon using the javascript backend.
The example below inserts the pythonjs runtime `from runtime import *` and the THREE.js library `three.min.js` into the output html file.
This is triggered by using `~/` at the start of the path in the `src` attribute of the script tag.  The path is relative to your home directory.

```html
<html>
<head>
<script src="~/three.js/build/three.min.js" git="https://github.com/mrdoob/three.js.git"></script>
<@myscript>

</head>
<body>
<button onclick="main()">click me</button>
</body>
</html>
```
Above a special syntax is used `<@myscript>` this tells Rusthon where to insert the output of scripts it translates using the javascript backend.

rusthon
-------
Below `@myscript` is given on the line just before the fenced rusthon code block.  This allows you to insert multiple scripts into your html, in the head or body.

@myscript
```rusthon
#backend:javascript
from runtime import *

Meshes = []
ren = None
scn = None
cam = None

def main():
	global ren, scn, cam

	div = document.createElement( 'div' )
	document.body.appendChild(div)
	print(div)

	width = 640; height = 320
	scn = new( THREE.Scene() )
	print(scn)
	cam = new( THREE.PerspectiveCamera( 45, width/height, 0.01, 10000) )
	print(cam)
	cam.position.z = 60
	cam.position.x = 5

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
	scn.add( mesh )
	Meshes.append( mesh )

	radiusTop=3; radiusBottom=6; height=10
	geo = new( THREE.CylinderGeometry( radiusTop, radiusBottom, height ) )
	mat = new( THREE.MeshPhongMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = -15
	scn.add( mesh )
	Meshes.append( mesh )

	radius=4.0; detail=1
	geo = new( THREE.IcosahedronGeometry( radius, detail ) )
	mat = new( THREE.MeshPhongMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = 0
	scn.add( mesh )
	Meshes.append( mesh )

	geo = new( THREE.OctahedronGeometry( radius, detail ) )
	mat = new( THREE.MeshPhongMaterial() )
	mesh = new( THREE.Mesh( geo, mat ) )
	mesh.position.x = 15
	scn.add( mesh )
	Meshes.append( mesh )

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
```

JavaScript Backend - Static Types
-------

To run this example, run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/threejs_static_types.md
```


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

Example
--------

The function below `add_mesh` has its arguments typed with two external types from THREE.js: `THREE.Scene` and `THREE.Mesh`


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
Catmull Clark Subdivision Surface
---------------------------------

* https://github.com/mrdoob/three.js/archive/r66.tar.gz
* http://www.rorydriscoll.com/2008/08/01/catmull-clark-subdivision-the-basics/

Extract r66.tar.gz to your home directory, then run:
```
./rusthon.py ./examples/threejs_catmullclark.md
```

@myscript
```rusthon
#backend:javascript
from runtime import *

BaseGeom = None
ren = None
scn = None
cam = None

def avg( arr ):
	n = arr.length
	x = []; y = []; z = []
	for v in arr:
		x.push( v.x )
		y.push( v.y )
		z.push( v.z )
	return new THREE.Vector3( sum(x)/n, sum(y)/n, sum(z)/n )

def avg2( a, b ):
	x = a.x + b.x
	y = a.y + b.y
	z = a.z + b.z
	return new THREE.Vector3(x/2, y/2, z/2)

def avg4( a, b, c, d ):
	x = a.x + b.x + c.x + d.x
	y = a.y + b.y + c.y + d.y
	z = a.z + b.z + c.z + d.z
	return new THREE.Vector3(x/4, y/4, z/4)

class CatmullClark:
	def id(self, a,b):
		v1 = Math.min(a,b)
		v2 = Math.max(a,b)
		return v1+':'+v2

	def __init__(self, geo, parent=None, replace=None, wire=False, wiresize=4, color=0x00ff00):
		self.input_geom = geo
		geo.computeCentroids()  ## requires three.js R66

		# Q is the average of the surrounding face points
		q = [ [] for i in range(geo.vertices.length) ]

		# R is the average of the surrounding edge midpoints
		r = [ [] for i in range(geo.vertices.length) ]

		self.edge_faces = edge_faces = {}
		for face in geo.faces:
			id1 = self.id(face.a, face.b)
			id2 = self.id(face.b, face.c)
			id3 = self.id(face.c, face.a)
			if id1 not in edge_faces:
				edge_faces[id1] = []
			if id2 not in edge_faces:
				edge_faces[id2] = []
			if id3 not in edge_faces:
				edge_faces[id3] = []

			edge_faces[id1].append( face )
			edge_faces[id2].append( face )
			edge_faces[id3].append( face )

			mid = avg2( geo.vertices[face.a], geo.vertices[face.b] )
			r[ face.a ].push( mid )
			r[ face.b ].push( mid )

			mid = avg2( geo.vertices[face.b], geo.vertices[face.c] )
			r[ face.b ].push( mid )
			r[ face.c ].push( mid )

			mid = avg2( geo.vertices[face.c], geo.vertices[face.a] )
			r[ face.c ].push( mid )
			r[ face.a ].push( mid )

			q[ face.a ].push( face.centroid )
			q[ face.b ].push( face.centroid )
			q[ face.c ].push( face.centroid )


		# 0.5  from the surrounding edge midpoints `R`, 
		R = []
		for a in r:
			R.push( avg(a).multiplyScalar(0.5) )

		# 0.25 weight from the average of surrounding face-points `Q`, 
		Q = []
		for u in q:
			Q.push( avg(u).multiplyScalar(0.25) )

		fgeo = new THREE.Geometry()
		egeo = new THREE.Geometry()
		rgeo = new THREE.Geometry()

		sgeo = new THREE.Geometry()

		edgeverts = []
		i = 0
		for face in geo.faces:
			id = self.id(face.a, face.b); edge = edge_faces[id]
			e1 = avg4( geo.vertices[face.a], geo.vertices[face.b], edge[0].centroid, edge[1].centroid )

			id = self.id(face.b,face.c); edge = edge_faces[id]
			e2 = avg4( geo.vertices[face.b], geo.vertices[face.c], edge[0].centroid, edge[1].centroid )

			id = self.id(face.c, face.a); edge = edge_faces[id]
			e3 = avg4( geo.vertices[face.c], geo.vertices[face.a], edge[0].centroid, edge[1].centroid )

			egeo.vertices.append(e1)
			egeo.vertices.append(e2)
			egeo.vertices.append(e3)

			fgeo.vertices.append( face.centroid )

			sgeo.vertices.append(e1)
			sgeo.vertices.append(e2)
			sgeo.vertices.append(e3)
			sgeo.faces.push( new THREE.Face3(i,i+1,i+2) )


			# 0.25 from the original control-point.

			vpoint = R[face.a].clone().add( Q[face.a] ).clone().add( geo.vertices[face.a].clone().multiplyScalar(0.25) )
			sgeo.vertices.push( vpoint )
			rgeo.vertices.push( vpoint )

			vpoint = R[face.b].clone().add( Q[face.b] ).clone().add( geo.vertices[face.b].clone().multiplyScalar(0.25) )
			sgeo.vertices.push( vpoint )
			rgeo.vertices.push( vpoint )

			vpoint = R[face.c].clone().add( Q[face.c] ).clone().add( geo.vertices[face.c].clone().multiplyScalar(0.25) )
			sgeo.vertices.push( vpoint )
			rgeo.vertices.push( vpoint )

			sgeo.faces.push( new THREE.Face3(i+3,i,i+2) )
			sgeo.faces.push( new THREE.Face3(i+4,i+1,i) )
			sgeo.faces.push( new THREE.Face3(i+5,i+2,i+1) )

			i += 6


		pmat = new THREE.ParticleSystemMaterial( size=0.2, color=0x0000ff )
		p = new THREE.ParticleSystem( egeo, pmat )
		self._p1 = p
		if parent:
			parent.add( p )

		pmat = new THREE.ParticleSystemMaterial( size=0.3, color=0xffff00 )
		p = new THREE.ParticleSystem( rgeo, pmat )
		self._p2 = p
		if parent:
			parent.add( p )

		pmat = new THREE.ParticleSystemMaterial( size=0.4, color=0xff0000 )
		p = new THREE.ParticleSystem( fgeo, pmat )
		self._p2 = p
		if parent:
			parent.add( p )

		sgeo.mergeVertices()
		#sgeo.computeCentroids();
		sgeo.computeFaceNormals();
		sgeo.computeVertexNormals()
		mat = new THREE.MeshLambertMaterial( color=color, wireframe=wire, wireframeLinewidth=wiresize )
		self.mesh = new THREE.Mesh( sgeo, mat )

		if parent:
			parent.add( self.mesh )

		self.output_geom = sgeo
		self.mesh = mesh
		self.parent = parent

		if replace:
			replace.geometry.vertices = sgeo.vertices
			replace.geometry.verticesNeedUpdate = True

	def remove(self):
		self.parent.remove(self._p1)
		self.parent.remove(self._p2)
		self.parent.remove(self._p2)
		self.parent.remove(self.mesh)



def main():
	global ren, scn, cam, mesh, controls, stats
	global BaseGeom
	global WireMesh

	stats = new Stats()
	stats.domElement.style.position = 'absolute'
	stats.domElement.style.left = '0px'
	stats.domElement.style.top = '60px'
	document.body.appendChild(stats.domElement)

	div = document.createElement( 'div' )
	document.body.appendChild(div)

	width = window.innerWidth-20; height = window.innerHeight-20
	scn = new( THREE.Scene() )
	cam = new( THREE.PerspectiveCamera( 45, width/height, 0.01, 10000) )
	cam.position.z = 60
	cam.position.x = 5
	controls = new THREE.TrackballControls( cam )

	ren = new( THREE.WebGLRenderer(antialias=True) )
	ren.setSize( width, height )

	div.appendChild( ren.domElement )

	light = new( THREE.PointLight(0xffffff, 2, 500) )
	light.position.set( 0, 100, 90 )
	scn.add( light )

	BaseGeom = new THREE.BoxGeometry( 20,20,20 )
	mat = new THREE.MeshBasicMaterial( wireframe=True )
	mesh = new THREE.Mesh( BaseGeom, mat )
	scn.add( mesh )
	WireMesh = mesh

	animate()

SS1 = SS2 = None
def update_subdivs():
	global SS1, SS2

	WireMesh.geometry.verticesNeedUpdate = True
	for v in WireMesh.geometry.vertices:
		#print v
		r = (Math.random() - 0.5) * 0.3
		v.x += r
		v.y += r
		v.z += r

	children = [child for child in WireMesh.children]
	for child in children:
		WireMesh.remove(child)

	SS1 = CatmullClark( WireMesh.geometry, parent=WireMesh, wire=True )
	SS2 = CatmullClark( SS1.output_geom, parent=WireMesh, wire=True, wiresize=2, color=0x00ffff )
	SS3 = CatmullClark( SS2.output_geom, parent=WireMesh, wire=True, wiresize=1, color=0xff0000 )
	if document.getElementById('SS4').checked:
		SS4 = CatmullClark( SS3.output_geom, parent=WireMesh, wire=document.getElementById('WIRE').checked, wiresize=1, color=0x0000ff )


def animate():
	requestAnimationFrame( animate )
	stats.update()
	update_subdivs()
	controls.update()
	ren.render( scn, cam )

```

@mypage.html

```html
<html>
<head>
<script src="~/three.js-r66/build/three.min.js"></script>
<script src="~/three.js-r66/examples/js/controls/TrackballControls.js"></script>
<script src="~/three.js-r66/examples/js/libs/stats.min.js"></script>

<@myscript>

</head>
<body onload="main()">
<input id="SS4" type="checkbox" checked="true"/>
<input id="WIRE" type="checkbox" checked="true"/>
</body>
</html>
```
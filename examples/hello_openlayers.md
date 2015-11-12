OpenLayers Hello World
-----------------------
* https://github.com/openlayers/ol3
* http://openlayers.org/en/master/apidoc/


@index.html
```html
<html>
<head>

<link href='~/v3.11.0-dist/ol.css' rel='stylesheet' zip="https://github.com/openlayers/ol3/releases/download/v3.11.0/v3.11.0-dist.zip"/>

<script src="~/v3.11.0-dist/ol.js"></script>

<@myscript>
</head>
<body onload="main()">
<div id="MAPDIV"></div>
</body>
</html>
```

Script
---------------

@myscript
```rusthon
#backend:javascript
from runtime import *

@debugger
def main():
	london = ol.proj.fromLonLat([-0.12755, 51.507222])
	moscow = ol.proj.fromLonLat([37.6178, 55.7517])
	istanbul = ol.proj.fromLonLat([28.9744, 41.0128])
	rome = ol.proj.fromLonLat([12.5, 41.9])
	bern = ol.proj.fromLonLat([7.4458, 46.95])
	madrid = ol.proj.fromLonLat([-3.683333, 40.4])

	view = new ol.View(center=istanbul, zoom=6)

	layers = [
		new ol.layer.Tile(
			preload=4, 
			source = new ol.source.OSM()
		)
	]

	map = new ol.Map(
		view   = view,
		layers = layers,
		target = 'MAPDIV',
		controls = ol.control.defaults(attributionOptions={collapsible: false}),
		loadTilesWhileAnimating = True,
	)


```

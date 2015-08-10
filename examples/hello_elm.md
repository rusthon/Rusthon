Elm Language Frontend
---------------------

install elm transpiler: `sudo npm install --global elm`

why is this not working?
```
import Html
myfunc a =
  Html.text a

```

the elm transpiler gives up with:
```
Error when searching for modules imported by module 'Main':
    Could not find module 'Html'

Potential problems could be:
  * Misspelled the module name
  * Need to add a source directory or new dependency to elm-package.json

```

Simple Clock Example
--------------------

@myscript
```elm
import Color exposing (..)
import Graphics.Collage exposing (..)
import Graphics.Element exposing (..)
import Time exposing (..)


main =
  Signal.map clock (every second)



clock t =
  collage 400 400
    [ filled lightGrey (ngon 12 110)
    , outlined (solid grey) (ngon 12 110)
    , hand orange 100 t
    , hand charcoal 100 (t/60)
    , hand charcoal 60 (t/720)
    ]


hand clr len time =
  let
    angle = degrees (90 - 6 * inSeconds time)
  in
    segment (0,0) (fromPolar (len,angle))
      |> traced (solid clr)


```

javascript
-----------

@myjs
```javascript
var myapp = Elm.embed( Elm.Main, document.getElementById('CONTAINER'));
```

html
-------

http://elm-lang.org/guide/interop


@index.html
```html
<html>
<head>
</head>
<body>
<div id="CONTAINER"></div>
<@myscript>
<@myjs>
</body>
</html>
```
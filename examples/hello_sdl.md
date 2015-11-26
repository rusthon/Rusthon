SDL C++ Example
-------------
* git clone https://github.com/AMDmi3/libSDL2pp.git
* cd libSDL2pp
* cmake . && make && make install


* @include:/usr/include/SDL2pp

Build Options
-------------
* @link:SDL2pp
```rusthon
#backend:c++
import SDL2pp/SDL2pp.hh

namespace('SDL2pp')

def main():
	print 'init sdl'
	SDL( SDL_INIT_VIDEO )

	win = Window(
		"SDL2pp demo",
		SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
		640, 480,
		SDL_WINDOW_RESIZABLE
	)

```
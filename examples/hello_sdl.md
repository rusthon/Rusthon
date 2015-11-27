SDL C++ Example
-------------
* requires libSDL2pp
* libSDL2pp is downloaded from github, built and installed automatically.


libSDL2pp
----------
@https://github.com/AMDmi3/libSDL2pp.git
```bash
cmake .
make
sudo make install
```

Build Options
-------------
* @link:SDL2pp
```rusthon
#backend:c++
import SDL2pp/SDL2pp.hh
from time import sleep

namespace('SDL2pp')

def main():
	print 'init sdl'
	SDL( SDL_INIT_VIDEO )

	ttf = new(SDLTTF())

	win = Window(
		"my sdl window",
		SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
		640, 480,
		SDL_WINDOW_RESIZABLE
	)

	// Create accelerated video renderer with default driver
	ren = new Renderer(win, -1, SDL_RENDERER_ACCELERATED)
	font = new Font('/usr/share/fonts/gnu-free/FreeSans.ttf', 20)

	let color : SDL_Color = {255,0,255, 255}
	tex  = new Texture(*ren, font.RenderText_Blended("hello world", color))

	// Clear screen
	ren.Clear()
	// Render text
	ren.Copy(*tex)
	// Show rendered frame
	ren.Present()
	// 5 second delay
	sleep(5.0)


```
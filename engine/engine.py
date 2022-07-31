import sdl2
import sdl2.ext


class Engine:
    def __init__(
        self,
        title="Rotation Helper",
        width=588,
        height=50,
        colour=(
            15,
            15,
            15,
            255)) -> None:
        self.title = title.encode()
        self.width = width
        self.height = height
        self.colour = colour

        self.delta_time = 1.0 / 60.0
        self.update_delta_time = 0.0
        self.update_handlers = []
        self.draw_handlers = []

        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
        self.window = sdl2.ext.Window(
            self.title,
            (self.width,
             self.height),
            (sdl2.SDL_WINDOWPOS_CENTERED,
             1090),
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_BORDERLESS | sdl2.SDL_WINDOW_ALWAYS_ON_TOP | sdl2.SDL_WINDOW_INPUT_FOCUS)
        self.renderer = sdl2.ext.Renderer(self.window)
        self.factory = sdl2.ext.SpriteFactory(renderer=self.renderer)

        self.running = True
        self.started = False

    def loop(self):
        event = sdl2.SDL_Event()

        current = sdl2.SDL_GetPerformanceCounter()
        frequency = sdl2.SDL_GetPerformanceFrequency()

        while self.running:
            if sdl2.SDL_PollEvent(event) != 0:
                if event.type == sdl2.SDL_QUIT:
                    self.running = False
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        self.running = False
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_p:
                        self.started = True
                        current = sdl2.SDL_GetPerformanceCounter()

            if self.started:
                new = sdl2.SDL_GetPerformanceCounter()
                self._update((new - current) / frequency)
                current = new

            self.renderer.clear((30, 30, 30, 255))
            self._draw()
            self.renderer.present()

        sdl2.SDL_Quit()

    def _update(self, delta_time):
        self.update_delta_time += delta_time
        while self.update_delta_time > self.delta_time:
            for update in self.update_handlers:
                update(self.delta_time)
            self.update_delta_time -= self.delta_time

    def update(self, function):
        self.update_handlers.append(function)
        return function

    def _draw(self):
        for draw in self.draw_handlers:
            draw()

    def draw(self, function):
        self.draw_handlers.append(function)
        return function

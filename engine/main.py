import sdl2
import sdl2.ext

class Engine:
    def __init__(self, title = "Rotation Helper", width = 800, height = 75, colour = (0,100,0,255)) -> None:
        self.title = title.encode()
        self.width = width
        self.height = height
        self.colour = colour

        self.deltaTime = 1.0/60.0
        self.update_deltaTime = 0.0
        self.update_handlers = []
        self.draw_handlers = []

        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        self.window = sdl2.SDL_CreateWindow(self.title, sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, self.width, self.height, sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_BORDERLESS | sdl2.SDL_WINDOW_ALWAYS_ON_TOP)
        self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)

        self.running = True

    def _update(self, deltaTime):
        self.update_deltaTime += deltaTime
        while self.update_deltaTime > self.deltaTime:
            for update in self.update_handlers:
                update(self.deltaTime)
            self.update_deltaTime -= self.deltaTime

    def _draw(self):
        for draw in self.draw_handlers:
            draw()

    def loop(self):
        sdl2.SDL_ShowWindow(self.window)

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

            new = sdl2.SDL_GetPerformanceCounter()
            self._update((new - current) / frequency)
            current = new

            sdl2.SDL_RenderClear(self.renderer)
            self._draw()
            sdl2.SDL_SetRenderDrawColor(self.renderer, self.colour[0], self.colour[1], self.colour[2], self.colour[3])
            sdl2.SDL_RenderPresent(self.renderer)

        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def update(self, fn):
        self.update_handlers.append(fn)
        return fn

    def draw(self, fn):
        self.draw_handlers.append(fn)
        return fn
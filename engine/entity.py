import sdl2

class Entity(object):
    def __init__(self, window, x = 0, y = 0, width = 40, height = 40, colour = (255, 255, 255, 255)) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.colour = colour

        self.rect = sdl2.SDL_FRect(self.x, self.y, self.width, self.height)

    def draw(self):
        sdl2.SDL_SetRenderDrawColor(self.window.renderer, self.colour[0], self.colour[1], self.colour[2], self.colour[3])
        
        sdl2.SDL_RenderDrawRectF(self.window.renderer, self.rect)
        sdl2.SDL_RenderFillRectF(self.window.renderer, self.rect)

    def center_x(self):
        self.rect.x = self.window.width / 2 - self.width / 2

    def center_y(self):
        self.rect.y = self.window.height / 2 - self.height / 2

    def center(self):
        self.center_x()
        self.center_y()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_x(self) -> int:
        return self.rect.x

    def get_y(self) -> int:
        return self.rect.y
        
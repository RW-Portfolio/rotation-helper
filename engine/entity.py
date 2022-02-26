from shutil import move
import sdl2
import sdl2.ext

class Entity(object):
    def __init__(self, window, sprite, x = 0, y = 0, width = 40, height = 40, colour = (255, 255, 255, 255)) -> None:
        self.window = window
        self.colour = colour
        self.rect = sdl2.SDL_FRect(x, y, width, height)

        self.renderer = self.window.renderer
        self.sprite = sprite

    def draw(self):
        self.renderer.copy(self.sprite, dstrect=(self.rect.x, self.rect.y, self.rect.w, self.rect.h))

    def update(self, movement):
        self.rect.x -= movement
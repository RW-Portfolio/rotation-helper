import sdl2
import sdl2.ext

RESOURCES = sdl2.ext.Resources("c:/Users/ryanw/Documents/GitHub/rotation-helper/", "resources")

class Entity(object):
    def __init__(self, window, spriteFn, x = 0, y = 0, width = 40, height = 40, colour = (255, 255, 255, 255)) -> None:
        self.window = window
        self.colour = colour
        self.rect = sdl2.SDL_FRect(x, y, width, height)

        self.renderer = self.window.renderer
        self.factory = sdl2.ext.SpriteFactory(renderer=self.renderer)
        self.sprite = self.factory.from_image(RESOURCES.get_path(spriteFn))


    def draw(self):
        self.renderer.copy(self.sprite, dstrect=(self.rect.x, self.rect.y, self.rect.w, self.rect.h))

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
        
import sdl2
import sdl2.ext
import sdl2.sdlgfx
import time

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)

class SpaceObj(object):
    def __init__(self, sprite, sprite_original=None):
        self.sprite = sprite
        self.sprite.x = 700
        self.sprite.y = 10
        self.sprite_original = sprite_original

    def update(self, movement):
        surface = sdl2.sdlgfx.rotozoomSurface(self.sprite_original.surface,
                                                  0,
                                                  1,
                                                  1).contents
        sdl2.SDL_FreeSurface(self.sprite.surface)
        self.sprite.surface = surface

        self.sprite.x = self.sprite.x + movement


sdl2.ext.init()
window = sdl2.ext.Window("Physics PySDL2", size=(800, 100))
window.show()
world = sdl2.ext.World()
spriterenderer = SoftwareRenderer(window)
factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

asteroids = []
asteroid_sprites = []

RESOURCES = sdl2.ext.Resources("C:/Users/Ryan/Documents/Git/rotation-helper", "resources")
sp_asteroid = factory.from_image(RESOURCES.get_path("Attonement.png"))
sp_asteroid_original = factory.from_image(RESOURCES.get_path("Attonement.png"))
asteroid = SpaceObj(sp_asteroid, sp_asteroid_original)

asteroids.append(asteroid)
asteroid_sprites.append(sp_asteroid)

time_new = time.time()
time_old = time.time()
running = True
while running:
    time_elapsed = time_new - time_old
    time_old = time_new
    time_new = time.time()
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    time.sleep(0.016)
    for item in asteroids:
        item.update(-1)
    spriterenderer.render(asteroid_sprites)
    window.refresh()
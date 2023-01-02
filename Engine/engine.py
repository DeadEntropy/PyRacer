import sys
import sdl2
import sdl2.ext
import constants as cst
from movement import RelativeMovementSystem, RelativeFrictionSystem
from collision import CollisionSystem
from entities import RelativeCar, DebugInfo, VerticalWall, HorizontalWall
from debugsystem import CarDebugSystem

from sdl2 import rect, render
from sdl2.ext import SDLError
from sdl2.ext.compat import isiterable


class TextureRenderer(sdl2.ext.TextureSpriteRenderSystem):
    def __init__(self, target):
        super(TextureRenderer, self).__init__(target)

    def render(self, sprites, x=None, y=None):
        r = rect.SDL_Rect(0, 0, 0, 0)
        rcopy = render.SDL_RenderCopyEx
        if isiterable(sprites):
            renderer = self.sdlrenderer
            x = x or 0
            y = y or 0
            for sprite in sprites:
                r.x = x + sprite.x
                r.y = y + sprite.y
                r.w, r.h = sprite.size
                if rcopy(renderer, sprite.texture, None, r, sprite.angle,
                         sprite.center, sprite.flip) == -1:
                    raise SDLError()
        else:
            r.x = sprites.x
            r.y = sprites.y
            r.w, r.h = sprites.size
            if x is not None and y is not None:
                r.x = x
                r.y = y
            if rcopy(self.sdlrenderer, sprites.texture, None, r, sprites.angle,
                     sprites.center, sprites.flip) == -1:
                raise SDLError()
        render.SDL_RenderPresent(self.sdlrenderer)

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window(cst.GAME_NAME, size=(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    spriterenderer = TextureRenderer(renderer)

    world = sdl2.ext.World()
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    sdl2.ext.FontManager(font_path = ".\Asset\OpenSans-Regular.ttf", size = 14, color=cst.WHITE)

    movement = RelativeMovementSystem(0, 0, cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    friction = RelativeFrictionSystem()
    collision = CollisionSystem(0, 0, cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    cardebug = CarDebugSystem()
    
    
    world.add_system(friction)
    world.add_system(movement)
    world.add_system(collision)
    world.add_system(cardebug)
    world.add_system(spriterenderer)

    sp_car = factory.from_color(cst.RED, size=(cst.CAR_WIDTH, cst.CAR_HEIGHT))

    car = RelativeCar(world, sp_car, 350, 40)
    car.relativevelocity.acceleration = 0
    car.relativevelocity.angle = 3*cst.PI/2

    debug_info = DebugInfo(world, 0, 0, renderer=renderer)

    the_map = sdl2.ext.Entity(world)
    the_map.sprite = factory.from_image(r".\Asset\background_1.png")
    the_map.sprite.x = 0
    the_map.sprite.y = 0
    the_map.sprite.depth = cst.LayerType.BACKGROUND

    
    the_map = sdl2.ext.Entity(world)
    the_map.sprite = factory.from_image(r".\Asset\tree_1.png")
    the_map.sprite.x = 700
    the_map.sprite.y = 500
    the_map.sprite.depth = cst.LayerType.DECOR


    VerticalWall(world, 180, 120, 200, cst.WHITE, factory)
    HorizontalWall(world, 180, 120, 440, cst.WHITE, factory)

    VerticalWall(world, 600, 120, 280, cst.WHITE, factory)
    HorizontalWall(world, 450, 380, 150, cst.WHITE, factory)   
     
    VerticalWall(world, 450, 200, 250, cst.WHITE, factory)
    HorizontalWall(world, 180, 200, 290, cst.WHITE, factory)
    VerticalWall(world, 270, 450, 150, cst.WHITE, factory)

    cardebug.car = car
    collision.car = car

    running = True
    while running:
        print('Tick')
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
                car.update_d2(event.type, event.key.keysym.sym)
        sdl2.SDL_Delay(10)
        renderer.clear()
        print('Process World')
        world.process()

if __name__ == "__main__":
    sys.exit(run())
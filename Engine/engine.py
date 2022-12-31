import sys
import sdl2
import sdl2.ext
import constants as cst
from movement import RelativeMovementSystem, RelativeFrictionSystem
from collision import CollisionSystem
from entities import RelativeCar, DebugInfo, VerticalWall, HorizontalWall
from debugsystem import CarDebugSystem

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, cst.BLACK)
        super(SoftwareRenderer, self).render(components)

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window(cst.GAME_NAME, size=(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT))
    window.show()

    renderer = sdl2.ext.Renderer(window)

    world = sdl2.ext.World()
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    sdl2.ext.FontManager(font_path = ".\Asset\OpenSans-Regular.ttf", size = 14, color=cst.WHITE)

    movement = RelativeMovementSystem(0, 0, cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    friction = RelativeFrictionSystem()
    collision = CollisionSystem(0, 0, cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    cardebug = CarDebugSystem()
    spriterenderer = factory.create_sprite_render_system()
    
    
    world.add_system(friction)
    world.add_system(movement)
    world.add_system(collision)
    world.add_system(cardebug)
    world.add_system(spriterenderer)

    sp_car = factory.from_color(cst.WHITE, size=(cst.CAR_WIDTH, cst.CAR_HEIGHT))

    car = RelativeCar(world, sp_car, (cst.WINDOW_WIDTH - cst.CAR_WIDTH)//2, (cst.WINDOW_HEIGHT - cst.CAR_HEIGHT)//2)
    car.relativevelocity.acceleration = 0
    car.relativevelocity.angle = 0

    DebugInfo(world, 0, 0, renderer=renderer)

    VerticalWall(world, 100, 100, 300, cst.WHITE, factory)
    HorizontalWall(world, 400, 400, 200, cst.RED, factory)

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
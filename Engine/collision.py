import random
from movement import Collision
import constants as cst
from entities import RelativeCar
import sdl2.ext

class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Collision, sdl2.ext.Sprite
        self.car:RelativeCar  = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        pos, sprite = item
        if sprite == self.car.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.car.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def process(self, world, componentsets):
        print(f"Process - {type(self).__name__}")
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if collitems:
            swidth, sheight = self.car.sprite.size
            _, obstacle_sprite = collitems[0]
            
            left, top, right, bottom = obstacle_sprite.area
            bleft, btop, bright, bbottom = self.car.sprite.area

            dist_from_wall = min(abs(bleft - right), abs(bright - left), abs(btop - bottom), abs(bbottom - top))
            if abs(bleft - right) == dist_from_wall:
                    self.car.relativevelocity.x = right + 1
                    self.car.relativevelocity.bounce_from_left()
            elif abs(bright - left) == dist_from_wall:
                    self.car.relativevelocity.x = left - 1 - swidth
                    self.car.relativevelocity.bounce_from_right()
            elif abs(btop - bottom) == dist_from_wall:
                    self.car.relativevelocity.y = bottom + 1
                    self.car.relativevelocity.bounce_from_below()
            elif abs(bbottom - top) == dist_from_wall:
                    self.car.relativevelocity.y = top - 1 - sheight
                    self.car.relativevelocity.bounce_from_above()

            self.car.sprite.x = int(self.car.relativevelocity.x)
            self.car.sprite.y = int(self.car.relativevelocity.y)
            self.car.sprite.angle = -self.car.relativevelocity.angle * cst.RAD_TO_DEG

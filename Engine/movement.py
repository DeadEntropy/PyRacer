import sdl2.ext
import numpy as np
from enum import Enum 
import constants as cst

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        print(f"Process - {type(self).__name__}")
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            
            velocity.dx += velocity.d2x
            velocity.dy += velocity.d2y

            velocity.x += velocity.dx
            velocity.y += velocity.dy
            
            pmaxx = velocity.x + swidth
            pmaxy = velocity.y + sheight
            if pmaxx > self.maxx:
                velocity.x = self.maxx - swidth
                velocity.dx = 0
                velocity.d2x = 0
            if pmaxy > self.maxy:
                velocity.y = self.maxy - sheight
                velocity.dy = 0
                velocity.d2y = 0
            if velocity.x < self.minx:
                velocity.x = self.minx
                velocity.dx = 0
                velocity.d2x = 0
            if velocity.y < self.miny:
                velocity.y = self.miny
                velocity.dy = 0
                velocity.d2y = 0
                
            sprite.x = int(velocity.x)
            sprite.y = int(velocity.y)

class RelativeMovementSystem(sdl2.ext.Applicator):

    def __init__(self, minx, miny, maxx, maxy):
        super(RelativeMovementSystem, self).__init__()
        self.componenttypes = RelativeVelocity, RelativeFriction, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy


    def process(self, world, componentsets):
        print(f"Process - {type(self).__name__}")
        for relativevelocity, relativeFriction, sprite in componentsets:
            swidth, sheight = sprite.size
            
            relativevelocity.speed += relativevelocity.acceleration + relativeFriction.friction_force
            relativevelocity.angle = (relativevelocity.angle + relativevelocity.angular_acceleration) % (2 * cst.PI)

            relativevelocity.x += relativevelocity.speed * np.sin(relativevelocity.angle)
            relativevelocity.y += relativevelocity.speed * np.cos(relativevelocity.angle)
            
            # Handles collision with the edge of the screen
            pmaxx = relativevelocity.x + swidth
            pmaxy = relativevelocity.y + sheight
            if pmaxx > self.maxx:
                relativevelocity.x = self.maxx - swidth - 1
                relativevelocity.bounce_from_right() 
            if pmaxy > self.maxy:
                relativevelocity.y = self.maxy - sheight - 1
                relativevelocity.bounce_from_above()
            if relativevelocity.x < self.minx:
                relativevelocity.x = self.minx + 1
                relativevelocity.bounce_from_left()
            if relativevelocity.y < self.miny:
                relativevelocity.y = self.miny + 1
                relativevelocity.bounce_from_below()
                
            sprite.x = int(relativevelocity.x)
            sprite.y = int(relativevelocity.y)
            sprite.angle = -relativevelocity.angle * cst.RAD_TO_DEG

    

class RelativeFrictionSystem(sdl2.ext.Applicator):
    A = 0.001
    B = 0.01

    def __init__(self):
        super(RelativeFrictionSystem, self).__init__()
        self.componenttypes = RelativeVelocity, RelativeFriction, sdl2.ext.Sprite

    def process(self, world, componentsets):
        print(f"Process - {type(self).__name__}")
        for relativevelocity, relativeFriction, sprite in componentsets:
            if relativevelocity.speed == 0:
                break
            friction_force = relativevelocity.speed * relativevelocity.speed * self.A + abs(relativevelocity.speed) * self.B
            sign = relativevelocity.speed / abs(relativevelocity.speed)
            relativeFriction.friction_force = - friction_force * sign

class SpeedUnit(Enum):
    PixelTick = 1

class Velocity(object):
    def __init__(self, x, y):
        super(Velocity, self).__init__()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.d2x = 0
        self.d2y = 0
        self.unit = SpeedUnit.PixelTick

class Collision(object):
    def __init__(self):
        super(Collision, self).__init__()
        self.is_impassable = True

class RelativeVelocity(object):
    def __init__(self, x, y):
        super(RelativeVelocity, self).__init__()
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = 0
        self.acceleration = 0
        self.angular_acceleration = 0
        self.unit = SpeedUnit.PixelTick

    def bounce_from_below(self):
        if self.angle > cst.PI:
            self.angle = 1.49*cst.PI
        else:
            self.angle = 0.51*cst.PI
        self.speed = self.speed / 2
        self.acceleration = 0

    def bounce_from_left(self):
        if self.angle < 0.5 * cst.PI:
            self.angle = -0.01*cst.PI
        else:
            self.angle = 1.01*cst.PI
        self.speed = self.speed / 2
        self.acceleration = 0

    def bounce_from_right(self):
        if self.angle < 1.5 * cst.PI:
            self.angle = 0.99 * cst.PI
        else:
            self.angle = 0.01*cst.PI
        self.speed = self.speed / 2
        self.acceleration = 0

    def bounce_from_above(self):
        if self.angle < cst.PI:
            self.angle = 0.49*cst.PI
        else:
            self.angle = 1.51*cst.PI
        self.speed = self.speed / 2
        self.acceleration = 0
    

class RelativeFriction(object):
    def __init__(self):
        super(RelativeFriction, self).__init__()
        self.friction_force = 0.0
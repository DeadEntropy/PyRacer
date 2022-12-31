import numpy as np
from movement import Velocity, RelativeVelocity, RelativeFriction, Collision
from debugsystem import TextObject
from Others.textsprite import TextSprite
import sdl2.ext

class Car(sdl2.ext.Entity):
    ACCELERATION = 0.1

    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity(posx, posy)

    def update_d2(self, type, sym):
        if type == sdl2.SDL_KEYDOWN:
            if sym == sdl2.SDLK_UP:
                self.velocity.d2y = -self.ACCELERATION
            elif sym == sdl2.SDLK_DOWN:
                self.velocity.d2y = self.ACCELERATION
            if sym == sdl2.SDLK_LEFT:
                self.velocity.d2x = -self.ACCELERATION
            elif sym == sdl2.SDLK_RIGHT:
                self.velocity.d2x = self.ACCELERATION
        elif type == sdl2.SDL_KEYUP:
            if sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                self.velocity.d2y = 0
            if sym in (sdl2.SDLK_LEFT, sdl2.SDLK_RIGHT):
                self.velocity.d2x = 0

    def status(self):
        return f"x = {self.velocity.x:,.1f}\ny = {self.velocity.y:,.1f}\n"\
            + f"dx = {self.velocity.dx:,.1f}\ndy = {self.velocity.dy:,.1f}\n"\
            + f"d2x = {self.velocity.d2x:,.1f}\nd2y = {self.velocity.d2y:,.1f}"

class RelativeCar(sdl2.ext.Entity):
    ACCELERATION = 0.1
    ANGULAR_SPEED = 0.05
    RAD_TO_DEG = 57.2958
    PI = 3.141589

    def __init__(self, world, sprite, posx=0, posy=0, angle=0, ai=False):   
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.relativevelocity = RelativeVelocity(posx, posy)
        self.relativefriction = RelativeFriction()

    def update_d2(self, type, sym):
        print('Update')
        if type == sdl2.SDL_KEYDOWN:
            print('Key Down')
            if sym == sdl2.SDLK_LEFT:
                self.relativevelocity.angular_acceleration = self.ANGULAR_SPEED
            elif sym == sdl2.SDLK_RIGHT:
                self.relativevelocity.angular_acceleration = -self.ANGULAR_SPEED
            if sym == sdl2.SDLK_UP: 
                self.relativevelocity.acceleration = -self.ACCELERATION
            elif sym == sdl2.SDLK_DOWN:
                self.relativevelocity.acceleration = self.ACCELERATION
        elif type == sdl2.SDL_KEYUP:
            print('Key Up')
            if sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                self.relativevelocity.acceleration = 0   
            if sym in (sdl2.SDLK_LEFT, sdl2.SDLK_RIGHT):
                self.relativevelocity.angular_acceleration = 0

    def status(self):
        return f"x = {self.relativevelocity.x:,.1f}\ny = {self.relativevelocity.y:,.1f}\n"\
            + f"speed = {self.relativevelocity.speed:,.1f}\nangle = {self.relativevelocity.angle * self.RAD_TO_DEG:,.1f}\n"\
            + f"acceleration = {self.relativevelocity.acceleration:,.4f}\nangular_acceleration = {self.relativevelocity.angular_acceleration:,.1f}\n"\
            + f"friction={self.relativefriction.friction_force:,.4f}" 

class VerticalWall(sdl2.ext.Entity):
    WIDTH = 20

    def __init__(self, world, x, y, length, color, spriteFactory: sdl2.ext.SpriteFactory):
        self.sprite = spriteFactory.from_color(color, size=(self.WIDTH, length))
        self.sprite.position = x, y
        self.collision = Collision()

class HorizontalWall(sdl2.ext.Entity):
    WIDTH = 20

    def __init__(self, world, x, y, length, color, spriteFactory: sdl2.ext.SpriteFactory):
        self.sprite = spriteFactory.from_color(color, size=(length, self.WIDTH))
        self.sprite.position = x, y
        self.collision = Collision()
        

class DebugInfo(sdl2.ext.Entity):
    def __init__(self, world, posx, posy, renderer):        
        self.sprite = TextSprite(renderer, text=" - ", fontSize=11)
        self.sprite.position = posx, posy
        self.scorecounter = TextObject()
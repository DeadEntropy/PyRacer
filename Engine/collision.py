import random
import movement as mov
import constants as cst
import sdl2.ext

class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = mov.Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        pos, sprite = item
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def process(self, world, componentsets):
        print(f"Process - {type(self).__name__}")
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if collitems:
            self.ball.velocity.vx = -self.ball.velocity.vx

            sprite = collitems[0][1]
            ballcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
            halfheight = sprite.size[1] // 2
            stepsize = halfheight // 10
            degrees = 0.7
            paddlecentery = sprite.y + halfheight
            if ballcentery < paddlecentery:
                factor = (paddlecentery - ballcentery) // stepsize
                self.ball.velocity.vy = -int(round(factor * degrees))
            elif ballcentery > paddlecentery:
                factor = (ballcentery - paddlecentery) // stepsize
                self.ball.velocity.vy = int(round(factor * degrees))
            else:
                self.ball.velocity.vy = - self.ball.velocity.vy

        if (self.ball.sprite.y <= self.miny or
            self.ball.sprite.y + self.ball.sprite.size[1] >= self.maxy):
            self.ball.velocity.vy = - self.ball.velocity.vy

        if self.ball.sprite.x <= self.minx + cst.PADDLE_WIDTH // 2:
            # Player 1 wins
            self._reset()
        elif self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxx - cst.PADDLE_WIDTH // 2:
            # Player 2 wins
            self._reset()

    def _reset(self):
        self.ball.sprite.x = int((cst.WINDOW_WIDTH - cst.PADDLE_WIDTH)/2)
        self.ball.sprite.y = int((cst.WINDOW_HEIGHT - cst.PADDLE_WIDTH)/2)
        self.ball.velocity.vx = -3
        self.ball.velocity.vy = random.randint(-3, 3)
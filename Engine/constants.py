
import sdl2.ext
from enum import IntEnum

WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
BLACK = sdl2.ext.Color(0, 0, 0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GAME_NAME = 'PyRacer'

CAR_WIDTH = 20
CAR_HEIGHT = 30

PI = 3.141592
RAD_TO_DEG = 57.2958

class LayerType(IntEnum):
    BACKGROUND = 0
    DECOR = 1
    WALL = 2
    CAR = 3
    UI = 4
import sdl2.ext
import constants as cst

class CarDebugSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (TextObject, sdl2.ext.Sprite)
        self.car = None

    def process(self, world, componentsets):
        print(f"Process - {type(self).__name__}")

        for textobject, textsprite in componentsets:            
            textsprite.text = self.car.status()



class TextObject(object):
    def __init__(self):
        super().__init__()

        self.text = ""
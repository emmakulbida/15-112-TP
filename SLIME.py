import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

#def initImages(app):

class SLIME:
    def __init__(self, startX, startY, sprite):
        self.slimeSprite = dict()
        self.slimeWidth = sprite.size[0]
        self.slimeHeight = sprite.size[1]
        self.x = startX
        self.y = startY
        for direction in (["d0", "r1", "u2", "l3"]): # down 0, right 1, up 2, left 3
            index = int(direction[-1])
            y0 = (self.slimeHeight/4) * index
            y1 = y0 + self.slimeHeight/4
            directionSprites = []
            for i in range(4):
                x0 = (self.slimeWidth/4 * i)
                x1 = x0 + self.slimeWidth/4 
                newSprite = sprite.crop((x0,y0,x1,y1))
                directionSprites.append(newSprite)
            self.slimeSprite[direction] = directionSprites
        
        # initial direction and counter
        self.direction = "u2"
        self.spriteCounter = 0

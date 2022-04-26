import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

class MC:
    def __init__(self, startX, startY, mainSprite, choice):
        self.mainSprite = dict()
        self.mainWidth = mainSprite.size[0]
        self.mainHeight = mainSprite.size[1]
        self.mainChoice = choice # which main character (0,1,2)
        self.x = startX
        self.y = startY
        for direction in (["d0", "l1", "u2"]): # down 0, right 1, up 2, left 3
            index = int(direction[-1])
            y0 = (self.mainHeight/3) * self.mainChoice
            y1 = y0 + self.mainHeight/3
            directionSprites = []
            directionRange = []
            for i in range(3):
                directionRange.append(index)
                index += 3
            for i in directionRange:
                x0 = (self.mainWidth/9 * i)
                x1 = x0 + self.mainWidth/9 
                sprite = mainSprite.crop((x0,y0,x1,y1))
                directionSprites.append(sprite)
            self.mainSprite[direction] = directionSprites
        self.mainSprite["r3"] = []
        for image in self.mainSprite["l1"]:
            newImage = image.transpose(Image.FLIP_LEFT_RIGHT)
            self.mainSprite["r3"].append(newImage)
        
        # initial direction and counter
        self.direction = "d0"
        self.spriteCounter = 0
        self.timerDelay = 20 # speed

import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

#import mazeGeneration

#def initImages(app):

class MC:
    def __init__(self, startX, startY, mainSprite, choice):
        self.mainSprite = dict()
        self.mainWidth = mainSprite.size[0]
        self.mainHeight = mainSprite.size[1]
        print(f'self.mainWidth: {self.mainWidth}, self.mainHeight: {self.mainHeight}')
        self.mainChoice = choice # which main character (0,1,2)
        self.x = startX
        self.y = startY
        for direction in (["d0", "l1", "u2"]): # down 0, right 1, up 2, left 3
            index = int(direction[-1])
            print(f'self.mainChoice: {self.mainChoice}')
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
                #print(f'x0,x1 = {x0,x1}')
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




'''
def appStarted(app):
    # MAIN CHARACTER
    mainSprite = app.loadImage("chibi-layered.png")
    mainSprite = app.scaleImage(mainSprite, 4) # SCALED
    app.mainSprite = dict()
    mainWidth, mainHeight = mainSprite.size
    app.mainChoice = 0 # which main character (0,1,2)
    app.mainX = app.height//2
    app.mainY = app.width//2

    # making a dictionary with directions mapped to sprites 
    for direction in (["d0", "l1", "u2"]): # down 0, right 1, up 2, left 3
        print(f'direction: {direction}')
        index = int(direction[-1])
        y0 = (mainHeight/3) * app.mainChoice
        y1 = y0 + mainHeight/3
        directionSprites = []
        directionRange = []
        for i in range(3):
            directionRange.append(index)
            index += 3
        for i in directionRange:
            x0 = (mainWidth/9 * i)
            x1 = x0 + mainWidth/9 
            #print(f'x0,x1 = {x0,x1}')
            sprite = mainSprite.crop((x0,y0,x1,y1))
            directionSprites.append(sprite)
        app.mainSprite[direction] = directionSprites
        #print("sprites: ", app.mainSprite)

    # sprites for the right direction (transposed left sprites)
    app.mainSprite["r3"] = []
    for image in app.mainSprite["l1"]:
        newImage = image.transpose(Image.FLIP_LEFT_RIGHT)
        app.mainSprite["r3"].append(newImage)

    # initial direction and counter
    app.direction = "d0"
    app.spriteCounter = 0
    app.timerDelay = 20 # speed
'''

def appStarted(app):
    mainSprite = app.loadImage("chibi-layered.png")
    mainSprite = app.scaleImage(mainSprite, 4) # SCALED
    app.mc = MC(app.height//2, app.width//2, mainSprite)

def moveCharacter(app, dX, dY):
    app.mc.x += dX
    app.mc.y += dY

def keyPressed(app,event):
    magnitude = 10
    app.mc.spriteCounter = (1 + app.mc.spriteCounter) % 3
    if event.key == "Up":
        app.mc.direction = "u2"
        moveCharacter(app, 0,-magnitude)
    if event.key == "Down":
        app.mc.direction = "d0"
        moveCharacter(app, 0,magnitude)
    if event.key == "Left":
        app.mc.direction = "l1"
        moveCharacter(app, -magnitude,0)
    if event.key == "Right":
        app.mc.direction = "r3"
        moveCharacter(app, magnitude,0)


# def timerFired(app):
#     app.mc.spriteCounter = (1 + app.mc.spriteCounter) % 3

# def redrawAll(app, canvas):
#     main = app.mc.mainSprite[app.mc.direction][app.mc.spriteCounter]
#     canvas.create_image(app.mc.mainX, app.mc.mainY, image=ImageTk.PhotoImage(main))

# runApp(width=400, height=400)
import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

#def initImages(app):

class SLIME:
    def __init__(self, startX, startY, sprite):
        self.slimeSprite = dict()
        self.slimeWidth = sprite.size[0]
        self.slimeHeight = sprite.size[1]
        print(f'width: {self.slimeWidth}, height: {self.slimeHeight}')
        self.x = startX
        self.y = startY
        for direction in (["d0", "r1", "u2", "l3"]): # down 0, right 1, up 2, left 3
            print("direction: " ,direction)
            index = int(direction[-1])
            y0 = (self.slimeHeight/4) * index
            y1 = y0 + self.slimeHeight/4
            directionSprites = []
            for i in range(4):
                x0 = (self.slimeWidth/4 * i)
                x1 = x0 + self.slimeWidth/4 
                print(f'Dimensions: {x0,y0,x1,y1}')
                newSprite = sprite.crop((x0,y0,x1,y1))
                directionSprites.append(newSprite)
            self.slimeSprite[direction] = directionSprites
        
        # initial direction and counter
        self.direction = "u2"
        self.spriteCounter = 0
        # print("!! ",self.slimeSprite)




'''
def appStarted(app):
    # SLIME
    smallSlimeSprite = app.loadImage("blueSlime.png")
    imageWidth, imageHeight = smallSlimeSprite.size
    print(f'height: {imageHeight}, width: {imageWidth}')
    slimeSprite = app.scaleImage(smallSlimeSprite, 4) # SCALED
    imageWidth, imageHeight = slimeSprite.size
    app.slimes = dict()
    #imageWidth, imageHeight = slimeSprite.size
    for direction in (["d0", "r1", "u2", "l3"]): # down 0, right 1, up 2, left 3
        index = int(direction[-1])
        y0 = (imageHeight/4) * index
        y1 = y0 + imageHeight/4
        directionSprites = []
        for i in range(4):
            x0 = (imageWidth/4 * i)
            x1 = x0 + imageWidth/4 
            sprite = slimeSprite.crop((x0,y0,x1,y1))
            directionSprites.append(sprite)
        app.slimes[direction] = directionSprites
    app.direction = "u2"
    app.spriteCounter = 0
    app.ground = app.loadImage("ground.jpeg")
'''






# def appStarted(app):
#     slimeSprite = app.loadImage("blueSlime.png")
#     slimeSprite = app.scaleImage(slimeSprite, 10)
#     app.slime1 = SLIME(app.height//2, app.width//2, slimeSprite)


# def keyPressed(app,event):
#     if event.key == "Up":
#         app.slime1.direction = "u2"
#     if event.key == "Down":
#         app.slime1.direction = "d0"
#     if event.key == "Left":
#         app.slime1.direction = "l3"
#     if event.key == "Right":
#         app.slime1.direction = "r1"


# def timerFired(app):
#     app.slime1.spriteCounter = (1 + app.slime1.spriteCounter) % len(app.slime1.slimeSprite)


# def redrawAll(app, canvas):
#     #canvas.create_image(64,64,image = ImageTk.PhotoImage(app.slimeSprite))
#     sprite = app.slime1.slimeSprite[app.slime1.direction][app.slime1.spriteCounter]
#     canvas.create_image(200, 200, image=ImageTk.PhotoImage(sprite))
# runApp(width=400, height=400)
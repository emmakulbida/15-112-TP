import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

#def initImages(app):


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

def keyPressed(app,event):
    if event.key == "Up":
        app.direction = "u2"
    if event.key == "Down":
        app.direction = "d0"
    if event.key == "Left":
        app.direction = "l3"
    if event.key == "Right":
        app.direction = "r1"


# def appStarted(app):
#     # SLIME
#     slimeSprite = app.loadImage("blueSlime.png")
#     imageWidth, imageHeight = slimeSprite.size
#     print(f'width: {imageWidth}, height: {imageHeight}')
#     app.sprites = [ ]
#     for i in range(4):
#         sprite = slimeSprite.crop((32*i,0,32*i+32,32))
#         app.sprites.append(sprite)
#     app.spriteCounter = 0

def timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.slimes)

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,400,400,fill = "black")
    slime = app.slimes[app.direction][app.spriteCounter]
    canvas.create_image(200, 200, image=ImageTk.PhotoImage(slime))


# def redrawAll(app, canvas):
#     #canvas.create_image(64,64,image = ImageTk.PhotoImage(app.slimeSprite))
#     sprite = app.sprites[app.spriteCounter]
#     canvas.create_image(200, 200, image=ImageTk.PhotoImage(sprite))

runApp(width=400, height=400)
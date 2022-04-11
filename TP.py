import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

#def initImages(app):


def appStarted(app):
    # MAIN CHARACTER
    mainSprite = app.loadImage("chibi-layered.png")
    mainSprite = app.scaleImage(mainSprite, 4) # SCALED
    app.mainSprite = dict()
    mainWidth, mainHeight = mainSprite.size
    app.mainChoice = 1 # which main character (0,1,2)
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


def moveCharacter(app, dX, dY):
    app.mainX += dX
    app.mainY += dY

def keyPressed(app,event):
    app.spriteCounter = (1 + app.spriteCounter) % 3
    if event.key == "Up":
        app.direction = "u2"
        moveCharacter(app, 0,-10)
    if event.key == "Down":
        app.direction = "d0"
        moveCharacter(app, 0,10)
    if event.key == "Left":
        app.direction = "l1"
        moveCharacter(app, -10,0)
    if event.key == "Right":
        app.direction = "r3"
        moveCharacter(app, 10,0)


# def timerFired(app):
#     app.spriteCounter = (1 + app.spriteCounter) % 3

def redrawAll(app, canvas):
    main = app.mainSprite[app.direction][app.spriteCounter]
    canvas.create_image(app.mainX, app.mainY, image=ImageTk.PhotoImage(main))

runApp(width=400, height=400)
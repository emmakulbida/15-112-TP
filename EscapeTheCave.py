import math, copy, random
from cmu_112_graphics import * 
from PIL import Image
import MC
import SLIME

'''
Image Citations: 
Slime sprite: https://stealthix.itch.io/animated-slimes?download
Torch: https://pixelartmaker-data-78746291193.nyc3.digitaloceanspaces.com/image/3eeb8d5ba6ba852.png
Game Over image: https://www.shutterstock.com/video/clip-31008892-game-over-insert-coin-arcade-retro-video
You Win image: https://www.istockphoto.com/video/you-win-glitch-text-animation-old-gaming-console-style-rendering-background-loop-gm966897440-263778509 
Key: https://icons-for-free.com/key-131982518810247060/
Heart: https://icons-for-free.com/heart-131982518789423215/ 
Arrow and Space keys: https://www.iconfinder.com/icons/4661457/arrow_down_keys_left_right_up_icon 
Characters: https://route1rodent.itch.io/16x16-rpg-character-sprite-sheet/devlog/250689/new-style-released
Ground: https://www.shutterstock.com/image-vector/seamless-texture-ground-small-stones-concept-1398204977 
Snowflake: https://www.pikpng.com/transpng/bmJxRh/ 
Speed: https://pixelartmaker-data-78746291193.nyc3.digitaloceanspaces.com/image/44e7ea4ae2a9981.png 
Shield: http://pixelartmaker.com/art/cc9ed077aed46f5
'''

def appStarted(app):
    app.mode = "start" 
    app.sideMargin = None
    app.topMargin = None
    app.rows = None
    app.cols = None
    app.cellSize = 28
    app.mcChoice = None 
    app.levelChoice = None
    app.lightCoordinates = set()
    app.maze = None 
    app.mazeWalls = []
    # start screen characters for selection
    app.mainSprite = app.loadImage("chibi-layered.png")
    app.mainSpriteStart = app.scaleImage(app.mainSprite, app.width/75)
    app.mcStartScreen0 = MC.MC(0, 0, app.mainSpriteStart, 0)
    app.mcStartScreen1 = MC.MC(0, 0, app.mainSpriteStart, 1)
    app.mcStartScreen2 = MC.MC(0, 0, app.mainSpriteStart, 2)
    # scale MC based on window size
    app.mainSprite = app.scaleImage(app.mainSprite, app.cellSize / 10) 
    # initializing main character
    app.mcStartX = 0
    app.mcStartY = 0
    app.mc = None 
    app.lives = 3
    # initializing friend
    app.friend = None
    app.friendX = None
    app.friendY = None
    app.friendChoice = None
    # loading in images
    ground = app.loadImage("ground.jpeg")
    ground = app.scaleImage(ground, 1.2)
    app.ground = ImageTk.PhotoImage(ground)
    torch = app.loadImage("torch.png")
    app.torch = app.scaleImage(torch, app.cellSize/50)
    app.mcTorch = app.loadImage("torch.png")
    app.torchStartScreen = app.scaleImage(torch, app.cellSize/15)
    app.gameOverText = app.loadImage("gameover.png")
    app.youWonText = app.scaleImage(app.loadImage("youwin1.png"),0.7)
    title = app.loadImage("title1.png")
    app.title = app.scaleImage(title, 6/11)
    app.slimeSprite = app.loadImage("redSlime.png")
    app.key = app.loadImage("key.png")
    app.heart = app.loadImage("heart.png")
    app.helpScreen = app.loadImage("howToPlay.png")
    app.helpScreen = app.scaleImage(app.helpScreen, 1.15)
    app.freezePic = app.loadImage("snowflake.png")
    app.speedPic = app.loadImage("speed.png")
    app.shieldPic = app.loadImage("shield.png")
    # intiializing slimes
    app.slimes = []
    app.slimeCoordinates = []
    app.randomTargets = [] # in row col
    app.randomTargetCoordinates = []
    # boolean flags
    app.torchOn = True
    app.keyFound = False
    app.keyPosition = None
    app.doorUnlocked = False
    app.exitedChannel = False
    app.foundFriend = False
    # timers
    app.collidedTimer = 0
    app.runningTimer = 0
    app.timerDelay = 20
    # powerups
    app.freezeCoordinates, app.speedCoordinates, app.shieldCoordinates = set(), set(), set()
    app.freeze = False
    app.speed = False
    app.shield = False

    app.freezeInventory = app.loadImage("snowflake.png")
    app.shieldInventory = app.loadImage("shield.png")
    app.speedInventory = app.loadImage("speed.png")

    app.freezeTimer = 50
    app.speedTimer = 50
    app.shieldTimer = 50

    app.magnitude = 10

#####################
# help mode
#####################

def help_mousePressed(app, event):
    if event.x > 1*app.width/3 and event.x < 2*app.width/3 and event.y < 7*app.width/8:
        app.mode = "start"

def help_redrawAll(app, canvas):
    canvas.create_image(app.width//2, app.height//2, image = ImageTk.PhotoImage(app.helpScreen))

#####################
# start screen mode
#####################

def start_mousePressed(app, event):
    # choosing a character
    char0Bounds = startScreenCharactersBounds(app, 0)
    if event.x > char0Bounds[0] and event.x < char0Bounds[2] and event.y > char0Bounds[1] \
        and event.y < char0Bounds[3]:
        app.mcChoice = 0
    char1Bounds = startScreenCharactersBounds(app, 1)
    if event.x > char1Bounds[0] and event.x < char1Bounds[2] and event.y > char1Bounds[1] \
        and event.y < char1Bounds[3]:
        app.mcChoice = 1
    char2Bounds = startScreenCharactersBounds(app, 2)
    if event.x > char2Bounds[0] and event.x < char2Bounds[2] and event.y > char2Bounds[1] \
        and event.y < char2Bounds[3]:
        app.mcChoice = 2

    # click on torch
    torchBounds = (5 * app.width / 6, 7 * app.height / 10)
    if event.x > torchBounds[0] - app.width/20 and event.x < torchBounds[0] + app.width/20 \
        and event.y > torchBounds[1] - app.height/5.5 and event.y < torchBounds[1] + app.height/5.5:
        if app.mcChoice != None and app.levelChoice != None: 
            pickCharacterAndLevel(app)
            pickOtherCharacter(app)
            app.mode = "gameplay"

    # choosing a level
    levelx0, levelx1 = 18*app.width/25, 24*app.width/25
    if event.x > levelx0 and event.x < levelx1 and event.y > 2*app.height/18 \
        and event.y < 4*app.height/18:
        app.levelChoice = "easy"
    if event.x > levelx0 and event.x < levelx1 and event.y > 4*app.height/18 \
        and event.y < 6*app.height/18:
        app.levelChoice = "medium"
    if event.x > levelx0 and event.x < levelx1 and event.y > 6*app.height/18 \
        and event.y < 8*app.height/18:
        app.levelChoice = "hard"
    
    # click on help button
    if event.x > app.width - app.cellSize*4 and event.y > app.height - app.cellSize*4:
        app.mode = "help"

def reset(app):
    app.mode = "start" # "start"
    app.sideMargin = None #None
    app.topMargin = None #None
    app.rows = None
    app.cols = None
    app.cellSize = 28 #None
    app.friendX = None
    app.friendY = None
    app.mcChoice = None
    app.levelChoice = None
    app.maze = None
    app.mazeWalls = []
    app.mcStartX = 0
    app.mcStartY = 0
    app.mc = None
    app.friend = None
    app.friendChoice = None
    app.foundFriend = False
    app.friend = None
    ground = app.loadImage("ground.jpeg")
    ground = app.scaleImage(ground, 1.2)
    app.ground = ImageTk.PhotoImage(ground)
    torch = app.loadImage("torch.png")
    app.torch = app.scaleImage(torch, app.cellSize/50)
    app.mcTorch = app.loadImage("torch.png")
    app.torchStartScreen = app.scaleImage(torch, app.cellSize/15)
    app.lightCoordinates = set()
    app.slimes = []
    app.slimeCoordinates = []
    app.slimeSprite = app.loadImage("redSlime.png")
    app.runningTimer = 0
    app.torchOn = True
    app.randomTargets = [] # in row col
    app.randomTargetCoordinates = []
    app.key = app.loadImage("key.png")
    app.keyFound = False
    app.keyPosition = None
    app.heart = app.loadImage("heart.png")
    app.lives = 3
    app.doorUnlocked = False
    app.collidedTimer = 0
    app.exitedChannel = False
    app.mainSprite = app.loadImage("chibi-layered.png")
    app.mainSprite = app.scaleImage(app.mainSprite, app.cellSize / 10)
    app.freezePic = app.loadImage("snowflake.png")
    app.speedPic = app.loadImage("speed.png")
    app.shieldPic = app.loadImage("shield.png")
    app.freezeInventory = app.loadImage("snowflake.png")
    app.shieldInventory = app.loadImage("shield.png")
    app.speedInventory = app.loadImage("speed.png")
    app.freezeCoordinates, app.speedCoordinates, app.shieldCoordinates = set(), set(), set()
    app.freeze = False
    app.speed = False
    app.shield = False

def retry(app):
    app.freezePic = app.loadImage("snowflake.png")
    app.speedPic = app.loadImage("speed.png")
    app.shieldPic = app.loadImage("shield.png")
    app.freezeInventory = app.loadImage("snowflake.png")
    app.shieldInventory = app.loadImage("speed.png")
    app.speedInventory = app.loadImage("shield.png")
    app.mcStartX, app.mcStartY = determineStartPosition(app)
    app.mc = MC.MC(app.mcStartX, app.mcStartY, app.mainSprite, app.mcChoice)
    app.foundFriend = False
    app.slimes = []
    app.slimeCoordinates = []
    app.slimeSprite = app.loadImage("redSlime.png")
    app.slimeSprite = app.scaleImage(app.slimeSprite, app.cellSize/18)
    app.runningTimer = 0
    app.torchOn = True
    app.randomTargets = [] # in row col
    app.randomTargetCoordinates = []
    app.key = app.loadImage("key.png")
    app.key = app.scaleImage(app.key, app.cellSize / 50)
    app.keyFound = False
    app.heart = app.loadImage("heart.png")
    app.freezeCoordinates, app.speedCoordinates, app.shieldCoordinates = set(), set(), set()
    if app.levelChoice == "easy":
        app.heart = app.scaleImage(app.heart, app.cellSize//10)
        placeSlimes(app, 2)
        placePowerups(app, 2)
    elif app.levelChoice == "medium":
        app.heart = app.scaleImage(app.heart, app.cellSize//10)
        placeSlimes(app, 5)
        placePowerups(app, 3)
    elif app.levelChoice == "hard":
        app.heart = app.scaleImage(app.heart, app.cellSize//7)
        placeSlimes(app, 7)
        placePowerups(app, 4)
    app.lives = 3
    app.doorUnlocked = False
    app.collidedTimer = 0
    app.exitedChannel = False
    app.freezePic = app.loadImage("snowflake.png")
    app.speedPic = app.loadImage("speed.png")
    app.shieldPic = app.loadImage("shield.png")
    adjustPowerupSize(app)
    app.freeze = False
    app.speed = False
    app.shield = False


def pickOtherCharacter(app):
    randCharacter = random.randint(0,2)
    while randCharacter == app.mcChoice: 
        # until it's not the same as the main character
        randCharacter = random.randint(0,2)
    x1,x2,y1,y2 = cellBounds(app, app.rows-3, app.cols-4)
    app.friendX = (x1+x2)/2
    app.friendY = (y1+y2)/2
    app.friendChoice = randCharacter
    app.friend = MC.MC(app.friendX, app.friendY, app.mainSprite, randCharacter)

def pickCharacterAndLevel(app):
    if app.levelChoice == "easy":
        app.rows = 20
        app.cols = 30
        app.maze = [["?"] * app.cols for i in range(app.rows)]
        app.cellSize = getCellSize(app)
        app.sideMargin, app.topMargin = getMargin(app)
        makeMaze(app, 20) # walls removed
        app.mcStartX, app.mcStartY = determineStartPosition(app)
        makeEntrance(app)
        app.mainSprite = app.scaleImage(app.mainSprite, app.cellSize / 26)
        app.mc = MC.MC(app.mcStartX, app.mcStartY, app.mainSprite, app.mcChoice)
        app.mcTorch = app.scaleImage(app.mcTorch, app.cellSize/300)
        app.slimeSprite = app.scaleImage(app.slimeSprite, app.cellSize / 18)
        placeSlimes(app, 2)
        placeKey(app)
        app.key = app.scaleImage(app.key, app.cellSize / 50)
        app.inventoryKey = app.scaleImage(app.key, app.cellSize / 20)
        app.heart = app.scaleImage(app.heart, app.cellSize//10)
        adjustPowerupSize(app)
        placePowerups(app, 2)
    if app.levelChoice == "medium":
        app.rows = 25
        app.cols = 35
        app.maze = [["?"] * app.cols for i in range(app.rows)]
        app.cellSize = getCellSize(app)
        app.sideMargin, app.topMargin = getMargin(app)
        makeMaze(app,30) # walls removed
        app.mcStartX, app.mcStartY = determineStartPosition(app)
        makeEntrance(app)
        app.mainSprite = app.scaleImage(app.mainSprite, app.cellSize / 26)
        app.mc = MC.MC(app.mcStartX, app.mcStartY, app.mainSprite, app.mcChoice)
        app.mcTorch = app.scaleImage(app.mcTorch, app.cellSize/300)
        app.slimeSprite = app.scaleImage(app.slimeSprite, app.cellSize / 18)
        placeSlimes(app, 5)
        placeKey(app)
        app.key = app.scaleImage(app.key, app.cellSize / 50)
        app.inventoryKey = app.scaleImage(app.key, app.cellSize / 12)
        app.heart = app.scaleImage(app.heart, app.cellSize//10)
        adjustPowerupSize(app)
        placePowerups(app, 3)
    if app.levelChoice == "hard":
        app.rows = 30
        app.cols = 40
        app.maze = [["?"] * app.cols for i in range(app.rows)]
        app.cellSize = getCellSize(app)
        app.sideMargin, app.topMargin = getMargin(app)
        makeMaze(app,40) # walls removed
        app.mcStartX, app.mcStartY = determineStartPosition(app)
        makeEntrance(app)
        app.mainSprite = app.scaleImage(app.mainSprite, app.cellSize / 26)
        app.mc = MC.MC(app.mcStartX, app.mcStartY, app.mainSprite, app.mcChoice)
        app.mcTorch = app.scaleImage(app.mcTorch, app.cellSize/300)
        app.slimeSprite = app.scaleImage(app.slimeSprite, app.cellSize / 18)
        placeSlimes(app, 7)
        placeKey(app)
        app.key = app.scaleImage(app.key, app.cellSize / 50)
        app.inventoryKey = app.scaleImage(app.key, app.cellSize / 10)
        app.heart = app.scaleImage(app.heart, app.cellSize//7)
        adjustPowerupSize(app)
        placePowerups(app, 4)
    updateLightCoordinates(app)

def drawLevels(app, canvas):
    canvas.create_text(21*app.width/25, 3*app.height/18, fill = "#ffce00", \
    text = "EASY", font = f"Helvetica {int(app.width/25)} bold")
    canvas.create_text(21*app.width/25, 5*app.height/18, fill = "#ff9a00", \
    text = "MEDIUM", font = f"Helvetica {int(app.width/25)} bold")
    canvas.create_text(21*app.width/25, 7*app.height/18, fill = "#ff0000", \
    text = "HARD", font = f"Helvetica {int(app.width/25)} bold")
        
def drawLevelChoice(app, canvas):
    levelx0, levelx1 = 18*app.width/25, 24*app.width/25
    if app.levelChoice == "easy":
        canvas.create_rectangle(levelx0, 2*app.height/18,levelx1, \
            4*app.height/18, fill = "#404040", outline = "#707070")
    if app.levelChoice == "medium":
        canvas.create_rectangle(levelx0, 4*app.height/18,levelx1, \
            6*app.height/18, fill = "#404040", outline = "#707070")
    if app.levelChoice == "hard":
        canvas.create_rectangle(levelx0, 6*app.height/18,levelx1, \
            8*app.height/18, fill = "#404040", outline = "#707070")

def placeSlimes(app, numberSlimes):
    for i in range(numberSlimes):
        row,col = determineSlimeStartPosition(app)
        app.slimeCoordinates.append([row,col])
        x1,x2,y1,y2 = cellBounds(app, row, col)
        app.slimes.append(SLIME.SLIME((x1+x2)//2, (y1+y2)//2, app.slimeSprite))

def placePowerups(app, num):
    for powerup in (app.freezeCoordinates, app.speedCoordinates, app.shieldCoordinates):
        for i in range(num):
            placeItem(app, powerup)

def adjustPowerupSize(app):
    app.freezePic = app.scaleImage(app.freezePic, app.cellSize/700)
    app.shieldPic = app.scaleImage(app.shieldPic, app.cellSize/350)
    app.speedPic = app.scaleImage(app.speedPic, app.cellSize/500)
    app.freezeInventory = app.scaleImage(app.freezeInventory, app.cellSize/350)
    app.shieldInventory = app.scaleImage(app.shieldInventory, app.cellSize/175)
    app.speedInventory = app.scaleImage(app.speedInventory, app.cellSize/250)

def placeItem(app, powerup):
    while True:  
        row = random.randint(1, app.rows-1)
        col = random.randint(1, app.cols-1)
        x1,x2,y1,y2 = cellBounds(app, row, col)
        if app.maze[row][col] == "path" and not (row > app.rows-6 and col > app.cols - 7)\
            and ((x1+x2)//2, (y1+y2)//2) not in powerup: 
            powerup.add(((x1+x2)//2, (y1+y2)//2))
            return

def placeKey(app):
    while True:  
        row = random.randint(3, app.rows-1)
        col = random.randint(2, app.cols-6)
        if app.maze[row][col] == "path" and [row,col] not in app.slimeCoordinates\
            and not (row > app.rows-6 and col > app.cols - 7)\
            and row != app.mc.y and col!= app.mc.x: 
            x1,x2,y1,y2 = cellBounds(app, row, col)
            app.keyPosition = ((x1+x2)//2, (y1+y2)//2)
            return

def start_redrawAll(app, canvas):
    drawGround(app, canvas)
    if app.mcChoice != None: 
        drawCharacterChoice(app, canvas, app.mcChoice)
    if app.levelChoice != None: 
        drawLevelChoice(app, canvas)
    drawCharacters(app, canvas)
    drawLevels(app, canvas)
    drawTorch(app, canvas)
    drawTitle(app, canvas)
    drawHelp(app, canvas)

def drawTitle(app, canvas):
    canvas.create_image((app.width//10 + app.width//11 * 2.5 * 1) + app.width//16,\
        3*app.height//12, image = ImageTk.PhotoImage(app.title))
    canvas.create_text((app.width//10 + app.width//11 * 2.5 * 1) + app.width//16,\
        5*app.height//12 - 10, text = "select character and difficulty. click torch to start.", \
        font = "Helvetica 22", fill = "#999999")

def drawTorch(app, canvas):
    canvas.create_image(5 * app.width / 6, 7 * app.height / 10, image = ImageTk.PhotoImage(app.torch))

def drawCharacterChoice(app, canvas, choice):
    bounds = startScreenCharactersBounds(app, choice)
    sideBorder = app.width//21
    topBorder = app.height//40
    canvas.create_rectangle(bounds[0] - sideBorder, bounds[1] - topBorder, \
        bounds[2] + sideBorder, bounds[3] + topBorder, fill = "#404040", \
        outline = "#707070")

def startScreenCharactersBounds(app, i):
    startY = int(app.height//2)
    endY = int(7*app.height//8)
    startX = int(app.width//10 + app.width//11 * 2.5 * i)
    endX = int(startX + app.width//8)
    return startX, startY, endX, endY

def drawCharacters(app, canvas):
    i = 0
    for character in ([app.mcStartScreen0, app.mcStartScreen1, app.mcStartScreen2]):
        startX, startY, endX, endY = startScreenCharactersBounds(app, i)
        midY = int((startY+endY)//2)
        midX = int((startX+endX)/2)
        canvas.create_image(midX, midY, image = ImageTk.PhotoImage(character.mainSprite["d0"][0]))
        i += 1

def drawHelp(app, canvas):
    canvas.create_text(19*app.width/20, 18*app.height/20, text = "?", \
        font = "Helvetica 70 bold", fill = "#999999")

#####################
# gameplay mode
#####################

def gameplay_keyPressed(app, event):
    updateLightCoordinates(app)
    if event.key == "Space":
        getRandomTargets(app)
        # torch only works when you get past the entrance channel
        if app.exitedChannel == True:
            app.torchOn = not app.torchOn
        # shifts the random target coordinates every time you switch the torch on/off
    magnitude = app.magnitude
    if event.key == "Up":
        app.mc.spriteCounter = (1 + app.mc.spriteCounter) % 3
        app.mc.direction = "u2"
        if moveIsLegal(app, 0, -magnitude):
            moveCharacter(app, 0, -magnitude)
    if event.key == "Down":
        app.mc.spriteCounter = (1 + app.mc.spriteCounter) % 3
        app.mc.direction = "d0"
        if moveIsLegal(app, 0, magnitude):
            moveCharacter(app, 0, magnitude)
    if event.key == "Left":
        app.mc.spriteCounter = (1 + app.mc.spriteCounter) % 3
        app.mc.direction = "l1"
        if moveIsLegal(app, -magnitude, 0):
            moveCharacter(app, -magnitude, 0)
    if event.key == "Right":
        app.mc.spriteCounter = (1 + app.mc.spriteCounter) % 3
        app.mc.direction = "r3"
        if moveIsLegal(app, magnitude, 0):
            moveCharacter(app, magnitude,0)
    
    # goes back to home
    if event.key == "h":
        app.mode = "start"
        reset(app)
    
    # restarts level
    if event.key == "r":
        app.mode = "gameplay"
        retry(app)

    # almost win state
    if event.key == "w":
        app.lives = 2
        app.keyFound = True
        app.mc.x = app.width - app.sideMargin - app.cellSize * 5
        app.mc.y = app.height - app.topMargin - app.cellSize * 5

def gameplay_timerFired(app):
    app.freezeTimer += 2
    app.speedTimer += 2
    app.shieldTimer += 2
    if app.freezeTimer >= 50:
        app.freeze = False
    if app.speedTimer >= 50:
        app.speed = False
        app.magnitude = 10
    if app.shieldTimer >= 50:
        app.shield = False
    checkChannel(app)
    checkPowerupFound(app)
    applyPowerups(app)
    updateLightCoordinates(app)
    checkKeyFound(app)
    checkDoorUnlocked(app)
    app.collidedTimer += 1
    if app.collidedTimer % 20 == 0 and app.shield == False: 
        checkSlimeCollision(app)

    # if the characters run into each other
    diffX = app.mc.x - app.friend.x
    diffY = app.mc.y - app.friend.y
    if (diffX < 30 and diffX > -30) and (diffY < 30 and diffY > -30) and app.keyFound:
        app.foundFriend = True
    if app.foundFriend == True: 
        app.friend.x = app.mc.x - 35
        app.friend.y = app.mc.y
    for slime in app.slimes: 
        slime.spriteCounter = (slime.spriteCounter + 1) % 4
    
    app.runningTimer += 1
    if app.runningTimer % 5 == 0 and app.freeze == False:
        slimeMovements(app)

def applyPowerups(app):
    if app.speed == True: 
        app.magnitude = 15

def gameplay_redrawAll(app, canvas):
    drawMaze(app, canvas)

    # drawing key
    if app.keyFound == False:
        canvas.create_image(app.keyPosition[0], app.keyPosition[1], image = ImageTk.PhotoImage(app.key))

    # drawing main character
    main = app.mc.mainSprite[app.mc.direction][app.mc.spriteCounter]
    mcRow, mcCol = getRowCol(app, app.mc.x, app.mc.y)
    if app.torchOn or ((mcRow, mcCol) in app.lightCoordinates):
        canvas.create_image(app.mc.x, app.mc.y - 3*app.cellSize//5, image=ImageTk.PhotoImage(main))

    # drawing friend
    if app.foundFriend == False: 
        friend = app.friend.mainSprite["d0"][1]
    else: 
        friend = app.friend.mainSprite[app.mc.direction][app.mc.spriteCounter]
    canvas.create_image(app.friend.x, app.friend.y - 3*app.cellSize//5, image=ImageTk.PhotoImage(friend))
    
    # drawing the torch
    if app.torchOn: 
        drawMCTorch(app, canvas)
    
    # drawing the slimes
    for slime in app.slimes: 
        slimeImage = slime.slimeSprite["u2"][slime.spriteCounter]
        canvas.create_image(slime.x, slime.y, image = ImageTk.PhotoImage(slimeImage))

    # draw key inventory and health
    if not(app.mc.x > app.width - app.sideMargin//2 - 10* app.cellSize and app.mc.y < app.topMargin + 3* app.cellSize):
        canvas.create_rectangle(app.width - app.sideMargin//2 - 8* app.cellSize, \
            app.topMargin, app.width - app.sideMargin//2, app.topMargin + 2* app.cellSize, \
            fill = "#222222", width = 0)

    if app.keyFound == True: 
        canvas.create_image(app.width - app.sideMargin //2 - (app.cellSize), \
            app.topMargin + app.cellSize, image = ImageTk.PhotoImage(app.inventoryKey))

    if app.lives >= 1: 
        canvas.create_image(app.width - app.sideMargin // 2 - (app.cellSize * 3), \
            app.topMargin + app.cellSize, image = ImageTk.PhotoImage(app.heart))
        if app.lives >= 2: 
            canvas.create_image(app.width - app.sideMargin // 2 - (app.cellSize * 5), \
                app.topMargin + app.cellSize, image = ImageTk.PhotoImage(app.heart))
            if app.lives == 3: 
                canvas.create_image(app.width - app.sideMargin // 2 - (app.cellSize * 7), \
                    app.topMargin + app.cellSize, image = ImageTk.PhotoImage(app.heart))

    # drawing door
    if app.doorUnlocked == False:
        canvas.create_rectangle(app.sideMargin + (app.cellSize * (app.cols-1)), \
            app.height - app.topMargin - app.cellSize * 3, app.sideMargin + app.cellSize * (app.cols-1) + app.cellSize/4,\
            app.height - app.topMargin- app.cellSize * 2, fill = "#654321", width = 0)
    elif app.doorUnlocked == True: 
        canvas.create_rectangle(app.sideMargin + (app.cellSize * (app.cols-1)) - app.cellSize/4, \
            app.height - app.topMargin - app.cellSize * 4, app.sideMargin + app.cellSize * (app.cols-1), \
            app.height - app.topMargin - app.cellSize * 3, fill = "#654321", width = 0)
    drawPowerupInventory(app, canvas)

def drawPowerupInventory(app, canvas):
    if app.freeze == True :
        canvas.create_image(app.width - app.sideMargin/2, app.topMargin + app.cellSize * 5, image = ImageTk.PhotoImage(app.freezeInventory))
    if app.shield == True :
        canvas.create_image(app.width - app.sideMargin/2, app.topMargin + app.cellSize * 7, image = ImageTk.PhotoImage(app.shieldInventory))
    if app.speed == True :
        canvas.create_image(app.width - app.sideMargin/2, app.topMargin + app.cellSize * 9, image = ImageTk.PhotoImage(app.speedInventory))

def drawPowerups(app, canvas):
    for powerup in (app.freezeCoordinates, app.speedCoordinates, app.shieldCoordinates):
        for x,y in (powerup):
            if powerup == app.freezeCoordinates: 
                image = app.freezePic
            elif powerup == app.speedCoordinates: 
                image = app.speedPic
            elif powerup == app.shieldCoordinates: 
                image = app.shieldPic
            canvas.create_image(x,y,image = ImageTk.PhotoImage(image))

def checkChannel(app):
    if app.mc.x > app.sideMargin: 
        app.exitedChannel = True

def getRandomTarget(app):
    while True:  
        row = random.randint(2, app.rows-1)
        col = random.randint(2, app.cols-1)
        if app.maze[row][col] == "path" and [row,col] not in app.randomTargets\
            and not (row > app.rows-6 and col > app.cols - 7)\
            and row != app.mc.y and col!= app.mc.x: 
            return [row, col]

def getRandomTargets(app):
    # resets list
    app.randomTargets = []
    app.randomTargetCoordinates = []
    for i in range(len(app.slimes)):
        row,col = getRandomTarget(app)
        app.randomTargets.append([row,col])
        x1,x2,y1,y2 = cellBounds(app, row, col)
        app.randomTargetCoordinates.append(((x1+x2)//2, (y1+y2)//2))

def checkDoorUnlocked(app):
    if app.keyFound and app.mc.x > app.sideMargin + (app.cellSize * (app.cols-2)) \
        and app.mc.y > app.height - app.topMargin - app.cellSize * 4 and \
        app.mc.y < app.height - app.topMargin - app.cellSize:
        app.doorUnlocked = True
        app.friendFound = True

def checkKeyFound(app):
    diffX = app.mc.x - app.keyPosition[0]
    diffY = app.mc.y - app.keyPosition[1]
    if (diffX < 20 and diffX > -20) and (diffY < 20 and diffY > -20):
        app.keyFound = True

def checkPowerupFound(app):
    freezeCoor = set.union(set(),app.freezeCoordinates)
    speedCoor = set.union(set(), app.speedCoordinates)
    shieldCoor = set.union(set(), app.shieldCoordinates)
    for coordinate in app.freezeCoordinates: 
        diffX = app.mc.x - coordinate[0]
        diffY = app.mc.y - coordinate[1]
        if (diffX < 20 and diffX > -20) and (diffY < 20 and diffY > -20):
            app.freeze = True
            app.freezeTimer = 0
            freezeCoor.remove(coordinate)
    for coordinate in app.speedCoordinates: 
        diffX = app.mc.x - coordinate[0]
        diffY = app.mc.y - coordinate[1]
        if (diffX < 20 and diffX > -20) and (diffY < 20 and diffY > -20):
            app.speed = True
            app.speedTimer = 0
            speedCoor.remove(coordinate)
    for coordinate in app.shieldCoordinates: 
        diffX = app.mc.x - coordinate[0]
        diffY = app.mc.y - coordinate[1]
        if (diffX < 20 and diffX > -20) and (diffY < 20 and diffY > -20):
            app.shield = True
            app.shieldTimer = 0
            shieldCoor.remove(coordinate)
    app.freezeCoordinates = freezeCoor
    app.speedCoordinates = speedCoor
    app.shieldCoordinates = shieldCoor

def checkSlimeCollision(app):
    slimeXY = getSlimeXY(app)
    for slimeX, slimeY in slimeXY: 
        diffX = app.mc.x - slimeX
        diffY = app.mc.y - slimeY
        if ((diffX < 3* app.cellSize/2 and diffX > -3*app.cellSize/2) and \
            (diffY > - 3*app.cellSize/2 and diffY < 3*app.cellSize/2)):
            app.lives -= 1
        if app.lives == 0: 
            app.mode = "gameOver"

def slimeMovements(app):
    for slime in app.slimes:
        slimeX, slimeY = slime.x, slime.y
        if not app.torchOn:
            index = app.slimes.index(slime)
            target = app.randomTargetCoordinates[index]
            targetRow, targetCol = getRowCol(app, target[0], target[1])
            changeSlimePosition(app, slime, slimeX, slimeY, targetRow, targetCol)

        if app.torchOn: 
            # target is the main character
            if app.slimes.index(slime) % 2 == 0:
                target = [app.mc.x, app.mc.y]
            # target is 5 steps ahead of the main character
            elif app.slimes.index(slime) % 2 == 1: 
                if app.mc.direction == "d0":
                    target = [app.mc.x, app.mc.y+5*app.cellSize]
                if app.mc.direction == "r1":
                    target = [app.mc.x+5*app.cellSize, app.mc.y]
                if app.mc.direction == "u2":
                    target = [app.mc.x, app.mc.y-5*app.cellSize]
                if app.mc.direction == "l3":
                    target = [app.mc.x-5*app.cellSize, app.mc.y] 
            # in row col format
            targetRow, targetCol = getRowCol(app, target[0], target[1])
            # in x, y format
            changeSlimePosition(app, slime, slimeX, slimeY, targetRow, targetCol)

def changeSlimePosition (app,slime, x, y, trow,tcol): # target row, target col
    currDirection = slime.direction
    if currDirection == "d0":
        allowed = ((0,1),(1,0),(-1,0))
        notAllowed = (0,-1)
    elif currDirection == "r1":
        allowed = ((0,-1),(0,1),(1,0))
        notAllowed = (-1,0)
    elif currDirection == "u2":
        allowed = ((0,-1),(1,0),(-1,0))
        notAllowed = (0,1)
    elif currDirection == "l3":
        allowed = ((0,1),(-1,0),(0,-1))
        notAllowed = (1,0)
    
    distances = {}
    row,col = getRowCol(app,x,y)

    #building a dictionary of each move mapped to distance from target
    for dir in allowed: 
        if slimeMoveIsLegal(app, row, col, dir[0], dir[1]):
            distances[dir] = distance(trow, tcol, row + dir[0], col + dir[1])
    
    best = (app.rows + app.cols) * app.cellSize # bigger than max possible distance
    bestDir = None
    for dir in distances: 
        if distances[dir] < best: 
            best = distances[dir]
            bestDir = dir

    # turn around if no other move is legal
    if best == (app.rows + app.cols) * app.cellSize:
        bestDir = notAllowed
    
    newRow, newCol = row + bestDir[0], col + bestDir[1]
    x1,x2,y1,y2 = cellBounds(app, newRow, newCol)

    if bestDir == (1,0): slime.direction = "r1" # "d0"
    if bestDir == (0,1): slime.direction = "d0" # "l3"
    if bestDir == (0,-1): slime.direction = "u2" # "r1"
    if bestDir == (-1,0): slime.direction = "l3" # "u2"

    # updates slime position
    slime.x = (x1+x2)//2
    slime.y = (y1+y2)//2
    
def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def drawMCTorch(app, canvas): 
    if app.mc.direction == "d0":
        canvas.create_image(app.mc.x+(app.cellSize//2), app.mc.y-(app.cellSize//5), \
            image = ImageTk.PhotoImage(app.mcTorch))
    if app.mc.direction == "l1":
        canvas.create_image(app.mc.x+(app.cellSize//4), app.mc.y-(app.cellSize//5), \
            image = ImageTk.PhotoImage(app.mcTorch))
    if app.mc.direction == "r3":
        canvas.create_image(app.mc.x+(app.cellSize//4), app.mc.y-(app.cellSize//5), \
            image = ImageTk.PhotoImage(app.mcTorch))

#####################
# won game mode
#####################

def won_mousePressed(app, event):
    x = 17 * app.width// 26
    dWidth = app.width//8
    dHeight = app.height//10
    y = 3 * app.height//4
    if event.x > x - dWidth and event.x < x + dWidth and \
        event.y > y - dHeight and event.y < y + dHeight: 
        app.mode = "start"
        reset(app)

def won_redrawAll(app, canvas):
    drawGround(app, canvas)
    messageBoxHeight = app.height // 5.8
    messageBoxWidth = app.width // 2.6
    youWon = app.youWonText
    canvas.create_rectangle(app.width//2 - messageBoxWidth, app.height//2 - \
        messageBoxHeight - app.height//6, app.width//2 + messageBoxWidth, app.height//2 + \
        messageBoxHeight - app.height//11, fill = "black")
    canvas.create_rectangle(app.width//2 - messageBoxWidth + app.width//20, app.height//2 - \
        messageBoxHeight - app.height//8, app.width//2 + messageBoxWidth - app.width//20, app.height//2 + \
        messageBoxHeight - app.height//7.6, fill = "#625D52")
    canvas.create_image(app.width//2, app.height*3//8, image=ImageTk.PhotoImage(youWon))

    drawEndCharacters(app, canvas)
    # draw torch
    endTorch = app.scaleImage(app.torchStartScreen, 0.18)
    canvas.create_image(5* app.width // 11, 4 * app.height//5 - 5, image=ImageTk.PhotoImage(endTorch))
    drawWonBackToHome(app, canvas)

def drawEndCharacters(app, canvas):
        main = MC.MC(0, 0, app.mainSprite, app.mcChoice)
        friend = MC.MC(0, 0, app.mainSprite, app.friendChoice)
        main = app.scaleImage(main.mainSprite["d0"][0], 3.5)
        friend = app.scaleImage(friend.mainSprite["d0"][0], 3.5)
        canvas.create_image(5* app.width//13, 3*app.height//4, image = ImageTk.PhotoImage(main))
        canvas.create_image(1*app.width//4, 3*app.height//4, image = ImageTk.PhotoImage(friend))

def drawWonBackToHome(app, canvas):
    x = 17 * app.width// 26
    y = 3 * app.height//4
    canvas.create_text(x, y, text = "RETURN \n  HOME", font = f"Helvetica \
        {int(app.width/22)} bold", fill = "#ffcd01")

#####################
# game over mode
#####################
def gameOver_mousePressed(app, event):
    # return home
    if event.x > 1*app.width//7 and event.x < 3*app.width//7 and \
        event.y > 11*app.height//16 and event.y < 13*app.height//16:
        app.mode = "start"
        reset(app)
    
    # retry level
    if event.x > 4*app.width//7 and event.x < 6*app.width//7 and \
        event.y > 11*app.height//16 and event.y < 13*app.height//16:
        app.mode = "gameplay"
        retry(app)

def gameOver_redrawAll(app, canvas):
    drawGround(app, canvas)
    messageBoxHeight = app.height // 5.8
    messageBoxWidth = app.width // 2.6
    gameOver = app.gameOverText
    canvas.create_rectangle(app.width//2 - messageBoxWidth, app.height//2 - \
        messageBoxHeight - app.height//6, app.width//2 + messageBoxWidth, app.height//2 + \
        messageBoxHeight - app.height//11, fill = "black")
    canvas.create_rectangle(app.width//2 - messageBoxWidth + app.width//50, app.height//2 - \
        messageBoxHeight - app.height//7.65, app.width//2 + messageBoxWidth - app.width//50, app.height//2 + \
        messageBoxHeight - app.height//8, fill = "#625D52")
    canvas.create_image(app.width//2, app.height*3//8, image=ImageTk.PhotoImage(gameOver))

    # draw torch
    endTorch = app.scaleImage(app.torchStartScreen, 0.3)
    canvas.create_image(app.width // 2, 4 * app.height//5 - 5, image=ImageTk.PhotoImage(endTorch))
    drawBackToHome(app, canvas)
    drawReplay(app, canvas)

def drawBackToHome(app, canvas):
    x = 2 * app.width// 7
    y = 3*app.height//4
    canvas.create_text(x, y, text = "RETURN \n  HOME", font = f"Helvetica \
        {int(app.width/25)} bold", fill = "#ffcd01")

def drawReplay(app, canvas):
    x = 5* app.width // 7
    y = 3*app.height//4
    canvas.create_text(x, y, text = "REPLAY", font = f"Helvetica \
        {int(app.width/25)} bold", fill = "#ffcd01")

#####################
#####################

def determineStartPosition(app):
    for row in range (1, app.rows-1):
        if app.maze[row][1] == "path":
            xPos = app.cellSize 
            yPos = row * app.cellSize + app.topMargin
            return xPos, yPos
    
def determineSlimeStartPosition(app):
    while True:  
        row = random.randint(2, app.rows-1)
        col = random.randint(2, app.cols-1)
        if app.maze[row][col] == "path" and [row,col] not in app.slimeCoordinates\
            and not (row > app.rows-6 and col > app.cols - 7)\
            and row != app.mc.y and col!= app.mc.x: 
            return [row, col] 

def getCellSize(app):
    maxWidth = int((app.width - 30) / app.cols)
    maxHeight = int((app.height - 30) / app.rows)
    return min(maxWidth, maxHeight)

def getMargin(app):
    mazeLength = app.cellSize * app.cols
    mazeHeight = app.cellSize * app.rows
    sideMargin = (app.width - mazeLength)/2
    topMargin = (app.height - mazeHeight)/2
    return sideMargin, topMargin

# modified from course notes
def cellBounds(app, row, col): 
    x1 = app.sideMargin + col * app.cellSize
    x2 = x1 + app.cellSize
    y1 = app.topMargin + row * app.cellSize
    y2 = y1 + app.cellSize
    return (x1, x2, y1, y2)

# modified from course notes
def drawCell(app, canvas, row, col, color):
    x1,x2,y1,y2 = cellBounds(app, row, col)
    canvas.create_rectangle(x1, y1, x2, y2, fill = color, width = 0)

####################################
# maze generation: prim's algorithm
####################################

'''
inspired by: 
https://en.wikipedia.org/wiki/Prim%27s_algorithm 
https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e 
'''

def makeMaze(app, numRemoved):
    maze = app.maze # initial maze
    startRow = random.randint(1,app.rows-2)
    startCol = random.randint(1,app.cols-2)
    maze[startRow][startCol] = "path"
    addSurroundingWalls(app, startRow, startCol)
    while app.mazeWalls != []:
        randIndex = random.randint(0, len(app.mazeWalls)-1)
        randWall = app.mazeWalls[randIndex]
        # checks left wall
        if randWall[1] != 0:
            if app.maze[randWall[0]][randWall[1]-1] == "?" and \
                maze[randWall[0]][randWall[1]+1] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "left", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks right wall
        if randWall[1] != app.cols-1:
            if app.maze[randWall[0]][randWall[1]+1] == "?" and \
                maze[randWall[0]][randWall[1]-1] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "right", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks up wall
        if randWall[0] != 0:
            if app.maze[randWall[0]-1][randWall[1]] == "?" and \
                maze[randWall[0]+1][randWall[1]] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "up", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks down wall
        if randWall[0] != app.rows-1:
            if app.maze[randWall[0]+1][randWall[1]] == "?" and \
                maze[randWall[0]-1][randWall[1]] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "down", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        removeWall(app, randWall[0], randWall[1])
    fillMaze(app)
    makeChamber(app)
    removeWalls(app, numRemoved)

def makeChamber(app):
    for row in range(-2,-6, -1):
        for col in range(-2,-7, -1):
            app.maze[row][col] = "path"
    app.maze[-3][-1] = "path"

def makeEntrance(app):
    entranceRow = getRowCol(app, 0, app.mcStartY)[0]
    app.maze[entranceRow][0] = "path"

# makes the maze have loops 
def removeWalls(app, numRemoved):
    count = 0
    while numRemoved > 0: 
        randomRow = random.randint(3,app.rows-3)
        randomCol = random.randint(3,app.cols-3)
        if app.maze[randomRow][randomCol] == "wall" and \
            (((app.maze[randomRow + 1][randomCol] == "path" and \
            app.maze[randomRow - 1][randomCol] == "path" and \
            app.maze[randomRow + 2][randomCol] == "path" and \
            app.maze[randomRow - 2][randomCol] == "path") or (
            app.maze[randomRow][randomCol-1] == "path" and \
            app.maze[randomRow][randomCol+1] == "path" and \
            app.maze[randomRow][randomCol-2] == "path" and \
            app.maze[randomRow][randomCol+2] == "path"
            ))):
            app.maze[randomRow][randomCol] = "path"
            numRemoved -= 1
        count += 1
        if count > 100: 
            break
    while numRemoved > 0: 
        randomRow = random.randint(2,app.rows-2)
        randomCol = random.randint(2,app.cols-2)
        if app.maze[randomRow][randomCol] == "wall" and \
            ((app.maze[randomRow + 1][randomCol] == "path" and \
            app.maze[randomRow - 1][randomCol] == "path") or (
            app.maze[randomRow][randomCol-1] == "path" and \
            app.maze[randomRow][randomCol+1] == "path")):
            app.maze[randomRow][randomCol] = "path"
            numRemoved -= 1

def fillMaze(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.maze[row][col] == "?":
                app.maze[row][col] = "wall"

def removeWall(app,row,col):
    for wall in app.mazeWalls:
        if wall == [row,col]:
            app.mazeWalls.remove(wall)

def addNewWalls(app, direction, randWall):
    row = randWall[0]
    col = randWall[1]
    if direction != "left": 
        if col != app.cols-1: # within bounds
            if app.maze[row][col+1] != "path":
                app.maze[row][col+1] = "wall"
            if app.maze[row][col+1] not in app.mazeWalls:
                app.mazeWalls.append([row,col+1])
    if direction != "right":
        if col != 0: # within bounds
            if app.maze[row][col-1] != "path":
                app.maze[row][col-1] = "wall"
            if app.maze[row][col-1] not in app.mazeWalls:
                app.mazeWalls.append([row,col-1])
    if direction != "up":
        if row != app.rows-1: # within bounds
            if app.maze[row+1][col] != "path":
                app.maze[row+1][col] = "wall"
            if app.maze[row+1][col] not in app.mazeWalls:
                app.mazeWalls.append([row+1,col])
    if direction != "down":
        if row != 0: # within bounds
            if app.maze[row-1][col] != "path":
                app.maze[row-1][col] = "wall"
            if app.maze[row-1][col] not in app.mazeWalls:
                app.mazeWalls.append([row-1,col])

# checks if the wall has 0 or 1 cells around it
def surroundingCells(app, randWall): 
    total = 0
    for direction in ((-1,0),(1,0),(0,1), (0,-1)):
        dRow = direction[0]
        dCol = direction[1]
        if app.maze[randWall[0] + dRow][randWall[1] + dCol] == "path":
            total += 1
    return total

def addSurroundingWalls(app, startRow, startCol):
    for direction in ((-1,0),(1,0),(0,1), (0,-1)):
        dRow = direction[0]
        dCol = direction[1]
        app.mazeWalls.append([startRow + dRow, startCol + dCol])
        app.maze[startRow + dRow][startCol + dCol] = "wall"

def moveCharacter(app, dX, dY):
    app.mc.x += dX
    app.mc.y += dY

# checks if a move is legal, and checks if it ends the game
def moveIsLegal(app, dx, dy): 
    newX, newY = app.mc.x + dx, app.mc.y + dy
    row, col = getRowCol(app, newX, newY)
   
    # entrance channel is legal
    if newX >= 10 and newX <= app.sideMargin + app.cellSize * 2 and \
        newY <= app.mcStartY + app.cellSize and newY >= app.mcStartY and \
        app.exitedChannel == False:
        return True

    # exit channel is legal if door is unlocked: 
    if app.doorUnlocked == True:
        if newX >= app.sideMargin + app.cols * app.cellSize and\
            newY > app.height - app.topMargin - 3 * app.cellSize and \
            newY < app.height - app.topMargin - 2 * app.cellSize:
                if newX >= app.sideMargin + app.cols * app.cellSize + app.sideMargin/3:
                    if app.foundFriend: 
                        app.mode = "won"
                app.torchOn == True
                return True
    elif app.doorUnlocked == False: 
        if newX >= app.width - app.sideMargin - app.cellSize and\
            newY > app.height - app.topMargin - 3 * app.cellSize and \
            newY < app.height - app.topMargin - 2 * app.cellSize:
                return False

    if row < 0 or col < 0:
        return False
    if app.maze[row][col] == "wall":
        return False
    else: return True

def slimeMoveIsLegal(app, row, col, drow, dcol): # checks if a move is legal
    newRow, newCol = (row + drow, col + dcol)
    if newRow < 0 or newCol < 0 or newRow > app.rows-1 or newCol > app.cols-1:
        return False
    elif app.maze[newRow][newCol] == "wall":
        return False
    elif app.maze[newRow][newCol] == "path" \
            and not (row > app.rows-6 and col > app.cols - 7): 
            return True

def updateLightCoordinates(app):
    app.lightCoordinates = set()
    playerRowCol = getRowCol(app, app.mc.x, app.mc.y)
    app.lightCoordinates.add((app.rows-3, app.cols-1))
    for row in range(app.rows - 6, app.rows-1):
        for col in range(app.cols-7, app.cols-1):
            app.lightCoordinates.add((row,col))
    slimeXY = getSlimeXY(app)
    slimeRowsCols = []
    for slime in slimeXY: 
        slimeRow, slimeCol = getRowCol(app, slime[0], slime[1])
        slimeRowsCols.append([slimeRow, slimeCol])

    # making the slimes glow
    for slimeRow, slimeCol in slimeRowsCols: 
        for row in range(app.rows):
            for col in range(app.cols):
                if isInRadius(app, row, col, slimeRow, slimeCol, app.rows//10):
                    app.lightCoordinates.add((row, col))

    if app.torchOn:
        for row in range(app.rows):
            for col in range(app.cols):
                if isInRadius(app, row, col, playerRowCol[0], playerRowCol[1], app.rows//6):
                    app.lightCoordinates.add((row,col))

def getSlimeXY(app):
    XYList = []
    for slime in app.slimes:
        x = slime.x
        y = slime.y
        XYList.append((x,y))
    return XYList

def isInRadius(app, row0, col0, row1, col1, distance):
    dist = math.sqrt((row0-row1)**2 + (col0-col1)**2)
    if dist < distance: 
        return True
    else: return False

def drawPassages(app, canvas):
    playerRowCol = getRowCol(app, app.mc.x, app.mc.y)
    if app.mc.x < app.sideMargin + app.cellSize and app.mc.y < app.sideMargin + app.cellSize\
        and app.torchOn:
        canvas.create_rectangle(0,0,app.sideMargin, app.mcStartY, fill = "black")
    else: 
        canvas.create_rectangle(0,0,app.sideMargin, app.mcStartY + app.cellSize, fill = "black")
    canvas.create_rectangle(0,0, app.width, app.topMargin, fill = "black")
    canvas.create_rectangle(app.cols * app.cellSize + app.sideMargin, \
                0, app.width, app.height - app.topMargin - 3 * app.cellSize, fill = "black")
    canvas.create_rectangle(app.cols * app.cellSize + app.sideMargin, \
                app.height - app.topMargin - 2 * app.cellSize, app.width, app.height, fill = "black")
    canvas.create_rectangle(0, app.topMargin + app.cellSize * app.rows, app.width, app.height, fill = "black")
    canvas.create_rectangle(0, app.mcStartY + app.cellSize, app.sideMargin, app.height, fill = "black")

def getRowCol(app, x, y): # modified from course notes
    row = int((y-app.topMargin)/app.cellSize)
    col = int((x-app.sideMargin)/app.cellSize)
    return row, col

def drawGround(app, canvas):
    for row in range(0,5):
        for col in range(0,4):
                canvas.create_image(row*app.width//4, col*app.height//4, image=app.ground)

def drawMaze(app, canvas):
    drawGround(app, canvas)
    drawPowerups(app, canvas)
    for row in range(app.rows):
        for col in range(app.cols):
                if (row,col) in app.lightCoordinates:
                    if app.maze[row][col] == "wall": 
                        drawCell(app, canvas, row, col, "#111111")
                # cell is black if it isn't in light coordinates
                elif (row,col) not in app.lightCoordinates:
                    drawCell(app, canvas, row, col, "black")
                elif app.maze[row][col] == "path": 
                    drawCell(app, canvas, row, col, "black")
    drawPassages(app, canvas)

runApp(width=1000, height=600)
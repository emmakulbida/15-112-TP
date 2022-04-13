import math, copy, random
from cmu_112_graphics import * 
from PIL import Image
import MC

'''
BUTTON CLASS 
'''

# width = 1000
# height = 600

def appStarted(app):
    app.mode = "start" # "start"
    app.sideMargin = 80 #None
    app.topMargin = 20 #None
    app.rows = 20
    app.cols = 30
    app.cellSize = 28 #None
    app.mcChoice = None # input from user
    app.levelChoice = None
    app.mainSprite = app.loadImage("chibi-layered.png")
    app.mainSpriteStart = app.scaleImage(app.mainSprite, app.cellSize/2)
    app.mcStartScreen0 = MC.MC(0, 0, app.mainSpriteStart, 0)

    app.mcStartScreen1 = MC.MC(0, 0, app.mainSpriteStart, 1)
    app.mcStartScreen2 = MC.MC(0, 0, app.mainSpriteStart, 2)
    app.mainSprite = app.scaleImage(app.mainSprite, app.cellSize / 10) # scale MC based on window size
    app.maze = [["?"] * app.cols for i in range(app.rows)]
    app.mazeWalls = []
    app.mcStartX = 0
    app.mcStartY = 0
    app.mc = None # MC.MC(app.mcStartX, app.mcStartY, app.mainSprite, app.mcChoice)
    #app.mcStartScreen = MC.MC(0, 0, app.mainSpriteStart, app.mcChoice)
    app.timerDelay = 20
    ground = app.loadImage("ground.jpeg")
    #ground = app.PhotoImage("ground1.jpeg")
    ground = app.scaleImage(ground, 1.2)
    app.ground = ImageTk.PhotoImage(ground)
    torch = app.loadImage("torch.png")
    app.torch = app.scaleImage(torch, app.cellSize/50)
    app.torchStartScreen = app.scaleImage(torch, app.cellSize/15)
    # app.ground.place


#####################
# start screen mode
#####################

def start_mousePressed(app, event):
    # if event.x < app.width and event.x > 0: # easy
    #     appStarted(app)
    #     app.rows = 20
    #     app.cols = 30
    #     app.cellSize = getCellSize(app)
    #     app.sideMargin, app.topMargin = getMargin(app)
    #     makeMaze(app, 0)
    #     app.mcStartX, app.mcStartY = determineStartPosition(app)
    #     makeEntrance(app)
    #     app.mc = MC.MC(app.mcStartX, app.mcStartY, app.mainSprite, app.mcChoice)
    #     #getMCPosition(app)
    #     #print("maze made!")

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
    torchBounds = (5 * app.width / 6, 7 * app.height / 10)
    if event.x > torchBounds[0] - app.width/20 and event.x < torchBounds[0] + app.width/20 \
        and event.y > torchBounds[1] - app.height/5.5 and event.y < torchBounds[1] + app.height/5.5:
        if app.mcChoice != None and app.levelChoice != None: 
            app.mode = "gameplay"
        
    
# def start_timerFired(app):
#     if app.mcChoice != None and app.levelChoice != None: 
#         app.mode = "gameplay"


def start_keyPressed(app, event):
    pass

def start_redrawAll(app, canvas):
    drawGround(app, canvas)
    if app.mcChoice != None: 
        drawCharacterChoice(app, canvas, app.mcChoice)
    # if app.levelChoice != None: 
    #     drawLevelChoice(app, canvas, app.levelChoice)
    drawCharacters(app, canvas)
    torchBounds = (5 * app.width / 6, 7 * app.height / 10)
    canvas.create_rectangle(torchBounds[0] - app.width/20, torchBounds[1] - app.height/5.5, \
        torchBounds[0] + app.width/20, torchBounds[1] + app.height/5.5, fill = "purple")
    drawTorch(app, canvas)
    #drawLevels(app, canvas)
    # drawTitle(app, canvas)
    #canvas.create_rectangle(0,0,app.width, app.height, fill = "black")
    

def drawTorch(app, canvas):
    canvas.create_image(5 * app.width / 6, 7 * app.height / 10, image = ImageTk.PhotoImage(app.torch))

# def drawLevelChoice(app, canvas, choice):
#     bounds = levelBounds(app, choice)


def drawCharacterChoice(app, canvas, choice):
    bounds = startScreenCharactersBounds(app, choice)
    sideBorder = app.width//21
    topBorder = app.height//40
    canvas.create_rectangle(bounds[0] - sideBorder, bounds[1] - topBorder, \
        bounds[2] + sideBorder, bounds[3] + topBorder, fill = "#404040", outline = "#707070")


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
        #print(f'character: {character}')
        canvas.create_image(midX, midY, image = ImageTk.PhotoImage(character.mainSprite["d0"][0]))
        i += 1
    
    # i = 0
    # character = app.mcStartScreen0.mainSprite["d0"][0]
    # canvas.create_image(midX, midY, image = ImageTk.PhotoImage(character))
    # i = 1
    # character = app.mcStartScreen1.mainSprite["d0"][0]
    # canvas.create_image(midX, midY, image = ImageTk.PhotoImage(character))
    # i = 2
    # character = app.mcStartScreen2.mainSprite["d0"][0]
    # canvas.create_image(midX, midY, image = ImageTk.PhotoImage(character))

    '''
    #app.mcStartScreen1 = MC.MC(0, 0, app.mainSpriteStart, i)
    #canvas.create_image(startX, startY, endX, endY, image=ImageTk.PhotoImage(character))
    canvas.create_rectangle(startX, startY, endX, endY, fill = "red")

    main = app.mc.mainSprite[app.mc.direction][app.mc.spriteCounter]
    #print(f'x: {app.mc.mainX}, y: {app.mc.mainY}')
    canvas.create_image(app.mc.x, app.mc.y - 15, image=ImageTk.PhotoImage(main))
    # character = app.mc.mainSprite["d0"][0]
    # canvas.create_image(startX, startY, endX, endY, image=ImageTk.PhotoImage(character))
    '''

#####################
# gameplay mode
#####################

def gameplay_mousePressed(app, event):
    pass

def gameplay_keyPressed(app, event):
    magnitude = 10
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

def gameplay_redrawAll(app, canvas):
    drawMaze(app, canvas)
    main = app.mc.mainSprite[app.mc.direction][app.mc.spriteCounter]
    #print(f'x: {app.mc.mainX}, y: {app.mc.mainY}')
    canvas.create_image(app.mc.x, app.mc.y - 15, image=ImageTk.PhotoImage(main))
    #canvas.create_rectangle(0,0,width,height,fill = "purple")
    # drawMaze(app)

def gameplay_timerFired(app):
    pass

#####################
# won game mode
#####################



#####################
# lost game mode
#####################




#####################
#####################

def determineStartPosition(app):
    for row in range (1, app.rows-1):
        if app.maze[row][1] == "path":
            # xPos = row * app.cellSize + app.sideMargin
            # xPos = app.sideMargin
            xPos = app.cellSize 
            yPos = row * app.cellSize + app.topMargin
            return xPos, yPos
    
def getCellSize(app):
    maxWidth = int((app.width - 30) / app.cols)
    maxHeight = int((app.height - 30) / app.rows)
    #print(f'width: {app.width}, height: {app.height}, maxWidth: {maxWidth}, maxHeight: {maxHeight}')
    return min(maxWidth, maxHeight)

def getMargin(app):
    mazeLength = app.cellSize * app.cols
    mazeHeight = app.cellSize * app.rows
    sideMargin = (app.width - mazeLength)/2
    topMargin = (app.height - mazeHeight)/2
    #print(f'mazeLength = {mazeLength}, mazeHeight = {mazeHeight}, sizeMargin = {sideMargin}, topMargin = {topMargin}')
    return sideMargin, topMargin

def cellBounds(app, canvas, row, col): # modified from course notes
    x1 = app.sideMargin + col * app.cellSize
    x2 = x1 + app.cellSize
    y1 = app.topMargin + row * app.cellSize
    y2 = y1 + app.cellSize
    return (x1, x2, y1, y2)

def drawCell(app, canvas, row, col, color): 
    x1,x2,y1,y2 = cellBounds(app, canvas, row, col)
    canvas.create_rectangle(x1, y1, x2, y2, fill = color, width = 0)

# def drawCorrectWall(app, canvas, row, col, color):
#     if surroundingCells(app, [row,col]) == 4: 
#         canvas.create_rectangle()
#     x1 = app.sideMargin + col * app.cellSize
#     x2 = x1 + app.cellSize
#     y1 = app.topMargin + row * app.cellSize
#     y2 = y1 + app.cellSize
#     canvas.create_rectangle(x1, y1, x2, y2, fill = "black", width = 0)

def makeMaze(app, numRemoved):
    maze = app.maze # initial maze
    startRow = random.randint(1,app.rows-2)
    startCol = random.randint(1,app.cols-2)
    maze[startRow][startCol] = "path"
    # startRow = 1
    # startCol = 1
    addSurroundingWalls(app, startRow, startCol)
    while app.mazeWalls != []:
        randIndex = random.randint(0, len(app.mazeWalls)-1)
        randWall = app.mazeWalls[randIndex]
        # checks left wall
        #print(f'randWall: {randWall}')
        if randWall[1] != 0:
            if app.maze[randWall[0]][randWall[1]-1] == "?" and maze[randWall[0]][randWall[1]+1] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "left", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks right wall
        if randWall[1] != app.cols-1:
            if app.maze[randWall[0]][randWall[1]+1] == "?" and maze[randWall[0]][randWall[1]-1] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "right", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks up wall
        if randWall[0] != 0:
            if app.maze[randWall[0]-1][randWall[1]] == "?" and maze[randWall[0]+1][randWall[1]] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "up", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks down wall
        if randWall[0] != app.rows-1:
            if app.maze[randWall[0]+1][randWall[1]] == "?" and maze[randWall[0]-1][randWall[1]] == "path":
                if surroundingCells(app, randWall) < 2:
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "down", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        removeWall(app, randWall[0], randWall[1])
    fillMaze(app)
    makeChamber(app)
    # while pathfinding algorithm > __: removeWalls
    removeWalls(app, numRemoved)

def makeChamber(app):
    for row in range(-2,-5, -1):
        for col in range(-2,-6, -1):
            print(app.maze[row][col])
            app.maze[row][col] = "path"
    app.maze[-3][-1] = "path"

def makeEntrance(app):
    print(f'app.mcStartY: {app.mcStartY}')
    print(f'ROWCOL: {getRowCol(app, 0, app.mcStartY)}')
    entranceRow = getRowCol(app, 0, app.mcStartY)[0]
    app.maze[entranceRow][0] = "path"

def removeWalls(app, numRemoved):
    while numRemoved > 0: 
        randomRow = random.randint(2,app.rows-2)
        randomCol = random.randint(2,app.cols-2)
        #print(f'randomRow: {randomRow}, randomCol : {randomCol}')
        if app.maze[randomRow][randomCol] == "wall":
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

def surroundingCells(app, randWall): # checks if the wall has 0 or 1 cells around it
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
        # print(f'[startRow + dRow, startCol + dCol]: {[startRow + dRow, startCol + dCol]}')
        app.mazeWalls.append([startRow + dRow, startCol + dCol])
        app.maze[startRow + dRow][startCol + dCol] = "wall"
        #print(app.maze)

def moveCharacter(app, dX, dY):
    app.mc.x += dX
    app.mc.y += dY

def moveIsLegal(app, dx, dy): # checks if a move is legal, and checks if it ends the game
    newX, newY = app.mc.x + dx, app.mc.y + dy
    row, col = getRowCol(app, newX, newY)
    # entrance channel is legal
    print(f'row: {row}, col :{col}')
    print(f'newX: {newX}, newY: {newY}')
    if newX >= 10 and newX <= app.sideMargin + app.cellSize * 2 and \
        newY <= app.mcStartY + app.cellSize and newY >= app.mcStartY:
        return True
    # exit channel is legal: 
    if newX >= app.sideMargin + app.cols * app.cellSize and\
        newY > app.height - app.topMargin - 3 * app.cellSize and \
        newY < app.height - app.topMargin - 2 * app.cellSize:
            if newX >= app.sideMargin + app.cols * app.cellSize + app.sideMargin/3:
                app.gameMode = "won"
                print("you win!")
            return True
    if row < 0 or col < 0:
        return False
    if app.maze[row][col] == "wall":
        return False
    else: return True

def drawPassages(app, canvas):
    canvas.create_rectangle(0,0,app.sideMargin, app.mcStartY, fill = "black")
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
                #canvas.create_line(0, 0, row * app.cellSize, col * app.cellSize, fill = "red")

def drawMaze(app, canvas):
    drawGround(app, canvas)
    for row in range(app.rows):
        for col in range(app.cols):
            if app.maze[row][col] == "wall": # wall
                #drawCorrectWall(app, canvas, row, col, "black")
                drawCell(app, canvas, row, col, "black")
            # elif app.maze[row][col] == "path": 
            #     drawCell(app, canvas, row, col, "black")
    drawPassages(app, canvas)

# def drawStartScreen(app, canvas):
#     drawGround(app, canvas)
#     canvas.create_rectangle(0,0,app.width, app.height, fill = "black")
#     canvas.create_text(app.width/2, app.height/2,text = 'press "S" to start', fill = "white")


runApp(width=1000, height=600)

import math, copy, random
from cmu_112_graphics import * 
from PIL import Image

# width = 1000
# height = 600

def keyPressed(app, event):
    if app.screen == "start":
        if event.key == "s":
            app.screen = "gameMode"
    
def mousePressed(app, event):
    # if app.screen == "start":
    if event.x < app.width and event.x > 0: 
        maze = [["?"] * app.cols for i in range(app.rows)]
        print(f'clicked: x:{event.x}')
        app.rows = 20
        app.cols = 30
        app.cellSize = getCellSize(app)
        app.sideMargin, app.topMargin = getMargin(app)
        makeMaze(app)
        print("maze made!")

        
def getCellSize(app):
    maxWidth = int((app.width - 30) / app.cols)
    maxHeight = int((app.height - 30) / app.rows)
    print(f'width: {app.width}, height: {app.height}, maxWidth: {maxWidth}, maxHeight: {maxHeight}')
    return min(maxWidth, maxHeight)

def getMargin(app):
    mazeLength = app.cellSize * app.cols
    mazeHeight = app.cellSize * app.rows
    sideMargin = (app.width - mazeLength)/2
    topMargin = (app.height - mazeHeight)/2
    print(f'mazeLength = {mazeLength}, mazeHeight = {mazeHeight}, sizeMargin = {sideMargin}, topMargin = {topMargin}')
    return sideMargin, topMargin

def drawCell(app, canvas, row, col, color): # modified from course notes
    x1 = app.sideMargin + col * app.cellSize
    x2 = x1 + app.cellSize
    y1 = app.topMargin + row * app.cellSize
    y2 = y1 + app.cellSize
    canvas.create_rectangle(x1, y1, x2, y2, fill = color, width = 0.5)

def appStarted(app):
    app.screen = "start" # "start"
    app.sideMargin = 80 #None
    app.topMargin = 20 #None
    app.rows = 20
    app.cols = 30
    app.cellSize = 28 #None
    app.player = 1
    app.mazeLevel = "easy"
    app.maze = [["?"] * app.cols for i in range(app.rows)]
    app.mazeWalls = []
    #app.maze[10][3] = "wall"
    print(app.maze)

def makeMaze(app):
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
        print(f'randWall: {randWall}')
        if randWall[1] != 0:
            if app.maze[randWall[0]][randWall[1]-1] == "?" and maze[randWall[0]][randWall[1]+1] == "path":
                if surroundingCells(app, randWall):
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "left", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks right wall
        if randWall[1] != app.cols-1:
            if app.maze[randWall[0]][randWall[1]+1] == "?" and maze[randWall[0]][randWall[1]-1] == "path":
                if surroundingCells(app, randWall):
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "right", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks up wall
        if randWall[0] != 0:
            if app.maze[randWall[0]-1][randWall[1]] == "?" and maze[randWall[0]+1][randWall[1]] == "path":
                if surroundingCells(app, randWall):
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "up", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        # checks down wall
        if randWall[0] != app.rows-1:
            if app.maze[randWall[0]+1][randWall[1]] == "?" and maze[randWall[0]-1][randWall[1]] == "path":
                if surroundingCells(app, randWall):
                    app.maze[randWall[0]][randWall[1]] = "path"
                    addNewWalls(app, "down", randWall)
                removeWall(app, randWall[0], randWall[1])
                continue
        removeWall(app, randWall[0], randWall[1])
    fillMaze(app)

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
    if total < 2: return True
    else: return False 

def addSurroundingWalls(app, startRow, startCol):
    for direction in ((-1,0),(1,0),(0,1), (0,-1)):
        dRow = direction[0]
        dCol = direction[1]
        print(f'[startRow + dRow, startCol + dCol]: {[startRow + dRow, startCol + dCol]}')
        app.mazeWalls.append([startRow + dRow, startCol + dCol])
        app.maze[startRow + dRow][startCol + dCol] = "wall"
        print(app.maze)

def redrawAll(app, canvas):
    if app.screen == "start":
        drawStartScreen(app, canvas)
    if app.screen == "gameMode":
        drawMaze(app, canvas)
    #canvas.create_rectangle(0,0,width,height,fill = "purple")
    # drawMaze(app)

def drawMaze(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.maze[row][col] == "wall": # wall
                drawCell(app, canvas, row, col, "black")
            elif app.maze[row][col] == "?": # unvisited
                drawCell(app, canvas, row, col, "tan")
            elif app.maze[row][col] == "path": 
                drawCell(app, canvas, row, col, "white")

def drawStartScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = "black")
    canvas.create_text(app.width/2, app.height/2,text = 'press "S" to start', fill = "white")
    

runApp(width=1000, height=600)

#sasha slepnev
#pong
from cmu_graphics import*
import random


app.width = 1250
app.height = 900

#variables/necessary things
score = 0
score2 = 0
misses = 0
speed = 6
myY = 0
targetY = 0
ballspeedX = 8
ballspeedY = 9
paddleSpeed = 6
gameOver = False
gameRunning = False
currentLevel = None


#structural elements (continuation of variables)
bg = Rect(0,0,1250,900, fill = 'black', visible = False)
me = Rect(10,400,15,100, fill = 'white', visible = False)
target = Rect(1225,400,15,100, fill = 'white', visible = False)
ball = Circle(625,450,15, fill = 'white', visible = False)
centerline = Line(625,900,625,0, fill = 'white', dashes = True, visible = False)

counter2 = Label(score2,500,25,fill = 'white', size = 40, visible = False)
counter1 = Label(score,750,25, fill = 'white', size = 40, visible = False)
missLabel = Label(misses,625,60, fill = 'white', size = 40, visible = False)

gameOverLabel = Label('GAME OVER', 625, 400, size = 90, fill = "red", visible = False)
retryBtn = Rect(450, 500, 350, 70, fill="lightgray", visible=False)
retryLabel = Label("Retry Level", 625, 535, size=35, fill="black", visible=False)

menuBtn = Rect(450, 600, 350, 70, fill="lightgray", visible=False)
menuLabel = Label("Choose Level", 625, 635, size=35, fill="black", visible=False)

title = Label("SELECT YOUR LEVEL", 625, 200, size=70, fill='black')

easyBtn = Rect(450, 350, 350, 70, fill='lightgray')
easyLabel = Label("EASY", 625, 385, size=35, fill='black')

mediumBtn = Rect(450, 450, 350, 70, fill='lightgray')
mediumLabel = Label("MEDIUM", 625, 485, size=35, fill='black')

hardBtn = Rect(450, 550, 350, 70, fill='lightgray')
hardLabel = Label("HARD", 625, 585, size=35, fill='black')

#show/hide game functions
def showGame():
    for obj in [bg, me, target, ball, centerline,
                counter1, counter2, missLabel]:
        obj.visible = True

def hideGame():
    for obj in [bg, me, target, ball, centerline,
                counter1, counter2, missLabel]:
        obj.visible = False

def showMenu():
    title.visible = True
    easyBtn.visible = True
    easyLabel.visible = True
    mediumBtn.visible = True
    mediumLabel.visible = True
    hardBtn.visible = True
    hardLabel.visible = True

def hideMenu():
    title.visible = False
    easyBtn.visible = False
    easyLabel.visible = False
    mediumBtn.visible = False
    mediumLabel.visible = False
    hardBtn.visible = False
    hardLabel.visible = False

#level select
def selectLevel(levelName):
    global ballspeedX, ballspeedY, paddleSpeed, currentLevel, gameRunning

    currentLevel = levelName

    if levelName == "easy":
        ballspeedX = 6
        ballspeedY = 7
        paddleSpeed = 8
    elif levelName == "medium":
        ballspeedX = 8
        ballspeedY = 9
        paddleSpeed = 6
    elif levelName == "hard":
        ballspeedX = 10
        ballspeedY = 11
        paddleSpeed = 4

    resetGame()
    hideMenu()
    showGame()
    gameRunning = True

#very large onstep to make me not be able to leave the border plus a million other things
def onStep():
    global targetY, ballspeedX, ballspeedY, score, score2, misses, gameOver

    if not gameRunning:
        return

    if gameOver:
        return

    if (me.centerY > 950):
        me.centerY = -50
    if (me.centerY < -50):
        me.centerY = 950
    if (target.centerY > 950):
        target.centerY = -50
    if (target.centerY < -50):
        target.centerY = 950
    if (ball.centerY > 845):
        ballspeedY = -9
    if (ball.centerY < 30):
        ballspeedY = 9

    ball.centerX += ballspeedX
    ball.centerY += ballspeedY
    me.centerY += myY
    target.centerY += targetY

    #ball bouncing off paddles
    #also the ballspeedX < 0 and whatnot because if i dont have it, it scores 2 each hit for some reason.
    if ball.hitsShape(me) and ballspeedX < 0:
        ballspeedX = 8
        score2 += 1
        counter2.value = score2

    if ball.hitsShape(target) and ballspeedX > 0:
        ballspeedX = -8
        score += 1
        counter1.value = score
    
    if ball.centerX > app.width + 20:
        misses += 1
        missLabel.value = misses
        ball.centerX = 625
        ball.centerY = 450
        ballspeedX = -8
    
    if ball.centerX < - 20:
        misses += 1
        missLabel.value = misses
        ball.centerX = 625
        ball.centerY = 450
        ballspeedX = 8
    
    if misses >= 5:
        gameOver = True
        gameOverLabel.visible = True
        retryBtn.visible = True
        retryLabel.visible = True
        menuBtn.visible = True
        menuLabel.visible = True

#hide certain text/buttons when you choose to change your level after loss, not tg with earlier hide b/c this was a later fix i made and i'm too lazy to combine them
def hideGameOver():
    gameOverLabel.visible = False
    retryBtn.visible = False
    retryLabel.visible = False
    menuBtn.visible = False
    menuLabel.visible = False

#reset game after game over
def resetGame():
    global score, score2, misses, ballspeedX, ballspeedY, gameOver, gameRunning
    
    score = 0
    score2 = 0
    misses = 0 

    me.centerY = 450
    target.centerY = 450
    ball.centerX = 625
    ball.centerY = 450

    counter1.value = score
    counter2.value = score2
    missLabel.value = misses
    
    gameOverLabel.visible = False
    retryBtn.visible = False
    retryLabel.visible = False
    menuBtn.visible = False
    menuLabel.visible = False

    gameOver = False

#moving me and target detailed in later comment
def onKeyPress(key):
    global myY, targetY

    if not gameRunning:
        return
    
    if (key == "s"):
        myY = paddleSpeed
    if (key == "w"):
        myY = -paddleSpeed
    if (key == "up"):
        targetY = -paddleSpeed
    if (key == "down"):
        targetY = paddleSpeed

#on key release function to stop moevemnt of the person
def onKeyRelease(key):
    global myY, targetY
    if (key == "s"):
        myY = 0
    if(key == "w"):
        myY = 0
    if (key == "up"):
        targetY = 0
    if(key == "down"):
        targetY = 0

#click to restart and level selection
def onMousePress(x, y):
    global gameRunning

    if easyBtn.visible and easyBtn.hits(x,y):
        selectLevel("easy")
    if mediumBtn.visible and mediumBtn.hits(x,y):
        selectLevel("medium")
    if hardBtn.visible and hardBtn.hits(x,y):
        selectLevel("hard")
    
    if gameOver:
        if retryBtn.hits(x,y):
            resetGame()
        if menuBtn.hits(x,y):
            hideGame()
            showMenu()
            hideGameOver()
            gameRunning = False
        
#show menu on start
showMenu()


cmu_graphics.run()

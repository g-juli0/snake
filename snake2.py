# Gianna Julio
# Period 7-8 HCP
# Snake (improved version)

import pygame, sys, math, random

# initialize game engine
pygame.init()

# open and set window size
w = 520
h = 520
size = (w, h)
surface = pygame.display.set_mode(size)

# set title bar
pygame.display.set_caption("Snake")

# color constants
BLACK  = (  0,   0,   0)
GRAY   = (100, 100, 100)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
ORANGE = (255, 144,   0)
YELLOW = (255, 255,   0)
LGREEN = (  0, 255,   0)
DGREEN = (  0, 145,   0)
LBLUE  = (  0, 255, 255)
DBLUE  = (  0,   0, 255)
PURPLE = (200,   0, 255)
PINK   = (255,   0, 200)

COLOR_LIST = [PINK, PURPLE, DBLUE, LBLUE, DGREEN, LGREEN, YELLOW, ORANGE, RED]

# initialize game font
FONT = "Times New Roman"

# initialize clock
clock = pygame.time.Clock()

# initialize size
numRows = 20
numCols = 20

# initialize sounds
eatSound = pygame.mixer.Sound("beep2.ogg")
bonusSound = pygame.mixer.Sound("match1.wav")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Functions:

''' creates empty board, places snake head in the middle, and places one food randomly '''
def loadBoard():
    # initialize board
    snakeBoard = []
    
    for row in range(numRows):
        snakeBoard.append([0] * numCols)
    
    # place snake head in middle of board
    snakeBoard[numRows//2][numCols//2] = 1
    
    # places food
    placeFood(snakeBoard)
    
    return snakeBoard

''' prepares message to blit to screen '''
def showMessage(words, size, fontName, xLoc, yLoc, color, bg=None):
    font = pygame.font.SysFont(fontName, size, True, False)
    text = font.render(words, True, color, bg)
    
    # get bounding box
    textBounds = text.get_rect()
    
     # center text at (xLoc, yLoc)
    textBounds.center = (xLoc, yLoc)
    
    return text, textBounds

''' moves the snake by placing a new head and removing the tail '''
def moveSnake(board, dRow, dCol, gameState, score, superCount):
    headRow, headCol = findSnakeHead(board)
    headVal = board[headRow][headCol]
    headRow += dCol
    headCol += dRow
    
    # checks if the snake has hit the edges
    if headRow < 0 or headRow > len(board)-1:
        return True, score, superCount
    elif headCol < 0 or headCol > len(board[0])-1:
        return True, score, superCount
    # checks if the snake has run into itself 
    elif board[headRow][headCol] > 0:
        return True, score, superCount
    # checks if the snake has eaten a piece of food
    elif board[headRow][headCol] == -1:
        board[headRow][headCol] = headVal + 1 # make the snake longer
        placeFood(board)
        eatSound.play()
        score += 10
    # checks if snake has eaten bonus
    elif board[headRow][headCol] == -2:
        board[headRow][headCol] = headVal + 1
        bonusSound.play()
        score += 50
    # checks if snake has eaten super food
    elif board[headRow][headCol] == -3:
        board[headRow][headCol] = headVal + 1
        bonusSound.play()
        score += 100
        superCount += 1
    else:
        # if just moving normally, add a temporary head, then remove the tail
        board[headRow][headCol] = headVal + 1
        board = removeTail(board)
    
    return gameState, score, superCount

''' finds the row and column of the snake head on the board '''
def findSnakeHead(board):
    maxi = 0 ## maximum value is at the head of the snake
    row = 0
    col = 0
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] > maxi:
                row = r
                col = c
                maxi = board[r][c]
    return row, col

''' subtracts one from each value of the snake, removing the tail '''
def removeTail(board):
    for row in range(len(board)):
        for col in range(len(board)):
            # if part of snake
            if board[row][col] > 0:
                board[row][col] -= 1

''' changes the direction of the snake based on user's keypress '''            
def getDirection(event):
    dRow = 0
    dCol = 0
    
    if event.key == pygame.K_RIGHT:
        dCol += 1
    if event.key == pygame.K_LEFT:
        dCol -= 1
    if event.key == pygame.K_UP:
        dRow -= 1
    if event.key == pygame.K_DOWN:
        dRow += 1

    return dRow, dCol

''' places one food randomly in board, making sure its not on snake '''
def placeFood(board):
    valid = False
    while not(valid):
        randRow = random.randint(1, len(board)-1)
        randCol = random.randint(1, len(board)-1)
        
        # if not on snake
        if board[randRow][randCol] == 0:
            board[randRow][randCol] = -1
            valid = True
            
''' places a bonus food - 1/200 chance '''
def placeBonus(board):
    num = random.randint(0, 200)
    
    if num == 4: ## 1/200 chance, i just like the number 4
        valid = False
        while not(valid):
            randRow = random.randint(1, len(board)-1)
            randCol = random.randint(1, len(board)-1)
            
            # if not on snake
            if board[randRow][randCol] == 0:
                board[randRow][randCol] = -2
                valid = True

''' places a super food - 1/2000 chance '''
def placeSuper(board):
    num = random.randint(0, 2000)
    
    if num == 4: ## 1/2000 chance, i just like the number 4
        valid = False
        while not(valid):
            randRow = random.randint(1, len(board)-1)
            randCol = random.randint(1, len(board)-1)
            
            # if not on snake
            if board[randRow][randCol] == 0:
                board[randRow][randCol] = -3
                valid = True

''' reads scores from file and returns top num names:scores into dict '''
def loadScores(num):
    allScores = condenseFile()
    
    values = sorted(list(allScores.values())) ## sorts values
    
    topScores = {}
    top = []
    
    # creates new dict with only top 5
    if len(allScores) > num:
        pos = -1
        for i in range(num):
            top.append(values[pos])
            pos -= 1
    
    for name in allScores:
        for each in top:
            if allScores[name] == each:
                topScores[name] = each
    
    return topScores, top

''' gets and returns user's name for leaderboard '''
def getName(name, letter):
    if len(name) < 12: ## cannot be longer than 12 letters
        # if letter entered is actually a letter
        if letter >= 'a' and letter <= 'z':
            name += letter
    
    return name

''' appends user's name and score to highscore file '''
def addToScores(name, score):
    # open file
    highscores = open("highscores2.txt", 'a')
    line = name + " " + str(score) + "\n" ## combines name and score into one line
    
    # writes line to file
    highscores.write(line)
    
    # close file
    highscores.close()
    
    condenseFile()

''' makes sure each username and score is only recorded once (takes highest score only for each username) '''
def condenseFile():
    allScores = {}
    
    # opens file in a loop
    with open("highscores2.txt") as highscores:
        for line in highscores:
            line = line.strip("\n").split()
            name, score = line[0], int(line[1])
            if name in allScores: ## if already in dict, use higher score
                if allScores[name] < score:
                    allScores[name] = score
            else:
                allScores[name] = score
    
    # close file           
    highscores.close()
    
    # re-open file just to be safe
    highscores = open("highscores2.txt", 'w')
    for name in allScores: 
        ## copy contents of allScores to file, which holds the highest score for each username
        highscores.write(name + " " + str(allScores[name]) + "\n")
    
    # close file           
    highscores.close()
    
    return allScores

''' checks for mouseOver for directions and leaderboard buttons on title screen '''
def checkButtons(gameState, event, buffer):
    # initialize bounds
    directionsText, directionsBounds = showMessage(" Instructions ", 30, FONT, w/3 - buffer, h/3, BLACK, WHITE)
    scoresText, scoresBounds = showMessage(" Leaderboard ", 30, FONT, 2*w/3 + buffer, h/3, BLACK, WHITE)
    
    # instructions button
    if directionsBounds.collidepoint(pygame.mouse.get_pos()):
        directionsText, directionsBounds = showMessage(" Instructions ", 30, FONT, w/3 - buffer, h/3, WHITE, GRAY)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            gameState = "I"
    else:
        directionsText, directionsBounds = showMessage(" Instructions ", 30, FONT, w/3 - buffer, h/3, BLACK, WHITE)        
    surface.blit(directionsText, directionsBounds)
    
    # leaderboard button
    if scoresBounds.collidepoint(pygame.mouse.get_pos()):
        scoresText, scoresBounds = showMessage(" Leaderboard ", 30, FONT, 2*w/3 + buffer, h/3, WHITE, GRAY)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            gameState = "SCORES"
    else:
        scoresText, scoresBounds = showMessage(" Leaderboard ", 30, FONT, 2*w/3 + buffer, h/3, BLACK, WHITE)
    surface.blit(scoresText, scoresBounds)
    
    return gameState

''' updates clock tick speed based on player's score so snake moves faster '''
def updateTick(score, superCount):
    return 9 + score//100 - (2*superCount)

def drawX(x, y, width, height):
    pygame.draw.line(surface, GRAY, (x, y), (x + width, y + height), 5)
    pygame.draw.line(surface, GRAY, (x, y + height), (x+ width, y), 5)

''' draws instructions screen '''
def drawInstructions(board, effect):
    # set background color
    surface.fill(RED)
    
    buffer = len(board)//2 ## leaves space around the outside
    pygame.draw.rect(surface, BLACK, (buffer, buffer, w-(buffer*2), h-(buffer*2)))
    
    # text
    instructionsText, instructionsBounds = showMessage("Instructions", 28, FONT, w/2, h/10, WHITE)
    surface.blit(instructionsText, instructionsBounds)
    
    text1, bounds1 = showMessage("Use the arrow keys to move your snake.", 16, FONT, w/2, h/5, WHITE)
    surface.blit(text1, bounds1)
    
    text2, bounds2 = showMessage("Collect white or gray food to grow your snake and earn points.", 16, FONT, w/2, 3*h/10, WHITE)
    surface.blit(text2, bounds2)
    
    text3, bounds3 = showMessage("Dont run into the walls or your snake's tail, or you lose the game.", 16, FONT, w/2, 2*h/5, WHITE)
    surface.blit(text3, bounds3)
    
    # point values
    foodRect = pygame.Rect(w/4, h/2, (w-2*buffer)//len(board), (h-2*buffer)//len(board))
    bonusRect = pygame.Rect(3*w/4, h/2, (w-2*buffer)//len(board), (h-2*buffer)//len(board))
    bonusRect.x = bonusRect.x - 2*(bonusRect.w*2)
    superRect = pygame.Rect(2*w/5 - buffer, 2*h/3, (w-2*buffer)//len(board), (h-2*buffer)//len(board))
    superRect.x = superRect.x - (superRect.w*2)
    
    if(effect == "square"):
        pygame.draw.rect(surface, WHITE, foodRect) ## white food
        pygame.draw.rect(surface, GRAY, bonusRect) ## gray bonus
        pygame.draw.rect(surface, random.choice(COLOR_LIST), superRect) ## rainbow bonus
    else:
        pygame.draw.ellipse(surface, WHITE, foodRect) ## white food
        pygame.draw.ellipse(surface, GRAY, bonusRect) ## gray bonus
        pygame.draw.ellipse(surface, random.choice(COLOR_LIST), superRect) ## rainbow bonus
    
    foodText, foodBounds = showMessage("+ 10 points", 14, FONT, w/3 + 2*buffer, 26*h/50, WHITE)
    surface.blit(foodText, foodBounds)
    
    bonusText, bonusBounds = showMessage("+ 50 points", 14, FONT, 2*w/3 + buffer, 26*h/50, WHITE)
    surface.blit(bonusText, bonusBounds)
    
    superText, superBounds = showMessage("+ 100 points, slows snake speed", 14, FONT, w/2 + 2*buffer, 2*h/3 + 1.5*buffer, WHITE)
    surface.blit(superText, superBounds)    
    
    #lockText1, lockBounds1 = showMessage("The higher the score you get,", 16, FONT, w/2, 3*h/5 + 4*buffer, WHITE)
    #surface.blit(lockText1, lockBounds1)
    
    #lockText2, lockBounds2 = showMessage("the more colors you unlock for your snake!", 16, FONT, w/2, 7*h/10 + 2*buffer, WHITE)
    #surface.blit(lockText2, lockBounds2)    
    
    spaceText, spaceBounds = showMessage("Press Space to return to the title screen", 20, FONT, w/2, 9*h/10, WHITE)
    surface.blit(spaceText, spaceBounds)

''' draws leaderboard screen '''
def drawHighscores(board, topScores, name):
    # set background color
    surface.fill(RED)
    
    buffer = len(board)//2 ## leaves space around the outside
    pygame.draw.rect(surface, BLACK, (buffer, buffer, w-(buffer*2), h-(buffer*2)))
    
    # text
    scoresText, scoresBounds = showMessage("Leaderboard", 28, FONT, w/2, h/10, WHITE)
    surface.blit(scoresText, scoresBounds)
    
    # load in top 10
    top10List, top10= loadScores(10)
    
    # loop through highscores list
    height = h/5
    i = 1
    usedNames = []
    CLR = WHITE
    for value in sorted(list(top10List.values()))[::-1]: ## sorted highest to lowest
        for key in top10List:
            if top10List[key] == value and key not in usedNames:
                if (key == name):
                    CLR = YELLOW ## if user is signed in and on the leaderboard, score is highlighted in yellow
                else:
                    CLR = WHITE
                numText, numBounds = showMessage(str(i), 20, FONT , w/4 + 2*buffer, height, CLR)
                surface.blit(numText, numBounds)
                keyText, keyBounds = showMessage(key, 20, FONT , w/3 + 5*buffer, height, CLR)
                surface.blit(keyText, keyBounds)
                valueText, valueBounds = showMessage(str(top10List[key]), 20, FONT , 2*w/3 + 2*buffer, height, CLR)
                surface.blit(valueText, valueBounds)
                height += h/15
                i += 1
                usedNames.append(key)    
    
    spaceText, spaceBounds = showMessage("Press Space to return to the title screen", 20, FONT, w/2, 9*h/10, WHITE)
    surface.blit(spaceText, spaceBounds) 

def drawTitleScreen(board, name, added, event, gameState, COLOR, EFFECT, color, effect, allScores):
    #set background color
    surface.fill(RED)
    
    buffer = len(board)//2 ## leaves space around the outside
    pygame.draw.rect(surface, BLACK, (buffer, buffer, w-(buffer*2), h-(buffer*2)))
    
    # text
    welcomeText1, welcomeBounds1 = showMessage("Welcome to Snake!", 36, FONT , w/2, h/10, WHITE)
    welcomeText2, welcomeBounds2 = showMessage("Welcome to Snake!", 36, FONT , w/2 - buffer/4, h/10 + buffer/4, random.choice(COLOR_LIST))
    ##welcomeText3, welcomeBounds3 = showMessage("Welcome to Snake!", 36, FONT , w/2 - buffer/2, h/10 + buffer/2, YELLOW)
    ##surface.blit(welcomeText3, welcomeBounds3)
    surface.blit(welcomeText2, welcomeBounds2)    
    surface.blit(welcomeText1, welcomeBounds1)
    ## blit text multiple times in slightly different pos for 3D effect
    
    nameText, nameBounds = showMessage("Username: " + name, 20, FONT , w/2, h/5, WHITE)
    surface.blit(nameText, nameBounds)
    
    if added == True:
        if name in allScores:
            addedText, addedBounds = showMessage("Welcome back, " + name, 14, FONT, w/2, h/4, WHITE)
        else:
            addedText, addedBounds = showMessage("Hello, " + name, 14, FONT, w/2, h/4, WHITE)
    else:
        addedText, addedBounds = showMessage("Please enter a username", 14, FONT, w/2, h/4, WHITE)
        
    surface.blit(addedText, addedBounds)

    choose1Text, choose1Bounds = showMessage("Choose a color", 20, FONT, w/3, h/2, WHITE)
    surface.blit(choose1Text, choose1Bounds)
    
    colorText, colorBounds = showMessage("Color selected: " + color, 16, FONT, 2*w/3, h/2, COLOR)
    surface.blit(colorText, colorBounds)
    
    choose2Text, choose2Bounds = showMessage("Choose an effect", 20, FONT, w/3, 7*h/10, WHITE)
    surface.blit(choose2Text, choose2Bounds)    
    
    effectText, effectBounds = showMessage("Effect selected: " + effect, 16, FONT, 2*w/3, 7*h/10, WHITE)
    surface.blit(effectText, effectBounds)    
    
    spaceText, spaceBounds = showMessage("Press Space to start", 20, FONT, w/2, 9*h/10, WHITE)
    surface.blit(spaceText, spaceBounds)
    
    # buttons
    gameState = checkButtons(gameState, event, buffer)
    
    # colors
    ## initialize each color button
    red = pygame.Rect(w/10 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    orange = pygame.Rect(w/5 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    yellow = pygame.Rect(3*w/10 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    lgreen = pygame.Rect(2*w/5 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    dgreen = pygame.Rect(w/2 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    lblue = pygame.Rect(3*w/5 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    dblue = pygame.Rect(7*w/10 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    purple = pygame.Rect(4*w/5 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    pink = pygame.Rect(9*w/10 - buffer, 3*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    
    ## compile into lists
    buttonList = [pink, purple, dblue, lblue, dgreen, lgreen, yellow, orange, red]
    selectedList = ["pink", "purple", "blue", "light blue", "dark green", "green", "yellow", "orange", "red"]    
    
    ## check for mouseOver and mouseClick for each color button
    for i in range(len(buttonList)):
        if buttonList[i].collidepoint(pygame.mouse.get_pos()):
            selected = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                color = selectedList[i]
                COLOR = COLOR_LIST[i]
        else:
            selected = False
        pygame.draw.ellipse(surface, COLOR_LIST[i], buttonList[i]) ## draw each color button
        #drawX(buttonList[i].x, buttonList[i].y, buttonList[i].w, buttonList[i].h)
        if(selected or color == selectedList[i]):
            pygame.draw.ellipse(surface, WHITE, buttonList[i], 3) ## if color has been selected, outline in white
    
    ## draw square
    square = pygame.Rect(w/4 + buffer, 4*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    pygame.draw.rect(surface, DBLUE, square)
    
    # effects
    ## draw gradient
    gradient = pygame.Rect(5*w/12 + buffer, 4*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    b = 255
    
    while(b > 50):
        pygame.draw.ellipse(surface, (255, 255, b), gradient)
        b -= 50
        gradient.x += 10
    
    gradientButton = pygame.Rect(5*w/12 + buffer, 4*h/5 - buffer, (w - (buffer * 2))/len(board) + 40, (h - (buffer * 2))/len(board))

    ## draw rainbow
    rainbow = pygame.Rect(2*w/3 + buffer, 4*h/5 - buffer, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board))
    for c in COLOR_LIST:
        pygame.draw.ellipse(surface, c, rainbow)
        rainbow.x += 10
    
    rainbowButton = pygame.Rect(2*w/3 + buffer, 4*h/5 - buffer, (w - (buffer * 2))/len(board) + 80, (h - (buffer * 2))/len(board))
    
    noneText, noneBounds = showMessage(" None ", 16, FONT, w/10 + 2*buffer, 4*h/5, WHITE)
    surface.blit(noneText, noneBounds)    
    
    effectList = [square, gradientButton, rainbowButton, noneBounds]
    textList = ["square", "gradient", "rainbow", "None"]
    
    ## check for mouseOver and mouseClick for each effect button
    for i in range(len(effectList)):
        if effectList[i].collidepoint(pygame.mouse.get_pos()):
            selected = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                effect = textList[i] ## these are the same thing
                EFFECT = textList[i] ## why do i have two variables
        else:
            selected = False
        if(selected or effect == textList[i]):
            pygame.draw.rect(surface, WHITE, effectList[i], 3) ## if color has been selected, outline in white    
    
    return gameState, COLOR, EFFECT, color, effect

def increase(num, amt):
    if(num + amt < 255):
        num += amt
    return num

''' draws all elements on the screen '''
def drawScreen(board, gameState, score, name, added, topScores, COLOR, EFFECT):
    #set background color
    surface.fill(RED)
    
    buffer = len(board)//2 ## leaves space around the outside
    pygame.draw.rect(surface, BLACK, (buffer, buffer, w-(buffer*2), h-(buffer*2)))
    
    # draws grid lines
    '''x, y = buffer, buffer
    for i in range(len(board)+1):
        pygame.draw.line(surface, BLACK, (x, buffer), (y, h-buffer))
        pygame.draw.line(surface, BLACK, (buffer, y), (w-buffer, x))
        
        x += (w - (buffer * 2))/len(board)
        y += (h - (buffer * 2))/len(board)'''
    
    x, y = buffer, buffer ## initializes the starting values
    
    i = len(COLOR_LIST) - 1
    
    for row in range(len(board)):
        for col in range(len(board)):
            if EFFECT == "square":
                # if part of snake
                if board[col][row] > 0:
                    extra = 1
                    pygame.draw.rect(surface, COLOR, (x + extra, y + extra, ((w - (buffer * 2))/len(board)) - (extra*2), ((h - (buffer * 2))/len(board)) - (extra*2)), 0)
                # if food
                elif board[col][row] == -1:
                    pygame.draw.rect(surface, WHITE, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                # if bonus
                elif board[col][row] == -2:
                    pygame.draw.rect(surface, GRAY, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                # if super food
                elif board[col][row] == -3:
                    pygame.draw.rect(surface, random.choice(COLOR_LIST), (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                x += (h - (buffer * 2))/len(board)                     
            else:
                # if part of snake
                if board[col][row] > 0:
                    if EFFECT == "gradient":
                        r = COLOR[0]
                        g = COLOR[1]
                        b = COLOR[2]
                        
                        if(b - (board[col][row]*25) > 0):
                            pygame.draw.ellipse(surface, (r, g, b - (board[col][row]*25)), (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                        else:
                            pygame.draw.ellipse(surface, COLOR, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                        
                        
                        #pygame.draw.ellipse(surface, (r, g, b), (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                        r = increase(r, 25)
                        g = increase(g, 25)
                        b = increase(b, 25)
                        
                        COLOR = (r, g, b)
                        
                        '''
                        if(255 - (board[col][row]*25) > 0):
                            pygame.draw.ellipse(surface, (255, 255, 255 - (board[col][row]*25)), (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                        else:
                            pygame.draw.ellipse(surface, YELLOW, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                        '''
                    elif EFFECT == "rainbow":
                        pygame.draw.ellipse(surface, COLOR_LIST[board[col][row]%9], (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)   
                        i -= 1
                        if(i < 0):
                            i = len(COLOR_LIST) - 1
                    else:
                        pygame.draw.ellipse(surface, COLOR, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                # if food
                elif board[col][row] == -1:
                    pygame.draw.ellipse(surface, WHITE, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                # if bonus
                elif board[col][row] == -2:
                    pygame.draw.ellipse(surface, GRAY, (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)
                elif board[col][row] == -3:
                    pygame.draw.ellipse(surface, random.choice(COLOR_LIST), (x, y, (w - (buffer * 2))/len(board), (h - (buffer * 2))/len(board)), 0)                
                # blit numbers to screen
                ## numText, numBounds = showMessage(str(board[col][row]), 12, FONT, x+(w - (buffer * 2))/len(board)/2, y+(w - (buffer * 2))/len(board)/2, BLACK)
                ## surface.blit(numText, numBounds)            
                x += (h - (buffer * 2))/len(board) 
        x = buffer
        y += (h - (buffer * 2))/len(board)
    
    # score
    scoreText, scoreBounds = showMessage("score: " + str(score), 18, FONT , w/10, h/20, WHITE)
    surface.blit(scoreText, scoreBounds)
    
    # highscores - loops through the highest scores (sorted backwards)
    height = h/20
    i = 1
    usedNames = []
    CLR = WHITE
    for value in sorted(list(topScores.values()))[::-1]: ## sorted highest to lowest
        for key in topScores:
            if topScores[key] == value and key not in usedNames:
                if (key == name):
                    CLR = YELLOW ## if user is signed in and on the leaderboard, name is highlighted in yellow
                else:
                    CLR = WHITE
                numText, numBounds = showMessage(str(i), 12, FONT , 5.8*w/8, height, CLR)
                surface.blit(numText, numBounds)                
                keyText, keyBounds = showMessage(key, 12, FONT , 6.5*w/8, height, CLR)
                surface.blit(keyText, keyBounds)
                valueText, valueBounds = showMessage(str(topScores[key]), 12, FONT , 7.5*w/8, height, CLR)
                surface.blit(valueText, valueBounds)
                height += h/20
                i += 1
                usedNames.append(key)
    
    if gameState == True:
        # game over
        overText, overBounds = showMessage(" Game Over! ", 72, FONT , w/2, h/2, RED, BLACK)
        surface.blit(overText, overBounds)
        
        # play again
        againText, againBounds = showMessage("Press Space to play again", 28, FONT , w/2, 3*h/4, WHITE, BLACK)
        surface.blit(againText, againBounds)
        
        if added == False:
            if score >= max(sorted(list(topScores.values()))):
                addText, addBounds = showMessage("You beat the high score!", 18, FONT , w/2, h/4, WHITE, BLACK)
                surface.blit(addText, addBounds)                 
                
            elif score >= min(sorted(list(topScores.values()))):
                addText, addBounds = showMessage("You made it onto the leaderboard!", 18, FONT , w/2, h/4, WHITE, BLACK)
                surface.blit(addText, addBounds)            
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Main Program Loop:

def main():
    
    # initialize variables
    board = loadBoard()
    topScores, top = loadScores(5)
    allScores = condenseFile()
    
    score = 0
    superCount = 0
    name = ""
    added = False
    gameState = "TITLE"
    
    ## default color is red, default effect is none
    COLOR = RED
    EFFECT = None
    color = "red"
    effect = "None"
    
    ## clock tick speed starts at 9
    clockTick = 9
    
    dRow = 1 ## starts the game moving down
    dCol = 0
    
    while(True):        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: ## if a key is pressed, check for direction change
                dRow, dCol = getDirection(event)
                
                letter = (event.unicode).lower() ## gets each letter pressed and returns it
                if gameState == "TITLE" and event.key:
                    name = getName(name, letter)
                    # checks for backspace
                    if event.key == pygame.K_BACKSPACE and len(name) > 0:
                        name = name[:-1]
                    # checks to see if user has entered name
                    if event.key == pygame.K_RETURN and len(name) > 0 and added == False:
                        addToScores(name, score)
                        topScores, top = loadScores(5)
                        added = True
                    if len(name) <= 0:
                        added = False
                        
                    if event.key == pygame.K_SPACE: ## if space is pressed and username has been entered
                        if gameState == "TITLE" and not (name == "" or name == " "):
                            board = loadBoard()
                            topScores, top = loadScores(5)
                            gameState = False
                            superCount = 0
                            score = 0
                            dRow = 1
                            dCol = 0           
                                
                # return to title screen
                if event.key == pygame.K_SPACE and gameState == "I":
                    gameState = "TITLE"
                if event.key == pygame.K_SPACE and gameState == "SCORES":
                    gameState = "TITLE"
                        
                # resets game
                if event.key == pygame.K_SPACE and gameState == True:
                    board = loadBoard()
                    if(len(name) > 0):
                        addToScores(name, score)
                    topScores, top = loadScores(5)
                    gameState = "TITLE"
                    superCount = 0
                    score = 0
                    dRow = 1
                    dCol = 0
        
        # moves the snake only if the game is still in play
        if gameState == False:
            gameState, score, superCount = moveSnake(board, dRow, dCol, gameState, score, superCount)
            placeBonus(board)
            placeSuper(board)
        
        # drawing code:
        if(gameState == "TITLE"): ## title screen
            gameState, COLOR, EFFECT, color, effect = drawTitleScreen(board, name, added, event, gameState, COLOR, EFFECT, color, effect, allScores)
        elif(gameState == "I"): ## instruction screen
            drawInstructions(board, effect)
        elif(gameState == "SCORES"): ## leaderboard screen
            drawHighscores(board, topScores, name)
        else: ## gameplay screen
            drawScreen(board, gameState, score, name, added, topScores, COLOR, EFFECT)
        
        # update screen and clock tick speed
        pygame.display.update()
        clockTick = updateTick(score, superCount)
        clock.tick(clockTick)

main()

'''
 * lock colors/effects until certain score reached
 * allow numbers in usernames
 * passwords
 * easter egg ??
'''
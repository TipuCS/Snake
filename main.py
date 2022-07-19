import pygame
import time
import random

# CONSTANTS
windowWidth = 1000a
windowHeight = 583
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
RED = (255, 0, 0)
GREEN = (30, 180, 90)
BROWN = (64, 41, 10, 0.5)
BLUE = (0, 0, 255)


# PYGAME SETUP
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('snek')

#   0 1 2 3 4 5
# 0
# 1
# 2
# 3
# 4
# 5

class Food():
  def __init__(self):
    self.foodCords = (1, 1)
    self.foodEaten = True
    self.foodColor = BLUE

  def update(self, boardObj, snakeObj):
    self.respawnFoodIfEaten(snakeObj, boardObj)

  def drawFood(self, boardObj):
    pieceInfoList = boardObj.getCordListForBox(self.foodCords)

    drawBox(pieceInfoList[0], pieceInfoList[1], pieceInfoList[2], pieceInfoList[3], self.foodColor)
  
  def respawnFoodIfEaten(self, snakeObj, boardObj):
    # is food eaten?
    if (self.foodEaten):
      foodRespawned = False
      # respawn in random place that isn't part of the snake
      while not (foodRespawned):
        x = random.randint(0, boardObj.numOfBlocksX - 1)
        y = random.randint(0, boardObj.numOfBlocksY - 1)
        positionTaken = False
        # is position not taken by head?
        if (x == snakeObj.headCord[0]) and (y == snakeObj.headCord[1]):
          positionTaken = True
          # is this position taken by any of the body
        for bodyCord in snakeObj.snakeBodyList:
          if (x == bodyCord[0]) and (y == bodyCord[1]):
            positionTaken = True
        # if the position wasn't taken, then respawn food
        if not (positionTaken):
          self.foodCords = (x, y)
          foodRespawned = True
          self.foodEaten = False

class Snake():
  def __init__(self):
    self.headCord = (5, 7)
    self.snakeBodyList = [(5, 8), (5, 9)]
    self.snakeBodyColor = GREEN
    self.snakeHeadColor = BLUE
    self.currentDirection = "up"
    self.lockTurning = True
    self.addedOne = False
    self.isSnakeAlive = True

  def update(self, boardObj, foodObj):
    self.moveBody()
    self.moveHead()
    self.ifHeadOutsideMapMoveInside(boardObj)
    self.isFoodEaten(boardObj, foodObj)
    self.checkIfSnakeDead()

  def checkIfSnakeDead(self):
    for bodyPos in self.snakeBodyList:
      if self.headCord == bodyPos:
        self.isSnakeAlive = False
  
  def isFoodEaten(self, boardObj, foodObj):
    if (self.headCord == foodObj.foodCords):
      self.addLengthOne()
      foodObj.foodEaten = True
  
  def addLengthOne(self):
    lengthBody = len(self.snakeBodyList)
    self.snakeBodyList.append((self.snakeBodyList[lengthBody - 1]))
    self.addedOne = True
    print(self.snakeBodyList)

  def moveBody(self):
    # go through list backwards
    # if not first item, make the item equal the one before
    # if first item make it equal head
    if (self.addedOne):
      lengthBody = len(self.snakeBodyList) - 1
    else:
      lengthBody = len(self.snakeBodyList)

        
    for i in range(lengthBody - 1, -1, -1):
      if (i != 0):
        self.snakeBodyList[i] = self.snakeBodyList[i-1]
      else:
        self.snakeBodyList[i] = self.headCord

    self.addedOne = False
      
      
  
  def moveHead(self):
    if self.currentDirection == "up":
      self.headCord = (self.headCord[0], self.headCord[1] - 1)
    elif self.currentDirection == "down":
      self.headCord = (self.headCord[0], self.headCord[1] + 1)
    elif self.currentDirection == "left":
      self.headCord = (self.headCord[0] - 1, self.headCord[1])
    elif self.currentDirection == "right":
      self.headCord = (self.headCord[0] + 1, self.headCord[1])

  def ifHeadOutsideMapMoveInside(self, boardObj):
    cord = self.headCord
    if (self.isCordOffBoard(cord, boardObj) == False):
      if (cord[0] < 0):
        self.headCord = (boardObj.numOfBlocksX - 1, cord[1])
      elif (cord[0] >= boardObj.numOfBlocksX):
        self.headCord = (0, cord[1])
      elif (cord[1] < 0):
        self.headCord = (cord[0], boardObj.numOfBlocksY - 1)
      elif (cord[1] >= boardObj.numOfBlocksY):
        self.headCord = (cord[0], 0)

  def drawSnake(self, boardObj):
    # draw body
    lengthBody = len(self.snakeBodyList)
    for i in range(0, lengthBody):
      self.drawSnakePiece(self.snakeBodyList[i], boardObj, GREEN)
    # draw head
    self.drawSnakeHead(boardObj, RED)
  
  def setHeadCord(self, cord):
    self.headCord = cord
  
  def isCordOffBoard(self, cord, boardObj):
    if (cord[0] < 0) and (cord[0] > boardObj.numOfBlocksX):
      if (cord[1] < 0) and (cord[1] > boardObj.numOfBlocksY):
        return True
    return False

  def drawSnakeHead(self, boardObj, color):
    pieceInfoList = boardObj.getCordListForBox(self.headCord)
    self.drawSnakePiece(self.headCord, boardObj, RED)

    x = pieceInfoList[0]
    y = pieceInfoList[1]
    width = pieceInfoList[2]
    height = pieceInfoList[3]

    # left eye
    drawLine((x + (width * 0.3), y + (height * 0.1)), (x + (width * 0.3), (y + height * 0.5)), BLACK)
    drawLine((x + (width * 0.2), y + (height * 0.1)), (x + (width * 0.2), (y + height * 0.5)), BLACK)
    drawLine((x + (width * 0.3), y + (height * 0.1)), (x + (width * 0.2), y + (height * 0.1)), BLACK)
    drawLine((x + (width * 0.3), y + (height * 0.5)), (x + (width * 0.2), y + (height * 0.5)), BLACK)

    # right eye
    drawLine((x + (width * 0.7), y + (height * 0.1)), (x + (width * 0.7), (y + height * 0.5)), BLACK)
    drawLine((x + (width * 0.8), y + (height * 0.1)), (x + (width * 0.8), (y + height * 0.5)), BLACK)
    drawLine((x + (width * 0.7), y + (height * 0.1)), (x + (width * 0.8), y + (height * 0.1)), BLACK)
    drawLine((x + (width * 0.7), y + (height * 0.5)), (x + (width * 0.8), y + (height * 0.5)), BLACK)
    # smile
    drawLine((x + (width * 0.2), y + (height * 0.7)), (x + (width * 0.4), y + (height * 0.8)), BLACK)
    drawLine((x + (width * 0.4), y + (height * 0.8)), (x + (width * 0.6), y + (height * 0.8)), BLACK)
    drawLine((x + (width * 0.6), y + (height * 0.8)), (x + (width * 0.8), y + (height * 0.7)), BLACK)

    drawLine((x + (width * 0.2), y + (height * 0.7)), (x + (width * 0.2), y + (height * 0.8)), BLACK)
    drawLine((x + (width * 0.8), y + (height * 0.7)), (x + (width * 0.8), y + (height * 0.8)), BLACK)

    drawLine((x + (width * 0.2), y + (height * 0.8)), (x + (width * 0.4), y + (height * 0.9)), BLACK)
    drawLine((x + (width * 0.4), y + (height * 0.9)), (x + (width * 0.6), y + (height * 0.9)), BLACK)
    drawLine((x + (width * 0.6), y + (height * 0.9)), (x + (width * 0.8), y + (height * 0.8)), BLACK)
    
  
  def drawSnakePiece(self, cords, boardObj, color):
    pieceInfoList = boardObj.getCordListForBox(cords)

    drawBox(pieceInfoList[0], pieceInfoList[1], pieceInfoList[2], pieceInfoList[3], color)

  def keyPressed(self, key):
    # if currently going up
    updateKey = False
    if (self.lockTurning == False):
      if self.currentDirection == "up":
        # if a turns it left, d turns it right
        if key == "a":
          self.currentDirection = "left"
        if key == "d":
          self.currentDirection = "right"
        # if currently going down
      elif self.currentDirection == "down":
        # if a turns it left, d turns it right
        if key == "a":
          self.currentDirection = "right"
        if key == "d":
          self.currentDirection = "left"
      elif self.currentDirection == "right":
        # if a turns it left, d turns it right
        if key == "a":
          self.currentDirection = "up"
        if key == "d":
          self.currentDirection = "down"
      elif self.currentDirection == "left":
        # if a turns it left, d turns it right
        if key == "a":
          self.currentDirection = "down"
        if key == "d":
          self.currentDirection = "up"
      self.lockTurning = True
    # if (updateKey):
    #   directionList = ["up", "down", "right", "left"]
    #   keyList = ["w", "s", "d", "a"]
    #   indexKey = keyList.index(key)
    #   self.currentDirection = directionList[indexKey]

  def drawHeadPosition(self):
    text = "(" +str(self.headCord[0])+", "+str(self.headCord[1])+")"
    drawText(text, 350, 10, 30, BLACK)

  
class Board():
  def __init__(self, x, y, sizeOfBlockX, sizeOfBlockY, numOfBlocksX, numOfBlocksY):
    self.x = x
    self.y = y
    self.sizeOfBlockX = sizeOfBlockX
    self.sizeOfBlockY = sizeOfBlockY
    self.numOfBlocksX = numOfBlocksX
    self.numOfBlocksY = numOfBlocksY
    self.boxColor = GREY
    self.outlineColor = BLACK


  # ex: (3, 2)
  # need box num: (4, 6)
  # returns [x, y, width, height]
  def getCordListForBox(self, cords):
    xCord = cords[0]
    yCord = cords[1]
    xPos = self.x + (self.sizeOfBlockX * xCord)
    yPos = self.y + (self.sizeOfBlockY * yCord)
    return [xPos, yPos, self.sizeOfBlockX, self.sizeOfBlockY]
    
    
  
  def drawBoard(self):
    for j in range(0, self.numOfBlocksY):
      for i in range (0, self.numOfBlocksX):
        drawBox(self.x + (i * self.sizeOfBlockX), self.y + (j * self.sizeOfBlockY), self.sizeOfBlockX, self.sizeOfBlockY, self.boxColor)

  def drawBoardGridLines(self):
    for j in range(0, self.numOfBlocksY):
      for i in range (0, self.numOfBlocksX):
        self.drawBoxLine(self.x + (i * self.sizeOfBlockX), self.y + (j * self.sizeOfBlockY), self.sizeOfBlockX, self.sizeOfBlockY, self.boxColor, self.outlineColor)
    
  def drawBoxLine(self, x, y, width, height, boxColor, outlineColor):
    drawLine((x, y), (x + width, y), outlineColor)
    drawLine((x + width, y), (x + width, y + height), outlineColor)
    drawLine((x, y + height), (x + width, y + height), outlineColor)
    drawLine((x, y), (x, y + height), outlineColor)

class Button():
  def __init__(self, numberID, x, y, width, height, color, text, textColor, textSize):
    self.numberID = numberID
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color
    self.text = text
    self.textColor = textColor
    self.textSize = textSize

class Mouse():
  def __init__(self):
    self.buttonList = []
    self.leftClickLocked = False
  
  def update(self, boardObj, snakeObj):
    buttonClicked = self.isAnyButtonClicked()
    if not (buttonClicked == False):
      print("a button clicked")
      # addBody
      if buttonClicked.numberID == 1:
        snakeObj.addLengthOne()

  def addButtonToList(self, numberID, x, y, width, height, color, text, textColor, textSize):
    button = Button(numberID, x, y, width, height, color, text, textColor, textSize)
    self.buttonList.append(button)
  
  def isAnyButtonClicked(self):
    # get the button that's clicked
    for button in self.buttonList:
      # is button Clicked
      if self.isButtonClicked(button.x, button.y, button.width, button.height):
        return button
    return False
    
  def drawButtonList(self):
    for button in self.buttonList:
      drawBox(button.x, button.y, button.width, button.height, button.color)
      drawText(button.text, button.x, button.y, button.textSize, button.textColor)

  def isButtonClicked(self, buttonX, buttonY, buttonWidth, buttonHeight):
    
    if (pygame.mouse.get_pressed()[0] == False):
      self.leftClickLocked = False
    # LEFT CLICKED
    if (self.leftClickLocked == False):
      if pygame.mouse.get_pressed()[0] == True:
        coordPosition = pygame.mouse.get_pos()
        # IS CLICK INSIDE BOX
        if (coordPosition[0] > buttonX) and (coordPosition[0] < buttonX + buttonWidth):
          if (coordPosition[1] > buttonY) and (coordPosition[1] < buttonY + buttonHeight):
            self.leftClickLocked = True
            return True
    return False

def drawBox(x, y, width, height, color):
  pygame.draw.rect(window, (color), (x, y, width, height))

def drawText(text, x, y, size, color):
  arialFont = pygame.font.SysFont('arial', size)
  textRenderer = arialFont.render(text, False, color)
  window.blit(textRenderer, (x, y))

def drawBackGround():
  drawBox(0, 0, windowWidth, windowHeight, WHITE)

def getLetterWidth(letter, size):
  arialFont = pygame.font.SysFont('arial', size)
  textRenderer = arialFont.render(letter, False, BLACK)
  return textRenderer.get_width()

def getLetterHeight(letter, size):
  arialFont = pygame.font.SysFont('arial', size)
  textRenderer = arialFont.render(letter, False, BLACK)
  return textRenderer.get_height()

def drawLine(startPos, endPos, Color):
  pygame.draw.line(window, Color, startPos, endPos)

def running():
  # Run once at start
  run = True
  boardObj = Board(10, 10, 30, 30, 10, 10)
  snakeObj = Snake()
  mouseObj = Mouse()
  foodObj = Food()
  mouseObj.addButtonToList(1, 350, 100, 200, 100, BLACK, "ADD +1 SNAKE", GREEN, 25)
  clock = pygame.time.Clock()

  mainTime = 0
  snakeTimer = 0
  i = 0
  while run:
    
    # PROGRAM
    drawBackGround()
    boardObj.drawBoard()
    snakeObj.drawSnake(boardObj)
    foodObj.drawFood(boardObj)
    boardObj.drawBoardGridLines()
    snakeObj.drawHeadPosition()
    mouseObj.drawButtonList()

    mouseObj.update(boardObj, snakeObj)
    clock.tick(60)
    #print(clock.get_time())
    mainTime += clock.get_time() / 1000
    #print(f"{round(mainTime, 0)=}")
    timeBetweenUpdate = 0.10
    if (snakeTimer + timeBetweenUpdate < mainTime):
      if (snakeObj.isSnakeAlive):
        snakeObj.lockTurning = False
        snakeTimer = mainTime
        snakeObj.update(boardObj, foodObj)
        foodObj.update(boardObj, snakeObj)
            
    pygame.display.flip()
    
    for event in pygame.event.get():
      
      # QUITTING
      if event.type == pygame.QUIT:
        run = False   

      if event.type == pygame.KEYDOWN:
        snakeObj.keyPressed(event.unicode)


running()

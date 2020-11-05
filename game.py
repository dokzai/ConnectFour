# I ended up having a lot of trouble trying to implement discord so I left out the bot idea and focused on algortihm and application
# visuals were lacking as a result since i used a text representation (originally for discord emojis)

import random

def printboard(board):

  for x in range (0, len(board)):
    for y in range (0,len(board[0])):
      if board[x][y] == 0:
        print("0 ", end = '')
      elif board[x][y] == 1:
        print("1 ", end = '')
      elif board[x][y] == 2:
        print("2 ", end = '')
    print("")
  print("-------------")
  print("1 2 3 4 5 6 7 \n")

def initboard():
  board = []
  newRow = []
  for i in range (0, 6):
      for j in range (0, 7):
        newRow.append(0)
      board.append(newRow)
      newRow = []
  return board

def addDisc(board, userInput, playerNum):
  boarditer = 5
  while boarditer >= 0:
    if board[boarditer][userInput-1] == 0:
      board[boarditer][userInput-1] = playerNum
      break
    else:
      boarditer = boarditer-1

def colIsFull(board, userInput):
  discsInCol = 0
  for x in range (0,len(board)):
    if board[x][userInput-1] != 0:
      discsInCol = discsInCol + 1
  if discsInCol == 6:
    return True
  else:
    return False

def boardIsFull(board):
  columns = 0
  for x in range(0,7):
    if colIsFull(board, x):
      columns = columns + 1
  if columns == 7:
    return True

# needs testing
def horizontalCheck(board, player,maxSeq)->int:
  counter = 0
  for x in range(0, 6):
    for y in range(0,7):
      if board[x][y] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        #it used to be return y 
        return int(x)
  return -1
  
def verticalCheck(board,player,maxSeq)->int:
  counter = 0
  for x in range(0, 7):
    for y in range(0,6):
      if board[y][x] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(x)
  return -1

def diagonalCheck(board, player, maxSeq)->int:
  desc = descDiagonalCheck(board, player, maxSeq)
  asc = ascDiagonalCheck(board, player, maxSeq)
  if desc > 0:
    return desc
  elif asc > 0:
    return asc
  else:
    return -1

def descDiagonalCheck(board, player, maxSeq)->int:
  for x in range(0,3):
    counter = 0
    for y in range(0,6-x):
      if board[y+x][y] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(y)

  for x in range(1,4):
    counter = 0
    for y in range(0,7-x):
      if board[y][y+x] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(y+x)
  return -1

def ascDiagonalCheck(board, player, maxSeq)->int:
  for x in range(3,6):
    counter = 0
    for y in range(0,1+x):
      if board[x-y][y] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(y)

  for x in range(1,4):
    counter = 0
    for y in range(5,-2+x,-1):
      if board[y][x+(5-y)] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(x+(5-y))
  return -1

def checkWin(board):

  if horizontalCheck(board,1,4) >= 0 or verticalCheck(board,1,4) >= 0 or diagonalCheck(board,1,4) >= 0:
    return 1
  elif horizontalCheck(board,2,4) >= 0 or verticalCheck(board,2,4) >= 0 or diagonalCheck(board,2,4) >= 0:
    return 2
  elif boardIsFull(board):
    return 0
  else:
    return -1

def playGame():
  board = initboard()
  print("NOTE: 1 represents the disks of player 1. 2 represents the disks of player 2. 0 represents an empty space. The dashes represent the split between the board and the columns you may use as inputs to play your disk!\n")
  printboard(board)

  gameOver = False
  playerNum = 1

  while gameOver == False:
    while True:
      userInput = int(input("Player "+str(playerNum)+", please enter the column you would like to place your connect four disk: "))
      #or column is full
      if userInput > 7 or userInput < 1:
        print("Invalid input. Please renter a valid number between 1 to 7 inclusive.")
      elif colIsFull(board,userInput):
        print("That column in the board is filled please renter a valid column")
      else:
        break

    if playerNum % 2 == 0:
      addDisc(board,userInput,playerNum)
      printboard(board)
      state = checkWin(board)
      if state >= 0:
        gameOver = True
      playerNum = 1
    else:
      addDisc(board,userInput,playerNum)
      printboard(board)
      state = checkWin(board)
      if state >= 0:
        gameOver = True
        print("Player "+str(state)+" has won!")
      playerNum = 2

# checks if issue is resolved for that specific player



def sequenceLen(board,player,seqLength, validMoves):


  validCols = []
  # not fixed
  print(horizontalCheck(board,player,seqLength))
  if horizontalCheck(board,player,seqLength) >= 0 and (board[horizontalCheck(board,player,seqLength)][seqLength-1] == 0 or board[horizontalCheck(board,player,seqLength)][seqLength-1] == 0):
    print("fds")
  
    validCols.append(horizontalCheck(board,player,seqLength)+1)
    validCols.append(horizontalCheck(board,player,seqLength)-seqLength)
 
  
  elif verticalCheck(board,player,seqLength) >= 0 and board[seqLength-1][verticalCheck(board,player,seqLength)] == 0:
    print("vert exists")
    validCols.append(verticalCheck(board,player,seqLength))
  elif diagonalCheck(board,player,seqLength) >= 0:

    validCols.append(diagonalCheck(board,player,seqLength))

  possibleMoves = []
  for x in range (0, len(validCols)):
    if validCols[x] in validMoves:
      # not working for 7???
      possibleMoves.append(validCols[x]+1)

  print(possibleMoves)
  return possibleMoves

def minimax(board):
  #valid moves
  validMoves = []
  for x in range(0,7):
    if colIsFull(board, x) == False:
      print(x)
      validMoves.append(x)

  print("valid moves: "+str(validMoves))

  # ai wins
  if len(sequenceLen(board,2, 3, validMoves)) > 0:
    AIInput = random.choice(sequenceLen(board,2, 3, validMoves))
  # prevent player from winning
  elif len(sequenceLen(board,1, 3, validMoves)) > 0:
    AIInput = random.choice(sequenceLen(board,1, 3, validMoves))
  # offensive moves
  elif len(sequenceLen(board,2, 2, validMoves)) > 0:
    AIInput = random.choice(sequenceLen(board,2, 2, validMoves))
  else:
    AIInput = random.choice(validMoves)

  return AIInput

def playGameAI():
  board = initboard()
  print("NOTE: 1 represents the disks of player 1. 2 represents the disks of player 2. 0 represents an empty space. The dashes represent the split between the board and the columns you may use as inputs to play your disk!\n")
  printboard(board)

  gameOver = False
  playerNum = 1

  while gameOver == False:
    if playerNum % 2 == 0:
      AIInput = minimax(board)
      addDisc(board,AIInput,playerNum)
      print("AI has placed disk in column "+str(AIInput))
      printboard(board)
      state = checkWin(board)
      if state >= 0:
        gameOver = True
        print("Player "+str(state)+" has won!")
        if state == 2:
            print("Aw shucks... Looks like I've lost. Good job!")
      playerNum = 1
    else:
      while True:
        userInput = int(input("Player "+str(playerNum)+", please enter the column you would like to place your connect four disk: "))
        #or column is full
        if userInput > 7 or userInput < 1:
          print("Invalid input. Please renter a valid number between 1 to 7 inclusive.")
        elif colIsFull(board,userInput):
          print("That column in the board is filled please renter a valid column")
        else:
          break
      addDisc(board,userInput,playerNum)
      printboard(board)
      state = checkWin(board)
      if state >= 0:
        gameOver = True
        print("Player "+str(state)+" has won!")
        if state == 2:
            print("Aw shucks... Looks like I've lost. Good job!")
      playerNum = 2


while True:
    userChoice = int(input("Would you like to play against an AI or with a friend? Enter 1 for AI, 2 for friend."))
    if (userChoice == 1 or userChoice == 2):
      break
    else:
      print("Invalid input. Please renter a valid input.")

if (userChoice == 1):
  playGameAI()
elif (userChoice == 2):
  playGame()

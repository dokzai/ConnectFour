# imports modules
import random
import math
import copy
import time

#prints board
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

# initializes board of 6 rows and 7 columns
def initboard():
  board = []
  newRow = []
  for i in range (0, 6):
      for j in range (0, 7):
        newRow.append(0)
      board.append(newRow)
      newRow = []
  return board

# adds the disc into the lowest open spot of the column of the board
def addDisc(board, userInput, playerNum):
  boarditer = 5
  # while top of the column has not yet been reached
  while boarditer >= 0:
    if board[boarditer][userInput-1] == 0:
      board[boarditer][userInput-1] = playerNum
      break
    else:
      boarditer = boarditer-1

# checks if the column is full
def colIsFull(board, userInput):
  discsInCol = 0
  # iterates through board and checks if the column is full
  for x in range (0,len(board)):
    if board[x][userInput-1] != 0:
      discsInCol = discsInCol + 1
  if discsInCol == 6:
    return True
  else:
    return False

# checks if the board is full
def boardIsFull(board):
  columns = 0
  for x in range(0,7):
    if colIsFull(board, x):
      columns = columns + 1
  if columns == 7:
    return True

# checks all possible horizontal/row wins
def horizontalCheck(board, player,maxSeq):
  for x in range(0, 6):
    counter = 0
    for y in range(0,7):
      if board[x][y] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(x)
  return -1

# checks vertical/columns for wins
def verticalCheck(board,player,maxSeq):
  for x in range(0, 7):
    counter = 0
    for y in range(0,6):
      if board[y][x] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter == maxSeq:
        return int(x)
  return -1

# covers checks descending and ascending columns
def diagonalCheck(board, player, maxSeq):
  desc = descDiagonalCheck(board, player, maxSeq)
  asc = ascDiagonalCheck(board, player, maxSeq)
  if desc > 0:
    return desc
  elif asc > 0:
    return asc
  else:
    return -1

# covers ascending diagonal checks
def descDiagonalCheck(board, player, maxSeq):\
  # covers descending diagonals from rows 0 to 2 inclusive
  for x in range(0,3):
    counter = 0
    for y in range(0,6-x):
      if board[y+x][y] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(y)
  # covers descending diagonals from columns 1-3 inclusive
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

# covers ascending diagonal checks
def ascDiagonalCheck(board, player, maxSeq):
  # ascending diagonals from rows 3 to 5 inclusive
  for x in range(3,6):
    counter = 0
    for y in range(0,1+x):
      if board[x-y][y] == player:
        counter = counter + 1
      else:
        counter = 0
      if counter >= maxSeq:
        return int(y)
  # ascending diagonals from col 1-3 inclusive
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

# checks if any player won
def checkWin(board,player):
  # checks all possible directions
  if horizontalCheck(board,player,4) >= 0 or verticalCheck(board,player,4) >= 0 or diagonalCheck(board,player,4) >= 0:
    return True
  else:
    return False

# returns a list of valid moves to take
def valid_moves(board):
  validMoves = [1,2,3,4,5,6,7]
  for x in range(1,8):
    if colIsFull(board, x):
      validMoves.remove(x)
  return validMoves

# returns the column of the board
def column(board,col):
  column = []
  for x in range(0,6):
    column.append(board[x][col]) 
  return column

# rates the board and gives it a score
def score(board, player):
  # init variable
  boardScore = 0
  centerPieces = column(board,3).count(player)
  # place a high emphasis on center column by giving a higher score
  boardScore += centerPieces*3

  # checks all possible horizontal sublists of length 4
  for row in range(6):
    currentRow = board[row]
    for col in range(4):
      subrow = currentRow[col:col+4]
      boardScore += evaluate_subsequence(subrow,player)
  # checks all possible vertical sublists of length 4
  for col in range(7):
    currentCol = column(board,col)
    for row in range(3):
      sublist = currentCol[row:row+4]
      boardScore += evaluate_subsequence(sublist,player)
  # checks all possible diagonal ascending sublists of length 4
  for row in range(3):
    for col in range(4):
      sublist = [board[row+i][col+i] for i in range(4)]
      boardScore += evaluate_subsequence(sublist,player)
  # checks all possible diagonal descending sublists of length 4
  for row in range(3):
    for col in range(4):
      sublist = [board[row+3-i][col+i] for i in range(4)]
      boardScore += evaluate_subsequence(sublist,player)
  return boardScore

# evalutes the subsequence
def evaluate_subsequence(subsequence,player):
  # init score
  score = 0
  #swaps player/opposing player values depending on player value given
  otherPlayer = 1
  if player == 1:
    otherPlayer = 2
  # high score since the player would win / edge case
  if subsequence.count(player) == 4:
    score += 1000
  # player would win
  elif subsequence.count(player) == 3 and subsequence.count(0) == 1:
    score += 9
  # player would increase potential of winning
  elif subsequence.count(player) ==2 and subsequence.count(0) ==2:
    score += 4
  # opposing player can win
  if subsequence.count(otherPlayer) == 3 and subsequence.count(0) == 1:
    score -= 10
  return score

# node that would end game
def terminal_node(board):
  # checks if player would win game or if board is full/tied
  return checkWin(board, 1) or checkWin(board,2) or len(valid_moves(board)) == 0

# recursively looks ahead to maximise gain and minimize loss with alpha and beta pruning
def minimax(board,depth,maximizingPlayer, alpha,beta):
  validColumns = valid_moves(board)
  # base case when depth = 0
  if depth == 0 or terminal_node(board):
    if terminal_node(board):
      if checkWin(board, 2):
        return (None, math.inf)
      elif checkWin(board,1):
        return (None, -math.inf)
      else:
        return (None, 0)
    else:
      return (None, score(board,2))
  # one of the recursive cases/maximizingPlayer
  if maximizingPlayer:
    column = random.choice(validColumns)
    value = -math.inf
    # looks at all possible moves and chooses the best/max outcome by evaluating all possible boards
    for col in validColumns:
      b_copy = copy.deepcopy(board)
      addDisc(b_copy,col,2)
      # recurisvely calculate score and look into minimizing tree
      new_score = minimax(b_copy,depth-1,False,alpha,beta)[1]
      if new_score > value:
        value = new_score
        column = col
      alpha = max(value,alpha)
      if alpha >= beta:
        break
    return column, value

  # minimizing player/recursive case
  else:
    column = random.choice(validColumns)
    value = math.inf
    # looks at all possible moves and chooses the worst outcome
    for col in validColumns:
      b_copy = copy.deepcopy(board)
      addDisc(b_copy,col,1)
      # recurisvely calculate score and look into maximising tree
      new_score = minimax(b_copy,depth-1,True,alpha,beta)[1]
      if new_score < value:
        value = new_score
        column = col
      beta = min(value,beta)
      if alpha >=beta:
        break
    return column, value

# chooses how the ai should play
def ai_output(board, difficulty):
  if difficulty == 3:
    aiOutput,minimax_score = minimax(board,4,True,-math.inf,math.inf)
  elif difficulty == 2:
    aiOutput,minimax_score = minimax(board,1,True,-math.inf,math.inf)
  else:
    validColumns = valid_moves(board)
    aiOutput = random.choice(validColumns)
  return aiOutput

# plays game
def playGame(AI, difficulty):
  print("Just a note. I am unable to display emojis in console for python unless I ask you to pip install some emoji displayer (I was originally intending to use discord as a platform to handle that), so if you would like to play with slightly better visuals and colors, just visit this repl.it link with my code. It's the same code written by me (the author is wujudy-my name) except the printboard prints emojis, which I find easier on the eyes to see patterns and sequences.")
  print("Link: https://repl.it/@wujudy/FinalConnectFour")
  print("Aside from that. In the console, the discs are instead just represented by numbers. 1 is player one. 2 is player two. 0 is an empty spot. The dashed line at the bottom represents the separation from the board and displays the columns as inputs you can enter. As an example, if you want to place a disc in a column and see that the number below the dashed line is 1, just enter 1. \n")
  # init board and display board
  board = initboard()
  printboard(board)

  gameOver = False
  # randomly choose which player goes first
  playerNum = random.randint(1,2)

  # loops until game is over
  while gameOver == False:
    if playerNum % 2 == 0:
      #if user is playing against AI, calculate score
      if AI:
        p2input = ai_output(board,difficulty)
      # takes userinput
      else:
        # input validation
        while True:
          p2input = int(input("Player "+str(playerNum)+", please enter the column you would like to place your connect four disk: "))
          #or column is full
          if p2input > 7 or p2input < 1:
            print("Invalid input. Please renter a valid number between 1 to 7 inclusive.")
          elif colIsFull(board,p2input):
            print("That column in the board is filled please renter a valid column")
          else:
            break
      # adds disc
      addDisc(board,p2input,playerNum)
      print("Player 2 has placed their disk in column "+str(p2input))
      # prints newly changed board
      printboard(board)
      # checks if player has won
      if checkWin(board,playerNum):
        gameOver = True
        print("Player "+str(playerNum)+" has won!")
      # checks for a tie
      elif boardIsFull(board):
        gameOver = True
        print("Game is tied!")
      # changes to opposing players turn
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
      if checkWin(board,playerNum):
        gameOver = True
        print("Player "+str(playerNum)+" has won!")
      #if tie
      elif boardIsFull(board):
        gameOver = True
        print("Game is tied!")
      playerNum = 2

# initalize randomness by setting system time seed
random.seed(time.time())
# init AI variable and difficulty
AI = False
difficulty =-1

# validate user input
while True:
    userChoice = int(input("Would you like to play against an AI or with a friend? Enter 1 for AI, 2 for friend: "))
    if (userChoice == 1 or userChoice == 2):
      break
    else:
      print("Invalid input. Please renter a valid input.")

# if the user selected to play against an AI, ask for difficulty
if userChoice == 1:
  AI = True
  while True:
    difficulty = int(input("How difficult would you want the AI you play against to be? Enter 1 for dead easy, 2 for medium, 3 for relatively hard: "))
    if (userChoice == 1 or userChoice == 2 or userChoice == 3):
      break
    else:
      print("Invalid input. Please renter a valid input.")

# plays game
playGame(AI, difficulty)


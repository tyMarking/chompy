import numpy as np
"""
A mXn board is an array of ints with length m.
The fist value must be exactly n.
Each subsequent value must be less than or equal to the previous.
Each value represents the number of squares in the row.
The poison is at coordinate 0, 0 (in the top left).
The poison is counted in the number of squares in the first row.
"""

#bite the matrix based board at the coordinates x, y
#x, y are 0 indexed. X is the column, Y is the row
#returns the bitten board
def bite(board, x, y):
	#check x and y in bounds
	if abs(x) > board[0] or abs(y) > len(board):
		print("Error: Bite taken out of range")
		return board

	#convert the values of x and y to positives so the for loop works
	if x < 0:
		x = board[0] + x
	if y < 0:
		y = len(board) + y

	#shallow copy board
	board = board[:]

	#loop through the rows of board, starting at y
	#if the value of board at the current row is greater than x,
		#set the value of the new board at the row to x
	#else
		#none of the others will have a greater length value, so we can end
		#break

	#trim the board
	#if x is 0, remove elements starting at y
	for row in range(y, len(board)):
		if board[row] > x:
			board[row] = x;
		else:
			break;

	if x == 0:
		board = board[0:y]
	return board

def addRow(boardStates, newM):
	newStates = []
	for board in boardStates:
		if len(board) == newM - 1:
			for i in range(1, board[-1] + 1):
				newBoard = board[:]
				newBoard.append(i)
				print(newBoard)
				newStates.append(newBoard)
	boardStates.extend(newStates)

def addCol(boardStates, newN):
	newStates = []
	for board in boardStates:
		newCol = [0] * len(board)#new array of zeros, with length of board
		for i in range(len(board)):
			if board[i] != newN - 1:
				break
			newCol[i] = 1
			newBoard = [board[j] + newCol[j] for j in range(len(board))]
			#TODO: matrix addition of newBoard and newCol
			newStates.append(newBoard)
	boardStates.extend(newStates)

def getM(board):
	return len(board)

def getN(board):
	return board[0]

#returns a 2d array corresponding to the board state
def toArrayNotation(board):
	#true (1) is bitten
	n = board[0]
	boardAsArr = [[0] * n for i in range(len(board))]#generate an MxN array
	for i in range(len(board)):
		print(board[i])
		for j in range(board[i], n):
			boardAsArr[i][j] = 1
	boardAsArr[0][0] = -1
	return boardAsArr

#the number of cols that have a bite taken out of it, if there are no bites, 0
def file(board):
	return board[0] - board[-1]

def inverseFile(board):
	return board[-1]

#the first row that has a bite taken out of it, if there are no bites, 0
def inverseRank(board):
	n = board[0]
	for i in range(1, len(board)):
		if i < n:
			return i
	return 0

def rank(board):
	return len(board) - inverseRank(board)

#generates a unique key to be used in the dict.
def dKey(board):
	key = ""
	for row in board:
		key += "/" + str(int(row))
	return key[1:]#remove the first "/"

def genEndBoard():
	return [1]

def genBoard(m, n):
	return [n] * m

def possibleLs(board, newSize):
	L = []
	#l is a tuple (m, n)
	#m is across the row
	#n is down the col
	if getM(board) == newSize-1 or getN(board) == newSize-1:
		#by default l starts as a tuple (newSize, newSize)
		#for each row with lenghth newSize-1, decrement l[1]
		#at the first row that isnt newSize-1, break the loop
		#subtact file(graph) from newSize

	return L

def possibleLPrimes(board):



# TODO: add getChoices

"""
TEST STUFF
"""
states = [
[1], [2], [1,1], [2,1], [2,2]
]

addRow(states, 3)
addCol(states, 3)

print("\nNew States")
print(states)
print("\n")
board = states[14]

arrNotation = toArrayNotation(board)
print(np.array(arrNotation))

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
		if board[i] < n:
			return i
	return len(board)

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

def getL(board, newSize):
	L = []
	#l is a tuple (m, n)
	#m is across the row
	#n is down the col
	if getM(board) == newSize-1 and getN(board) == newSize-1:
		#min m is file(board) + 1
		#min n is rank(board) + 1
		#max of both is newSize-1
		L = [(i, j) for i in range(file(board) + 1, newSize + 1) for j in range(rank(board) + 1, newSize)]
	elif getM(board) == newSize-1:
		#getN(board) is less than newSize-1
		#n will be newSize
		#m will have min file(board)+2 and max newSize-1
		L = [(i, newSize) for i in range(file(board)+2, newSize)]
	elif getN(board) == newSize-1:
		#getM(board) is less than newSize-1
		#m will be newSize
		#n will have min rank(board)+2 and max newSize-1
		L = [(newSize, j) for j in range(rank(board)+2, newSize)]
	toRemove = []
	for i in range(len(L)):
		if L[i][0] < L[i][1]:
		# 	l = (l[1], l[0])
			toRemove.append(i)
	for index in toRemove:
		L.remove(L[index])
	return L

def getLPrime(board):
	return [i for i in range(rank(board), getM(board))]

def getChoices(board):
	choices = [(i, j) for i in range(getM(board)) for j in range(board[i])]
	choices = choices[1:]
	return choices

def getMxNFileName(m, n):
	return str(m) + "x" + str(n) + ".json"

def load(fileName):
	with open(fileName, "r") as file:
		jData = file.read()
		data = json.loads(jData)
		return data

def store(data, fileName):
	with open(fileName, "w") as file:
		jData = json.dumps(data)
		file.write(jData)
		return 1

def seed():
	#{key:eta}
	#[(node,eta)]
	etaData = {dKey([1]):0, dKey([2]):1, dKey([2,1]):2, dKey([2,2]):3}#don't seed [1,1] b/c rows > cols
	workingData = [([2], 1), ([2,1], 2), ([2,2], 3)]
	return etaData, workingData

def mirror(board):
	# [ for i in range(len(board))]
	mirrored = [0] * board[0] #initialize the mirrored rectangular board
	for i in range(board[0]):
		mirrored[i] = 0
		for j in range(len(board)):
			if board[j] > i:
				mirrored[i] += 1
	return mirrored


"""
TEST STUFF
"""
def main():
	states = [
	[1], [2], [1,1], [2,1], [2,2]
	]

	# board = [2, 2]
	# print(rank(board))
	# print(file(board))
	# print(inverseRank(board))
	# print(inverseFile(board))
	# print(getL(board, 3))


if __name__ == "__main__":
	main()

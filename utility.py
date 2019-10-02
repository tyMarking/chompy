import random
import json
import numpy as np
import extendBoardStates as ebs
import heritage
from datetime import datetime
import xlsxwriter as xlsxw

def display(board):
	#print(board)
	print("")
	for row in board:
		rowStr = ""
		for entry in row:
			if entry == -1:
				rowStr += "X"
			elif entry == 0:
				rowStr += "O"
			elif entry == 1:
				rowStr += "1"
			#elif entry == 2:
			#	rowStr += "2"
			else:
				print("Unexpected entry in board: " + str(entry))
			rowStr += " "
		print(rowStr)

def genBoard(m, n):
	board = np.zeros((m, n))
	board[-1][0] = -1
	return board

def extendToMxN(m, n):
	workbook = xlsxw.Workbook(r'./data/extensionTimesAndLengths'+str(m)+'X'+str(n)+'.xlsx')
	worksheet = workbook.add_worksheet()
	row = 2
	col = 2
	worksheet.write(0, 0, "M")
	worksheet.write(0, 1, "N")
	worksheet.write(0, 2, "Num States")
	worksheet.write(0, 3, "Added Time")

	states2x2 = [
	[[0 ,0],
	 [-1,0]],
	[[0 ,1],
	 [-1,0]],
	[[1 ,1],
	 [-1,0]],
	[[0 ,1],
	 [-1,1]],
	[[1 ,1],
	 [-1,1]]
	]

	heritage2x2 = heritage.getHeritage(states2x2)

	worksheet.write(1, 0, 2)
	worksheet.write(1, 1, 2)
	worksheet.write(1, col, len(states2x2))
	worksheet.write(1, col + 1, 0)

	if m < 2 or n < 2:
		print("Board must be at least 2x2")
	elif m == 2 and n == 2:
		return states2x2

	currBoardsAndHeritage = [np.copy(states2x2), heritage2x2]

	currM = 2
	currN = 2
	beginningDateTime = datetime.now()
	startDateTime = 0
	endDateTime = 0
	while (currM < n and currN < n):
		startDateTime = datetime.now()
		if (currM < m):
			currBoardsAndHeritage = ebs.appendRowToBoardStates(currBoardsAndHeritage[0], currBoardsAndHeritage[1])
			print(len(currBoardsAndHeritage[0]))
		if (currN < n):
			currBoardsAndHeritage = ebs.appendColToBoardStates(currBoardsAndHeritage[0], currBoardsAndHeritage[1])
			print(len(currBoardsAndHeritage[0]))
		print(str(currM) + "x" + str(currN))
		currM = len(currBoardsAndHeritage[0])
		currN = len(currBoardsAndHeritage[0][0])

		endDateTime = datetime.now()
		addedTime = endDateTime - startDateTime
		print(addedTime)

		currRow = row + currN - 3
		worksheet.write(currRow, 0, currM)
		worksheet.write(currRow, 1, currN)
		worksheet.write(currRow, col, len(currBoardsAndHeritage[0]))
		worksheet.write(currRow, col + 1, addedTime)

		startDateTime = endDateTime

	print("Total time: " + str(datetime.now() - beginningDateTime))
	workbook.close()
	return currBoardsAndHeritage

def genEndBoard(m, n):
	board = np.ones((m, n))
	board[-1][0] = -1
	return board

def dKey(board):
	key = ""
	for row in board:
		key += "/"
		for s in row:
			key += str(s)
	return key

"""
DEPRICATED: Using np.copy after np refactor
def copy(board):
	return [row[:] for row in board]
"""

def bite(board,pos):
	m = pos[0]
	n = pos[1]
	if abs(m) > len(board)-1 or abs(n) > len(board[0])-1:
		print("Error: Bite taken out of range")
		return

	#convert the values of m and n to positives, so the for loop works
	if m < 0:
		m = len(board) + m
	if n < 0:
		n = len(board[0]) + n

	for i in range(0,m+1):
		for j in range(n, len(board[0])):
			board[i][j] = 1

	if m == len(board)-1 and n == 0:
		print("Ate The Poision!")
		#board[m][n] = -1

def superimpose(size, bites):
	b = genBoard(size[0], size[1])
	for singBite in bites:
		bite(b, singBite)
	return b

#get list of possible moves (all 0 squares)
def getChoices(board):
	options = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				options.append((i,j))
	return options

#previously called getInverseChoices
def getBitten(board):
	bitten = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 1:
				bitten.append((i,j))
	return bitten

def unBite(board, pos):

	modPos = (pos[0],pos[1])
	#looking down
	while modPos[0] < len(board) and board[modPos[0]][modPos[1]] == 1:
		modPosPrime = (modPos[0], modPos[1])

		#looking left
		while modPosPrime[1] > 0 and board[modPosPrime[0]][modPosPrime[1]] == 1:

			board[modPosPrime[0]][modPosPrime[1]] = 0
			modPosPrime = ( modPosPrime[0], modPosPrime[1] - 1)

		modPos= ( modPos[0] + 1, modPos[1])


"""
def choiceRandom(board):
	options = get_choices(board)
	#only poison left
	if len(options) == 0:
		return (len(board)-1, 0)
	return random.choice(options)
"""

def rank(board):
	for i in reversed(range(len(board))):
		if board[i][-1] == 1:
			return i+1
	return 0

def lastColRank(board):
	for i in reversed(range(len(board))):
		if board[i][0] == 1:
			return i+1
	return 0

def file(board):
	for i in range(len(board[0])):
		if board[0][i] == 1:
			return len(board[0])-i
	return 0

def lastRowFile(board):
	for i in range(len(board[-1])):
		if board[-1][i] == 1:
			return len(board[0])-i
	return 0

def gamma(board):
	bites = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 1:
				for k in range(j, len(board[i])):
					bites.append((i,k))
				break
	return bites

def phi(board):
	return len(gamma(board))

#s1-s2
def setSubtract(s1, s2):
	diff = []
	for a in s1:
		inS2 = False
		for b in s2:
			if b == a:
				inS2 = True
		if not inS2:
			diff.append(a)
	return diff

def delta(board1, board2):
	g1 = gamma(board1)
	g2 = gamma(board2)
	return setSubtract(g1,g2) + setSubtract(g2,g1)

#1 << 2 or 2 << 1
def isRelated(board1, board2):
	g1 = gamma(board1)
	g2 = gamma(board2)
	if len(g2) > len(g1):
		g1, g2, board1, board2 = g2, g1, board2, board1
	if len(setSubtract(g2,g1)) > 0:
		return False
	else:
		return True

#1<<2
def isDecendent(board1, board2):
	g1 = gamma(board1)
	g2 = gamma(board2)
	if len(setSubtract(g2,g1)) > 0:
		return False
	else:
		return True

#data = [(board,[parents,]),]
def store(data, fileName):

	try:
		with open(fileName, "w") as file:
			jData = json.dumps(data)
			file.write(jData)
			return 1
	except:
		print("Failed to store to " + str(fileName))
		return -1


def load(fileName, npArray = True):
	#print("LOAD FUNCTION LOADING: " + fileName)
	try:
		with open(fileName, "r") as file:
			jData = file.read()
			data = json.loads(jData)
			if npArray:
				data = np.array(data)
			return data
	except:
		print("ERROR: could not find file: " + str(fileName))
		return []

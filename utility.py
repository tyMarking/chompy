import random
import json
import numpy as np

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
	if m > len(board)-1 or n > len(board[0])-1 or m < 0 or n < 0:
		print("Error: Bite taken out of range")
		return
	
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


def file(board):
	for i in range(len(board[0])):
		if board[0][i] == 1:
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

#data = [(board,[parents,],num),]
def store(data, fileName):
	
	try:
		with open(fileName, "w") as file:
			jData = json.dumps(data)
			file.write(jData)
			return 1
	except:
		return -1


def load(fileName):
	try:
		with open(fileName, "r") as file:
			jData = file.read()
			data = np.array(json.loads(jData))
			return data
	except:
		print("ERROR: could not find file: " + str(fileName))
		return []


import random
import json

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

def genBoard(rows,cols):
	board = [x[:] for x in [[0] * cols] * rows]
	board[rows-1][0] = -1
	return board

def genEndBoard(rows,cols):
	board = [x[:] for x in [[1] * cols] * rows]
	board[rows-1][0] = -1
	return board

def dKey(board):
	key = ""
	for row in board:
		key += "/"
		for s in row:
			key += str(s)
	return key

def copy(board):
	return [row[:] for row in board]

def bite(board,pos):
	row = pos[0]
	col = pos[1]
	if row > len(board)-1 or col > len(board[0])-1 or row < 0 or col < 0:
		print("Error: Bite taken out of range")
		return
	
	for i in range(0,row+1):
		for j in range(col, len(board[0])):
			board[i][j] = 1

	if row == len(board)-1 and col == 0:
		print("Ate The Poision!")
		#board[row][col] = -1

def getChoices(board):
	options = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				options.append((i,j))
	return options

def getInverseChoices(board):
	options = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 1:
				options.append((i,j))
	return options


def choiceRandom(board):
	options = get_choices(board)
	#only poison left
	if len(options) == 0:
		return (len(board)-1, 0)
	return random.choice(options)


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
	return len(gamma)

def delta(board1, board2):
	g1 = gamma(board1)
	g2 = gamma(board2)
	if len(g2) > len(g1):
		g1, g2, board1, board2 = g2, g1, board2, board1

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
			data = json.loads(jData)
			return data
	except:
		print("ERROR: could not find file: " + str(fileName))
		return []


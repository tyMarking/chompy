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

#only depends on size of board, contents ignored
def getBoardPermutations(board):
	rows = len(board)
	cols = len(board[0])

	globalKey = str(rows) + "--" + str(cols)
	if globalKey in global_perms.keys():
		return global_perms[globalKey]
	#build 
	baseB = genBoard(rows,cols)
	perms = []
	bXparent = {dKey(baseB) : []}
	endB = genEndBoard(rows,cols)
	cB = baseB
	toCheck = [baseB]
	while len(toCheck) > 0:
		moves = getChoices(cB)
		for move in moves:
			nB = copy(cB)
			bite(nB,move)
			if dKey(nB) in bXparent.keys():
				if cB not in bXparent[dKey(nB)]:
					bXparent[dKey(nB)].append(cB)
			else:
				bXparent[dKey(nB)] = [cB]

			if nB not in toCheck:
				toCheck.append(nB)
		toCheck.remove(cB)
		perms.append(cB)
		if len(toCheck) == 0:
			break
		cB = toCheck[0]

	global_perms[globalKey] = (perms, bXparent)
	return (perms, bXparent)


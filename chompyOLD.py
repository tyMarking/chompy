#board: 2D array, -1 = posion, 0 = uneaten, 1 = eaten 

import random
import queue

global_perms = {}
def main(rows, cols):
	game_engine((rows,cols))


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

def copy(board):
	return [row[:] for row in board]

def dKey(board):
	key = ""
	for row in board:
		key += "/"
		for s in row:
			key += str(s)
	return key

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

def get_choices(board):
	options = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				options.append((i,j))
	return options

def get_inverse_choices(board):
	options = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 1:
				options.append((i,j))
	return options


def choice_random(board):
	options = get_choices(board)
	#only poison left
	if len(options) == 0:
		return (len(board)-1, 0)
	return random.choice(options)

def check_done(board):
	return board[-1][0] != -1

#only depends on size of board, contents ignored
def get_board_permutations(board):
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
		moves = get_choices(cB)
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




def gen_path_numbers(board):
	#dictionary of board permutations with their playable options
	#build perms as it goes?
	#start with fully bitten board
	rows = len(board)
	cols = len(board[0])

	endBoard = genEndBoard(rows, cols)
	startBoard = genBoard(rows, cols)

	bXnum = {dKey(endBoard) : 0}

	perms, bXparents = get_board_permutations(board)
	#permXchoices = {}
	#sorted by least number of choices
	evalQ = queue.PriorityQueue()
	for b in perms:
		#permXchoices[b] = len(get_choices(b))
		evalQ.put((len(get_choices(b)), b))

	evalQ.put((-1, endBoard))

	checked = []

	while evalQ.qsize() > 0:
		#print("Q size: " + str(evalQ.qsize()))
		cB = evalQ.get()[1]
		#print("cB:")
		#display(cB)
		num = bXnum[dKey(cB)]
		#print("cB's num: " + str(num))

		for parent in bXparents[dKey(cB)]:
			#print("parent:")
			#display(parent)
			#print(bXnum.keys())
			#print("parent key: " + str(dKey(parent)))
			if not (dKey(parent) in bXnum.keys()):
				#print("condition 1")
				bXnum[dKey(parent)] = num + 1
			elif (num + 1) % 2 == 1 and (bXnum[dKey(parent)] % 2 == 0 or (num+1) < bXnum[dKey(parent)]):
				#print("condition 2")
				bXnum[dKey(parent)] = num + 1
			elif (num + 1) < bXnum[dKey(parent)] and bXnum[dKey(parent)] % 2 == 0:
				#print("condition 3")
				bXnum[dKey(parent)] = num + 1
			
	return bXnum


				


#size = (rows,cols)
def game_engine(size):
	rows = size[0]
	cols = size[1]
	board = genBoard(rows,cols)

	bXnum = gen_path_numbers(board)

	#get dict of children
	perms, bXparent = get_board_permutations(board)
	bXchild = {}
	for b in perms:
		bXchild[dKey(b)] = []
	for b in perms:
		for parent in bXparent[dKey(b)]:
			if not b in bXchild[dKey(parent)]:
				bXchild[dKey(parent)].append(b)

	for c in bXchild[dKey(board)]:
		if bXnum[dKey(c)] % 2 == 0:
			display(c)




	"""
	while True:
		print("Player 1s turn")
		display(board)
		play = choice_random(board)
		bite(board, play)
		display(board)
		if check_done(board):
			print("Player 1 Lost!")
			break

		print("Player 2s turn")
		display(board)
		play = choice_random(board)
		bite(board, play)
		display(board)
		if check_done(board):
			print("Player 2 Lost!")
			break
	"""


def game_tick(board, turn):
	#todo
	pass

if __name__ == '__main__':
	
	#board = genEndBoard(3,15)
	
	#print(gen_path_numbers(board))
	#for i in range(21,30):
		#print("3x"+str(i))
		#game_engine((3,i))

	game_engine((8,10))
	#gen_path_numbers(genBoard(4,5))
	#main(2,5)


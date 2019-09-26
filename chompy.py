#board: 2D array, -1 = posion, 0 = uneaten, 1 = eaten 

import random

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

def choice_random(board):
	options = get_choices(board)
	#only poison left
	if len(options) == 0:
		return (len(board)-1, 0)
	return random.choice(options)

def check_done(board):
	return board[-1][0] != -1

#size = (rows,cols)
def game_engine(size):
	rows = size[0]
	cols = size[1]
	board = genBoard(rows,cols)
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



def game_tick(board, turn):
	#todo
	pass

if __name__ == '__main__':

	main(2,5)


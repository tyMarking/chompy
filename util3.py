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


states = [
[1], [2], [1,1], [2,1], [2,2]
]

addRow(states, 3)
addCol(states, 3)

print("\nNew States")
print(states)

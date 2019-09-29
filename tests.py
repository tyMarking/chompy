import utility as util
import numpy as np
import extendBoardStates as ebs
"""
board = util.genBoard(3,5)
board[0][4] = 1
board[0][3] = 1
board[1][4] = 1
board[2][4] = 1
util.display(board)
#board[2][3] = 1
print(util.gamma(board))

data = util.load("./data/3x5TEST3")
print(data)
board = data[0][0]
util.display(board)
print(data[0][1])S
print(data[0][2])
#util.store([(board, [], 1)], "./data/3x5TEST2")



"""

# b1, b2 = util.genBoard(3,5), util.genBoard(3,5)
# util.bite(b1, (0,4))
# util.bite(b1, (2,4))
# util.bite(b2, (1,3))

# print("B1")
# util.display(b1)
# print("B2")
# util.display(b2)

# print(util.delta(b1,b2))
# print(util.isRelated(b1,b2))
# print(util.isDecendent(b2,b1))


def extendToMxN(m, n):
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
	if m < 2 or n < 2:
		print("Board must be at least 2x2")
	elif m == 2 and n == 2:
		return states2x2

	currBoards = np.copy(states2x2)

	# print(m)
	# print(n)

	currM = 2
	currN = 2
	while (currM < n and currN < n):
		if (currM < m):
			currBoards = ebs.appendColToBoardStates(currBoards)
			print(len(currBoards))
		if (currN < n):
			currBoards = ebs.appendRowToBoardStates(currBoards)
			print(len(currBoards))
		currM = len(currBoards[0])
		currN = len(currBoards[0][0])
		# print(currM)
		# print(currN)

	return currBoards

extendedBoardStates = extendToMxN(10, 10)
print(len(extendedBoardStates[0]))
print(len(extendedBoardStates[0][0]))
# for i in range(len(extendedBoardStates)):
	# print(extendedBoardStates[i])
	# print("\n")
	# if i > 50:
		# break
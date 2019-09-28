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

#arr = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]
#added = np.insert(arr, 0, 0, axis=0)
#print(added)

arr = [
	[[0 ,1],
	 [-1,0]],
	[[1 ,1],
	 [-1,0]],
	[[0 ,1],
	 [-1,1]],
	[[1 ,1],
	 [-1,1]]
]
newStates = ebs.appendRowToBoardStates(arr)
# print(newStates)
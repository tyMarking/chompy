import utility as util

board = util.genBoard(3,5)
board[0][4] = 1
board[0][3] = 1
board[1][4] = 1
#board[2][4] = 1
util.display(board)
#board[2][3] = 1
"""
data = util.load("./data/3x5TEST3")
print(data)
board = data[0][0]
util.display(board)
print(data[0][1])
print(data[0][2])
#util.store([(board, [], 1)], "./data/3x5TEST2")
"""

print(util.file(board))
import utility as util

#board = util.genBoard(3,5)
#board[2][3] = 1
data = util.load("./data/3x5TEST3")
print(data)
board = data[0][0]
util.display(board)
print(data[0][1])
print(data[0][2])
#util.store([(board, [], 1)], "./data/3x5TEST2")
import utility as util 
import heritage

b = util.genBoard(3,4)
util.bite(b, (0,1))
util.bite(b, (2,2))
util.display(b)

h = heritage.getHeritage([b])
for key in h.keys():
	for board in h[key]:
		util.display(board)
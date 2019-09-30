import utility as util 
import heritage
import chompyDriver as cd
"""
b = util.genBoard(3,4)
util.bite(b, (0,1))
util.bite(b, (2,2))
util.display(b)

h = heritage.getHeritage([b])
for key in h.keys():
	for board in h[key]:
		util.display(board)
"""
"""
b = util.genBoard(3,4)
util.bite(b, (0,0))
util.bite(b, (2,1))

util.display(b)
util.unBite(b, (0,1))
util.display(b)
"""
cd.seed()
cd.cleanup()
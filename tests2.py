import utility as util 
import heritage
import chompyDriver as cd
import profile, cProfile 
#pstats, StringIO
"""
pr = cProfile.Profile()
pr.enable()
cd.main()
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
"""
profile.run("chompyDriver.py")


#b = util.genBoard(2,2)

#print(util.getChoices(b))
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
#cd.seed()
#cd.cleanup()


"""
b = util.genBoard(3,4)
util.bite(b, (0,1))
util.bite(b, (2,2))
util.display(b)
print(b)
print(util.dKey(b))
print(util.revDKey(util.dKey(b)))

states2x2 = [
	[[False,False],
	 [False,False]],
	[[False,True],
	 [False,False]],
	[[True,True],
	 [False,False]],
	[[False,True],
	 [False,True]],
	[[True,True],
	 [False,True]]
	]

for state in states2x2:
	util.display(state)
"""

#x = util.reduceToRF(b)
#print(x)
#print(util.reconstructFromRF(x, 4))

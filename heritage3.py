import numpy as np
import util3 as util



def getHeritage(state):
	children = []
	#get choices needs to be upgraded to new board state
	bites = util.getChoices(state)
	for bite in bites:
		parent = state.copy()
		util.bite(parent, bite)
		children.append(parent)
	return children



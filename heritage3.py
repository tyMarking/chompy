import numpy as np
import util3 as util



def getChildren(state):
	children = []
	bites = util.getChoices(state)
	for bite in bites:
		child = util.bite(state, bite)
		if util.getN(child) >= util.getM(child):
			children.append(child)
	return children

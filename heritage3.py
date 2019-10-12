import numpy as np
import util3 as util



def getChildren(state):
	children = []
	#print("State: " +str(state))
	bites = util.getChoices(state)
	#print("Choices: " + str(bites))
	for bite in bites:
		child = util.bite(state, bite)
		#if util.getN(child) >= util.getM(child):
		children.append(child)
	return children

import numpy as np
import util3 as util
from multiprocessing import Pool


def getChildren(state):

	children = []
	#print("State: " +str(state))
	bites = util.getChoices(state)
	#print("Choices: " + str(bites))
	
	items = []
	for bite in bites:
		items.append((state, bite))

	for bite in bites:
		child = util.bite(state, bite)
		#if util.getN(child) >= util.getM(child):
		children.append(child)
	return children

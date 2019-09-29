import numpy as np 
import utility as util

def getHeritage(states):
	
	stateXparents = {}
	
	for state in states:
		stateXparents[util.dKey(state)] = [] 
		bites = util.gamma(state)
		print("Bites: ")
		print(bites)
		print("\n\n")
		for bite in bites:
			newBites = [a[:] for a in bites]
			newBites.remove(bite)

			print("new bites: ")
			print(newBites)
			parent = util.superimpose( (len(state), len(state[0])), newBites)
			print("parent: ")
			util.display(parent)
			if np.all(parent == state):
				continue
			"""
			print("parents from dict")
			print(stateXparents[util.dKey(state)])
			print("parent")
			print(parent)
			"""
			isIn = False

			for dictParent in stateXparents[util.dKey(state)]:
				if np.all(parent == dictParent):
					isIn = True
					break

			if not isIn:
				stateXparents[util.dKey(state)].append(parent)
		return stateXparents

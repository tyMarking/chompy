import numpy as np 
import utility as util

"""
Look don't ask how it works.
I won't know.
I don't know.
It's a mess but it covers all cases (I think)
"""


def getHeritage(states):
	
	stateXparents = {}
	
	for state in states:
		stateXparents[util.dKey(state)] = []

		bites = util.gamma(state)
		for bite in bites:

			if not (bite[0] == len(state)-1 or bite[1] == 0 or (state[bite[0]+1][bite[1]-1] == 0 
			and not (state[bite[0]][bite[1]-1] == 1 and state[bite[0]+1][bite[1]] == 1)) ):
				newRow = bite[0] + 1
				newCol = bite[1] - 1

				while newRow < len(state) and newCol > -1 and state[newRow][newCol] == 1:
					newRow += 1
					newCol -= 1

				if newRow != len(state) and newCol != 0:

					if (state[bite[0]][newCol] == 1 or state[newRow][bite[1]] == 1):
						continue		

			parent = np.copy(state).tolist()
			util.unBite(parent, bite)
			stateXparents[util.dKey(state)].append(parent)
	return stateXparents

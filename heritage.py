import numpy as np 
import utility as util

def getHeritage(states):
	
	stateXparents = {}
	
	for state in states:
		stateXparents[util.dKey(state)] = []

		bites = util.gamma(state)
		for bite in bites:

			if not (bite[0] == len(state)-1 or bite[1] == 0 or (state[bite[0]+1][bite[1]-1] == 0 and not (state[bite[0]][bite[1]-1] == 1 and state[bite[0]+1][bite[1]] == 1)) ):
				#Check for square shit


				
				#don't ask
				#if bite[1] > 0 and state[bite[0]][bite[1]-1] == 1 and bite[0] < len(state)-1 and state[bite[0]+1][bite[1]] and state[bite[0]+1][bite[1]-1] == 0:
					#continue
				#print("bite: " + str(bite))
				newRow = bite[0] + 1
				newCol = bite[1] - 1
				while newRow < len(state) and newCol > -1 and state[newRow][newCol] == 1:
					#print("itered")
					newRow += 1
					newCol -= 1
				if newRow != len(state) and newCol != 0:
					#print("New row and col: " + str(newRow) + ", " + str(newCol))
					#if not on edge and cell to left or down of bite outside square == 1
					if (state[bite[0]][newCol] == 1 or state[newRow][bite[1]] == 1):
						#print("Continued")
						continue
					#if bite[1] > 0 and state[bite[0]][bite[1]-1] == 1 and bite[0] < len(state)-1 and state[bite[0]+1][bite[1]] and state[bite[0]+1][bite[1]-1] == 0:

				

			parent = np.copy(state)
			util.unBite(parent, bite)
			stateXparents[util.dKey(state)].append(parent)
	return stateXparents

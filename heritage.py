import numpy as np 
import utility as util

"""
Look don't ask how it works.
I won't know.
I don't know.
It's a mess but it covers all cases (I think)
"""
"""
def getPBites(board):
	rowFiles = [0]*len(board)
	colRanks = [0]*len(board[0])
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 1:
				rowFiles[i] = (len(board[i])-j)
				break
	for i in range(len(board[0])):
		for j in reversed(range(len(rowFiles))):
			if rowFiles[j] >= len(board[0])-i:
				colRanks[i] = j+1
				break
	print("rowFiles: " + str(rowFiles))
	print("colRanks: " + str(colRanks))
	ret = []
	for bite in util.getBitten(board):
		if colRanks[bite[1]] > bite[0]+1:
			continue
		if rowFiles[bite[0]] > len(board[0])-(bite[1]):
			continue
		print(bite)
		ret.append(bite)
	return ret
"""

def getHeritage(states):
	stateXchildren = {}

	for state in states:
		key = util.dKey(state)
		stateXchildren[key] = []
		bites = util.getChoices(state)

		for bite in bites:

			parent = np.copy(state)
			util.bite(parent, bite)
			stateXchildren[key].append(parent.tolist())
	return stateXchildren


"""
def getHeritage(states):

	stateXparents = {}

	for state in states:
		dKey = util.dKey(state)
		stateXparents[dKey] = []

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
			stateXparents[dKey].append(parent)
	return stateXparents
"""

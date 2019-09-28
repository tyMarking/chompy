import utility as util
import numpy as np

def appendRowToBoardStates(oldStates):
	newStates = []
	for oldState in oldStates:
		file = util.file(oldState)
		n = len(oldState)
		# m = len(oldState[0] + 1)
		maxCol = 0

		blankNewState = np.insert(oldState, 0, 0, axis=0)
		print(blankNewState)
		#if the oldState does not have any bites or bites only
		#from the first column, the bites in the new row can be from
		#any column up to n
		if file == 0 or file == 1:
			if file == 0:
				#for the special case of 0, add the blank state
				newStates.append(blankNewState)
			maxCol = n
		#if the oldState has bites taken out of it that aren't from the end
		#or beginning, the bites in the new row can be from any column
		#from m to the file
		elif not file == n:
			maxCol = file
		#for file == n, the default maxCol 0, requires that only the bite with
		#the whole row is taken.	
		for i in range(maxCol):
			addNewBittenRow(newStates, blankNewState, i)
	return newStates

def addNewBittenRow(newStates, blankNewState, col):
	newState = util.copy(blankNewState)
	util.bite(newState, [0, col])
	print(newState)
	newStates.append(newState)
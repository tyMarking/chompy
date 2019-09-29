import utility as util
import numpy as np

def appendRowToBoardStates(oldStates):
	newStates = []
	for oldState in oldStates:
		lastFile = util.lastRowFile(oldState)
		n = len(oldState[0])

		#the first column that new bites are taken from
		firstCol = n - lastFile

		#create a copy of the oldState with a new row of 0s at the bottom,
		#then move the poison into the bottom row
		blankNewState = np.append(oldState, np.zeros((1, n)), axis=0)
		blankNewState[-2][0] = 0
		blankNewState[-1][0] = -1

		if firstCol == 1 and blankNewState[-3][0] == 1:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-2][0] = 1
			addNewBittenRowsInRange(newStates, moddedNewState, firstCol, n)

		#if the second to last row does not have any bites, only add the blank state
		if lastFile == 0:
			newStates.append(blankNewState)
			continue

		addNewBittenRowsInRange(newStates, blankNewState, firstCol, n)

	return newStates

def appendColToBoardStates(oldStates):
	newStates = []
	for oldState in oldStates:
		rank = util.rank(oldState)
		#n = len(oldState[0])
		m = len(oldState)

		#firstRow is the first row of all new cols that have bites taken from it
		#since rank starts at 1 and ends at m, we subract 1
		firstRow = rank - 1
		# print("Rank: " + str(rank) + "\n")
		blankNewState = np.insert(oldState, 0, 0, axis=1)
		blankNewState[-1][1] = 0
		blankNewState[-1][0] = -1
		#if the oldState does not have any bites or bites only
		#from the first column, the bites in the new row can be from
		#any column up to n
		if rank <= 1:
			if rank == 0:
				#for the special case of 0, add the blank state
				newStates.append(blankNewState)
				# print(blankNewState)
				# print("\n")
			firstRow = 0

		#for rank == m, the default maxRow 1, requires that only the bite with
		#the whole column is taken.
		# print(m)
		for i in range(firstRow, m):
			addNewBittenCol(newStates, blankNewState, i, m)
	return newStates

#newStates is what the state is appended to
#blankNewState is the unbitten state based off of the state from a smaller board
#col is the column that the bite is taken from
#the bite is taken at [0, col]
def addNewBittenRowsInRange(newStates, blankNewState, rMin, rMax):
	newStates.append(blankNewState)
	for i in range(rMin, rMax):
		newState = np.copy(blankNewState)
		util.bite(newState, [-1, i])
		newStates.append(newState)

#same as addNewBittenRow, but col is replaced with row
#row is the row that the bite is taken from
#m is the last column
#the bite is taken at [row, m]
def addNewBittenCol(newStates, blankNewState, row, m):
	newState = np.copy(blankNewState)
	util.bite(newState, [row, m])
	# print(newState)
	# print("\n")
	newStates.append(newState)
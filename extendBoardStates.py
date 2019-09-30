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

		#if the second to last row does not have any bites, only add the blank state
		if lastFile == 0:
			newStates.append(blankNewState)
			continue

		if firstCol == 1 and blankNewState[-3][0] == 1:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-2][0] = 1
			addNewBittenRowsInRange(newStates, moddedNewState, firstCol, n)

		addNewBittenRowsInRange(newStates, blankNewState, firstCol, n)

	return newStates

#TODO modify the col expansion to add at the beginning
def appendColToBoardStates(oldStates):
	newStates = []
	for oldState in oldStates:
		lastColRank = util.lastColRank(oldState)

		#n = len(oldState[0])
		m = len(oldState)

		#lastRow is the upper bound of the for loop.
		#Do not add 1 even though the upper bound is not inclusive b/c then poison would be bitten
		lastRow = lastColRank

		#insert a new column at the beginning, then shif the poison over
		blankNewState = np.insert(oldState, 0, 0, axis=1)
		blankNewState[-1][1] = 0
		blankNewState[-1][0] = -1

		#if there are no bites next to the new column, add only the blank state
		if lastColRank == 0:
			newStates.append(blankNewState)
			continue

		#if it is valid for a bite to be there, add a new state where there is a bite
		#where the old poison was
		#the first part of the if is the same as saying blankNewState[-2][1] == 1
		if lastRow == m-1 and blankNewState[-1][2] == 1:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-1][1] = 1
			addNewBittenColsInRange(newStates, moddedNewState, lastRow)

		addNewBittenColsInRange(newStates, blankNewState, lastRow)
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
def addNewBittenColsInRange(newStates, blankNewState, rowMax):
	newStates.append(blankNewState)
	for i in range(0, rowMax):
		newState = np.copy(blankNewState)
		util.bite(newState, [i, 0])
		newStates.append(newState)
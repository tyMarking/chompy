import utility as util
import numpy as np
import heritage

def appendRowToBoardStates(oldStates, heritages):
	newStates = []
	extendedHeritage = {}
	for oldState in oldStates:
		lastFile = util.lastRowFile(oldState)

		n = len(oldState[0])

		#the first column that new bites are taken from
		firstCol = n - lastFile

		#create a copy of the oldState with a new row of 0s at the bottom,
		#then move the poison into the bottom row
		blankNewState = addNewRowToBoardState(oldState, n)

		#if the second to last row does not have any bites, only add the unmodified state
		if lastFile == 0:
			newStates.append(blankNewState)
			oldHeritages = heritages[util.dKey(oldState)]
			extendedHeritage[util.dKey(blankNewState)] = extendHeritageUnmodded(oldHeritages, blankNewState, False, 0)
			continue

		#if the 2 squares directly next to the poison have been bitten, add an additional new state
		# with the old poison's position bitten
		if oldState[-1][1] and oldState[-2][0]:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-2][0] = 1
			addNewBittenRowsInRange(newStates, moddedNewState, firstCol, n, extendedHeritage, heritages, True)

		addNewBittenRowsInRange(newStates, blankNewState, firstCol, n, extendedHeritage, heritages, False)

	return [newStates, extendedHeritage]

def appendColToBoardStates(oldStates, heritages):
	newStates = []
	extendedHeritage = {}

	for oldState in oldStates:
		lastColRank = util.lastColRank(oldState)

		#n = len(oldState[0])
		m = len(oldState)

		#lastRow is the upper bound of the for loop.
		#Do not add 1 even though the upper bound is not inclusive b/c then poison would be bitten
		lastRow = lastColRank

		#insert a new column at the beginning, then shif the poison over
		blankNewState = addNewToBoardState(oldState)
		oldHeritage = heritages[util.dKey(oldState)]

		#if there are no bites next to the new column, add only the blank state
		if lastColRank == 0:
			newStates.append(blankNewState)
			extendedHeritage[util.dKey(blankNewState)] = extendHeritageUnmodded(oldHeritage, blankNewState, False, 1)
			continue

		#if it is valid for a bite to be there, add a new state where there is a bite
		#where the old poison was
		#the first part of the if is the same as saying blankNewState[-2][1] == 1
		if lastRow == m-1 and blankNewState[-1][2] == 1:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-1][1] = 1
			addNewBittenColsInRange(newStates, moddedNewState, lastRow, extendedHeritage, oldHeritage, True)

		addNewBittenColsInRange(newStates, blankNewState, lastRow, extendedHeritage, oldHeritage, False)
	return [newStates, extendedHeritage]

#returns an array of the children of the unmodified state
#filled poison is a bool that states if the old position of the poison is 0 or 1
def extendHeritageUnmodded(oldHeritage, newState, filledPoison, axis):
	stop = len(newState[0]) if axis == 0 else len(newState)-1
	return extendHeritage(oldHeritage, newState, filledPoison, axis, stop, 0)


def extendHeritage(oldHeritage, newState, filledPoison, axis, stop, start):
	newHeritage = []
	length = len(newState[0])

	#add the old modified heritage
	for oldChild in oldHeritage:
		#extend the child
		#add newChild to newHeritage
		if axis == 0:
			newHeritage.append(addNewRowToBoardState(child, length))
		elif axis == 1:
			newHeritage.appen(addNewColToBoardState(child, length))

	#add/create the new heritage
	#if the old poison wasn't filled, take a bite at that position
	if not filledPoison:
		if axis == 0:
			newHeritage.append(bite(np.copy(newState), (-2, 0)))
		elif axis == 1:
			newHeritage.append(bite(np.copy(newState), (-1, 1)))

	#loop through the new row/col, adding the bite at each point be as child
	if axis == 0:
		#adding row
		#start at 1 so the poison isn't bitten
		for i in range(start, stop):
			newHeritage.append(bite(np.copy(newState), (-1, i)))
	elif axis == 1:
		#adding col
		for i in range(start, stop):
			newHeritage.append(bite(np.copy(newState), (0, i)))

	return newHeritage

#used to be called prependColToBoardState
def addNewColToBoardState(state):
	newState = np.insert(state, 0, 0, axis=1)
	newState[-1][1] = 0
	#newState[-1][0] = -1
	return newState

def addNewRowToBoardState(state, length):
	newState = np.append(state, np.zeros((1, length)), axis=0)
	newState[-2][0] = 0
	#newState[-1][0] = -1
	return newState

#newStates is what the state is appended to
#blankNewState is the unbitten state based off of the state from a smaller board
#col is the column that the bite is taken from
#the bite is taken at [0, col]
def addNewBittenRowsInRange(newStates, blankNewState, rMin, rMax, extendedHeritage, hertiage, filledPoison):
	#add the state based off of the old, unmodified state
	newStates.append(blankNewState)

	length = len(blankNewState[0])

	#this adds the heritage based off the unmodified state
	extendedHeritage[util.dKey(blankNewState)] = extendHeritageUnmodded(heritage, blankNewState, filledPoison, 0)

	#adds states that are modified from the base state
	for i in range(rMin, rMax):
		newState = np.copy(blankNewState)
		util.bite(newState, [-1, i])
		newStates.append(newState)

		extendedHeritage[util.dKey(newState)] = extendHeritage(heritage, newState, filledPoison, 0, i, 1)

		"""
		#old method, included in case this gets screwed up

		heritance = heritage.getHeritage([newState])
		dKeyStateBitten = util.dKey(newState)
		# extendedHeritage[dKeyStateBitten] = []
		extendedHeritage[dKeyStateBitten] = heritance[dKeyStateBitten]
		"""
#same as addNewBittenRow, but col is replaced with row
#row is the row that the bite is taken from
def addNewBittenColsInRange(newStates, blankNewState, rowMax, extendedHeritage, hertiage, filledPoison):
	newStates.append(blankNewState)

	#add the heritage for the current unmodified state
	extendedHeritage[util.dKey(blankNewState)] = extendHeritageUnmodded(heritage, blankNewState, filledPoison, 1)

	stop = len(blankNewState) - 1

	for i in range(0, rowMax):
		newState = np.copy(blankNewState)
		util.bite(newState, [i, 0])
		newStates.append(newState)

		extendedHeritage[util.dKey(newState)] = extendHeritage(heritage, newState, filledPoison, 0, stop, i)

		"""
		heritance = heritage.getHeritage([newState])
		dKeyStateBitten = util.dKey(newState)
		# extendedHeritage[dKeyStateBitten] = []
		extendedHeritage[dKeyStateBitten] = heritance[dKeyStateBitten]
		"""

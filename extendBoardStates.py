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

		#if the second to last row does not have any bites, only add the blank state
		if lastFile == 0:
			newStates.append(blankNewState)

			#add the heritage based off of the unmodified state
			newHeritages = heritages[util.dKey(oldState)]
			dKeyState = util.dKey(blankNewState)
			for newHeritage in newHeritages:
				if dKeyState in extendedHeritage.keys():
					extendedHeritage[dKeyState].append(addNewRowToBoardState(newHeritage, n))
				else:
					extendedHeritage[dKeyState] = [addNewRowToBoardState(newHeritage, n)]

			continue

		if firstCol == 1 and blankNewState[-3][0] == 1:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-2][0] = 1
			addNewBittenRowsInRange(newStates, moddedNewState, firstCol, n, extendedHeritage, heritages, oldState)

		addNewBittenRowsInRange(newStates, blankNewState, firstCol, n, extendedHeritage, heritages, oldState)

	return [newStates, extendedHeritage]

def appendColToBoardStates(oldStates, hertiages):
	newStates = []
	extendedHeritage = {}

	print(hertiages)

	for oldState in oldStates:
		lastColRank = util.lastColRank(oldState)

		#n = len(oldState[0])
		m = len(oldState)

		#lastRow is the upper bound of the for loop.
		#Do not add 1 even though the upper bound is not inclusive b/c then poison would be bitten
		lastRow = lastColRank

		#insert a new column at the beginning, then shif the poison over
		blankNewState = prependColToBoardState(oldState)

		#if there are no bites next to the new column, add only the blank state
		if lastColRank == 0:
			newStates.append(blankNewState)

			newHeritages = hertiages[util.dKey(oldState)]
			dKeyState = util.dKey(blankNewState)
			for newHeritage in newHeritages:
				if dKeyState in extendedHeritage.keys():
					extendedHeritage[dKeyState].append(prependColToBoardState(newHeritage))
				else:
					extendedHeritage[dKeyState] = [prependColToBoardState(newHeritage)]
			continue

		#if it is valid for a bite to be there, add a new state where there is a bite
		#where the old poison was
		#the first part of the if is the same as saying blankNewState[-2][1] == 1
		if lastRow == m-1 and blankNewState[-1][2] == 1:
			moddedNewState = np.copy(blankNewState)
			moddedNewState[-1][1] = 1
			addNewBittenColsInRange(newStates, moddedNewState, lastRow, extendedHeritage, heritages, oldState)

		addNewBittenColsInRange(newStates, blankNewState, lastRow, extendedHeritage, hertiages, oldState)
	return [newStates, extendedHeritage]

def prependColToBoardState(state):
	newState = np.insert(state, 0, 0, axis=1)
	newState[-1][1] = 0
	newState[-1][0] = -1
	return newState

def addNewRowToBoardState(state, length):
	newState = np.append(state, np.zeros((1, length)), axis=0)
	newState[-2][0] = 0
	newState[-1][0] = -1
	return newState


#newStates is what the state is appended to
#blankNewState is the unbitten state based off of the state from a smaller board
#col is the column that the bite is taken from
#the bite is taken at [0, col]
def addNewBittenRowsInRange(newStates, blankNewState, rMin, rMax, extendedHeritage, hertiages, oldState):
	newStates.append(blankNewState)

	length = len(blankNewState[0])

	#this adds the heritage based off the unmodified state
	newHeritages = hertiages[util.dKey(oldState)]
	dKeyState = util.dKey(blankNewState)
	for newHeritage in newHeritages:
		if dKeyState in extendedHeritage.keys():
			extendedHeritage[dKeyState].append(addNewRowToBoardState(newHeritage, length))
		else:
			extendedHeritage[dKeyState] = [addNewRowToBoardState(newHeritage, length)]

	for i in range(rMin, rMax):
		newState = np.copy(blankNewState)
		util.bite(newState, [-1, i])
		newStates.append(newState)
		heritance = heritage.getHeritage([newState])
		dKeyStateBitten = util.dKey(newState)
		if dKeyStateBitten in extendedHeritage.keys():
			extendedHeritage[dKeyStateBitten].append(heritance[dKeyStateBitten])
		else:
			extendedHeritage[dKeyStateBitten] = [heritance[dKeyStateBitten]]

#same as addNewBittenRow, but col is replaced with row
#row is the row that the bite is taken from
def addNewBittenColsInRange(newStates, blankNewState, rowMax, extendedHeritage, hertiages, oldState):
	newStates.append(blankNewState)

	length = len(blankNewState[0])

	newHeritages = hertiages[util.dKey(oldState)]
	dKeyState = util.dKey(blankNewState)
	#add the heritage for the current state
	for newHeritage in newHeritages:
		if dKeyState in extendedHeritage.keys():
			extendedHeritage[dKeyState].append(prependColToBoardState(newHeritage, length))
		else:
			extendedHeritage[dKeyState] = [addNewRowToBoardState(newHeritage, length)]

	for i in range(0, rowMax):
		newState = np.copy(blankNewState)
		util.bite(newState, [i, 0])
		newStates.append(newState)
		heritance = heritage.getHeritage([newState])
		if dKeyStateBitten in extendedHeritage.keys():
			extendedHeritage[dKeyStateBitten].append(heritance[dKeyStateBitten])
		else:
			extendedHeritage[dKeyStateBitten] = [heritance[dKeyStateBitten]]
import utility as util

def appendRowToBoardStates(oldStates):
	newStates = []
	for oldState in oldStates:
		file = util.file(oldState)
		n = len(oldState)
		m = len(oldState[0] + 1)
		#if the oldState does not have any bites or bites only
		#from the first column, the bites in the new row can be from
		#any column up to n
		if file == 0 or file == 1:
			newState = addBlankRowToBoardState(oldState, m)
			if file == 0:
				newStates.append(newState)
			for i in range(n):
				print(i)				

def addBlankRowToBoardState(oldState, m):
	newRow = []
	for i in range(m):
		newRow[i] = 0
	return util.copy(oldState).insert(0, newRow)
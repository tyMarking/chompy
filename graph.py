import utility as util
#import queue
import numpy as np

def gen_path_numbers(perms, bXparents):
	#dictionary of board permutations with their playable options
	#build perms as it goes?
	#start with fully bitten board

	endBoard = (util.genEndBoard(len(perms[0]), len(perms[0][0]))).astype(int).tolist()

	bXnum = {util.dKey(endBoard) : 0}
	#sorted by least number of choices
	"""
	evalQ = queue.PriorityQueue()
	for b in perms:
		evalQ.put((len(util.getChoices(b)), np.array(b).astype(int).tolist()))
	#evalQ.put((-1, endBoard))
	"""
	#choices:boards
	cXb = {}
	for i in range(len(endBoard)*len(endBoard[0])):
		cXb[i] = []
	for b in perms:
		cXb[len(util.getChoices(b))].append(b)

	checked = []

	for i in range(len(endBoard)*len(endBoard[0])):
		for cB in cXb[i]:
			cBKey = util.dKey(cB)
			num = bXnum[cBKey]
			for parent in bXparents[cBKey]:
				pKey = util.dKey(parent)
				if not (pKey in bXnum.keys()):
					bXnum[pKey] = num + 1
					continue
				pNum = bXnum[pKey]
				if (num + 1) % 2 == 1 and (pNum % 2 == 0 or (num+1) < pNum):
					bXnum[pKey] = num + 1
				elif (num + 1) < pNum and pNum % 2 == 0:
					bXnum[pKey] = num + 1

	"""
	while evalQ.qsize() > 0:

		cB = evalQ.get()[1]

		num = bXnum[util.dKey(cB)]

		for parent in bXparents[util.dKey(cB)]:
			pKey = util.dKey(parent)
			if not (pKey in bXnum.keys()):
				bXnum[pKey] = num + 1
			elif (num + 1) % 2 == 1 and (bXnum[pKey] % 2 == 0 or (num+1) < bXnum[pKey]):
				bXnum[pKey] = num + 1
			elif (num + 1) < bXnum[pKey] and bXnum[pKey] % 2 == 0:
				bXnum[pKey] = num + 1
	"""
	return bXnum



def getFirstMoves(perms, bXchild, bXnum):
	

	moves = []
	for c in bXchild[util.dKey(util.genBoard(len(perms[0]), len(perms[0][0])).astype(int).tolist())]:
		if bXnum[util.dKey(c)] % 2 == 0:
			rank = util.rank(c)
			file = util.rank(c)
			fmPos = (rank-1, len(c[0])-file)
			moves.append(fmPos)
	return moves
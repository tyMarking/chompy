import util3 as util
import heritage3
import os
from pathlib import Path 

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

etaData = util.load(DATA_FOLDER / "etaData.json")


#print(etaData[util.dKey([5,3,3,3,3])])

#print(util.file([3]))

n = 8

firstMoves = {}
for i in range(2,n+1):
	for j in range(i,n+1):
		fms = []
		emptyB = [j]*i
		children = heritage3.getChildren(emptyB)
		for child in children:
			if util.dKey(child) in etaData.keys():
				cNum = etaData[util.dKey(child)]
			else:
				cNum = etaData[util.dKey(util.mirror(child))]
			if cNum % 2 == 0:
				fms.append(child)
		firstMoves[str(i)+"X"+str(j)] = fms
util.store(firstMoves, DATA_FOLDER / "firstMovesV3.json")

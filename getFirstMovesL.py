import util3 as util
import heritage3
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc4/")
ETA_FOLDER = DATA_FOLDER / "etaData/"
#etaData = util.load(DATA_FOLDER / "etaData.dat")


#print(etaData[str([5,3,3,3,3])])

#print(util.file([3]))

n = 4

etaData = {}
for i in range (1,n+1):
	nFolder = ETA_FOLDER / (str(i)+"X"+str(i)+"/")
	print("Loading: " + str(i)+"X"+str(i))
	for f in range(i):
		for r in range(i):
			if f == 0 and r == 0:
				continue
			partData = util.load(nFolder / ("f="+str(r)+"_r="+str(f)+".dat"))
			for nodeN in partData:
				etaData[str(nodeN[0])] = nodeN[1]

	partData = util.load(nFolder / ("f="+str(i)+"_r="+str(i)+".dat"))
	for nodeN in partData:
		etaData[str(nodeN[0])] = nodeN[1]

	print("Loaded")

if str([2]) in etaData.keys():
    print("It's there!")
else:
    print("Nope sorry")

firstMoves = {}
mirrors = 0
for i in range(2,n+1):
	for j in range(i,n+1):
		fms = []
		emptyB = [j]*i
		children = heritage3.getChildren(emptyB)
		for child in children:
			if str(child) in etaData.keys():
				cNum = etaData[str(child)]
			else:
				mirrors += 1
				cNum = etaData[str(util.mirror(child))]
			if cNum % 2 == 0:
				fms.append(child)
		firstMoves[str(i)+"X"+str(j)] = fms
util.storeJson(firstMoves, DATA_FOLDER / "firstMovesV3-5_new_2.json")
print("Mirrors: " + str(mirrors))

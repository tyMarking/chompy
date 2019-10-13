import util3 as util 
import eta
from pathlib import Path
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")


def mirro(G):
	newGs = []
	#count = 0
	for g in G:
		newGs.append((g[0], g[1]))
	for g in G:
		#if len(g[0]) == g[0][0]:
		#count += 1
		mir = util.mirror(g[0])
		
		mirT = (mir, g[1])
		if mirT not in newGs:
			newGs.append(mirT)

	#print(count)
	return newGs

def gInNewGs(newGs, etaData, n):
	newNodes = []
	for g in newGs:
		#print("\n\ng: " + str(g))
		L = util.getL(g[0],n)
		#print("L: " + str(L))
		for l in L:
			N = util.combineG_L(g[0] ,l)
			#print(N)
			#print(g)
			#print("g: " + str(g)+"\tl: "+str(l) +" => " + str(N))
			#print("N: " + str(n))
			#print(N)
			#dat = [N, g[0], l, g[1]]
			dat = g
			#if dat not in newNodes:
			newNodes.append(dat)
			#else:
			#	print("DUPLICATE!!!!!!!")
	return newNodes


workingNodesData = util.load(DATA_FOLDER / "workingNodes.json")
n = workingNodesData[0]
print(len(workingNodesData[1]))
nodes = mirro(workingNodesData[1])
#nodes = workingNodesData[1]
print(len(nodes))
print("done mirroring")
newGs = []

gInNewGs(nodes, {}, n)

testGs = {}
for g in nodes:
	if util.dKey(g[0]) in testGs.keys():
		testGs[util.dKey(g[0])] += 1
		print(g)
	else:
		testGs[util.dKey(g[0])] = 1
#print(testGs)

numDupes = {}
for key in testGs.keys():
	val = testGs[key]
	if val in numDupes.keys():
		numDupes[val] += 1
	else:
		numDupes[val] = 1
print(numDupes)

for g in nodes:
	L = util.getL(g[0],n)
	for l in L:
		if (g[0],l) in newGs:
			#print("THERE IS A DUPLICATE: " + str((g[0],l)))
			pass
		else:
			newGs.append((g[0],l))

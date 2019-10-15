import util3 as util
import eta
import os
from pathlib import Path
import time
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

"""
start with 2x2 seed - have some way of tracking progress
for each g in G get L (don't need to do l max,max)
go through square cases and establish eta
go through non-square cases
do any manual eta if necessary
continue

Files:
etaData = {N : eta(N)}
workingNodes = [n-1,[(g,eta(g)), ]]
"""

MAX_SIZE = 10

def main():
	print("Loading Initial Data")
	etaData = util.load(DATA_FOLDER / "etaData.json")
	workingNodesData = util.load(DATA_FOLDER / "workingNodes.json")
	print("Loaded")

	timeBeginExpand = time.time()
	timeStart = timeBeginExpand

	timeDataFile = THIS_FOLDER / "expansionTime.csv"

	with open(timeDataFile, "w") as timeData:

		timeWriter = csv.writer(timeData, dialect='excel')

		timeWriter.writerow(["N", "Time Added", "Total Time"])

		for count in range(0, MAX_SIZE-workingNodesData[0]):
			timeStart = time.time()
			#data of form {node : eta}
			n = workingNodesData[0] + 1
			print("\nExpanding to " + str(n)+"X"+str(n))
			#working nodes [(g,eta(g)),]
			G = workingNodesData[1]
			#print("G: " + str(G))

			#print("etaData: " + str(etaData))

			#print("etaData: " + str(etaData))

			etaData, workingNodesData = expand(n, G, etaData)
			timeEnd = time.time()
			timeWriter.writerow([n, timeEnd-timeStart, timeEnd-timeBeginExpand])



#G = [(g, eta(g))]
def expand(n, G, etaData):
	nextWorkingNodes = []
	#for each g + l combo find eta and add to data

	#[N, g[0], l, g[1]]
	newGs = gInGs(G, etaData)
	newNodes = gInNewGs(newGs, etaData, n)

	muliProcessCost(newGs, n)

	newNodes.sort(key = lambda x: sum(x[0]))

	nodeInNodes(newNodes, etaData, nextWorkingNodes, n)


	#print("finished expand, etaData: " + str(etaData) + "\tnextWorkingNodes: " + str(nextWorkingNodes))
	#print("Storing...")
	util.store([n, nextWorkingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	#print("Stored")

	return etaData, [n, nextWorkingNodes]

def gInGs(G, etaData):
	"""
	newGs = []
	for g in G:
		newGs.append((g[0], g[1]))

	for g in G:
		if len(g[0]) == g[0][0]:
			mir = util.mirror(g[0])
			if (mir, g[1]) not in newGs:
				newGs.append((mir, g[1]))
				etaData[str(mir)] = g[1]

	return newGs
	"""
	newGs = []
	for g in G:
		newGs.append((g[0], g[1]))
		if len(g[0]) == g[0][0] and util.file(g[0]) > util.rank(g[0]):
			mir = util.mirror(g[0])

			newGs.append((mir, g[1]))
			etaData[str(mir)] = g[1]


	return newGs

def muliProcessCost(newGs, n):
	areaUnBittenXg = {}
	for i in range(1, (n-1)*(n-1)):
		areaUnBittenXg[i] = []
	for g in newGs:
		#print("g: " + str(g))
		areaUnBittenXg[len(util.getChoices(g[0]))].append(g)

def gInNewGs(newGs, etaData, n):
	newNodes = []
	for g in newGs:
		#print("\n\ng: " + str(g))
		L = util.getL(g[0],n)
		#print("L: " + str(L))
		for l in L:
			N = util.combineG_L(g[0] ,l)
			#print("g: " + str(g)+"\tl: "+str(l) +" => " + str(N))
			#print("N: " + str(n))
			#print(N)
			dat = [N, g[0], l, g[1]]
			# ifDat(dat, newNodes)
			# if dat not in newNodes:
			newNodes.append(dat)
			# else:
				# print("DUPLICATE!!!!!!!")
	return newNodes

def nodeInNodes(newNodes, etaData, nextWorkingNodes, n):
	for node in newNodes:

		N = node[0]
		g0 = node[1]
		l = node[2]
		g1 = node[3]
		#print("\n\netaData: " + str(etaData))
		#print("\n\nGetting eta for " + str(N))
		num = eta.eta(g0, l, g1, n, etaData)
		#print("N: " + str(N) + "\tnum: " + str(num))
		etaData[str(N)] = num
		nextWorkingNodes.append( (N, num) )

def seed():
	print("Seeding")
	etaData, workingNodes = util.seed()
	#print([2, workingNodes])
	util.store([2, workingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	print("Seeded")

def profileIt():
	seed()
	main()

if __name__ == "__main__":
	seed()
	main()

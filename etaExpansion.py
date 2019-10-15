import util3 as util
import eta
import os
from pathlib import Path
import time
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc3/")

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

MAX_SIZE = 5

def main():
	print("Loading Initial Data")
	#etaData = util.load(DATA_FOLDER / "etaData.json")
	evens = set(util.load(DATA_FOLDER / "evens.json"))

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
			#working nodes [g]
			G = workingNodesData[1]

			evens, workingNodesData = expand(n, G, evens)
			timeEnd = time.time()
			timeWriter.writerow([n, timeEnd-timeStart, timeEnd-timeBeginExpand])

def expand(n, G, evens):
	nextWorkingNodes = []
	#for each g + l combo find eta and add to data
	newNodes = gInNewGs(gInGs(G), n)
	del G
	sortNodes(newNodes)

	newEtaData = nodeInNodes(newNodes, evens, nextWorkingNodes, n)


	#print("finished expand, etaData: " + str(etaData) + "\tnextWorkingNodes: " + str(nextWorkingNodes))
	#print("Storing...")
	util.store([n, nextWorkingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(newEtaData, DATA_FOLDER / (str(n)+"X"+str(n)+"etaData.json"))
	util.store(list(evens), DATA_FOLDER / "evens.json")
	#print("Stored")

	return evens, [n, nextWorkingNodes]

def gInGs(G):
	newGs = []
	for g in G:
		if len(g) == g[0] and util.file(g) > util.rank(g):
			newGs.append(util.mirror(g))

	G = G + newGs
	return G

def gInNewGs(newGs, n):
	newNodes = []
	#print(newGs)
	for g in newGs:

		L = util.getL(g,n)
		for l in L:
			N = util.combineG_L(g ,l)
			dat = [N, g, l]

			newNodes.append(dat)

	return newNodes

def sortNodes(newNodes):
	newNodes.sort(key = lambda x: sum(x[0]))

def nodeInNodes(newNodes, evens, nextWorkingNodes, n):
	newEtaData = {}
	for node in newNodes:

		N = node[0]
		g = node[1]
		l = node[2]

		num = eta.eta(g, l, n, evens)

		if num % 2 == 0:
			evens.add(str(N))
			#if len(N) == N[0] and util.file(N) > util.rank(N):
			if N[0] > len(N):
				evens.add(str(util.mirror(N)))


		newEtaData[str(N)] = num
		nextWorkingNodes.append(N)
	return newEtaData

def seed():
	print("Seeding")
	etaData, workingNodes, evens= util.seed()
	#print([2, workingNodes])
	util.store([2, workingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "2X2etaData.json")
	util.store(evens, DATA_FOLDER / "evens.json")
	print("Seeded")

def profileIt():
	seed()
	main()

if __name__ == "__main__":
	seed()
	main()

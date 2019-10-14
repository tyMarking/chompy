import util3 as util
import eta
import os
from pathlib import Path
import time
import csv
from multiP import ProccesHandler

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

MULTI_PROCESS = True
THREADS = 2

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

MAX_SIZE = 20

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
			if MULTI_PROCESS:
				etaData, workingNodesData = multiExpand(n, G, etaData)
			else:
				etaData, workingNodesData = expand(n, G, etaData)
			timeEnd = time.time()
			timeWriter.writerow([n, timeEnd-timeStart, timeEnd-timeBeginExpand])


#G = [(g, eta(g))]
def expand(n, G, etaData):
	nextWorkingNodes = []
	#for each g + l combo find eta and add to data

	#[N, g[0], l, g[1]]
	newGs = gInGs(G, etaData)
	newNodes = gInNewGs(newGs, n)

	sortNodes(newNodes)

	nodeInNodes(newNodes, etaData, nextWorkingNodes, n)


	#print("finished expand, etaData: " + str(etaData) + "\tnextWorkingNodes: " + str(nextWorkingNodes))
	#print("Storing...")
	util.store([n, nextWorkingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	#print("Stored")

	return etaData, [n, nextWorkingNodes]

def multiExpand(n, G, etaData):
	nextWorkingNodes = []

	#[N, g[0], l, g[1]]
	newGs = gInGs(G, etaData)
	#dictionary of g's by choices
	areaUnBittenXg = {}
	for i in range(1,(n-1)*(n-1)):
		areaUnBittenXg[i] = []
	for g in newGs:
		#print("g: " + str(g))

		areaUnBittenXg[len(util.getChoices(g[0]))].append(g)

	handler = ProccesHandler(THREADS)

	#print("areaUnBittenXg: " + str(areaUnBittenXg))

	for i in range(1,(n-1)*(n-1)):
		Gi = areaUnBittenXg[i]
		#for g in Gi:
		for g in Gi:
			handler.add((g,n,etaData))

		handler.q.join()
		while not handler.outQ.empty():
			item = handler.outQ.get()
			for node in item:
				N = node[0]
				num = node[1]
				etaData[str(N)] = num
				nextWorkingNodes.append( (N, num) )
	

	util.store([n, nextWorkingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
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
		if g[0] == [4,4,3,3]:
			print("YES [4,4,3,3] EXISTS")
		if g[0] == [5,1,1]:
			print("YES [5,1,1] exists")
		if len(g[0]) == g[0][0] and util.file(g[0]) > util.rank(g[0]):
			mir = util.mirror(g[0])

			newGs.append((mir, g[1]))
			etaData[str(mir)] = g[1]


	return newGs

def gInNewGs(newGs, n):
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

def sortNodes(newNodes):
	newNodes.sort(key = lambda x: sum(x[0]))

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



def multiNodeInNodes(newNodes, etaData, n):
	ret = []
	for node in newNodes:

		N = node[0]
		g0 = node[1]
		l = node[2]
		g1 = node[3]

		num = eta.eta(g0, l, g1, n, etaData)
		ret.append((N, num))
	return ret

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

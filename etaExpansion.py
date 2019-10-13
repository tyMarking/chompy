import util3 as util
import eta
import os
from pathlib import Path
from multiprocessing import Pool

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")


"""
start with 2x2 seed - have some way of tracking progress
for each g in G get L (don't need to do l max,max)
go through square cases and establish eta
go through non-square cases
do any manual eta if necessary
continue

"""


"""
Files:
etaData = {N : eta(N)}
workingNodes = [n-1,[(g,eta(g)), ]]

"""
MAX_SIZE = 12

def main():
	print("Loading Initial Data")
	etaData = util.load(DATA_FOLDER / "etaData.json")
	workingNodesData = util.load(DATA_FOLDER / "workingNodes.json")
	print("Loaded")

	count = 0
	while count < MAX_SIZE-2:
		count += 1
		#data of form {node : eta}
		n = workingNodesData[0] + 1
		print("\nExpanding to " + str(n)+"X"+str(n)+"\n")
		#working nodes [(g,eta(g)),]
		G = workingNodesData[1]

		etaData, workingNodesData = expand(n, G, etaData)


#G = [(g, eta(g))]
def expand(n, G, etaData):
	nextWorkingNodes = []
	#for each g + l combo find eta and add to data

	#[N, g[0], l, g[1]]
	newNodes = []
	newGs = []
	for g in G:
		newGs.append(g)
		if len(g[0]) == g[0][0]:
			mir = util.mirror(g[0])
			newGs.append((mir, g[1]))

			etaData[util.dKey(mir)] = g[1]

	for g in newGs:
		L = util.getL(g[0],n)
		for l in L:
			N = util.combineG_L(g[0] ,l)
			#dat = [N, g[0], l, g[1], N]
			dat = [g[0], l, g[1], n, etaData, N]
			if dat not in newNodes:
				newNodes.append(dat)


	newNodes.sort(key = lambda x: sum(x[0]))

	#replace with pool
	"""
	for node in newNodes:

		N = node[0]
		g0 = node[1]
		l = node[2]
		g1 = node[3]

		num = eta.eta(g0, l, g1, n, etaData)

		etaData[util.dKey(N)] = num
		nextWorkingNodes.append( (N, num) )
	"""

	p = Pool(8)
	#g, l, etaG, n, NXn
	dat = p.map(eta.eta, newNodes)

	for nodeDat in dat:

		etaData[util.dKey(nodeDat[0])] = nodeDat[1]
		nextWorkingNodes.append( (nodeDat[0], nodeDat[1]) )


	print("Storing...")
	util.store([n, nextWorkingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	print("Stored")

	return etaData, [n, nextWorkingNodes]

def seed():
	print("Seeding")
	etaData, workingNodes = util.seed()
	util.store([2, workingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	print("Seeded")



if __name__ == "__main__":
	seed()
	main()

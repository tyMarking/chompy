import util3 as util
import eta
import os
from pathlib import Path

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


def main():
	print("Loading Initial Data")
	etaData = util.load(DATA_FOLDER / "etaData.json")
	workingNodesData = util.load(DATA_FOLDER / "workingNodes.json")
	print("Loaded")

	count = 0
	while count < 1:
		count += 1
		#data of form {node : eta}
		n = workingNodesData[0] + 1
		print("Expanding to " + str(n)+"X"+str(n))
		#working nodes [(g,eta(g)),]
		G = workingNodesData[1]
		#print("G: " + str(G))
		print("etaData: " + str(etaData))
		etaData, workingNodesData = expand(n, G, etaData)


#G = [(g, eta(g))]
def expand(n, G, etaData):
	nextWorkingNodes = []
	#for each g + l combo find eta and add to data
	for g in G:
		print("\n\ng: " + str(g))
		L = util.getL(g[0],n)
		print("L: " + str(L))
		for l in L:
			N = util.combineG_L(g[0] ,l)
			print(N)
			num = eta.eta(g[0], l, g[1], n, etaData)
			print("N: " + str(N) + "\tnum: " + str(num))
			etaData[util.dKey(N)] = num
			nextWorkingNodes.append( (N, num) )
	print("finished expand, etaData: " + str(etaData) + "\tnextWorkingNodes: " + str(nextWorkingNodes))
	print("Storing...")
	util.store([n, nextWorkingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	print("Stored")

	return etaData, [n, nextWorkingNodes]

def seed():
	print("Seeding")
	etaData, workingNodes = util.seed()
	print([2, workingNodes])
	util.store([2, workingNodes], DATA_FOLDER / "workingNodes.json")
	util.store(etaData, DATA_FOLDER / "etaData.json")
	print("Seeded")



if __name__ == "__main__":
	seed()
	main()

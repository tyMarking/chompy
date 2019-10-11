import util3 as util
import eta

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
	index = getIndex()
	#data of form {node : eta}
	etaData = util.load(DATA_FOLDER / "etaData.json")

	workingNodesData = util.load(DATA_FOLDER / "workingNodes.jsopn")
	n = workingNodesData[0] + 1
	#working nodes [(g,eta(g)),]
	G = workingNodesData[1]



def expand(n, G, etaData):
	newData = {}
	nextWorkingNodes = []
	for g in G:
		L = util.possibleLs(g[0])
		for l in L:
			num = eta.eta(g[0], l, g[1], etaData)
			newData[util.dKey(g[0])] = num
			nextWorkingNodes.append( (g[0], num) )


def seed():
	pass




if __name__ == "__main__":
	main()
import util3 as util 
import eta
from pathlib import Path
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

etaData = util.load(DATA_FOLDER / "etaData.json")


m = 9
n = m+1

#rank = 1
#g - 5x5s
G = []
for i in range(n-1):
	b = [n-1]*(m-1)
	b.append(i+1)
	G.append(b)

for g in G:
	N = g[:]
	for i in range(len(N)-1):
		N[i] += 1
	print("g: " + str(g) + "\tN: " + str(N))
	print("Eta(g): " + str(etaData[str(g)]) + "\tEta(N): " + str(etaData[str(N)]))
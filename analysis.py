import utility as util
import numpy as np
import os
from pathlib import Path
"""
#TODO
Get list of 1st moves
get list of all "even" states
	-turn into heatmap?
	-any paterns?

"""
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")
STATES_FOLDER = DATA_FOLDER / "states/"
TRANSFER_FOLDER = DATA_FOLDER / "transfer/"
SOLVED_FOLDER = DATA_FOLDER / "solved/"
TEST_FOLDER = DATA_FOLDER / "test/"
ANALYSIS_FOLDER = Path(THIS_FOLDER, "./data/analysis/")


def getSolvedFiles():
	files = os.listdir(SOLVED_FOLDER)

def getFirstMoves():
	firstMoves = {}
	files = os.listdir(SOLVED_FOLDER)
	for file in files:
		print("Analyzing " + str(file))
		data = util.loadSolved(SOLVED_FOLDER / file, True)
		size = (data[0][0], data[0][1])
		fm = data[2]
		firstMoves[str(size)] = fm
		del size
		del fm
		del data
	util.store(firstMoves, ANALYSIS_FOLDER / "firstMoves.json")

"""
#we are only doing squares right now
m = 3
n = 4
filePath = "./data/epoc1/solved/" + str(m) + "x" + str(n) + ".json"
solvedData = util.loadSolved(filePath)

m1 = m
n1 = n-1
gDataPath = "./data/epoc1/solved/" + str(m1) + "x" + str(n1) + ".json"
gData = util.loadSolved(gDataPath)
# state = [[0,0,0],[0,0,0]]
# key = util.dKey(state)
# node = solvedData[0][key]
# eta = node[1]
# print(eta)
# print("First move:")
# print(solvedData[1])
#print("\n")

flag = True

# print(len(solvedData[0].keys()))
for key in solvedData[0].keys():
	node = solvedData[0][key]
	state = util.revDKey(key)

	n = len(state[0])

	eta = node[1]
	# print(key + ": " + str(eta))

	gPrime = util.gPrime(state)
	dKeyGPrime = util.dKey(gPrime)

	etaGPrime = gData[0][dKeyGPrime][1]
	# print(dKeyGPrime + ": " + str(etaGPrime))

	lPrime = util.lPrime(state)
	if lPrime == 1:
		if not eta - etaGPrime % 2 == 0:
			flag = False

"""
	g = util.g(state)

	l = util.l(state)

	rankG = util.rank(g)
	fileG = util.file(g)

	# print("rankG: " + str(rankG))
	# print("fileG: " + str(fileG))

	# if rankG < n-1 and fileG == n-1 or rankG == n-1 and fileG < n-1:
	# if rankG < n - 1 and fileG < n - 1 and ( ( (l[0] == n) and (not l[1] == n) )): #or ( (not l[0] == n) and (l[1] == n) ) ):
	# if (l[0] == n and (not l[1] == n) ) or ( (not l[0] == n) and l[1] == n):
		print(l)

		eta = node[1]
		print(key + ": " + str(eta))


		dKeyG = util.dKey(g);
		etaG = gData[0][dKeyG][1]
		print(dKeyG + ": " + str(etaG))
		# print(util.display(state))
		# print("\n")
		if eta % 2 == 0:
			flag = False
"""
print(flag)

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
PRIME_FOLDER = ANALYSIS_FOLDER / "primeData/"


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

def genGLPrimeData(m, n):
	mXnData = util.loadSolved(SOLVED_FOLDER / (str(m)+"X"+str(n)+".json"))
	mXnMinus1Data = util.loadSolved(SOLVED_FOLDER / (str(m)+"X"+str(n-1)+".json"))

	mXnEtaData = {}

	for key in mXnData[0].keys():
		node = mXnData[0][key]
		eta = node[1]

		state = util.revDKey(key)
		gPrime = util.gPrime(state)
		lPrime = util.lPrime(state)
		dKeyGPrime = util.dKey(gPrime)
		etaGPrime = mXnMinus1Data[0][dKeyGPrime][1]
		rankGPrime = util.rank(gPrime)
		fileGPrime = util.rank(gPrime)

		#list order
		#m, n, gPrime, lPrime, etaGPrime, eta, rankGPrime, fileGPrime

		mXnEtaData[key] = [gPrime, lPrime, etaGPrime, eta, rankGPrime, fileGPrime]

	data = [(m, n), mXnEtaData]
	#util.store(data, PRIME_FOLDER / (str(m)+"X"+str(n)+".json"))
	return mXnEtaData

def genPrimeDataToBoardSize(m, n):
	if (m < 3):
		print("m is too small")
		return
	currM = 3
	currN = currM + 1
	path = SOLVED_FOLDER / util.getMxNFileName(currM, currN)
	while(True):
		genGLPrimeData(currM, currN)

		currN += 1
		if (currN > n):
			currM += 1
			currN = currM + 1
			if currM > m:
				break
		path = SOLVED_FOLDER / util.getMxNFileName(currM, currN)
		if (os.path.exists(path)):
			continue

		currM += 1
		currN = currM + 1
		path = SOLVED_FOLDER / util.getMxNFileName(currM, currN)
		if (os.path.exists(path)):
			continue
		else:
			break;

#genPrimeDataToBoardSize(9, 10)
data = genGLPrimeData(4,5)
oddDeltas = []
for key in data.keys():
	item = data[key]
	if (item[3]-item[2]) % 2 == 1:
		oddDeltas.append( (key, item[2], item[3]) )
print(oddDeltas)





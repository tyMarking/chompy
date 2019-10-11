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

if __name__ == "__main__":
	getFirstMoves()
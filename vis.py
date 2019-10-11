import utility as util
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"

PRIME_DATA_FOLDER = Path(THIS_FOLDER, "./data/analysis/primeData")

#[size, {util.bkey(N) : [g', l', n(g'), n(N), rank(g'), file(g')]}]


files = os.listdir(SOLVED_FOLDER)
for file in files:
	data = util.load(PRIME_DATA_FOLDER / file)

	"""
	Graphs: 
	*histogram of delta by l

	"""

	lXdelta = {}

	for key in data.keys():
		N = util.revDKey(key)
		Ndata = data[key]
		g = Ndata[0]
		l = Ndata[1]
		etaG = Ndata[2]
		etaN = Ndata[3]
		rankG = Ndata[4]
		fileG = Ndata[5]

		delta = etaN-etaG

		if l not in lXdelta:
			lXdelta[l] = [delta]
		else:
			lXdelta[l].append(delta)

	print(lXdelta)

	for l in lXdelta.keys():
		maxDelta = max(lXdelta[l])
		counts = [0]*maxDelta
		for delta in lXdelta[l]:
			counts[delta] += 1


		plt.rcdefaults()
		fig, ax = plt.subplots()
		ax.barh(np.arange(len(people)), counts)
		plt.show()
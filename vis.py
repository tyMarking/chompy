import utility as util
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"

PRIME_DATA_FOLDER = Path(THIS_FOLDER, "./data/analysis/primeData")

#[size, {util.bkey(N) : [g', l', n(g'), n(N), rank(g'), file(g')]}]


files = os.listdir(PRIME_DATA_FOLDER)
for file in files:
	data = util.load(PRIME_DATA_FOLDER / file)

	"""
	Graphs: 
	*histogram of delta by l

	"""

	lXdelta = {}

	for key in data[1].keys():
		N = util.revDKey(key)
		Ndata = data[1][key]
		g = Ndata[0]
		l = Ndata[1]
		etaG = Ndata[2]
		etaN = Ndata[3]
		rankG = Ndata[4]
		fileG = Ndata[5]

		delta = abs(etaN-etaG)

		if l not in lXdelta:
			lXdelta[l] = [delta]
		else:
			lXdelta[l].append(delta)

	print(lXdelta)

	fig = plt.figure()

	for l in lXdelta.keys():
		maxDelta = max(lXdelta[l])
		counts = [0]*(maxDelta+1)
		print(counts)
		for delta in lXdelta[l]:
			counts[delta] += 1


		print(l+101)
		ax = fig.add_subplot((l+551	))
		ax.title.set_text("l: " + str(l))
		ax.bar(np.arange(len(counts)), counts)
		#ax.suptitle('L: ' + str(l))
		#print("l: " + str(l))
	plt.title(file)
	plt.show()
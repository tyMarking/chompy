import numpy as np
import multiprocessing as mp
import time
import os
#import queue
import utility as util
import extendBoardStates as ebs
import graph
from pathlib import Path
from memory_profiler import profile

"""
Data structure:
index.txt - contains current state data
	JSON of ([solved - tuple (mxn)], [working nodes]) //working nodes even necesary?
solved/mXn - [(board,[parents,],num),] for m x n board
firstMoves.txt - list of first moves for mxn boards. JSON or CSV?
"""
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")
STATES_FOLDER = DATA_FOLDER / "states/"
TRANSFER_FOLDER = DATA_FOLDER / "transfer/"
SOLVED_FOLDER = DATA_FOLDER / "solved/"
TEST_FOLDER = DATA_FOLDER / "test/"
SOLVE_THREADS = 4
GRAPH_THREADS = 4

#have to seed 2x2

def main():
	mp.set_start_method('spawn')
	"""
	1. read index
		a. get list of current working nodes
			(unsolved nodes for which we have mXn-1 solved or the next square)
	2. for each working node create new thread (up to thread max)
	3. In thread:
		a. load data from mxn-1 or m-1xn if square
		b. extend board states
		c. extend heritage
		d. calculate state nums.
		e. find best first move
		f. open up next node and repeat
	"""

	solved,nodes = genIndexData()

	pHandler = ProccesHandler(SOLVE_THREADS, GRAPH_THREADS)

	for node in nodes:
		pHandler.run( node )
	time.sleep(7200)
	print("terminateing")
	pHandler.terminate()

class ProccesHandler:
	permQueue = None
	graphQueue = None

	def __init__(self, perm_workers=6, graph_workers=6):
		self.permQueue = mp.JoinableQueue()
		self.graphQueue = mp.JoinableQueue()
		#states processes
		self.processes = [mp.Process(target=statesThread, args=(self.permQueue,), daemon=True) for i in range(perm_workers)]
		#graph processes
		self.gProcesses = [mp.Process(target=graphThread, args=(self.graphQueue,), daemon=True) for i in range(graph_workers)]
		#self.cleanupProcesses = mp.Process(target=cleanup)
		#state reader process
		self.rProcess = mp.Process(target=stateReader, args=(self.graphQueue,), daemon=True)

		#self.cleanupProcesses.start()
		self.rProcess.start()
		for p in self.processes:
			p.start()
		for p in self.gProcesses:
			p.start()

	def run(self, item):
		self.permQueue.put(item)




	def terminate(self):
		""" wait until queue is empty and terminate processes """ #-except don't cause queue will never empty
		#self.queue.join()

		for p in self.processes:
			p.terminate()
		for p in self.gProcesses:
			p.terminate
		#self.cleanupProcesses.terminate()
		self.rProcess.terminate()


#gets the list of solved sizes and gens the list of current nodes to be worked on

def genIndexData():
	# return "3X8.json"
	files = os.listdir(STATES_FOLDER)
	if ".DS_Store" in files:
		files.remove(".DS_Store")

	solved = []
	#each file shoud be in form of mXn.json 0 - not fully checking yet
	for file in files:
			#rudementry check for format
			#if file[1] == "X" and file[3] == ".":
			print(file)
			charI = 0
			while file[charI] != "X":
				charI += 1
			m = int(file[:charI])
			charI2 = charI
			while file[charI2] != ".":
				charI2 += 1
			n = int(file[charI+1:charI2])

			solved.append( (m, n) )

	nodes = []
	for size in solved:
		#the next one in form mXn+1
		if not ((size[0], size[1]+1) in solved):
			nodes.append( (size[0], size[1]+1) )
		#for adding square nodes (stats another m value chain)
		# if size[0] + 1 == size[1] and not ((size[0]+1, size[1]) in solved):
			# nodes.append( (size[0]+1, size[1]) )

	return (solved, nodes)


# @profile
def statesThread(q):
	while True:
		size = q.get()
		if size is None:
			time.sleep(1)
			continue

		# process your item here
		print("Processing "  +str(size[0])+"X"+str(size[1]) + " in " + str(os.getpid()))


		#square node, start of new column
		if size[0] == size[1]:
			#expand vert
			#get states of root size - this case m-1Xn since square
			#data = [[board],[children]
			fileName = str(size[0]-1)+"X"+str(size[1])+".json"
			oldData = util.loadStates(STATES_FOLDER/ fileName)
			if oldData == "Failed":
				print("LOADING FAILED")
				q.task_done()
				continue
			states = util.getStatesFromDict(oldData)
			newData = ebs.appendRowToBoardStates(states, oldData)


		#not square
		else:
			#extend horiz
			#get states of root size - this case mXn-1
			#data = [[board],[children]
			fileName = str(size[0])+"X"+str(size[1]-1)+".json"
			oldData = util.loadStates(STATES_FOLDER / fileName)
			if oldData == "Failed":
				print("LOADING FAILED")
				q.task_done()
				continue
			#print("OLD DATA: " + str(oldData))
			states = util.getStatesFromDict(oldData)
			newData = ebs.appendColToBoardStates(states, oldData)

		#newData[0] = (np.array(newData[0])).tolist()

		#MAKE SURE TO REMOVE THIS LOL
		#time.sleep( (float(size[0]*size[1]) ** 0.5) / 2 )
		#time.sleep(1)
		fileName = str(size[0]) + "X" + str(size[1]) + ".json"
		util.storeStates(newData[1], size, STATES_FOLDER / fileName)

		#put mXn+1
		q.put( (size[0], size[1]+1) )
		#print("Added " + str(size[0]) + "X" + str(size[1]+1) + " to queue")

		#if m+1Xn is square (root of new column)
		# if size[0]+1 == size[1]:
			# q.put( (size[0]+1, size[1]) )
			#print("Added " + str(size[0]+1) + "X" + str(size[1]) + " to queue")

		del oldData
		del states
		del newData

		q.task_done()

# @profile
def graphThread(q):
	while True:
		if q.empty():
			time.sleep(1)
			#print("sleeping")
		else:
			file = q.get()
			print("Graph Solving " + str(file))
			fileName = TRANSFER_FOLDER / file
			#[[states],{stateXchild}]
			bXchild = util.loadStates(fileName)
			if bXchild == "Failed":
				q.task_done()
				continue
			states = util.getStatesFromDict(bXchild)


			#Gen parent dict
			bXparent = {}
			for b in states:
				bXparent[util.dKey(b)] = []
			for b in states:
				for child in bXchild[util.dKey(b)]:
					#if not b in bXparent[util.dKey(child)]:
					bXparent[util.dKey(child)].append(b)

			bXnum = graph.gen_path_numbers(states, bXparent)

			bXchild_num = {}
			for key in bXchild.keys():
				bXchild_num[key] = (bXchild[key], bXnum[key])

			firstMoves = graph.getFirstMoves(states, bXchild, bXnum)
			size = (len(states[0]), len(states[0][0]))

			#data = [states, bXchild, bXparent, bXnum, firstMoves]

			#data = "filler + graph"

			util.storeSolved(bXchild_num, firstMoves, size, SOLVED_FOLDER / file)
			os.remove(fileName)

			del bXchild
			del bXparent
			del bXnum
			del bXchild_num
			del states

			q.task_done()



# @profile
def stateReader(q):
	#read files names from folder
	#find all redundent files (not going to be used for inheriting by any nodes)
	#read storage file
	#add new data to old data from storage file
	#write to storage file
	#delet redundent files
	addedStates = set([])

	while True:
		files = os.listdir(STATES_FOLDER)
		if ".DS_Store" in files:
			files.remove(".DS_Store")

		#indexes should corresponnd
		solvedFiles = []
		solvedSizeOnly = []
		#each file shoud be in form of mXn.json 0 - not fully checking yet
		for file in files:
			charI = 0
			while file[charI] != "X":
				charI += 1
			m = int(file[:charI])
			charI2 = charI
			while file[charI2] != ".":
				charI2 += 1
			n = int(file[charI+1:charI2])

			solvedFiles.append( file )
			solvedSizeOnly.append( (m, n) )
		#print("Solved: " + str(solvedFiles))
		redundent = []
		for i in range(len(solvedFiles)):
			size = solvedSizeOnly[i]
			#if the next one in form mXn+1 is solved then redundent
			if ((size[0], size[1]+1) in solvedSizeOnly):
				#if needed for the m+1 square node
				if size[0] + 1 == size[1] and not ((size[0]+1, size[1]) in solvedSizeOnly):
					continue

				redundent.append( solvedFiles[i] )


		for file in redundent:
			os.rename(STATES_FOLDER / file, TRANSFER_FOLDER / file)

		files = os.listdir(TRANSFER_FOLDER)
		if ".DS_Store" in files:
			files.remove(".DS_Store")

		for file in files:
			if file not in addedStates:
				addedStates.add(file)
				q.put(file)


		time.sleep(3)

"""
def cleanup():
	#read files names from folder
	#find all redundent files (not going to be used for inheriting by any nodes)
	#read storage file
	#add new data to old data from storage file
	#write to storage file
	#delet redundent files
	while True:
		files = os.listdir(SOLVED_FOLDER)
		if ".DS_Store" in files:
			files.remove(".DS_Store")

		#Keep the seed to replant if neccessary
		#files.remove("2X2.json")
		#indexes should corresponnd
		solvedFiles = []
		solvedSizeOnly = []
		#each file shoud be in form of mXn.json 0 - not fully checking yet
		for file in files:
			#rudementry check for format
			#if file[1] == "X" and file[3] == ".":
			#print(file)
			charI = 0
			while file[charI] != "X":
				charI += 1
			m = int(file[:charI])
			charI2 = charI
			while file[charI2] != ".":
				charI2 += 1
			n = int(file[charI+1:charI2])

			solvedFiles.append( file )
			solvedSizeOnly.append( (m, n) )
		#print("Solved: " + str(solvedFiles))
		redundent = []
		for i in range(len(solvedFiles)):
			size = solvedSizeOnly[i]
			print(size)
			#if the next one in form mXn+1 is solved then redundent
			if ((size[0], size[1]+1) in solvedSizeOnly):
				#if needed for the m+1 square node
				if size[0] + 1 == size[1] and not ((size[0]+1, size[1]) in solvedSizeOnly):
					continue
				redundent.append( solvedFiles[i] )

		#print("redundent: " + str(redundent))
		data = util.load(DATA_FOLDER / "index.json", False)

		#means could not find file
		if type(data) == type([]):
			data = {}

		#print("DATA BITCHES")
		#print(data)
		#print("Type: " + str(type(data)))
		for file in redundent:
			fileName = SOLVED_FOLDER / file

			fData = util.load(fileName, False)


			#if fData == []:
				#util.store("THIS WAS DONE THROUGH CLEANUP", fileName)
			data[file] = fData
		#print("Storing")
		#print(data)
		util.store(data, DATA_FOLDER / "index.json")

		#remove old files
		for file in redundent:
			fileName = SOLVED_FOLDER / file
			os.remove(fileName)

		time.sleep(5)
"""




def graphManual(file):
	start = time.time()

	print("Graph Solving " + str(file))
	fileName = TRANSFER_FOLDER / file
	#[[states],{stateXchild}]
	bXchild = util.loadStates(fileName)
	if bXchild == "Failed":
		print("FAILED")
		return
	print("loaded: " + str(time.time()-start))

	states = util.getStatesFromDict(bXchild)
	print("Generated states: " + str(time.time()-start))

	#Gen parent dict
	bXparent = {}
	for b in states:
		bXparent[util.dKey(b)] = []
	for b in states:
		for child in bXchild[util.dKey(b)]:
			#if not b in bXparent[util.dKey(child)]:
			bXparent[util.dKey(child)].append(b)
	print("Generated parent dict: " + str(time.time()-start))
	bXnum = graph.gen_path_numbers(states, bXparent)
	print("Generated graph numbers: " + str(time.time()-start))
	bXchild_num = {}
	for key in bXchild.keys():
		bXchild_num[key] = (bXchild[key], bXnum[key])
	print("Combined Dicts: " + str(time.time()-start))
	firstMoves = graph.getFirstMoves(states, bXchild, bXnum)
	print("Gened first moves: " + str(time.time()-start))
	size = (len(states[0]), len(states[0][0]))


	#data = [states, bXchild, bXparent, bXnum, firstMoves]

	#data = "filler + graph"

	util.storeSolved(bXchild_num, firstMoves, size, TEST_FOLDER / file)
	print("Stored: " + str(time.time()-start))
	os.remove(fileName)
	print("Removed old: " + str(time.time()-start))
	end = time.time()
	print("Elapsed time: " + str(end-start))


#Creates the 2x2 solved case to act as seed for the expansion cycles
def seed():
	#Replace filler with actual data
	dataTwo = util.get2X2()
	#print("2data: " + str(dataTwo))
	util.storeStates(dataTwo, (2,2), STATES_FOLDER / "2X2.json")
	#util.storeStates(dataTwo, (2,2), TRANSFER_FOLDER / "2X2.json")
	#util.store({}, DATA_FOLDER / "index.json")



def graphTest():

	file = "2X2.json"

	graphManual(file)

if __name__ == "__main__":

	# seed()
	main()
	#graphTest()
